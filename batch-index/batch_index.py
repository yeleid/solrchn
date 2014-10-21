#!/usr/bin/python

import sys
import getopt

usage = """
Usage: batch_index.py
     -h                        Display this usage message
     -c collection_name        Name of the collection
     -n namenode_host          Namenode host
     -z zk_host                Zk host
"""

opts, args = getopt.getopt(sys.argv[1:], "hc:n:z:")
name = None
hdfs_host = None
zk_host = None

for op, value in opts:
  if op == "-c":
    name = value
  elif op == "-n":
    hdfs_host = value
  elif op == "-z":
    zk_host = value
  elif op == "-h":
    print usage
    sys.exit(0)

if name is None or hdfs_host is None or zk_host is None:
  print "Error: some parameter is missing."
  print usage
  sys.exit(1)


print "Parameter List:"
print "  Collection Name : {0}".format(name)
print "  Zk Host         : {0}".format(zk_host)

from subprocess import call
print
print "Prepare docs:"
cmd = "hadoop fs -ls /tmp/{0}_indir && hadoop fs -rm -r -skipTrash /tmp/{0}_indir".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)
cmd = "hadoop fs -mkdir -p /tmp/{0}_indir".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)
cmd = "hadoop fs -copyFromLocal data/* /tmp/{0}_indir/".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Delete indexed docs:"
cmd = "solrctl collection --deletedocs {0}".format(name)
print "  {0}".format(cmd)
call(cmd, shell=True)

print
print "Generate morphline configuration:"
template = "template/morphlines.template"
morphline = "tmp/morphlines.conf"
print "  src   : {0}".format(template)
print "  target: {0}".format(morphline)

src = file(template, "r")
dest = file(morphline, "w")
for line in src.readlines():
  dest.write(line.replace("[[COLLECTION_NAME]]", name).replace("[[ZK_HOST]]", zk_host))

src.close()
dest.close()

print
print "MapReduce Index:"
config = "/etc/hadoop/conf.cloudera.yarn"
parcel = "/opt/cloudera/parcels/CDH"
jar = "{0}/lib/solr/contrib/mr/search-mr-*-job.jar".format(parcel)
libjars = "lib/lucene-analyzers-smartcn-4.4.0-cdh5.1.3.jar"
cls = "org.apache.solr.hadoop.MapReduceIndexerTool"
opts = "'mapred.child.java.opts=-Xmx500m'"
log4j = "{0}/share/doc/search*/examples/solr-nrt/log4j.properties".format(parcel)
# hdfs_host = "ip-172-31-34-100.us-west-2.compute.internal"
input = "hdfs://{0}:8020/tmp/{1}_indir".format(hdfs_host, name)
output = "hdfs://{0}:8020/tmp/{1}_outdir".format(hdfs_host, name)
# zk_host = "ip-172-31-34-100.us-west-2.compute.internal"
zk = "{0}:2181/solr".format(zk_host)

cmd = "hadoop --config {0} jar {1} {2} --libjars {3} -D {4} --log4j {5} --morphline-file {6} --output-dir {7} --verbose --go-live --zk-host {8} --collection {9} {10}".format(config, jar, cls, libjars, opts, log4j, morphline, output, zk, name, input)
print cmd
call(cmd, shell=True)

sys.exit(0)
