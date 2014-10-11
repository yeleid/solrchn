#!/usr/bin/python

import sys
import getopt

usage = """
Usage: build-collection.sh
     -h                        Display this usage message
     -n collection_name        Name of the collection    
     -s shards_num             Number of shards, default 1
     -r replication_factor     Factor of replication, default 1
"""

opts, args = getopt.getopt(sys.argv[1:], "hn:s:r:")
name = None
shard = 1
replica = 1

for op, value in opts:
  if op == "-n":
    name = value
  elif op == "-s":
    shard = int(value)
  elif op == "-r":
    replica = int(value)
  elif op == "-h":
    print usage
    sys.exit(0)

if name is None:
  print "Error: collection name is not specified."
  print usage
  sys.exit(1)

print "Parameter List:"
print "  Collection Name      : {0}".format(name)
print "  Number of Shards     : {0}".format(shard)
print "  Factor of Replication: {0}".format(replica)

from subprocess import call
print
print "Generate instance:"
instance_dir = "tmp/{0}_configs".format(name)
cmd = "solrctl instancedir --generate {0}".format(instance_dir)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Override schema.xml:"
path = "{0}/conf/".format(instance_dir)
cmd = "cp conf/schema.xml {0}".format(path)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Create instance:"
cmd = "solrctl instancedir --create {0} {1}".format(name, instance_dir)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Create collection:"
cmd = "solrctl collection --create {0} -s {1} -r {2}".format(name, shard, replica)
print "  {0}".format(cmd)
call(cmd, shell=True)

sys.exit(0)
