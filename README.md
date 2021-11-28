<h1 align="center"> :runner: Kafka Offset Demo :runner:</h1>
<p align="center"> Demo showing how Kafka users can manually set the offset of the next consumed message with a call to the query procedure.</p>

## :bookmark_tabs: Instructions

Place yourself in the root folder and start Zookeeper, Kafka and Memgraph by running: 
```
docker-compose build
docker-compose up core
```
After that, run the Kafka producer:
```
docker-compose up kafka-producer
```

Now open [Memgraph Lab](https://memgraph.com/docs/memgraph-lab/), create and start stream:
```
CREATE KAFKA STREAM sales_stream TOPICS sales TRANSFORM kafkaoffset.sales;
START STREAM sales_stream;
```

You'll notice how nodes are being created in the Overview tab. Feel free to check out how the created nodes look like with query:
```
MATCH (n)
RETURN n
LIMIT 10;
```

Next, stop the stream:
```
STOP STREAM sales_stream;
```

Let's say you deleted all of your nodes in the database with:
```
MATCH (n)
DETACH DELETE n;
```

If you start the stream again, the last committed offset will be retrieved from the Kafka cluster. This means that you won't get all messages from the stream, but the ones starting from the last committed offset. New Memgraph feature is that you can change that easily and quickly by running:
```
CALL mg.kafka_set_stream_offset("sales_stream", -1);
```
After that, when you start your stream again, the consumed messages will be from the beginning of the stream. You'll notice the jump in the number of your nodes in the Overview tab, since all queries from consumed messages from before will be quickly run.

If you want to continue where the last committed offset is, stop the stream, and run:
```
CALL mg.kafka_set_stream_offset("sales_stream", -2);
```

To make sure that only new messages are being consumed, again delete everything in your database and start the stream. Then you can notice that the number of nodes in the Overview tab is slowly growing from zero.

## :scroll: References
For more information about this new feature, check out our [docs](https://memgraph.com/docs/memgraph/reference-guide/streams#setting-a-stream-offset).