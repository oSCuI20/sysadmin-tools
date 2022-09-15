# -*- coding: utf-8 -*-
#
# ./libs/pcap/_pcap_handle.py
# Eduardo Banderas Alba
# 2022-09
#
# Handle pcap
#
from utils  import Logger
from ._pcap import ( PCAP_ERRORBUF, PCAP_SNAPLEN, bpf_program, struct_pkthdr, struct_stat,
                     pcap_open_live, pcap_geterr, pcap_setnonblock, pcap_can_set_rfmon,
                     pcap_stats, pcap_close )

from ctypes import c_int, c_ubyte, byref, POINTER

class PCAPHandle(object):

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

    self.errbuf  = PCAP_ERRORBUF
    self.bpf     = bpf_program()
    self.stats   = struct_stat()
    self.pkthdr  = POINTER(struct_pkthdr)()
    self.pktdata = POINTER(c_ubyte * self.snaplen.value)()

    self.handle = pcap_open_live(self.interface, self.snaplen.value, self.promisc,
                                 self.timeout, self.errbuf)
    if not self.handle:
      raise Exception(f'error, handle: {self.errbuf}')

    if pcap_can_set_rfmon(self.handle) == 0:
      raise Exception(f'error, can not set interface in monitor mode: {pcap_geterr(self.handle)}')

    pcap_setnonblock(self.handle, 1, self.errbuf)

    self.__initialize__()
  #__init__

  def __initialize__(self):
    pass
  #__initialize__

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
#class PCAPHandle
