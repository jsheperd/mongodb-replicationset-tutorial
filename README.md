# mongodb-replicationset-tutorial
The simplest way to learn mongodb replication management is to run a replication set on your PC. Forget vagrant and vmware, we needn't any of them to learn. Mongodb can manage your database cluster out of the box with minimal effort.

# How to test replicationsets

## Prepare some extra network interfaces
Mongodb can be started in multiple instances on the same PC. It makes simple to emulate replicationsets on a single machine. You can create new subinterfaces with 

    sudo ./prepare_network.sh

I have used satic ip addresses for this test.

## Start multiple mongod sessions
We can start the 3 separate mongod sessions with the

    ./start_mongos.sh

We will have three separate sessions this way.

## Join the sessions
Start a mongo shell that connects to the db01 server session

    mongo --host 10.0.0.1
    
Enter the next commands to the db01 shell

    rs.initiate({
      _id: "rs",
      members: [ 
        { _id: 0, host: "10.0.0.1"},
        { _id: 1, host: "10.0.0.2"},
        { _id: 2, host: "10.0.0.3", hidden: true, priority: 0,  slaveDelay: NumberLong(3600)}
      ]
    })
    
The replication has been set up now with point in time recovery capabilities.

You can connect to the replicationset its name and one server's address like:

    mongo --host rs/10.0.0.1

You can also connect to a specific mongodb instance like:

    mongo --host 10.0.0.1
    
or
    
    mongo --host 10.0.0.2
    
or

    mongo --host 10.0.0.3
    

We can modify records only on the PRIMARY instance.
The good thing with mongo, we can connect to the PRIMARY by defining the recordset at connection.

    db.test.insert({"name":"0001"})
    db.test.insert({"name":"0002"})
    db.test.insert({"name":"0003"})

Check the result on the PRIMARY and on the SLAVEs

    db.test.find()

The slave should't allow to read the database, so you have to make it readable

    rs.slaveOk()
    

