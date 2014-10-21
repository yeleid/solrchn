#!/usr/bin/python

import sys
import getopt

usage = """
Usage: ngdata_index.py
     -h                        Display this usage message
     -i indexer_name           Name of the indexer
     -c collection_name        Name of the collection
     -z zk_host                Zk host
"""

opts, args = getopt.getopt(sys.argv[1:], "hi:c:z:")
name = None
zk_host = None
indexer = None

for op, value in opts:
  if op == "-c":
    name = value
  elif op == "-z":
    zk_host = value
  elif op == "-i":
    indexer = value
  elif op == "-h":
    print usage
    sys.exit(0)

if name is None or zk_host is None or indexer is None:
  print "Error: some parameter is missing."
  print usage
  sys.exit(1)

print "Parameter List:"
print "  Collection Name : {0}".format(name)
print "  Indexer Name    : {0}".format(indexer)
print "  Zk Host         : {0}".format(zk_host)

from subprocess import call
print
print "Register indexer:"
cmd = "hbase-indexer add-indexer -n {2} -c indexer/indexer-config.xml -cp solr.zk={0}:2181/solr -cp solr.collection={1} -z {0}:2181".format(zk_host, name, indexer)
call(cmd, shell=True)

print 
print "Check indexers:"
cmd = "hbase-indexer list-indexers -z {0}:2181".format(zk_host)
call(cmd, shell=True)

print
print "Generate morphline configuration:"
template = "indexer/indexer-morphline.template"
morphline = "indexer/indexer-morphline.conf"
print "  src   : {0}".format(template)
print "  target: {0}".format(morphline)

src = file(template, "r")
dest = file(morphline, "w")
for line in src.readlines():
  dest.write(line.replace("[[COLLECTION_NAME]]", name).replace("[[ZK_HOST]]", zk_host))

src.close()
dest.close()

sys.exit(0)

