# PITR

## Prepare some database content

Insert something into the replicationset

    echo 'db.log.insert({log:"Replicationset is running", at: new Date()})' | mongo --host rs/10.0.0.1

Make a full backup (we have only one record in the log)

    mongodump --host rs/10.0.0.1  -o backupOrig

A little later put some more entries

    echo 'db.log.insert({log:"Backup created", at: new Date()})' | mongo --host rs/10.0.0.1
    echo 'db.log.insert({log:"We are happy, nothing is BAD", at: new Date()})' | mongo --host rs/10.0.0.1
    echo 'db.log.insert({log:"BAD things happen", at: new Date()})' | mongo --host rs/10.0.0.1

# Restore the database to the happy state

## Dump the oplog, where mongo store the database changes

    mongodump --host rs/10.0.0.1 -d local -c oplog.rs -o oplog
    
## Find the time when we were happy

    echo 'db.log.find({ log: /BAD/ })' | mongo --host rs/10.0.0.1

it gave the next result in my case, where the entry dates visible in the records

    MongoDB server version: 3.4.5
    { "_id" : ObjectId("595cdc81dc6ab13427ea1dd3"), "log" : "We are happy, nothing is BAD", "at" : ISODate("2017-07-05T12:33:05.782Z") }
    { "_id" : ObjectId("595cdc880502241a73e936be"), "log" : "BAD things happen", "at" : ISODate("2017-07-05T12:33:12.210Z") }
    bye

We can check the actions's date in the oplog also

    echo """use local
    db.oplog.rs.find({op: 'i'}, {ts: 1, o: 1}) """ | mongo --host 10.0.0.1
    
    
    MongoDB server version: 3.4.5
    switched to db local
    { "ts" : Timestamp(1499257918, 2), "o" : { "_id" : ObjectId("595cdc3ed4b3f9153d26bc22"), "log" : "Replicationset is running", "at" : ISODate("2017-07-05T12:31:58.868Z") } }
    { "ts" : Timestamp(1499257973, 2), "o" : { "_id" : ObjectId("595cdc7577c130fa4bfc783f"), "log" : "Backup created", "at" : ISODate("2017-07-05T12:32:53.906Z") } }
    { "ts" : Timestamp(1499257985, 1), "o" : { "_id" : ObjectId("595cdc81dc6ab13427ea1dd3"), "log" : "We are happy, nothing is BAD", "at" : ISODate("2017-07-05T12:33:05.782Z") } }
    { "ts" : Timestamp(1499257992, 1), "o" : { "_id" : ObjectId("595cdc880502241a73e936be"), "log" : "BAD things happen", "at" : ISODate("2017-07-05T12:33:12.210Z") } }
    bye

    
# Roll back to the backupOrig

    mongorestore --host rs/10.0.0.1 --drop backupOrig

# Replay the oplog

    mongorestore --host rs/10.0.0.1 --oplogReplay oplog --oplogLimit 1499257992

We are happy again as

    echo 'db.log.find()' | mongo --host rs/10.0.0.1
    
results this:

    MongoDB server version: 3.4.5
    { "_id" : ObjectId("595cdc3ed4b3f9153d26bc22"), "log" : "Replicationset is running", "at" : ISODate("2017-07-05T12:31:58.868Z") }
    { "_id" : ObjectId("595cdc7577c130fa4bfc783f"), "log" : "Backup created", "at" : ISODate("2017-07-05T12:32:53.906Z") }
    { "_id" : ObjectId("595cdc81dc6ab13427ea1dd3"), "log" : "We are happy, nothing is BAD", "at" : ISODate("2017-07-05T12:33:05.782Z") }
    bye


# Rollback suceeded
    


    

