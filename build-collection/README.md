build-collection
=======

This tool helps you quick setup a solr Chinese search engine on CDH

copy the library into parcels:

    cp lib/lucene-analyzers-smartcn-4.4.0-cdh5.1.3.jar  /opt/cloudera/parcels/CDH/lib/solr/webapps/solr/WEB-INF/lib/

build Chinese collections on CDH:

    ./build-collection.py -n chn

remove Chinese collections on CDH:

    ./undo-collection.py -n chn
