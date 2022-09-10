# -*- coding: utf-8 -*-
#
# ./stats.py
# Eduardo Banderas Alba
# 2022-08
#
# Get read/write in bytes per seconds
#
import os

from time  import sleep
from utils import Logger

class CPUStats(object):
  # /proc/stat position of value, ignore position 0 its the name of cpu
  __cpu_mapping__ = {
    'user':    1,      #__CPU_USER,
    'nice':    2,      #__CPU_NICE,
    'system':  3,      #__CPU_SYSTEM,
    'idle':    4,      #__CPU_IDLE,
    'iowait':  5,      #__CPU_IOWAIT,
    'irq':     6,      #__CPU_IRQ,
    'softirq': 7,      #__CPU_SOFTIRQ,
    'steal':   8,      #__CPU_STEAL,
    'guest':   9       #__CPU_GUEST
  }

  ticks = os.sysconf(os.sysconf_names['SC_CLK_TCK']) #Clock ticks per seconds

  def __init__(self, interval=1, warning=45, critical=90):
    self.logger    = Logger()
    self.cpus      = {}
    self.interval  = interval
    self.terminate = False

    self.warning  = warning
    self.critical = critical

    self.__initialize__()
  #__init__

  def __initialize__(self):
    cpuinfo = '/proc/cpuinfo'
    cpustat = '/proc/stat'

    self.cpus.update({
      'fd': open(cpustat, 'r'),
      'cpu': { key: 0 for key in self.__cpu_mapping__.keys() }
    })

    with open(cpuinfo, 'r') as fr:
      info = fr.read()
      for c in info.split('\n'):
        if c.startswith('processor'):
          cpuN = f'cpu{c.split(":")[1].strip()}'
          self.cpus.update({
            cpuN: { key: 0 for key in self.__cpu_mapping__.keys() }
          })
        #endif
      #endfor
    #endwith

    self.logger.debug(f'CPUS: {self.cpus}')
  #__initialize__

  def loop(self):
    while not self.terminate:
      self.cpustats()
      cpus_usage, log_level = ([], -1)

      for cpu in self.cpus.keys():
        if cpu in ['fd', 'cpu']:
          continue

        usage = self.cpus[cpu]['usage']

        if   usage >= self.warning and usage < self.critical:
          log_level = -2
        elif usage >= self.critical:
          log_level = -3

        cpus_usage.append(f'{usage}')
      #endfor

      if log_level != -1:
        self.logger.log((log_level, f'usage {cpus_usage}'))

      sleep(self.interval)
    #endwhile
  #loop

  def cpustats(self):
    fd = self.cpus['fd']
    for cpu in self.cpus.keys():
      if cpu in ['fd', 'usage']:
        continue

      previous = self.cpus[cpu].copy()
      current  = self.__read_cpustats__(fd, cpu)

      current['usage'] = self.get_cpustatistics((previous, current))

      self.cpus.update({ cpu: current })
    #endfor
  #cpustats

  def get_cpustatistics(self, v):
    previous, current = v

    cpu_previous_sum = sum([y for x, y in previous.items() if x not in ['usage']])
    cpu_current_sum  = sum([y for x, y in current.items() if x not in ['usage']])

    cpu_delta = cpu_current_sum - cpu_previous_sum
    cpu_idle  = current['idle'] - previous['idle']
    cpu_inuse = cpu_delta - cpu_idle

    return round(100 * cpu_inuse / cpu_delta, 2)
  #get_cpustatistics

  def __read_cpustats__(self, fd, cpu):
    fd.seek(0)
    read_line_stats = fd.read().split('\n')
    read_stats = []
    while len(read_line_stats) > 0:
      line = read_line_stats.pop(0)
      if line.startswith(cpu):
        read_stats = line.strip().split()
        read_line_stats = []
    #endwhile

    stats = {}
    for key, pos in self.__cpu_mapping__.items():
      stats[key] = int(read_stats[pos])

    return stats
  #__read_cpustats__
#class CPUStats

