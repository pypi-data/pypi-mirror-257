#!/bin/python

from .task import MBIOTask
from .xmlconfig import XMLConfig
from .scheduler import Schedulers

import requests


class MBIOTaskPulsar(MBIOTask):
    def onInit(self):
        self._timeout=0
        self._period=1
        self._outputs=[]

    def onLoad(self, xml: XMLConfig):
        mbio=self.getMBIO()
        self._period=xml.getFloat('period', 1)
        items=xml.children('output')
        if items:
            for item in items:
                value=mbio[item.get('key')]
                if value and value.isWritable():
                    self._outputs.append(value)

    def poweron(self):
        self._timeout=self.timeout(self._period)
        return True

    def poweroff(self):
        return True

    def run(self):
        if self._outputs:
            if self.isTimeout(self._timeout):
                self._timeout=self.timeout(self._period)
                for value in self._outputs:
                    value.toggle()
            return min(5.0, self.timeToTimeout(self._timeout))


class MBIOTaskCopier(MBIOTask):
    def onInit(self):
        self._outputs=[]

    def onLoad(self, xml: XMLConfig):
        mbio=self.getMBIO()
        self._source=mbio.value(xml.get('source'))
        items=xml.children('output')
        if items:
            for item in items:
                value=mbio[item.get('key')]
                if value and value.isWritable():
                    self._outputs.append(value)

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def run(self):
        if self._source and self._outputs:
            for value in self._outputs:
                value.set(self._source.value)
            return 1


class MBIOTaskScheduler(MBIOTask):
    def onInit(self):
        self._schedulers=Schedulers()
        self._programs={}
        self._timeoutreload=0
        self.config.set('reloadperiod', 0)
        self.config.set('reloadurl', None)

    def onLoadProgram(self, scheduler, xml: XMLConfig):
        if scheduler is not None and xml is not None:
            items=xml.children('*')
            if items:
                for item in items:
                    if item.tag=='on':
                        scheduler.on(item.get('dow'), item.get('time'), item.getFloat('sp'))
                    elif item.tag=='off':
                        scheduler.off(item.get('dow'), item.get('time'), item.getFloat('sp'))
                    elif item.tag=='slot':
                        scheduler.on(item.get('dow'), item.get('time'), item.get('duration'), item.getFloat('sp'))

    def onLoad(self, xml: XMLConfig):
        items=xml.children('program')
        if items:
            for item in items:
                name=item.get('name')
                if name and not self._schedulers.get(name):
                    sp=item.child('sp')
                    default=None
                    if sp:
                        default=sp.getFloat('default')
                        unit=sp.get('unit', 'C')
                        resolution=item.getFloat('resolution', 0.1)

                    scheduler=self._schedulers.create(name=name, sp=default)
                    program={'state': self.valueDigital('%s_state' % name)}
                    if sp:
                        program['sp']=self.value('%s_sp' % name, unit=unit, resolution=resolution)
                    self._programs[name]=program
                    self.onLoadProgram(scheduler, item.child('triggers'))

        item=xml.child('download')
        if item and item.child('url'):
            try:
                self.valueDigital('comerr', default=False)
                self._timeoutReload=0
                self._type=item.get('type')
                self.config.reloadperiod=item.getInt('period', 60)
                self.config.reloadurl=item.child('url').text()
                self.logger.error(self.config.url)
                self.reload()
            except:
                pass

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def reload(self):
        self._timeoutReload=self.timeout(60*60)
        if self.config.reloadperiod>0 and self.config.reloadurl:
            try:
                r=requests.get(self.config.reloadurl, timeout=5.0)
                if r and r.ok:
                    data=r.text

                    # TODO: load
                    self.logger.warning(data)

                    self.values.comerr.updateValue(False)
                    self._timeoutReload=self.timeout(self.config.reloadperiod*60)
                    return True
            except:
                pass

        self.values.comerr.updateValue(True)
        return False

    def run(self):
        if self.config.reloadperiod>0 and self.isTimeout(self._timeoutReload):
            self.reload()

        for scheduler in self._schedulers:
            state, sp = scheduler.eval()
            try:
                self._programs[scheduler.name]['state'].updateValue(state)
                self._programs[scheduler.name]['sp'].updateValue(sp)
            except:
                pass
        return 1.0


