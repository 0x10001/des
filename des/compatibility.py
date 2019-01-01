#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: compatibility.py
     @time: 2018-12-27 22:31
"""

try:
    number_type = int, long
except NameError:
    number_type = int

try:
    iter_range = xrange
except NameError:
    iter_range = range
