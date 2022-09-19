# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/icmp.py
# Eduardo Banderas Alba
# 2022-08
#
# icmp packet building
#
from libs.pcap import checksum
from .         import IPv4Packet

from os     import urandom
from time   import time
from struct import unpack, pack


class ICMPPacket(object):

  __type     = None    # 1 byte
  __code     = None    # 1 byte
  __seq      = None    # 2 bytes
  __checksum = None    # 2 bytes
  __id       = None    # 2 bytes

  __transport_protocol = 0x01

  def __init__(self, target, sender):
    self.__id  = unpack('!H', urandom(2))[0]
    self.seq   = 0
    self.ipv4 = IPv4Packet(target, sender, self.__transport_protocol, 0, unpack('!H', urandom(2))[0])

  def __raw(self):
    self.seq += 1
    data = self.type + self.code + self.checksum + self.id + pack('!H', self.seq) + self.data
    self.ipv4.t_length = len(data)
    return self.ipv4.raw + data
  #__raw

  def __request(self):
    self.type = 0x08
    self.code = 0x00

  @property
  def data(self):
    return b''
  #data

  @property
  def raw_request(self):
    self.__request()
    return self.__raw()
  #raw_request

  @property
  def type(self):
    return pack('!B', self.__type)

  @type.setter
  def type(self, v):
    self.__type = v
  #type

  @property
  def code(self):
    return pack('!B', self.__code)

  @code.setter
  def code(self, v):
    self.__code = v
  #code

  @property
  def seq(self):
    return self.__seq

  @seq.setter
  def seq(self, v):
      self.__seq = v
  #seq

  @property
  def checksum(self):
    icmp = self.type + self.code + pack('!H', self.seq) + pack('!H', 0x00) + self.id + \
           self.data

    return pack('!H', checksum(unpack('!' + 'H' * (len(icmp) // 2), icmp)))
  #checksum

  @property
  def id(self):
    return pack('!H', self.__id)
  #id
#class ICMPPacket
