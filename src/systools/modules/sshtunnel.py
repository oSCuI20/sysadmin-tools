# -*- coding: utf-8 -*-
#
# ./modules/sshtunnel.py
# Eduardo Banderas Alba
# 2022-09
#
import os
import socket
import string
import hashlib

from subprocess import Popen, PIPE
from signal     import SIGTERM, SIGKILL

from modules   import Device, Config
from utils     import Logger, readfile, writefile


ALLOWED_SSH_USER_CHARACTERS = f'{string.ascii_letters}{string.digits}_-'


class SSHTunnel(object):

  __host    = None
  __user    = None
  __privkey = None
  __port    = 22
  __pidfile = None

  __bindhost = '127.0.0.1'
  __bindport = None
  __hostforward = '127.0.0.1'
  __portforward = None

  __ssh_command = None
  __ssh_options = ('-o UserKnownHostsFile=/dev/null', '-o StrictHostKeyChecking=no',
                   '-o ServerAliveInterval=60', '-o ServerAliveCountMax=2',
                   '-o ExitOnForwardFailure=yes', '-o PasswordAuthentication=no',
                   '-o ConnectTimeout=15')

  def __init__(self, host=None, user=None, privkey=None, port=22,
                     bindhost='127.0.0.1', bindport=8422,
                     hostforward='127.0.0.1', portforward=22, reversed=True):
    self.logger = Logger()

    self.host = host
    self.port = port
    self.user = user

    self.bindhost = bindhost
    self.bindport = bindport
    self.hostforward = hostforward
    self.portforward = portforward

    self.privkey  = privkey

    hash = hashlib.sha256(self.__concat_props().encode()).hexdigest()

    self.__pidfile = f'{Config.pidpath}/{hash}.pid'

    self.logger.debug(f'pid file {self.__pidfile}')

    mode = '-L'
    if reversed:
      mode = '-R'

    self.__ssh_command = f'/usr/bin/ssh {" ".join(self.ssh_options)} -p {self.port} ' + \
                         f'-i {self.privkey} -l {self.user} {self.host} ' + \
                         f'{mode} {self.bindhost}:{self.bindport}:{self.hostforward}:{self.portforward}'
  #__init__

  def start(self):
    self.logger.log((-1, f'Starting ssh tunnel: \n' +
                         f'\thost: {self.host}, port: {self.port}, user: {self.user}\n' +
                         f'\tbindhost: {self.bindhost}, bindport: {self.bindport}\n' +
                         f'\thostforward: {self.hostforward}, portforward: {self.portforward}'))
    self.logger.log((-1, f'cmdline: {self.__ssh_command}'))

    print(self.__pidfile)
    print(self.__ssh_command)
    if self.__cmd_exists():
      print('exists')

  #start

  def stop(self):
    pass
  #stop

  def __cmd_exists(self):
    pid = 0
    if os.path.isfile(self.__pidfile):
      pid = int(readfile(self.__pidfile).strip())

    for currentpid, currentproc in Device.process.items():
      if pid == currentpid and self.__ssh_command == currentproc['cmdline']:
        return True

    return False
  #__cmd_status

  def __concat_props(self):
    return (f'{self.bindhost}-{self.bindport}-{self.hostforward}-{self.portforward}')
  #__concat_props

  @property
  def ssh_options(self):
    return self.__ssh_options

  @ssh_options.setter
  def ssh_options(self, v):
    if not v:
      raise Exception(f'ssh_options property is missing')

     if not isinstance(v, tuple):
       raise Exception(f'ssh_options property invalid type')

    self.__ssh_options = v
  #ssh_options

  @property
  def host(self):
    return self.__host

  @host.setter
  def host(self, v):
    if not v:
      raise Exception(f'host property is missing')

    try:
      socket.inet_aton(socket.gethostbyname(v))    # check
    except socket.gaierror:
      raise Exception(f'host property has invalid value, {err}')

    self.__host = v
  #host

  @property
  def user(self):
    return self.__user

  @user.setter
  def user(self, v):
    if not v:
      raise Exception(f'user property is missing')

    if not all([ c in ALLOWED_SSH_USER_CHARACTERS for c in v ]):
      raise Exception(f'user value {v} not valid')

    self.__user = v
  #user

  @property
  def privkey(self):
    return self.__privkey

  @privkey.setter
  def privkey(self, v):
    if not v:
      raise Exception(f'privkey property is missing')

    if not os.path.isfile(v):
      raise Exception(f'private key not found, {v}')

    self.__privkey = v
  #privkey

  @property
  def port(self):
    return self.__port

  @port.setter
  def port(self, v):
    if not v:
      raise Exception(f'port property is missing')

    try:
      int(v)
    except ValueError as err:
      raise Exception(f'port value {v} not valid')

    self.__port = v
  #port

  @property
  def bindhost(self):
    return self.__bindhost

  @bindhost.setter
  def bindhost(self, v):
    if not v:
      raise Exception(f'bindhost property is missing')

    try:
      socket.inet_aton(socket.gethostbyname(v))    # check
    except socket.gaierror as err:
      raise Exception(f'bindhost property has invalid value, {err}')

    self.__bindhost = v
  #bindhost

  @property
  def bindport(self):
    return self.__bindport

  @bindport.setter
  def bindport(self, v):
    if not v:
      raise Exception(f'bindport property is missing')

    try:
      int(v)
    except ValueError as err:
      raise Exception(f'bindport value {v} not valid')

    self.__bindport = v
  #bindport

  @property
  def hostforward(self):
    return self.__hostforward

  @hostforward.setter
  def hostforward(self, v):
    if not v:
      raise Exception(f'hostforward property is missing')

    try:
      socket.inet_aton(socket.gethostbyname(v))    # check
    except socket.gaierror as err:
      raise Exception(f'hostforward property has invalid value, {err}')

    self.__hostforward = v
  #hostforward

  @property
  def portforward(self):
    return self.__portforward

  @portforward.setter
  def portforward(self, v):
    if not v:
      raise Exception(f'portforward property is missing')

    try:
      int(v)
    except ValueError as err:
      raise Exception(f'portforward value {v} not valid')

    self.__portforward = v
  #portforward
#class SSHTunnel
