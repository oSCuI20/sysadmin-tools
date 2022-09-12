# -*- coding: utf-8 -*-
#
# ./netpacket/wakeonlan.py
# Eduardo Banderas Alba
# 2022-09
#
from struct import pack


class WakeOnLanPacket(object):

  __ethertype = pack('!H', 0x0842)
  __mac_dst   = pack('!6B', *(0xff, 0xff, 0xff, 0xff, 0xff, 0xff))  # broadcast
  __mac_src   = None

  __mac_target = None  # 96 bytes - 16 duplications of the IEEE address
  __password   = b''  # 0, 4 or 6 bytes

  def __init__(self, src, target, password=None):
    self.mac_src    = src
    self.mac_target = target
    if password:
      self.password = password
  #__init__

  def payload(self):
    return self.mac_dst + \
           self.mac_src + \
           self.ethertype + \
           self.mac_dst + \
           self.mac_target + \
           self.password

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

  @property
  def ethertype(self):
    return self.__ethertype

  @ethertype.setter
  def ethertype(self, v):
    self.__ethertype = pack('!H', v)

  @property
  def mac_src(self):
    return self.__mac_src

  @mac_src.setter
  def mac_src(self, v):
    self.__mac_src = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))

  @property
  def mac_dst(self):
    return self.__mac_dst

  @mac_dst.setter
  def mac_dst(self, v):
    self.__mac_dst = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))

  @property
  def mac_target(self):
    return self.__mac_target

  @mac_target.setter
  def mac_target(self, v):
    self.__mac_target = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ])) * 16
