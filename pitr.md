# PITR

Insert something into the replicationset

    echo 'db.log.insert({log:"Replicationset is running", at: new Date()})' | mongo --host rs/10.0.0.1

Make a full backup (we have only one record in the log)

    mongodump --host rs/10.0.0.1  -o backupOrig

A little later put some more entries

    echo 'db.log.insert({log:"Backup created", at: new Date()})' | mongo --host rs/10.0.0.1
    echo 'db.log.insert({log:"We are happy, nothing is BAD", at: new Date()})' | mongo --host rs/10.0.0.1
    echo 'db.log.insert({log:"BAD things happen", at: new Date()})' | mongo --host rs/10.0.0.1

# Restore the database to the happy state

Dump the oplog, where mongo store the database chnages

    mongodump --host rs/10.0.0.1 -d local -c oplog.rs -o oplog
    
Find the time when we were happy

    echo 'db.log.find({ log: /BAD/ })' | mongo --host rs/10.0.0.1

it gave the next result in my case

    MongoDB server version: 3.4.4
    { "_id" : ObjectId("595a61ed4d1e3830ed373249"), "log" : "We are happy, nothing is BAD", "at" : ISODate("2017-07-03T15:25:33.604Z") }
    { "_id" : ObjectId("595a61f96b8bad461b2f849b"), "log" : "BAD things happen", "at" : ISODate("2017-07-03T15:25:45.238Z") }
    bye

Roll back to the backupOrig

    mongorestore --host rs/10.0.0.1 --drop backupOrig

Replay the oplog

    mongorestore --host rs/10.0.0.1 --oplogReplay oplog --oplogLimit `date --date='2017-07-03T15:25:35Z' +"%s"`

We are happy again as

    echo 'db.log.find()' | mongo --host rs/10.0.0.1
    
results this:

    MongoDB server version: 3.4.4
    { "_id" : ObjectId("595a5d6dcafe71b0cc12c0db"), "log" : "Replicationset up and running", "at" : ISODate("2017-07-03T15:06:21.343Z") }
    { "_id" : ObjectId("595a61e32be74348d722096a"), "log" : "Backup created", "at" : ISODate("2017-07-03T15:25:23.882Z") }
    { "_id" : ObjectId("595a61ed4d1e3830ed373249"), "log" : "We are happy, nothing is BAD", "at" : ISODate("2017-07-03T15:25:33.604Z") }
    bye

    
    


    

