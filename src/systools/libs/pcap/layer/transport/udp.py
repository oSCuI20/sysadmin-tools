# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/transport/udp.py
# Eduardo Banderas Alba
# 2022-08
#
# Disassemble udp packet
#
from ..layer import Layer, LayerException


class UDP(Layer):

  _HEADER_LEN = 8
  _unpack_format = '!HHHH'

  __src = None  #2 bytes
  __dst = None  #2 bytes
  __length   = None  #2 bytes
  __checksum = None  #2 bytes

  __protocol = None
  __support  = {
    80:  'HTTP',
    443: 'HTTPS',
    67:  'DHCP',
    68:  'DHCP',
    53:  'DNS'
  }

  properties = [ 'src', 'dst', 'length', 'checksum' ]

  def __init__(self, raw):
    super().__init__(raw)
  #__init__

  def _header(self):
    self.src, \
    self.dst, \
    self.length, \
    self.checksum = self.pktheader
    self.protocol = (self.src, self.dst)
  #_header

  def _data(self):
    if self.protocol:
      mod = None
      if self.protocol in self.APPLICATION:
        mod = f'{self.PATHLIB}.application.{self.protocol.lower()}'

      self._load_module(mod, self.protocol)
  #_data

  def protocol():
    def fget(self):
      return self.__protocol

    def fset(self, v):
      for p in v:
        if not self.__protocol:
          self.__protocol = self.__support.get(p)
      #endfor

    def fdel(self):
      del self.__protocol

    return locals()
  #end definition protocol property

  def format():
    def fget(self):
      msg = ''
      if hasattr(self, '_module'):
        msg = f'{self._module.format}'

      return f'length: {self.length} checksum: {self.checksum} {msg}'

    return locals()
  #end definition format property

  def src():
    doc = "The src property."
    def fget(self):
      return self.__src

    def fset(self, v):
      self.__src = v

    def fdel(self):
      del self.__src

    return locals()
  #end definition src property

  def dst():
    doc = "The dst property."
    def fget(self):
      return self.__dst

    def fset(self, v):
      self.__dst = v

    def fdel(self):
      del self.__dst

    return locals()
  #end definition dst property

  def checksum():
    doc = "The checksum property."
    def fget(self):
      return self.__checksum

    def fset(self, v):
      self.__checksum = v

    def fdel(self):
      del self.__checksum

    return locals()
  #end definition checksum property

  def length():
    doc = "The length property."
    def fget(self):
      return self.__length

    def fset(self, v):
      self.__length = v

    def fdel(self):
      del self.__length

    return locals()
  #end definition length property

  protocol = property(**protocol())
  format   = property(**format())
  src      = property(**src())
  dst      = property(**dst())
  checksum = property(**checksum())
  length   = property(**length())
#class udp


class udpException(LayerException):
  pass
#class udpException
