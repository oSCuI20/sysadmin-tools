# -*- coding: utf-8 -*-
#
# ./libs/pcap/packet/icmp.py
# Eduardo Banderas Alba
# 2022-08
#
# icmp packet building
#
class ICMPPacket(object):

  __type     = None    # 1 byte
  __code     = None    # 1 byte
  __seq      = None    # 2 bytes
  __checksum = None    # 2 bytes
  __id       = None    # 2 bytes

  def request(self):
    self.type = 0x08
    self.code = 0x00
    
  @property
  def type(self):
    return self.__type

  @type.setter
  def type(self, v):
    self.__type = v
  #type

  @property
  def code(self):
    return self.__code

  @code.setter
  def code(self, v):
    self.__code = v
  #code

  @property
  def seq(self):
    self.__seq += 1
    return self.__seq

  @seq.setter
  def seq(self, v):
    self.__seq = v
  #seq

  @property
  def checksum(self):
    return self.__checksum
  #checksum

  @property
  def id(self):
    return self.__id
  #id
#class ICMPPacket
