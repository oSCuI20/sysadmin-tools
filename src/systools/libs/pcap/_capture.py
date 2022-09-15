# -*- coding: utf-8 -*-
#
# ./libs/pcap/_capture.py
# Eduardo Banderas Alba
# 2022-09
#
# Capture network traffic
#
from ._pcap_handle import PCAPHandle
from ._pcap        import pcap_next_ex, pcap_compile, pcap_setfilter
from .layer        import Ethernet

from ctypes import c_int, c_ubyte, byref, POINTER
from time   import sleep
from struct import pack


class Capture(PCAPHandle):

  def __initialize__(self):
    self.setFilter()
  #__initialize__

  def sniff(self):
    counter = 0
    while (self.limit.value == -1     and not self.terminate) or \
          (self.limit.value > counter and not self.terminate):
      if pcap_next_ex(self.handle, byref(self.pkthdr), byref(self.pktdata)) == 1:
        caplen = self.pkthdr.contents.caplen
        packet = Ethernet(pack('B' * caplen, *self.pktdata.contents[:caplen]))

        if self.callback:
          self.callback(packet)

        self.logger.log((-1, packet))
        counter += 1
      #endif

      sleep(0.1)
    #endwhile

  def setFilter(self):
    if not self.filter:
      return

    if pcap_compile(self.handle, byref(self.bpf), self.filter, 1, 0xFFFFFF) == -1:
      raise Exception(f'error, pcap compile failure: {pcap_geterr(self.handle)}')

    if pcap_setfilter(self.handle, byref(self.bpf)) == -1:
      raise Exception(f'error, pcap setfilter failure: {pcap_geterr(self.handle)}')
  #setFilter

  @property
  def filter(self):
    return self.__filter

  @filter.setter
  def filter(self, v):
    if isinstance(v, str):
      v = v.encode()

    if not isinstance(v, bytes):
      raise TypeError('filter type must be bytes or string')

    self.__filter = v
  #filter
