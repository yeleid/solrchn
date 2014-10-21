#!/usr/bin/python

import sys
import getopt

usage = """
Usage: rm_ngdata_index.py
     -h                        Display this usage message
     -i indexer_name           Name of the indexer
     -z zk_host                Zk host
"""

opts, args = getopt.getopt(sys.argv[1:], "hi:c:z:")
name = None
zk_host = None
indexer = None

for op, value in opts:
  if op == "-z":
    zk_host = value
  elif op == "-i":
    indexer = value
  elif op == "-h":
    print usage
    sys.exit(0)

if zk_host is None or indexer is None:
  print "Error: some parameter is missing."
  print usage
  sys.exit(1)

print "Parameter List:"
print "  Indexer Name    : {0}".format(indexer)
print "  Zk Host         : {0}".format(zk_host)

from subprocess import call
print
print "Delete indexer:"
cmd = "hbase-indexer delete-indexer -n {1} -z {0}:2181".format(zk_host, indexer)
call(cmd, shell=True)

print 
print "Check indexers:"
cmd = "hbase-indexer list-indexers -z {0}:2181".format(zk_host)
call(cmd, shell=True)

sys.exit(0)

