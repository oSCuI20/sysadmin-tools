# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/ipv4.py
# Eduardo Banderas Alba
# 2022-08
#
# ipv4 packet building
#
from struct import pack


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

  def __init__(self, src, dst, protocol, length, id):
    self.src = src
    self.dst = dst
    self.protocol = protocol
    self.t_length = length
    self.identifier = id
  #__init__

  @property
  def raw(self):
    return self.version_length + self.type + self.t_length + self.identifier + \
           self.flag_fragment + self.ttl + self.protocol + self.checksum + \
           self.src + self.dst
  #raw
  
  @property
  def version_length(self):
    return pack('!B', self.__version << 4 | self.__h_length)
  #version_length

  @property
  def type(self):
    return pack('!B', self.__type)

  @property
  def t_length(self):
    return pack('!H', self.__t_length)

  @t_length.setter
  def t_length(self, v):
    self.__t_length = v
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
  #protocol

  @property
  def checksum(self):
    ip_header = unpack('!10H', self.version_length + self.type + self.t_length + self.identifier +
                self.flag_fragment + self.ttl + self.protocol + pack('!H', 0x00) +
                self.src + self.dst)

    checksum, counter, maxcounter = (0, 0, len(ip_header))
    checksum = 0
    while counter < maxcounter:
      checksum += ip_header[counter]
      checksum &= 0xffffffff
      counter  += 1
    #endwhile

    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)

    return pack('!H', ~checksum & 0xffff)
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
