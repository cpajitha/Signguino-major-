# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 19:56:12 2024

@author: Sys
"""

import splitfolders
dr='dataset/data'
splitfolders.ratio(dr,"dataset/datasplit",ratio=(0.8,0.2))
