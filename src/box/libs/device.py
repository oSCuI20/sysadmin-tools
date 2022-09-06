# -*- coding: utf-8 -*-
#
# ./libs/device.py
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

from fcntl  import ioctl
from struct import pack, unpack

class Device(object):

  def __init__(self):
    self.__hostname  = None
    self.__cpu_model = None
    self.__meminfo   = None
    self.__system    = None
    self.__loadavg   = None
    self.__uptime    = None
    self.__ifaces    = None
    self.__disks     = None
    self.__process   = None
    self.__routing   = None
  #__init__

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
      'cpu_model': self.cpu_model
    }.items()
  #__iter__

  def __str__(self):
    return json.dumps(dict(self), ensure_ascii=False)
  #__str__

  def __repr__(self):
    return self.__str__()
  #__repr__

  @property
  def process(self):
    if not self.__process:
      self.__process = []
      path = '/proc'
      for pid in os.listdir(path):
        if not pid.isdigit():
          continue

        p = f'{path}/{pid}'
        if not os.path.exists(p):
          continue

        st = os.stat(p)

        self.__process.append({
          'uid': st.st_uid,
          'gid': st.st_gid,
          'pid': pid,
          'cmdline': self.__readfile(f'{p}/cmdline').strip()
        })
      #endfor

    return self.__process
  #process

  @property
  def routing(self):
    if not self.__routing:
      self.__routing = []

      info = self.__readfile('/proc/net/route').strip().split('\n')
      headers = [ _.strip() for _ in info.pop(0).split('\t') if _ ]

      for d in info:
        values = d.split('\t')
        route  = { _: None for _ in headers }
        for i in range(0, len(headers)):
          val = None
          if headers[i] in [ 'Destination', 'Gateway', 'Mask' ]:
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
  def interfaces(self):
    if not self.__ifaces:
      self.__ifaces = []
      path = '/sys/class/net'

      for iface in os.listdir(path):
        if iface == 'lo':   continue  # ignore loopback

        hwaddr, ipaddr, netmask = self.__getifaceinfo(iface.encode())

        self.__ifaces.append({
          'interface': iface,
          'hwaddr':  hwaddr,
          'ipaddr':  ipaddr,
          'netmask': netmask
        })

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
            'size': int(self.__readfile(f'{path}/{disk}/{partition}/size')) * 512,
            'mountpoint': m,
            'free': f,
            'used': u
          })
        #endfor

        self.__disks.update({ disk: {
          'size': int(self.__readfile(f'{path}/{disk}/size')) * 512,
          'model': self.__readfile(f'{path}/{disk}/device/model').strip(),
          'serial': self.__readfile(f'{path}/{disk}/device/serial').strip(),
          'partitions': partitions
        }})
      #endfor

    return self.__disks
  #disks

  @property
  def loadavg(self):
    if not self.__loadavg:
      self.__loadavg = [ round(float(_), 2) for _ in self.__readfile('/proc/loadavg').split()[0:3] ]

    return self.__loadavg
  #loadavg

  @property
  def meminfo(self):
    if not self.__meminfo:
      self.__meminfo = { 'MemTotal': 0, 'MemFree': 0, 'MemAvailable': 0,
                         'Buffers': 0, 'Cached': 0, 'SwapTotal': 0, 'SwapFree': 0 }

      info = self.__readfile('/proc/meminfo')
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
      info = self.__readfile('/proc/cpuinfo')
      for c in info.split('\n'):
        if not self.__cpu_model and c.startswith('model name'):
          self.__cpu_model = f'{c.split(":")[1].strip()}'
        #endif
      #endfor

    return self.__cpu_model
  #cpu_model

  def __readfile(self, filename):
    out = ''
    with open(filename, 'r') as fr:
      out = fr.read()

    return out
  #__readfile

  def __getdiskinfo(self, partition):
    info = self.__readfile('/proc/mounts')
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

    hwaddr, ipaddr, netmask = (None, None, None)

    try:
      hwaddr  = ioctl(sock.fileno(), __io['hwaddr'],  pack('256s', iface))[18:24]
      ipaddr  = ioctl(sock.fileno(), __io['ipaddr'],  pack('256s', iface))[20:24]
      netmask = ioctl(sock.fileno(), __io['netmask'], pack('256s', iface))[20:24]
    except:
      pass

    if hwaddr:       hwaddr  = hwaddr.hex(':')
    if ipaddr:       ipaddr  = socket.inet_ntoa(ipaddr)
    if netmask:      netmask = socket.inet_ntoa(netmask)

    return (hwaddr, ipaddr, netmask)
#class Device
