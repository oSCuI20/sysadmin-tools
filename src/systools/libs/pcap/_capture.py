# -*- coding: utf-8 -*-
#
# ./libs/pcap/_capture.py
# Eduardo Banderas Alba
# 2022-09
#
# Capture network traffic
#
from utils           import Logger
from .layer          import Ethernet
from ._pcap import ( PCAP_ERRORBUF, PCAP_SNAPLEN, bpf_program, struct_pkthdr, struct_stat,
                     pcap_open_live, pcap_geterr, pcap_setnonblock, pcap_can_set_rfmon,
                     pcap_stats, pcap_close, pcap_next_ex, pcap_compile, pcap_setfilter )

from ctypes import c_int, c_ubyte, byref, POINTER
from time   import sleep
from struct import pack


class Capture(object):

  __errbuf = PCAP_ERRORBUF

  def __init__(self, iface=None, timeout=1, limit=-1, promisc=True,
                     snaplen=PCAP_SNAPLEN, filter=b'', callback=None):
    self.logger = Logger()

    self.interface = iface
    self.timeout   = timeout
    self.limit     = limit
    self.promisc   = promisc
    self.snaplen   = snaplen
    self.filter    = filter

    self.callback  = callback
    self.terminate = False

    self.__initialize__()

    self.setFilter()
  #__init__

  def sniff(self):
    counter = 0
    while (self.limit.value == -1     and not self.terminate) or \
          (self.limit.value > counter and not self.terminate):
      if pcap_next_ex(self.handle, byref(self.__pkthdr), byref(self.__pktdata)) == 1:
        caplen = self.__pkthdr.contents.caplen
        packet = Ethernet(pack('B' * caplen, *self.__pktdata.contents[:caplen]))

        if self.callback:
          self.callback(packet)

        self.logger.log((-1, packet))
        counter += 1
      #endif

      sleep(0.1)
    #endwhile

  def __initialize__(self):
    self.__bpf   = bpf_program()
    self.__stats = struct_stat()
    self.__pkthdr  = POINTER(struct_pkthdr)()
    self.__pktdata = POINTER(c_ubyte * self.snaplen.value)()

    self.handle = pcap_open_live(self.interface, self.snaplen.value, self.promisc,
                                 self.timeout, self.__errbuf)
    if not self.handle:
      raise Exception(f'Error: handle, {self.__errbuf}')

    if pcap_can_set_rfmon(self.handle) == 0:
      raise Exception(f'Error: Can not set interface in monitor mode, {pcap_geterr(self.handle)}')

    pcap_setnonblock(self.handle, 1, self.__errbuf)
  #__initialize__

  def setFilter(self):
    if not self.filter:
      return

    if pcap_compile(self.handle, byref(self.__bpf), self.filter, 1, 0xFFFFFF) == -1:
      raise Exception(f'Error: pcap compile failure, {pcap_geterr(self.handle)}')

    if pcap_setfilter(self.handle, byref(self.__bpf)) == -1:
      raise Exception(f'Error: pcap setfilter failure, {pcap_geterr(self.handle)}')
  #setFilter

  @property
  def interface(self):
    return self.__interface

  @interface.setter
  def interface(self, v):
    if isinstance(v, str):
      v = v.encode()

    if not isinstance(v, bytes):
      raise TypeError('interface type must be bytes or string')

    self.__interface = v
  #interface

  @property
  def promisc(self):
    return self.__promisc

  @promisc.setter
  def promisc(self, v):
    if not isinstance(v, bool):
      raise TypeError('promisc type must be bool')

    self.__promisc = v
  #promisc

  @property
  def snaplen(self):
    return self.__snaplen

  @snaplen.setter
  def snaplen(self, v):
    if not isinstance(v, int):
      raise TypeError('snaplen type must be integer')

    self.__snaplen = c_int(v)
  #snaplen

  @property
  def limit(self):
    return self.__limit

  @limit.setter
  def limit(self, v):
    if not isinstance(v, int):
      raise TypeError('limit type must be integer')

    self.__limit = c_int(v)
  #limit

  @property
  def timeout(self):
    return self.__timeout

  @timeout.setter
  def timeout(self, v):
    if not isinstance(v, int):
      raise TypeError('timeout type must be integer')

    self.__timeout = c_int(v)
  #timeout

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
