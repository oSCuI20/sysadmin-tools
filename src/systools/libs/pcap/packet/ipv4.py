# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/ipv4.py
# Eduardo Banderas Alba
# 2022-08
#
# ipv4 packet building
#
from libs.pcap import checksum
from .         import EtherPacket

from struct import pack, unpack


class IPv4Packet(object):

  __RAW_LEN = 20

  __version    = 0x04    # 4 bits
  __h_length   = 0x14    # 4 bits
  __type       = 0x00    # 1 byte
  __t_length   = None    # 2 bytes
  __identifier = None    # 2 bytes
  __ip_flag    = 0b010   # 3 bits
  __fragment   = 0x00    # 13 bits
  __ttl        = 0x78    # 1 byte
  __protocol   = 0x01    # 1 byte
  __checksum   = pack('!H', 0x00)    # 2 bytes
  __src        = None    # 4 bytes
  __dst        = None    # 4 bytes

  ethertype = 0x0800

  def __init__(self, target, sender, protocol, length, id):
    self.dst = target['ipaddr']
    self.src = sender['ipaddr']
    self.protocol = protocol
    self.t_length = length
    self.identifier = id

    self.ether = EtherPacket(target['hwaddr'], sender['hwaddr'], self.ethertype)
  #__init__

  @property
  def raw(self):
    return self.ether.raw + \
           self.version_length + self.type + self.t_length + self.identifier + \
           self.flag_fragment + self.ttl + self.protocol + self.checksum + \
           self.src + self.dst
  #raw

  @property
  def version_length(self):
    return pack('!B', (self.__version << 4) | self.__h_length // 4)
  #version_length

  @property
  def type(self):
    return pack('!B', self.__type)

  @property
  def t_length(self):
    return pack('!H', self.__t_length)

  @t_length.setter
  def t_length(self, v):
    self.__t_length = v + self.__h_length
  #t_length

  @property
  def identifier(self):
    return pack('!H', self.__identifier)

  @identifier.setter
  def identifier(self, v):
    self.__identifier = v
  #identifier

  @property
  def flag_fragment(self):
    return pack('!H', self.__ip_flag << 13 | self.__fragment)
  #flag_fragment

  @property
  def ttl(self):
    return pack('!B', self.__ttl)
  #ttl

  @property
  def protocol(self):
    return pack('!B', self.__protocol)

  @protocol.setter
  def protocol(self, v):
      self.__protocol = v
  #protocol

  @property
  def checksum(self):
    ip = self.version_length + self.type + self.t_length + self.identifier + \
         self.flag_fragment + self.ttl + self.protocol + pack('!H', 0x00) + \
         self.src + self.dst
    return pack('!H', checksum(unpack('!' + 'H' * (len(ip) // 2), ip)))
  #ip_checksum

  @property
  def src(self):
    return self.__src

  @src.setter
  def src(self, v):
    self.__src = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #src

  @property
  def dst(self):
    return self.__dst

  @dst.setter
  def dst(self, v):
    self.__dst = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #dst
#class IPv4Packet