class DiskStats(object):
  # /sys/block/<disk>/stat and /sys/block/<disk>/<partition>/stat position of value
  __disk_mapping__ = {
    'reads_completed':        0,     #__READ_COMPLETED,
    'reads_merged':           1,     #__READ_MERGED,
    'sectors_read':           2,     #__SECTORS_READ,
    'millsec_spent_reading':  3,     #__MILLSEC_SPENT_READING,
    'writes_completed':       4,     #__WRITES_COMPLETED,
    'writes_merged':          5,     #__WRITES_MERGED,
    'sectors_written':        6,     #__SECTORS_WRITTEN,
    'millsec_spent_writing':  7,     #__MILLSEC_SPENT_WRITTING,
    'io_currently_progress':  8,     #__IO_CURRENTLY_PROGRESS,
    'io_millsec_spent_doing': 9      #__IO_MILLSEC_SPENT_DOING
  }

  __disks_stats_mapping__ = {
    'sectors_read':    'rb/s',
    'sectors_written': 'wb/s'
  }

  def __init__(self, interval=1, warning=1*1024*1024, critical=10*1024*1024):
    self.logger    = Logger()
    self.disks     = {}
    self.interval  = interval
    self.terminate = False

    self.sector_size = 512

    self.warning  = warning  # default 1MB
    self.critical = critical # default 10MB

    self.__initialize__()
  #__init__

  def __initialize__(self):
    path = '/sys/block'
    for disk in os.listdir(path):
      if disk.startswith('loop'):
        continue

      self.disks.update({
        disk: {
          'path' : f'{path}/{disk}',
          'fd'   : open(f'{path}/{disk}/stat', 'r'),
          'stats': { key: 0 for key in self.__disk_mapping__.keys() },
          'rb/s': 0,
          'wb/s': 0,
          'partitions': {}
        }
      })

      partition_path = self.disks[disk]['path']
      for partition in os.listdir(partition_path):
        if not partition.startswith(disk):
          continue

        self.disks[disk]['partitions'].update({
          partition: {
            'fd': open(f'{partition_path}/{partition}/stat', 'r'),
            'stats': { key: 0 for key in self.__disk_mapping__.keys() },
            'rb/s': 0,
            'wb/s': 0
          }
        })
    #endfor

    self.logger.debug(f'DISKS: {self.disks}')
  #__initialize__

  def loop(self):
    while not self.terminate:
      self.diskstats()
      log_level = -1
      for disk in self.disks.keys():
        r_abuse = self.disks[disk]['rb/s']
        w_abuse = self.disks[disk]['wb/s']

        if   (r_abuse >= self.warning and r_abuse < self.critical) or \
             (w_abuse >= self.warning and w_abuse < self.critical):
          log_level = -2
        elif r_abuse >= self.critical or w_abuse >= self.critical:
          log_level = -3

        if log_level != -1:
          self.logger.log((log_level, f'writing abuse in {disk}, {w_abuse / 1024} kB/s ' +
                                      f'reading abuse in {disk}, {r_abuse / 1024} kB/s'))
      #endfor

      sleep(self.interval)
    #endwhile
  #loop

  def diskstats(self):
    for disk in self.disks.keys():
      fd = self.disks[disk]['fd']
      previous = self.disks[disk]['stats'].copy()
      current  = self.__read_diskstat__(fd)
      bps      = self.get_diskstatistics((previous, current))

      self.disks[disk]['stats'] = current
      self.disks[disk]['rb/s']  = bps['rb/s']
      self.disks[disk]['wb/s']  = bps['wb/s']

      for partition in self.disks[disk]['partitions'].keys():
        fd = self.disks[disk]['partitions'][partition]['fd']
        previous = self.disks[disk]['partitions'][partition]['stats'].copy()
        current  = self.__read_diskstat__(fd)
        bps      = self.get_diskstatistics((previous, current))

        self.disks[disk]['partitions'][partition]['stats'] = current
        self.disks[disk]['partitions'][partition]['rb/s']  = bps['rb/s']
        self.disks[disk]['partitions'][partition]['wb/s']  = bps['wb/s']
      #endfor
    #endfor
  #diskstats

  def get_diskstatistics(self, v, stats=['sectors_read', 'sectors_written']):
    #v => tuple(Dict(previous), Dict(current))
    previous, current = v

    out = {}
    for stat in stats:
      if previous[stat] == 0:
        previous[stat] = current[stat]

      key = self.__disks_stats_mapping__[stat]

      out[key] = self.__value__((previous[stat], current[stat]))
    #endfor

    return out
  #get_diskstatistics

  def __read_diskstat__(self, fd):
    fd.seek(0)
    read_stats = fd.read(1024).strip().split()

    stats = {}
    for key, pos in self.__disk_mapping__.items():
      stats[key] = float(read_stats[pos])

    return stats
  #__read_diskstat__

  def __value__(self, v):
    """
      param: v  tuple(previous, current)

      return: int value in bytes
    """
    iop, ioc = v
    return ((ioc * self.sector_size) - (iop * self.sector_size)) / self.interval
  #__value__
