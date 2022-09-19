# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/wakeonlan.py
# Eduardo Banderas Alba
# 2022-09
#
# WOL Packet building
#
from . import EtherPacket

from struct import pack


class WakeOnLanPacket(object):

  __dst = None
  __src = None

  __broadcast  = pack('!6B', *(0xff, 0xff, 0xff, 0xff, 0xff, 0xff))
  __password   = b''  # 0, 4 or 6 bytes

  ethertype = 0x0842

  def __init__(self, target, sender, password=None):
    self.dst = target['hwaddr']
    self.src = sender['hwaddr']

    if password:
      self.password = password

    self.ether = EtherPacket(dst='ff:ff:ff:ff:ff:ff', sender['hwaddr'], self.ethertype)
  #__init__

  @property
  def raw(self):
    return self.ether.raw + self.broadcast + self.dst + self.password

  @property
  def broadcast(self):
    return self.__broadcast

  @property
  def password(self):
    return self.__password

  @password.setter
  def password(self, v):
    try:
      n1, n2, n3, n4 = v.split('.')
      v = b''.join([ int(x).to_bytes(1, 'big') for x in [n1, n2, n3, n4] ])
    except ValueError:
      try:
        n1, n2, n3, n4, n5, n6 = v.split(':')
        v = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in [n1, n2, n3, n4, n5, n6] ]))
      except ValueError:
        v = v.encode()

    max_pack = 0
    if len(v) in [ 4, 5 ]:
      max_pack = 4
    elif len(v) == 6:
      max_pack = 6

    self.__password = v[:max_pack]
  #password

  @property
  def src(self):
    return self.__src

  @src.setter
  def src(self, v):
    self.__src = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
  #src

  @property
  def dst(self):
    return self.__dst

  @dst.setter
  def dst(self, v):
    self.__dst = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ])) * 16
  #dst