class MBIOTaskVirtualIO(MBIOTask):
    def onInit(self):
        pass

    def onLoad(self, xml: XMLConfig):
        items=xml.children('digital')
        if items:
            for item in items:
                name=item.get('name')
                if name:
                    self.valueDigital(name, default=item.getBool('default'), writable=True)

        items=xml.children('analog')
        if items:
            for item in items:
                name=item.get('name')
                unit=item.get('unit')
                resolution=item.getFloat('resolution', 0.1)
                if name:
                    self.value(name, unit=unit, default=item.getBool('default'), writable=True, resolution=resolution)

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def run(self):
        for value in self.values:
            # value.updateValue(value.value)
            if value.isPendingSync():
                value.clearSyncAndUpdateValue()
        return 5.0


# API: https://api.mystrom.ch/#a141a894-925c-4e8b-bcaf-68c3a67fa98d
class MBIOTaskMyStromSwitch(MBIOTask):
    def onInit(self):
        self.config.set('refreshperiod', 15)
        self._switches={}
        self._timeoutRefresh=0

    def onLoad(self, xml: XMLConfig):
        self.config.update('refreshperiod', xml.getInt('refresh'))

        items=xml.children('switch')
        if items:
            for item in items:
                name=item.get('name')
                ip=item.get('ip')
                if name and not self._switches.get(name):
                    data={}
                    data['state']=self.valueDigital('%s_state' % name, writable=True)
                    data['state'].config.set('ip', ip)
                    data['ene']=self.value('%s_ene' % name, unit='kWh', resolution=0.1)
                    data['pow']=self.value('%s_pow' % name, unit='W', resolution=0.1)
                    data['t']=self.value('%s_t' % name, unit='C', resolution=0.1)
                    self._switches[name.lower()]=data

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def url(self, ip, command):
        return 'http://%s/%s' % (ip, command)

    def run(self):
        for name in self._switches.keys():
            value=self._switches[name]['state']
            if value.isPendingSync():
                self.microsleep()
                try:
                    ip=value.config.ip
                    url=self.url(ip, 'relay')
                    state=bool(value.toReachValue)
                    if state:
                        url=url + '?state=1'
                    else:
                        url=url + '?state=0'
                    self.logger.debug('mystrom(%s)->%s' % (value.key, url))
                    r=requests.get(url, timeout=3.0)
                    if r and r.ok:
                        value.clearSync()
                        self._timeoutRefresh=0
                except:
                    pass
                value.clearSyncAndUpdateValue()

        if self.config.refreshperiod>0 and self.isTimeout(self._timeoutRefresh):
            self._timeoutRefresh=self.timeout(self.config.refreshperiod)
            for name in self._switches.keys():
                self.microsleep()
                dev=self._switches[name]
                try:
                    ip=dev['state'].config.ip
                    url=self.url(ip, 'report')
                    self.logger.debug('mystrom(%s)->%s' % (dev['state'].key, url))
                    r=requests.get(url, timeout=3.0)
                    if r and r.ok:
                        data=r.json()
                        # self.logger.warning(data)

                        value=dev['state']
                        try:
                            v=data['relay']
                            value.updateValue(v)
                            value.setError(False)
                        except:
                            value.setError(True)

                        value=dev['ene']
                        try:
                            v=float(data['energy_since_boot'])/3600000.0
                            value.updateValue(v)
                            value.setError(False)
                        except:
                            value.setError(True)

                        value=dev['pow']
                        try:
                            v=float(data['power'])
                            value.updateValue(v)
                            value.setError(False)
                        except:
                            value.setError(True)

                        value=dev['t']
                        try:
                            v=float(data['temperature'])
                            value.updateValue(v)
                            value.setError(False)
                        except:
                            value.setError(True)

                        continue
                except:
                    pass

                dev['state'].setError(True)
                dev['ene'].setError(True)
                dev['pow'].setError(True)
                dev['t'].setError(True)

        return 5.0


if __name__ == "__main__":
    pass