#class DiskStats

class NetworkStats(object):

  __receive_mapping__ = {
    'bytes':      0,
    'packets':    1,
    'errs':       2,
    'drop':       3,
    'fifo':       4,
    'frame':      5,
    'compressed': 6,
    'multicast':  7
  }

  __transmit_mapping__ = {
    'bytes':       8,
    'packets':     9,
    'errs':       10,
    'drop':       11,
    'fifo':       12,
    'colls':      13,
    'carrier':    14,
    'compressed': 15
  }

  def __init__(self, interval=1, warning=0, critical=0):
    self.logger    = Logger()
    self.networks  = {}
    self.interval  = interval
    self.terminate = False

    self.warning  = warning
    self.critical = critical

    self.__initialize__()
  #__init__

  def __initialize__(self):
    self.networks.update({
      'fd': open('/proc/net/dev', 'r'),
    })

    for iface in os.listdir('/sys/class/net'):
      self.networks.update({
        iface: {
          'receive':  { key: 0 for key in self.__receive_mapping__.keys() },
          'transmit': { key: 0 for key in self.__transmit_mapping__.keys() }
        }
      })
    #endfor

    self.logger.debug(f'NETWORK: {self.networks}')
  #__initialize__

  def loop(self):
    while not self.terminate:
      self.netstats()

      receive  = []
      transmit = []
      for net in self.networks.keys():
        if net in [ 'fd' ]:
          continue

        receive.append(f"{net} {self.networks[net]['receive']['kb/s']} kb/s")
        receive.append(f"{net} {self.networks[net]['receive']['packet/s']} packet/s")

        transmit.append(f"{net} {self.networks[net]['transmit']['kb/s']} kb/s")
        transmit.append(f"{net} {self.networks[net]['transmit']['packet/s']} packet/s")
      #endfor

      self.logger.log((-2, ' '.join(receive)))
      self.logger.log((-2, ' '.join(transmit)))

      sleep(self.interval)
    #endwhile
  #loop

  def netstats(self):
    fd = self.networks['fd']
    for iface in self.networks.keys():
      if iface in [ 'fd' ]:
        continue

      previous = self.networks[iface].copy()
      current  = self.__read_netstats__(fd, iface)

      stats = self.get_netstatistics((previous, current))

      current['receive'].update(stats['receive'])
      current['transmit'].update(stats['transmit'])

      self.networks.update({ iface: current })
    #endfor
  #netstats

  def get_netstatistics(self, v):
    previous, current = v

    return {
      'receive': {
        'kb/s': (current['receive']['bytes'] - previous['receive']['bytes']) / 1024,
        'packet/s': current['receive']['packets'] - previous['receive']['packets'],
        'err/s': current['receive']['errs'] - previous['receive']['errs'],
        'drop/s': current['receive']['drop'] - previous['receive']['drop']
      },
      'transmit': {
        'kb/s': (current['transmit']['bytes'] - previous['transmit']['bytes']) / 1024,
        'packet/s': current['transmit']['packets'] - previous['transmit']['packets'],
        'err/s': current['transmit']['errs'] - previous['transmit']['errs'],
        'drop/s': current['transmit']['drop'] - previous['transmit']['drop']
      }
    }
  #get_netstatistics

  def __read_netstats__(self, fd, iface):
    fd.seek(0)

    read_line_stats = fd.read(1024 * 8).strip().split('\n')[2:]

    read_stats = []

    while len(read_line_stats) > 0:
      line = read_line_stats.pop(0).strip()
      if line.startswith(iface):
        read_stats = line[len(iface) + 1:].strip().split()
        read_line_stats = []
    #endwhile

    receive  = {}
    transmit = {}

    for key, pos in self.__receive_mapping__.items():
      receive[key] = int(read_stats[pos])

    for key, pos in self.__transmit_mapping__.items():
      transmit[key] = int(read_stats[pos])

    return { 'receive': receive, 'transmit': transmit }
  #__read_netstats__
#class NetworkStats
