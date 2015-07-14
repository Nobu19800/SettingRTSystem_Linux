#!/usr/bin/env python
# -*- Python -*-



import sys,os

import OpenRTM_aist

import LoadRTCs

def main():
  manager = OpenRTM_aist.Manager.init(sys.argv)

  manager.activateManager()
  lcs = LoadRTCs.LoadRTCs(manager)
  lcs.openFile()
  
  manager.runManager()

  return

if __name__ == "__main__":
  main()
  #os.system("shutdown -h now")
