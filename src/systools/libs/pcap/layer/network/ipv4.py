# -*- coding: utf-8 -*-
#
# ./libs/pcap/layer/network/ethenet.py
# Eduardo Banderas Alba
# 2022-08
#
# ethernet frames
#
from ..layer import Layer, LayerException


class ipv4(Layer):

  _HEADER_LEN    = 20
  _unpack_format = '!BBHHHBBH 4s 4s'

  __IPV4_LEN = 4
  __type_protocol = {
    0x00: 'HOPOPT',            # IPv6 Hop-by-Hop Option
    0x01: 'ICMP',              # Internet Control Message Protocol
    0x02: 'IGMP',              # Internet Group Management Protocol
    0x03: 'GGP',               # Gateway-to-Gateway Protocol
    0x04: 'IP-in-IP',          # IP in IP (encapsulation)
    0x05: 'ST',                # Internet Stream Protocol
    0x06: 'TCP',               # Transmission Control Protocol
    0x07: 'CBT',               # Core-based trees
    0x08: 'EGP',               # Exterior Gateway Protocol
    0x09: 'IGP',               # Interior Gateway Protocol (any private interior gateway (used by Cisco for their IGRP))
    0x0A: 'BBN-RCC-MON',       # BBN RCC Monitoring
    0x0B: 'NVP-II',            # Network Voice Protocol
    0x0C: 'PUP',               # Xerox PUP
    0x0D: 'ARGUS',             # ARGUS
    0x0E: 'EMCON',             # EMCON
    0x0F: 'XNET',              # Cross Net Debugger
    0x10: 'CHAOS',             # Chaos
    0x11: 'UDP',               # User Datagram Protocol
    0x12: 'MUX',               # Multiplexing
    0x13: 'DCN-MEAS',          # DCN Measurement Subsystems
    0x14: 'HMP',               # Host Monitoring Protocol
    0x15: 'PRM',               # Packet Radio Measurement
    0x16: 'XNS-IDP',           # XEROX NS IDP
    0x17: 'TRUNK-1',           # Trunk-1
    0x18: 'TRUNK-2',           # Trunk-2
    0x19: 'LEAF-1',            # Leaf-1
    0x1A: 'LEAF-2',            # Leaf-2
    0x1B: 'RDP',               # Reliable Datagram Protocol
    0x1C: 'IRTP',              # Internet Reliable Transaction Protocol
    0x1D: 'ISO-TP4',           # ISO Transport Protocol Class 4
    0x1E: 'NETBLT',            # Bulk Data Transfer Protocol
    0x1F: 'MFE-NSP',           # MFE Network Services Protocol
    0x20: 'MERIT-INP',         # MERIT Internodal Protocol
    0x21: 'DCCP',              # Datagram Congestion Control Protocol
    0x22: '3PC',               # Third Party Connect Protocol
    0x23: 'IDPR',              # Inter-Domain Policy Routing Protocol
    0x24: 'XTP',               # Xpress Transport Protocol
    0x25: 'DDP',               # Datagram Delivery Protocol
    0x26: 'IDPR-CMTP',         # IDPR Control Message Transport Protocol
    0x27: 'TP++',              # TP++ Transport Protocol
    0x28: 'IL',                # IL Transport Protocol
    0x29: 'IPv6',              # IPv6 Encapsulation
    0x2A: 'SDRP',              # Source Demand Routing Protocol
    0x2B: 'IPv6-Route',        # Routing Header for IPv6
    0x2C: 'IPv6-Frag',         # Fragment Header for IPv6
    0x2D: 'IDRP',              # Inter-Domain Routing Protocol
    0x2E: 'RSVP',              # Resource Reservation Protocol
    0x2F: 'GRE',               # Generic Routing Encapsulation
    0x30: 'MHRP',              # Mobile Host Routing Protocol
    0x31: 'BNA',               # BNA
    0x32: 'ESP',               # Encapsulating Security Payload
    0x33: 'AH',                # Authentication Header
    0x34: 'I-NLSP',            # Integrated Net Layer Security Protocol
    0x35: 'SWIPE',             # SwIPe
    0x36: 'NARP',              # NBMA Address Resolution Protocol
    0x37: 'MOBILE',            # IP Mobility (Min Encap)
    0x38: 'TLSP',              # Transport Layer Security Protocol (using Kryptonet key management)
    0x39: 'SKIP',              # Simple Key-Management for Internet Protocol
    0x3A: 'IPv6-ICMP',         # ICMP for IPv6
    0x3B: 'IPv6-NoNxt',        # No Next Header for IPv6
    0x3C: 'IPv6-Opts',         # Destination Options for IPv6
    0x3D: ' ',                 # Any host internal protocol
    0x3E: 'CFTP',              # CFTP
    0x3F: ' ',                 # Any local network
    0x40: 'SAT-EXPAK',         # SATNET and Backroom EXPAK
    0x41: 'KRYPTOLAN',         # Kryptolan
    0x42: 'RVD',               # MIT Remote Virtual Disk Protocol
    0x43: 'IPPC',              # Internet Pluribus Packet Core
    0x44: ' ',                 # Any distributed file system
    0x45: 'SAT-MON',           # SATNET Monitoring
    0x46: 'VISA',              # VISA Protocol
    0x47: 'IPCU',              # Internet Packet Core Utility
    0x48: 'CPNX',              # Computer Protocol Network Executive
    0x49: 'CPHB',              # Computer Protocol Heart Beat
    0x4A: 'WSN',               # Wang Span Network
    0x4B: 'PVP',               # Packet Video Protocol
    0x4C: 'BR-SAT-MON',        # Backroom SATNET Monitoring
    0x4D: 'SUN-ND',            # SUN ND PROTOCOL-Temporary
    0x4E: 'WB-MON',            # WIDEBAND Monitoring
    0x4F: 'WB-EXPAK',          # WIDEBAND EXPAK
    0x50: 'ISO-IP',            # International Organization for Standardization Internet Protocol
    0x51: 'VMTP',              # Versatile Message Transaction Protocol
    0x52: 'SECURE-VMTP',       # Secure Versatile Message Transaction Protocol
    0x53: 'VINES',             # VINES
    0x54: 'TTP',               # TTP
    0x54: 'IPTM',              # Internet Protocol Traffic Manager
    0x55: 'NSFNET-IGP',        # NSFNET-IGP
    0x56: 'DGP',               # Dissimilar Gateway Protocol
    0x57: 'TCF',               # TCF
    0x58: 'EIGRP',             # EIGRP
    0x59: 'OSPF',              # Open Shortest Path First
    0x5A: 'Sprite-RPC',        # Sprite RPC Protocol
    0x5B: 'LARP',              # Locus Address Resolution Protocol
    0x5C: 'MTP',               # Multicast Transport Protocol
    0x5D: 'AX.25',             # AX.25
    0x5E: 'IPIP',              # IP-within-IP Encapsulation Protocol
    0x5F: 'MICP',              # Mobile Internetworking Control Protocol
    0x60: 'SCC-SP',            # Semaphore Communications Sec. Pro
    0x61: 'ETHERIP',           # Ethernet-within-IP Encapsulation
    0x62: 'ENCAP',             # Encapsulation Header
    0x63: ' ',                 # Any private encryption scheme
    0x64: 'GMTP',              # GMTP
    0x65: 'IFMP',              # Ipsilon Flow Management Protocol
    0x66: 'PNNI',              # PNNI over IP
    0x67: 'PIM',               # Protocol Independent Multicast
    0x68: 'ARIS',              # IBM's ARIS (Aggregate Route IP Switching) Protocol
    0x69: 'SCPS',              # SCPS (Space Communications Protocol Standards)
    0x6A: 'QNX',               # QNX
    0x6B: 'A/N',               # Active Networks
    0x6C: 'IPComp',            # IP Payload Compression Protocol
    0x6D: 'SNP',               # Sitara Networks Protocol
    0x6E: 'Compaq-Peer',       # Compaq Peer Protocol
    0x6F: 'IPX-in-IP',         # IPX in IP
    0x70: 'VRRP',              # Virtual Router Redundancy Protocol, Common Address Redundancy Protocol (not IANA assigned)
    0x71: 'PGM',               # PGM Reliable Transport Protocol
    0x72: ' ',                 # Any 0-hop protocol
    0x73: 'L2TP',              # Layer Two Tunneling Protocol Version 3
    0x74: 'DDX',               # D-II Data Exchange (DDX)
    0x75: 'IATP',              # Interactive Agent Transfer Protocol
    0x76: 'STP',               # Schedule Transfer Protocol
    0x77: 'SRP',               # SpectraLink Radio Protocol
    0x78: 'UTI',               # Universal Transport Interface Protocol
    0x79: 'SMP',               # Simple Message Protocol
    0x7A: 'SM',                # Simple Multicast Protocol
    0x7B: 'PTP',               # Performance Transparency Protocol
    0x7C: 'IS-IS over IPv4',   # Intermediate System to Intermediate System (IS-IS) Protocol over IPv4
    0x7D: 'FIRE',              # Flexible Intra-AS Routing Environment
    0x7E: 'CRTP',              # Combat Radio Transport Protocol
    0x7F: 'CRUDP',             # Combat Radio User Datagram
    0x80: 'SSCOPMCE',          # Service-Specific Connection-Oriented Protocol in a Multilink and Connectionless Environment
    0x81: 'IPLT',              #
    0x82: 'SPS',               # Secure Packet Shield
    0x83: 'PIPE',              # Private IP Encapsulation within IP
    0x84: 'SCTP',              # Stream Control Transmission Protocol
    0x85: 'FC',                # Fibre Channel
    0x86: 'RSVP-E2E-IGNORE',   # Reservation Protocol (RSVP) End-to-End Ignore
    0x87: 'Mobility Header',   # Mobility Extension Header for IPv6
    0x88: 'UDPLite',           # Lightweight User Datagram Protocol
    0x89: 'MPLS-in-IP',        # Multiprotocol Label Switching Encapsulated in IP
    0x8A: 'manet',             # MANET Protocols
    0x8B: 'HIP',               # Host Identity Protocol
    0x8C: 'Shim6',             # Site Multihoming by IPv6 Intermediation
    0x8D: 'WESP',              # Wrapped Encapsulating Security Payload
    0x8E: 'ROHC',              # Robust Header Compression
    0x8F: 'Ethernet'
  }

  __type_protocol_support = {
    0x01: 'icmp',              # Internet Control Message Protocol
    0x02: 'igmp',              # Internet Group Management Protocol
    0x06: 'tcp',               # Transmission Control Protocol
    0x08: 'egp',               # Exterior Gateway Protocol
    0x09: 'igp',               # Interior Gateway Protocol (any private interior gateway (used by Cisco for their IGRP))
    0x11: 'udp',               # User Datagram Protocol
  }

  def __init__(self, raw):
    self.__properties = [ 'dst', 'src', 'version', 'header_length', 'total_length', 'ttl',
                          'protocol_id', 'checksum', 'format' ]
    super().__init__(raw)
  #__init__

  def _header(self):
    version_length, \
    type,\
    self.total_length, \
    identifier, \
    flag_fragment, \
    self.ttl, \
    self.protocol_id, \
    self.checksum, \
    self.src, \
    self.dst = self.pktheader

    self.version       = version_length >> 4
    self.header_length = (version_length & 0x0F) * 4
  #_header

  def _data(self):
    if self.protocol:
      mod = None
      if self.protocol in self.TRANSPORT:
        mod = f'{self.PATHLIB}.transport.{self.protocol}'

      self._load_module(mod, self.protocol)
  #_data

  def format():
    def fget(self):
      msg = f'{self.protocol.upper()} '
      if self.protocol in [ 'tcp', 'udp' ]:
        msg += f'ttl: {self.ttl} src {self.src}:{self._module.src} ' + \
               f'-> dst {self.dst}:{self._module.dst} {self._module.format}'

      elif self.protocol in [ 'icmp' ]:
        msg += f'{self._module.format}'

      return msg

    return locals()
  #end definition format property

  def checksum():
    doc = "The checksum property."
    def fget(self):
      return self.__checksum

    def fset(self, v):
      self.___checksum = v

    def fdel(self):
      del self.__checksum

    return locals()
  #end definition checksum property

  def protocol():
    doc = "The protocol property."
    def fget(self):
      return self.__protocol

    def fset(self, v):
      self.__protocol = self.__type_protocol_support.get(v)

    def fdel(self):
      del self.__protocol

    return locals()
  #end definition protocol property

  def protocol_id():
    doc = "The protocol_id property."
    def fget(self):
      return self.__protocol_id

    def fset(self, v):
      self.protocol     = v
      self.__protocol_id = hex(v)

    def fdel(self):
      del self.__protocol_id

    return locals()
  #end definition protocol_id property

  def ttl():
    doc = "The ttl property."
    def fget(self):
      return self.__ttl

    def fset(self, v):
      self.__ttl = v

    def fdel(self):
      del self.__ttl

    return locals()
  #end definition ttl property

  def total_length():
    doc = "The total_length property."
    def fget(self):
      return self.__total_length

    def fset(self, v):
      self.__total_length = v

    def fdel(self):
      del self.__total_length

    return locals()
  #end definition total_length property

  def header_length():
    doc = "The header_length property."
    def fget(self):
      return self.__header_length

    def fset(self, v):
      self.__header_length = v

    def fdel(self):
      del self.__header_length

    return locals()
  #end definition header_length property

  def version():
    doc = "The version property."
    def fget(self):
      return self.__version

    def fset(self, v):
      self.__version = v

    def fdel(self):
      del self.__version

    return locals()
  #end definition version property

  def src():
    doc = "The src property."
    def fget(self):
      return self.__src

    def fset(self, v):
      if not isinstance(v, bytes):
        raise ipv4Exception(f'ERROR: src mac address is not bytes type {type(v)}')

      if len(v) != self.__IPV4_LEN:
        raise ipv4Exception(f'ERROR: src mac address should be {self.__IPV4_LEN} bytes')

      self.__src = '.'.join(map(str, v))

    def fdel(self):
      del self.__src

    return locals()
  #end definition src property

  def dst():
    doc = "The dst property."
    def fget(self):
      return self.__dst

    def fset(self, v):
      if not isinstance(v, bytes):
        raise ipv4Exception(f'ERROR: dst mac address is not bytes type {type(v)}')

      if len(v) != self.__IPV4_LEN:
        raise ipv4Exception(f'ERROR: dst mac address should be {self.__IPV4_LEN} bytes')

      self.__dst = '.'.join(map(str, v))

    def fdel(self):
      del self.__dst

    return locals()
  #end definition dst property

  format        = property(**format())
  checksum      = property(**checksum())
  protocol      = property(**protocol())
  protocol_id   = property(**protocol_id())
  ttl           = property(**ttl())
  total_length  = property(**total_length())
  header_length = property(**header_length())
  version       = property(**version())
  src           = property(**src())
  dst           = property(**dst())
#class ipv4

class ipv4Exception(LayerException):
  pass
#class ipv4Exception