from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.dataframe import DataFrame


def main():
    sc = SparkContext(appName="recomEngineStream")
    sc.setLogLevel("WARN")

    ssc = StreamingContext(sc, 10)

    kafkaStream = KafkaUtils.createStream(
        ssc, 'zookeeper:2181', 'PLAINTEXT', {'test-topic': 1},)

    lines = kafkaStream.map(lambda x: x[1])

    # Must fix to write stream to DB
    # print("Writing to the mongodb")
    # streamDF.write.format(
    #     "com.mongodb.spark.sql.DefaultSource") \
    #     .option("database", "transactions") \
    #     .option("collection", "stream") \
    #     .mode("append") \
    #     .save()

    lines.pprint()

    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    main()
