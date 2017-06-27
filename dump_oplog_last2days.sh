#!/usr/bin/env bash
mongodump --host 10.0.0.1 -d local -c oplog.rs -o oplog2days --query " \
{  \$and : \
	[ { \"ts\" : { \$gt :  Timestamp(`date --date="2 days ago" +%s`, 1) } },  \
	  { \"op\" : { \$ne : \"n\" } } \
	] \
}"

