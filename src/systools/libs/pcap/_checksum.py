# -*- coding: utf-8 -*-
#
# ./libs/_checksum.py
# Eduardo Banderas Alba
# 2022-09
#
# calculate checksum
#


def checksum(t):
  checksum, count, maxcount = (0, 0, len(t))

  while count < maxcount:
    checksum += t[count]
    checksum &= 0xffffffff
    count  += 1
  #endwhile

  if count < len(t):
    checksum += t[-1]
    checksum &= 0xffffffff

  while checksum >> 16:
    checksum = (checksum >> 16) + (checksum & 0xffff)

  checksum = checksum + (checksum >> 16)

  return ~checksum & 0xffff
#checksum
