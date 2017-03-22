# mongodb-replicationset-tutorial
The simplest way to learn mongodb replication management is to run a replication set on your PC. Forget vagrant and vmware, we needn't any of them to learn. Mongodb can manage your database cluster out of the box with minimal effort.

# How to test replicationsets

## Prepare some extra network interfaces
Mongodb can be started in multiple instances on the same PC. It makes simple to emulate replicationsets on a single machine. You can create new subinterfaces with ./prepare_network.sh. I have used satic ip addresses for this test.

## Start multiple mongod sessions
We can start the separate mongod sessions with the start_mongos.sh.
We will have separate sessions this way.

## Join the sessions
Start a mongo shell that connects to the db01 server session

    mongo --host 192.168.0.110
    
Enter the next commands to the db01 shell

    rs.initiate({
      _id: "rs",
      members: [ 
        { _id: 0, host: "192.168.0.110:27017"},
        { _id: 1, host: "192.168.0.111:27017"},
        { _id: 2, host: "192.168.0.112:27017"}
      ]
    })
    
The replication has been set up now.


## Insert some records
    db.test.insert({"name":"0001"})
    db.test.insert({"name":"0002"})
    db.test.insert({"name":"0003"})

## Check the result
    db.test.find()

## Make slaves readable
    rs.slaveOk()
    

