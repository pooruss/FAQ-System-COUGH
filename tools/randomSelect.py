#!/usr/bin/env python
# !-*- coding:utf-8 -*-
# !vim: set ts=4 sw=4 sts=4 tw=100 noet:
# ***************************************************************************
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
# $Id$
#
# **************************************************************************/


import os
import sys
import random

__author__ = 'work <feixiaoxu01baidu.com>'
__date__ = '2016/12/15 10:56:46'
__revision = '$Revision$'

print(sys.getdefaultencoding())
outNum = int(sys.argv[1])
cnt = 0
data = []
for line in sys.stdin:
    if cnt < outNum:
        data.append(line.strip())
        cnt += 1
    else:
        n = random.randint(0, cnt - 1)
        if n < outNum:
            data[n] = line.strip()
        cnt += 1

for line in data:
    print (line)

