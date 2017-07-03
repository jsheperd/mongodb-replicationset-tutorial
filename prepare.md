# Prepare some extra network interfaces
Mongodb can be started in multiple instances on the same PC. It makes simple to emulate replicationsets on a single machine. You can create new subinterfaces with 

    sudo ./prepare_network.sh

I have used satic ip addresses for this test.

# Start multiple mongod sessions
We can start the 3 separate mongod sessions with the

    ./start_mongos.sh

We will have three separate sessions this way.

# Join the sessions
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

    db.log.insert({log:"Replicationset up and running", at: new Date()})

Check the result on the PRIMARY and on the SLAVEs

    db.log.find()

The slave should't allow to read the database, so you have to make it readable

    rs.slaveOk()
    
The delayed slave will show the entry only 3600 seconds later.
