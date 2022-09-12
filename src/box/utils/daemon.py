# -*- coding: utf-8 -*-
#
# ./utils/daemon.py
# Eduardo Banderas Alba
# 2022-09
import os, sys
import io, atexit

from signal import SIGTERM, SIGKILL
from time   import sleep

from utils  import Logger, readfile, writefile


class Daemon:

  def __init__(self, pidfile=None, stdin=None, stdout=None, stderr=None):
    self.__stdin  = stdin  or '/dev/null'
    self.__stdout = stdout or '/dev/null'
    self.__stderr = stderr or '/dev/null'

    self.logger = Logger()

    self.__pidfile = pidfile or f'{os.getcwd}/pidfile/daemon.pid'
    self.logger.debug(f'pid file {self.__pidfile}')

    self.__initialize__()
  #__init__

  def __initialize__(self):
    dir = os.path.dirname(self.__pidfile)

    if not os.path.exists(dir):
      os.makedirs(dir, 0o700)

    if os.path.isfile(dir):
      self.logger.halt('error! cannot create directory, exists and it`s a directory', 1)
  #__initialize__

  def daemonize(self):
    try:
      pid = os.fork()
      if pid > 0:
        self.logger.halt(f'first parent {pid}, exit')

    except OSError as err:
      self.logger.halt(f'fork #1 failure, {err.errno} ({err.strerror})', 1)

    os.chdir(os.getcwd())
    os.setsid()
    os.umask(0)

    try:
      pid = os.fork()
      if pid > 0:
        self.logger.halt(f'seconds parent {pid}, exit')

    except OSError as err:
      self.logger.halt(f'fork #2 failure, {err.errno} ({err.strerror})', 1)

    self.logger.log((-1, 'daemon started'))

    # redirect file descriptors
    sys.stdout.flush()
    sys.stderr.flush()

    fdin  = io.open(self.__stdin, 'r')
    fdout = io.open(self.__stdout, 'a')
    fderr = io.open(self.__stderr, 'a')

    os.dup2(fdin.fileno(), sys.stdin.fileno())
    os.dup2(fdout.fileno(), sys.stdout.fileno())
    os.dup2(fderr.fileno(), sys.stderr.fileno())

    atexit.register(self.delete_pid)
    pid = os.getpid()

    writefile(self.__pidfile, str(pid))
  #daemonize

  def delete_pid(self):
    os.remove(self.__pidfile)
  #delete_pid

  def __check_process__(self, pid):
    try:
      os.kill(pid, 0)
    except OSError:
      return False

    return True
  #__check_process__

  def start(self):
    # check if the daemon already runs
    try:
      pid = int(readfile(self.__pidfile))

      if not self.__check_process__(pid):
        pid = None
        self.delete_pid()
    except IOError:
      pid = None

    if pid:
      self.logger.halt(f'{pid} exists. The daemon is running')

    self.daemonize()
    self.run()
  #start

  def stop(self):
    try:
      pid = int(readfile(self.__pidfile))

    except IOError:
      self.logger.halt(f'pid not found, daemon is running?')

    procs = f'/proc/{pid}/task'

    if os.path.isdir(procs):
      for process in os.listdir(procs):
        os.kill(int(process), SIGTERM)
        os.kill(int(process), SIGKILL)
        sleep(0.1)
      #endfor
    #endif
  #stop

  def restart(self):
    self.stop()
    self.start()
  #restart

  def run(self):
    """
      This method should be override
    """
    pass
