# -*- coding: utf-8 -*-
#
# ./libs/pcap/_sendpacket.py
# Eduardo Banderas Alba
# 2022-09
#
# Send a packet
#
from ._pcap_handle import PCAPHandle
from ._pcap        import pcap_sendpacket, pcap_geterr

from time import sleep


class SendPacket(PCAPHandle):

  def send(self, raw_packets):
    if not isinstance(raw_packets, tuple):
      raise TypeError('raw_packets must be a tuple type')

    for packet in raw_packets:
      if not isinstance(packet, bytes):
        self.logger.log((-3, f'the packet could not be sent, wrong type'))
        continue

      if pcap_sendpacket(self.handle, packet, len(packet)) != 0:
        self.logger.log((-3, f'the packet could not be sent, {pcap_geterr(self.handle)}'))

      sleep(0.1)
    #endfor
  #send
#class SendPacket
