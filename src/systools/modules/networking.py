# -*- coding: utf-8 -*-
#
# ./modules/networking.py
# Eduardo Banderas Alba
# 2022-09
from time   import time, sleep
from struct import unpack

from utils     import Logger
from modules   import dev, cfg
from libs      import SendPacket, Capture
from libs.pcap import ARPPacket, ICMPPacket

MAC_BROADCAST = 'ff:ff:ff:ff:ff:ff'


class NetStatus(object):

  packet = []

  __target = None

  __iface  = None
  __sender = None

  def __init__(self, target):
    self.logger = Logger()
    self.logger.logfile = cfg.logger['default']

    if self.__class__.__name__.lower() in cfg.logger:
      self.logger.logfile = cfg.logger[self.__class__.__name__.lower()]

    self.logger.log((-1, 'Init NetStatus'))

    self.iface, self.sender = list(dev.interface.items()).pop()

    self.target = target

    self.cap = Capture(self.iface, limit=1, callback=self.cb_capture)
    self.sp  = SendPacket(self.iface)

    self.__set_target_hwaddr()

    self.logger.log((-1, f'{self.iface} -> target: {self.target}, sender: {self.sender}'))
  #__init__

  def latency(self, num=10):
    self.logger.log((-1, f'Checking latency, number of packet {num}'))
    self.logger.log((-1, f'Interface {self.iface}, target {self.target}'))

    self.cap.filter = f'icmp and icmp[0] == 0 and host {self.target["ipaddr"]}'
    self.cap.setFilter()

    icmp = ICMPPacket(self.target, self.sender)

    lost, mos, counter = (0, 0, 0)
    tm_first_sent, tm_first_recv = (0, 0)
    latency = []
    jitter  = [ 0 ]

    while num > counter:
      start = time() * 1000
      icmp.data = start
      if not tm_first_sent:
        tm_first_sent = start

      self.sp.send((icmp.raw_request,))
      self.cap.sniff(timeout=1)

      end = time() * 1000
      counter += 1
      if len(self.packet) == 0:
        lost += 1
        continue

      latency.append(end - start)
      self.packet.pop()

      if not tm_first_recv:
        tm_first_recv = end

      drtt = (start - tm_first_sent) - (end - tm_first_recv)
      jitter.append(jitter[-1] + (abs(drtt) - jitter[-1]) / 16)
    #endwhile

    latmin, latmax, latavg = (-1, -1, -1)

    if len(latency) > 0:
      mos = self.__get_mos(latency, jitter, lost)
      latmin, latmax, latavg = (min(latency), max(latency), sum(latency) / len(latency))

    return {
      'packet': {
        'total': num,
        'lost': lost,
        'percent': round((lost / num) * 100, 4)
      },
      'latency': {
        'min': round(latmin, 4),
        'max': round(latmax, 4),
        'avg': round(latavg, 4)
      },
      'jitter': round(jitter[-1], 4)
    }
  #latency

  def __get_mos(self, latency, jitter, lost):
    # Calc MOS
    effective = (sum(latency) / len(latency)) + (max(jitter) * 2) + 10
    r = 93.2

    if effective < 160:
      r -= effective / 40
    else:
      r -= (effective - 120) / 10
      r -= lost * 2.5

    return 1 + (0.035) * r + (0.000007) * r * (r - 60) * (100 - r)
  #__get_mos

  def cb_capture(self, packet):
    self.packet.append(packet)
  #cb_capture

  @property
  def target(self):
    return self.__target

  @target.setter
  def target(self, v):
    if not isinstance(v, dict):
      raise Exception('target value must be a dictionary')

    if 'ipaddr' not in v:
      raise Exception('ipaddr key not found in target value')

    self.__target = v
  #target

  @property
  def sender(self):
    return self.__sender

  @sender.setter
  def sender(self, v):
    if not isinstance(v, dict):
      raise Exception('sender value must be a dictionary')

    if 'ipaddr' not in v:
      raise Exception('ipaddr key not found in sender value')

    if 'hwaddr' not in v:
      raise Exception('hwaddr key not found in sender value')

    self.__sender = v
  #sender

  def __set_target_hwaddr(self):
    addr = [ int(x) for x in self.target['ipaddr'].split('.') ]
    cidr = self.sender['cidr']

    mask = [0, 0, 0, 0]
    for i in range(cidr):
      mask[i // 8] = mask[i // 8] + (1 << (7 - i % 8))

    network = '.'.join(map(str, [ addr[i] & mask[i] for i in range(4) ]))

    if self.sender['gateway'] in dev.arpcache:
      self.target['hwaddr'] = dev.arpcache[self.sender['gateway']]

    if network == self.sender['network']:
      self.target['hwaddr'] = MAC_BROADCAST

      if self.target['ipaddr'] in dev.arpcache:
        self.target['hwaddr'] = dev.arpcache[self.target['ipaddr']]
      else:
        target = self.target.copy()
        self.target['hwaddr'] = self.__get_hwaddr(target)
    #endif

    if 'hwaddr' not in self.target:
      target = { 'ipaddr': self.sender['gateway'], 'hwaddr': MAC_BROADCAST }
      self.target['hwaddr'] = self.__get_hwaddr(target)
  #__set_target_hwaddr

  def __get_hwaddr(self, target):
    self.cap.filter = f'arp and arp[6:2] == 2 and host {target["ipaddr"]}'
    self.cap.setFilter()

    arp = ARPPacket(target, self.sender)
    self.sp.send((arp.raw_request,))
    self.cap.sniff(timeout=1)

    hwaddr = 'ff:ff:ff:ff:ff:ff'

    if len(self.packet) > 0:
      packet = self.packet.pop()
      hwaddr = packet.src

    self.logger.debug(f'hwaddr {hwaddr} -> {target["ipaddr"]}')

    return hwaddr
  #__get_hwaddr
#class NetStatus


class NetScanner(object):

  def __init__(self):
    pass
  #__init__
#class NetScanner
