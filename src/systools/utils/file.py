# -*- coding: utf-8 -*-
#
# ./utils/file.py
# Eduardo Banderas Alba
# 2022-09
#


def readfile(filename, mode='r'):
  out = ''
  with open(filename, mode) as fr:
    out = fr.read()

  return out.strip()
#readfile


def writefile(filename, data='', mode='w'):
  with open(filename, mode) as fw:
    fw.write(data)
#writefile
