# -*- coding: utf-8 -*-
#
# ./netpacket/icmp.py
# Eduardo Banderas Alba
# 2022-09
#
import os

from time   import time
from struct import pack, unpack


class icmpPacket(object):

  __types_codes = {
      0x03: {    #type: destination unreachable
        #codes
        0x00:	'Destination network unreachable',
        0x01:	'Destination host unreachable',
        0x02:	'Destination protocol unreachable',
        0x03:	'Destination port unreachable',
        0x04:	'Fragmentation required, and DF set',
        0x05:	'Source route failed',
        0x06:	'Destination network unknown',
        0x07:	'Destination host unknown',
        0x08:	'Source host isolated',
        0x09:	'Network administratively prohibited',
        0x0A:	'Host administratively prohibited',
        0x0B:	'Network unreachable for Type Of Service',
        0x0C:	'Host unreachable for Type of Service',
        0x0D:	'Administratively prohibited'
      },
      0x05: {    #type: redirect message
        #codes
        0x00:	'Redirect Datagram for the Network',
        0x01:	'Redirect Datagram for the Host',
        0x02:	'Redirect Datagram for the Type of Service & network',
        0x03:	'Redirect Datagram for the Type of Service & host'
      },
      0x0B: {    #type: time exceeded
        #codes
        0x00: 'TTL expired',
        0x01: 'Fragment reassembly time exceeded'
      },
      0x0C: {    #type: parameter problem
        0x00: 'Pointer indicates the error',
        0x01: 'Missing a required option',
        0x02: 'Bad length'
      },
      0x00: { 0x00: 'Echo reply' },                              #type: echo reply (used for ping/tracert)
      0x04: { 0x00: 'Traffic congestion control' },              #type: source quench
      0x06: { None: '' },                                        #type: alternate host address - deprecated
      0x08: { 0x00: 'Echo request' },                            #ŧype: echo request
      0x09: { 0x00: 'Router Advertisement' },                    #type: router advertisement
      0x0A: { 0x00: 'Router discovery/selection/solicitation' }, #type: router solicitation
      0x0D: { 0x00: 'Timestamp Request' },                       #type: timestamp request
      0x0E: { 0x00: 'Timestamp Reply' },                         #type: timestamp reply
      0x0f: { 0x00: 'Information Request' },                     #type: information request
      0x10: { 0x00: 'Information Reply' },                       #type: information reply
      0x11: { 0x00: 'Address Mask Request' },                    #type: address mask request
      0x12: { 0x00: 'Address Mask Reply' },                      #type: address mask reply
      0x1E: { 0x00: 'Information Request' },
      0x1F: { None: 'Datagram Conversion Error' },
      0x20: { None: 'Mobile Host Redirect' },
      0x21: { None: 'Where-Are-You' },
      0x22: { None: 'Here-I-Am' },
      0x23: { None: 'Mobile Registration Request' },
      0x24: { None: 'Mobile Registration Reply' },
      0x25: { None: 'Domain Name Request' },
      0x26: { None: 'Domain Name Reply' },
      0x27: { None: 'SKIP Algorithm Discovery Protocol' },       #type: SKIP Algorithm
      0x28: { None: 'Photuris (Firefly) security protocol' },    #type: Photuris protocol
      0x29: { None: 'ICMP for experimental mobility protocols such as Seamoby' },
      #0x01: { None: 'Reserved' },                               #type: reserved
      #0x02: { None: 'Reserved' },                               #type: reserved
      #0x07: { None: 'Reserved' },                               #ŧype: reserved
      #0x13: { None: 'Reserved for security' },                  #type: reserved for security
      #0x14: { None: 'Reserved for robustness experiment' },     #type: 20 through 29
      #0x2A: { None: 'Reserved' }                                #type: 42 through 255
    }
  __types_codes_reserved = [ 0x01, 0x02, 0x07 ] + list(range(0x13, 0x1E)) + list(range(0x2A, 0x100))

  # layer datalink
  __dst       = None     # 6 bytes
  __src       = None     # 6 bytes
  __ethertype = 0x0800   # 2 bytes

  # layer network ip header
  __version       = 0x04    # 4 bits
  __header_length = 0x14    # 4 bits
  __ip_type       = 0x00    # 1 byte
  __total_length  = None    # 2 bytes
  __identifier    = None    # 2 bytes
  __ip_flag       = 0b010   # 3 bits
  __fragment      = 0x00    # 13 bits
  __ttl           = 0x78    # 1 byte
  __protocol      = 0x01    # 1 byte
  __ip_checksum   = pack('!H', 0x00)    # 2 bytes
  __src_ip        = None    # 4 bytes
  __dst_ip        = None    # 4 bytes

  # layer transport
  __type       = None    # 1 byte
  __code       = None    # 1 byte
  __seq_number = 0x00    # 2 bytes
  __checksum   = None    # 2 bytes
  __id         = None    # 2 bytes

  def __init__(self, src, dst, src_ip, dst_ip):
    # Layer datalink
    self.src = src
    self.dst = dst

    # Layer network ip header
    self.identifier = unpack('H', os.urandom(2))[0]
    self.src_ip     = src_ip
    self.dst_ip     = dst_ip

    # Layer transport
    self.__seq_number = 0x00
    self.__id         = os.urandom(2)
  #__init__

  def request(self):
    self.type = 0x08
    self.code = 0x00

  # Layer datalink
  def src():
    doc = "The src property."
    def fget(self):
      return self.__src

    def fset(self, v):
      self.__src = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))

    def fdel(self):
      del self.__src

    return locals()
  #end definition src property

  def dst():
    doc = "The dst property."
    def fget(self):
      return self.__dst

    def fset(self, v):
      self.__dst = bytes.fromhex(''.join([ f'{int(x, 16):02x}' for x in v.split(':') ]))

    def fdel(self):
      del self.__dst

    return locals()
  #end definition dst property

  # Layer network ip headers properties
  @property
  def version_length(self):
    return pack('!B', self.__version << 4 | self.__header_length)
  #version_length

  @property
  def ip_type(self):
    return pack('!B', self.__ip_type)

  @property
  def total_length(self):
    return pack('!H', self.__total_length)

  @total_length.setter
  def total_length(self, v):
    self.__total_length = v
  #total_length

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
  def ip_checksum(self):
    ip_header = unpack('!10H', self.version_length + self.ip_type + self.total_length + self.identifier +
                self.flag_fragment + self.ttl + self.protocol + pack('!H', 0x00) +
                self.src_ip + self.dst_ip)

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
  def src_ip(self):
    return self.__src_ip

  @src_ip.setter
  def src_ip(self, v):
    self.__src_ip = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #src_ip

  @property
  def dst_ip(self):
    return self.__dst_ip

  @dst_ip.setter
  def dst_ip(self, v):
    self.__dst_ip = bytes.fromhex(''.join([f'{int(a):02x}' for a in v.split('.') ]))
  #dst_ip

  # Layer transport
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
  def seq_number(self):
    self.__seq_number += 1
    return self.__seq_number
  #seq_number

  @property
  def checksum(self):
    return self.__checksum
  #checksum

  @property
  def id(self):
    return self.__id
  #id
#class icmpPacket
