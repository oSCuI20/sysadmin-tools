# -*- coding: utf-8 -*-
#
# ./modules/device.py
# Eduardo Banderas Alba
# 2022-09
#
# Get all info about device
#  - cpu_model     (ok)
#  - temperature   (pending)
#  - ram           (ok)
#  - interfaces with network configurations and port listen
#  - disks         (ok)
#  - operating system
#  - load average (ok)
#  - uptime
#  - routing table
#  - running process
#
import os, socket, platform, json

from uuid   import uuid4 as uuid  # UUID V4
from fcntl  import ioctl
from struct import pack, unpack

from utils import Logger, readfile, writefile


class Device:

  __hostname  = None
  __cpu_model = None
  __meminfo   = None
  __system    = None
  __loadavg   = None
  __uptime    = None
  __iface     = None
  __ifaces    = None
  __disks     = None
  __process   = None
  __routing   = None
  __hwinfo    = None
  __arpcache  = None
  __fileinfo  = f'{os.getcwd()}/.device-info'

  def __init__(self):
    self.logger = Logger()

  def __iter__(self):
    yield from {
      'process': self.process,
      'routing': self.routing,
      'opersystem': self.opersystem,
      'interfaces': self.interfaces,
      'disks': self.disks,
      'loadavg': self.loadavg,
      'meminfo': self.meminfo,
      'hostname': self.hostname,
      'cpu_model': self.cpu_model,
      'hwinfo': self.hwinfo,
      'arpcache': self.arpcache,
    }.items()
  #__iter__

  def __str__(self):
    return json.dumps(dict(self), ensure_ascii=False)
  #__str__

  def __repr__(self):
    return self.__str__()
  #__repr__

  def __wr_device_info__(self, dev):
    writefile(self.__fileinfo, json.dumps(dev))
  #__wr_device_info__

  def __get_device_info__(self):
    info = { 'uuid': None, 'seed': None }
    try:
      info = json.loads(readfile(self.__fileinfo))
    except:
      pass

    return info
  #__get_device_info__

  @property
  def arpcache(self):
    if not self.__arpcache:
      self.__arpcache = {}

      info = readfile('/proc/net/arp').split('\n')
      info.pop(0)  # rm first line

      for i in info:
        ipaddr, hwtype, flags, hwaddr, mask, device = i.split()
        self.__arpcache[ipaddr] = hwaddr
      #endfor
    #endif

    return self.__arpcache
  #arpcache

  @property
  def hwinfo(self):
    if not self.__hwinfo:
      self.__hwinfo = {
        'bios':    {'date': None, 'version': None, 'release': None, 'vendor': None},
        'board':   {'name': None, 'version': None, 'serial' : None, 'vendor': None},
        'chassis': {'type': None, 'version': None, 'serial' : None, 'vendor': None},
        'product': {'name': None, 'version': None, 'serial' : None, 'family': None,
                    'uuid': None}
      }

      path = '/sys/devices/virtual/dmi/id'
      if os.path.exists(path):
        for key, values in self.__hwinfo.items():
          for val in values.keys():
            self.__hwinfo[key][val] = readfile(f'{path}/{key}_{val}')

      else:
        path = '/sys/firmware/devicetree/base'
        self.__hwinfo['product']['family'] = readfile(f'{path}/model')
        self.__hwinfo['product']['name']   = readfile(f'{path}/name')

      about_device = self.__get_device_info__()

      if not about_device['uuid']:
        about_device['uuid'] = str(uuid())
        about_device['seed'] = str(uuid())

        self.__wr_device_info__(about_device)
      #endif

      self.__hwinfo['product'].update(about_device)
    #endif

    return self.__hwinfo
  #hwinfo

  @property
  def process(self):
    process = {}
    path = '/proc'
    for pid in os.listdir(path):
      if not pid.isdigit():
        continue

      p = f'{path}/{pid}'
      if not os.path.exists(p):
        continue

      st = os.stat(p)

      process.update({
        int(pid): {
          'uid': st.st_uid,
          'gid': st.st_gid,
          'cmdline': readfile(f'{p}/cmdline')
        }
      })
    #endfor

    return process
  #process

  @property
  def routing(self):
    if not self.__routing:
      self.__routing = []

      info = readfile('/proc/net/route').split('\n')
      headers = [ _.strip().lower() for _ in info.pop(0).split('\t') if _ ]

      for d in info:
        values = d.split('\t')
        route  = { _: None for _ in headers }
        for i in range(0, len(headers)):
          val = None
          if headers[i] in [ 'destination', 'gateway', 'mask' ]:
            adr = unpack('!BBBB', bytearray.fromhex(values[i]))
            val = '.'.join([ str(adr[x]) for x in range(len(adr) -1, -1, -1) ])
          else:
            val = values[i].strip()

          route[headers[i]] = val
        #endfor

        self.__routing.append(route)
      #endfor
    #endif

    return self.__routing
  #routing

  @property
  def opersystem(self):
    if not self.__system:
      self.__system = f'{platform.system()} {platform.architecture()[0]} - {platform.release()}'

    return self.__system
  #opersystem

  @property
  def interface(self):
    if not self.__iface:

      for iface, val in self.interfaces.items():
        if self.__iface or not val['ipaddr']: continue

        self.__iface = {
          iface: val
        }
      #endfor
    #endif

    return self.__iface

  @interface.setter
  def interface(self, v):
    if v not in self.interfaces:
      raise Exception(f'interface {v} not found')

    self.__iface = { v: self.interfaces.get(v) }
  #interface

  @property
  def interfaces(self):
    if not self.__ifaces:
      self.__ifaces = {}
      path = '/sys/class/net'

      for iface in os.listdir(path):
        if iface == 'lo':   continue  # ignore loopback

        hwaddr, ipaddr, netmask, gateway, network, cidr = self.__getifaceinfo(iface.encode())
        self.__ifaces.update({
          iface: {
            'hwaddr': hwaddr,
            'ipaddr': ipaddr,
            'netmask': netmask,
            'gateway': gateway,
            'network': network,
            'cidr': cidr
          }
        })
      #endfor
    #endif

    return self.__ifaces
  #interfaces

  @property
  def disks(self):
    if not self.__disks:
      self.__disks = {}
      path = '/sys/block'

      for disk in os.listdir(path):
        if disk.startswith('loop'):
          continue

        partitions = []

        for partition in os.listdir(f'{path}/{disk}'):
          if not partition.startswith(disk):
            continue

          m, u, f = self.__getdiskinfo(partition)

          partitions.append({
            'name': partition,
            'size': int(readfile(f'{path}/{disk}/{partition}/size')) * 512,
            'mountpoint': m,
            'free': f,
            'used': u
          })
        #endfor

        self.__disks.update({ disk: {
          'size': int(readfile(f'{path}/{disk}/size')) * 512,
          'model': readfile(f'{path}/{disk}/device/model'),
          'serial': readfile(f'{path}/{disk}/device/serial'),
          'partitions': partitions
        }})
      #endfor
    #endif

    return self.__disks
  #disks

  @property
  def loadavg(self):
    if not self.__loadavg:
      self.__loadavg = [ round(float(_), 2) for _ in readfile('/proc/loadavg').split()[0:3] ]

    return self.__loadavg
  #loadavg

  @property
  def meminfo(self):
    if not self.__meminfo:
      self.__meminfo = { 'MemTotal': 0, 'MemFree': 0, 'MemAvailable': 0,
                         'Buffers': 0, 'Cached': 0, 'SwapTotal': 0, 'SwapFree': 0 }

      info = readfile('/proc/meminfo')
      for c in info.split('\n'):
        if not c:    continue

        key, value = c.split(':')
        if key in self.__meminfo.keys():
          self.__meminfo[key] = int(value.rstrip('kB')) * 1024  # bytes
      #endfor
    #endif

    return self.__meminfo
  #meminfo

  @property
  def hostname(self):
    if not self.__hostname:
      self.__hostname = socket.gethostname()

    return self.__hostname
  #hostname

  @property
  def cpu_model(self):
    if not self.__cpu_model:
      info = readfile('/proc/cpuinfo')
      for c in info.split('\n'):
        if not self.__cpu_model and c.startswith('model name'):
          self.__cpu_model = f'{c.split(":")[1].strip()}'
        #endif
      #endfor
    #endif

    return self.__cpu_model
  #cpu_model

  def __getdiskinfo(self, partition):
    info = readfile('/proc/mounts')
    mountpoint = None
    used = None
    free = None

    for linfo in info.split('\n'):
      if linfo.find(partition) == -1:
        continue

      mountpoint = linfo.split()[1]
    #endfor

    if mountpoint:
      data = os.statvfs(mountpoint)
      used = (data.f_blocks - data.f_bfree) * data.f_frsize
      free = data.f_bavail - data.f_frsize

    return (mountpoint, used, free)
  #__getdiskinfo

  def __getifaceinfo(self, iface):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    __io = { 'ipaddr' : 0x8915, 'hwaddr' : 0x8927, 'netmask': 0x891b }

    hwaddr, ipaddr, netmask, gateway, network, cidr = (None, None, None, None, None, None)

    try:
      hwaddr  = ioctl(sock.fileno(), __io['hwaddr'],  pack('256s', iface))[18:24]
      ipaddr  = ioctl(sock.fileno(), __io['ipaddr'],  pack('256s', iface))[20:24]
      netmask = ioctl(sock.fileno(), __io['netmask'], pack('256s', iface))[20:24]

      gateway = self.__getgateway(iface.decode())
    except:
      pass

    if hwaddr:    hwaddr  = hwaddr.hex(':')
    if ipaddr:    ipaddr  = socket.inet_ntoa(ipaddr)
    if netmask:   netmask = socket.inet_ntoa(netmask)

    if ipaddr and netmask:
      network, cidr = self.__getnetwork(ipaddr, netmask)

    return (hwaddr, ipaddr, netmask, gateway, network, cidr)
  #__getifaceinfo

  def __getgateway(self, iface):
    for route in self.routing:
      if route['iface'] == iface:
        return route['gateway']
    #endfor
  #__getgateway

  def __getnetwork(self, ipaddr, netmask):
    addr = [ int(x) for x in ipaddr.split('.') ]
    cidr = int(sum([ bin(int(x)).count('1') for x in netmask.split('.') ]))

    mask = [0, 0, 0, 0]
    for i in range(cidr):
      mask[i // 8] = mask[i // 8] + (1 << (7 - i % 8))

    network = '.'.join(map(str, [ addr[i] & mask[i] for i in range(4) ]))

    return (network, cidr)
#class Device


Device = Device()
