# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:36:58 2021

@author: Brian Ho
"""
import os
def MkDir():
    dirs = input()
    dirs = dirs.split('、')
 
    for dir in dirs:
        os.mkdir(dir)
        
MkDir()