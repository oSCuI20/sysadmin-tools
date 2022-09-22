# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/ether.py
# Eduardo Banderas Alba
# 2022-08
#
# ethernet packet building
#
from struct import pack


class EtherPacket(object):

  __RAW_LEN   = 14
  __dst       = None   #6 bytes
  __src       = None   #6 bytes
  __ethertype = None   #2 bytes

  def __init__(self, dst, src, ethertype):
    try:
      self.dst = dst
      self.src = src
      self.ethertype = ethertype
    except:
      raise EtherPacketException('Can not make packet')

    if len(self.raw) != self.__RAW_LEN:
      raise EtherPacketException('ethernet frame must be 14 bytes')
  #__init__

  @property
  def raw(self):
    return self.dst + self.src + self.ethertype
  #raw

  @property
  def dst(self):
    return self.__dst

  @dst.setter
  def dst(self, v):
    self.__dst = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
  #dst

  @property
  def src(self):
    return self.__src

  @src.setter
  def src(self, v):
    self.__src = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))
  #src

  @property
  def ethertype(self):
    return self.__ethertype

  @ethertype.setter
  def ethertype(self, v):
    self.__ethertype = pack('!H', v)
  #ethertype
#class EtherPacket


class EtherPacketException(Exception):
  pass
