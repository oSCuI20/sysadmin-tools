# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/layer.py
# Eduardo Banderas Alba
# 2022-08
#
# datalink layer
#
import struct
import importlib

from .constants import Constants


class Layer(Constants):

  _HEADER_LEN    = 0
  _unpack_format = None

  properties = []

  def __init__(self, raw):
    self.pktlen    = len(raw)
    self.pktheader = raw[:self._HEADER_LEN]
    self.pktdata   = raw[self._HEADER_LEN:]

    self._header()
    self._data()
  #__init__

  def __str__(self):
    result = { self.__class__.__name__: dict(self) }

    if hasattr(self, '_module'):
      mod = self._module

      while hasattr(mod, '_module'):
        result[mod.__class__.__name__] = dict(mod)
        mod = mod._module
      #endwhile
      
      result[mod.__class__.__name__] = dict(mod)
    #endif

    return repr(result)
  #__str__

  def __iter__(self):
    for k in self.properties:
      if not hasattr(self, k):
        continue

      yield (k, getattr(self, k))
  #__iter__

  def _load_module(self, path, module):
    if path and self.pktdata:

      obj = getattr(importlib.import_module(path, package=module), module)
      self._module = obj(self.pktdata)

      if issubclass(self._module.__class__, ApplicationLayer):
        self._module.dst = self.dst
        self._module.src = self.src

      self.__setattr__(module, dict(self._module))
  #_load_module

  def pktdata():
    doc = "The pktdata property."
    def fget(self):
      return self.__pktdata

    def fset(self, v):
      if not isinstance(v, bytes):
        raise LayerException(f'ERROR: pktdata is not bytes type {type(v)}')

      self.__pktdata = v

    def fdel(self):
      del self.__pktdata

    return locals()
  #end definition pktdata property

  def pktheader():
    doc = "The pktheader property."
    def fget(self):
      return self.__pktheader

    def fset(self, v):
      if not isinstance(v, bytes):
        raise LayerException(f'ERROR: pktheader is not bytes type {type(v)}')

      if len(v) != self._HEADER_LEN:
        raise LayerException(f'ERROR: pktheader should be {self._HEADER_LEN} bytes')

      self.__pktheader = struct.unpack(self._unpack_format, v)

    def fdel(self):
      del self.__pktheader

    return locals()
  #end definition pktheader property

  def pktlen():
    doc = "The pktlen property."
    def fget(self):
      return self.__pktlen

    def fset(self, v):
      self.__pktlen = v

    def fdel(self):
      del self.__pktlen

    return locals()
  #end definition pktlen property

  pktdata   = property(**pktdata())
  pktheader = property(**pktheader())
  pktlen    = property(**pktlen())
#class Layer


class ApplicationLayer(object):

  unpack      = struct.unpack
  unpack_from = struct.unpack_from

  __pktdata = None

  properties = [ 'data' ]

  def __init__(self, raw):
    self.pktdata = raw

    self._data()
  #__init__

  def __iter__(self):
    for k in self.properties:
      if not hasattr(self, k):
        continue

      yield (k, getattr(self, k))
  #__iter__

  def _data(self):
    try:
      self.data = self.pktdata.decode()
    except:
      self.data = ''
  #_data

  def format():
    def fget(self):
      return f'length {len(self.pktdata)}' + \
             f'\n{self.data}' if self.data else f''

    return locals()
  #end definition format property

  def pktdata():
    doc = "The pktdata property."
    def fget(self):
      return self.__pktdata

    def fset(self, v):
      if not isinstance(v, bytes):
        raise LayerException(f'ERROR: pktdata is not bytes type {type(v)}')

      self.__pktdata = v

    def fdel(self):
      del self.__pktdata

    return locals()
  #end definition pktdata property

  format  = property(**format())
  pktdata = property(**pktdata())
#class ApplicationLayer


class LayerException(Exception):
  def __init__(self, msg):      self.msg = msg
  def __str__(self):            return repr(self.msg)
#class LayerException


class ApplicationException(Exception):
  def __init__(self, msg):      self.msg = msg
  def __str__(self):            return repr(self.msg)
#class ApplicationException
