# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/datalink/ethenet.py
# Eduardo Banderas Alba
# 2022-08
#
# ethernet frames
#
from ..layer import Layer, LayerException


class Ether(Layer):

  _HEADER_LEN    = 14
  _unpack_format = '!6s 6s H'

  __dst   = None    # 6 Bytes
  __src   = None    # 6 Bytes
  __proto = None    # 2 Bytes

  __MAC_LEN   = 6
  __ethertype = {
    None  : 'ethernet header not recognize',
    0x0800: 'IPv4',
    #0x86DD: 'ipv6',
    0x0806: 'ARP'
  }

  properties = [ 'dst', 'src', 'proto' ]

  def __init__(self, raw):
    super().__init__(raw)
  #__init__

  def _header(self):
    self.dst, self.src, self.proto = self.pktheader
  #_header

  def _data(self):
    if self.protoid:
      mod = None
      if   self.protoid in self.DATALINK:
        mod = f'{self.PATHLIB}.datalink.{self.protoid.lower()}'

      elif self.protoid in self.NETWORK:
        mod = f'{self.PATHLIB}.network.{self.protoid.lower()}'

      self._load_module(mod, self.protoid)
  #_data

  def format():
    def fget(self):
      info = f'protocol {self.proto} not support'
      if self.protoid:
        info = f'{self.protoid} {self._module.format}'

      return f'-- {info}'

    return locals()
  #format

  def protoid():
    doc = "The protoid property."
    def fget(self):
      return self._protoid

    def fset(self, v):
      self._protoid  = self.__ethertype.get(v) or None

    def fdel(self):
      del self._protoid

    return locals()
  #end definition protoid property

  def proto():
    doc = "The proto property."
    def fget(self):
      return self._proto

    def fset(self, v):
      self.protoid = v
      self._proto  = hex(v)

    def fdel(self):
      del self._proto

    return locals()
  #end definition proto property

  def src():
    doc = "The src property."
    def fget(self):
      return self._src

    def fset(self, v):
      if not isinstance(v, bytes):
        raise EtherException(f'ERROR: src mac address is not bytes type {type(v)}')

      if len(v) != self.__MAC_LEN:
        raise EtherException(f'ERROR: src mac address should be {self.__MAC_LEN} bytes')

      self._src = v.hex(':') #':'.join(map(tohex, v))

    def fdel(self):
      del self._src

    return locals()
  #end definition src property

  def dst():
    doc = "The dst property."
    def fget(self):
      return self._dst

    def fset(self, v):
      if not isinstance(v, bytes):
        raise EtherException(f'ERROR: dst mac address is not bytes type {type(v)}')

      if len(v) != self.__MAC_LEN:
        raise EtherException(f'ERROR: dst mac address should be {self.__MAC_LEN} bytes')

      self._dst = v.hex(':') #':'.join(map(tohex, v))

    def fdel(self):
      del self._dst

    return locals()
  #end definition dst property

  format  = property(**format())
  protoid = property(**protoid())
  proto   = property(**proto())
  src     = property(**src())
  dst     = property(**dst())
#class Ether


class EtherException(LayerException):
  pass
#class EtherException
