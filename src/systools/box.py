#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ./box.py
# Eduardo Banderas Alba
# 2022-09
#
import sys, os

from time  import sleep
from utils import Daemon

def main():
  b = box('./pidfile/pidtest.pid')

  b.stop()

def parse_arguments():
  return

class box(Daemon):
  terminate = False
  def run(self):
    while not self.terminate:
      print('test')
      sleep(1)

if __name__ == "__main__":
  try:    reload(sys); sys.setdefaultencoding("utf8")
  except: pass

  main()
