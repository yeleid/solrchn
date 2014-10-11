#!/usr/bin/python

import sys
import getopt

usage = """
Usage: undo-collection.sh
     -h                        Display this usage message
     -n collection_name        Name of the collection
"""

opts, args = getopt.getopt(sys.argv[1:], "hn:")
name = None

for op, value in opts:
  if op == "-n":
    name = value
  elif op == "-h":
    print usage
    sys.exit(0)

if name is None:
  print "Error: collection name is not specified."
  print usage
  sys.exit(1)

print "Parameter List:"
print "  Collection Name      : {0}".format(name)

from subprocess import call
print
print "Delete collection:"
cmd = "solrctl collection --delete {0}".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Delete instance:"
cmd = "solrctl instancedir --delete {0}".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Trash instance:"
instance_dir = "tmp/{0}_configs".format(name)
cmd = "rm -rf {0}".format(instance_dir)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Cleaning HDFS:"
hdfs_dir = "/solr/{0}".format(name)
cmd = "hadoop fs -rm -r -skipTrash {0}".format(hdfs_dir)
print "  {0}".format(cmd)
call(cmd, shell=True)

sys.exit(0)

