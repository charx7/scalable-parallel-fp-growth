from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.dataframe import DataFrame
import json


def main():
    sc = SparkContext(appName="recomEngineStream")
    sc.setLogLevel("WARN")

    ssc = StreamingContext(sc, 10)

    # Create the Kafka stream connected to zookeeper and appropriate topic
    kafkaStream = KafkaUtils.createStream(
        ssc, 'zookeeper:2181', 'spark-stream', {'live-transactions': 1},)

    # Parse the JSON data
    parsed_Data = kafkaStream.map(lambda x: json.loads(x[1])[0])
    # Print the parsed transactions
    # parsed_Data.pprint()

    # Counts the number of transactions in the batch.
    parsed_Data.count().map(lambda x: 'Transactions in this batch: %s' % x).pprint()

    product_Codes = parsed_Data.flatMap(lambda x: x["ProductCode"])

    product_Count = product_Codes.countByValue()

    sorted_product_Counts = product_Count.transform(
        (lambda foo: foo.sortBy(lambda x: -x[1])))

    top_five_products = sorted_product_Counts.transform(
        lambda rdd: sc.parallelize(rdd.take(5)))

    top_five_products.pprint()


def createContext():
    sc = SparkContext(appName="recomEngineStream")
    sc.setLogLevel("WARN")
    ssc = StreamingContext(sc, 5)

    # Define Kafka Consumer
    kafkaStream = KafkaUtils.createStream(
        ssc, 'zookeeper:2181', 'spark-stream', {'live-transactions': 1},)

    ## --- Processing
    # Extract transactions
    parsed_Data = kafkaStream.map(lambda x: json.loads(x[1])[0])

    # Count number of transactions in the batch
    count_this_batch = parsed_Data.count().map(
        lambda x: 'Transactions in this batch: %s' % x)

    # Count by windowed time period
    count_windowed = kafkaStream.countByWindow(60, 5).map(
        lambda x: ('Transactions total (One minute rolling count): %s' % x))

    # Get =products
    product_Codes = parsed_Data.flatMap(lambda x: x["ProductCode"])

    # Count each value and number of occurences
    count_values_this_batch = product_Codes.countByValue()\
        .transform(lambda rdd: rdd
                   .sortBy(lambda x: -x[1]))\
        .map(lambda x: "Product counts this batch:\tValue %s\tCount %s" % (x[0], x[1]))

    # Count each value and number of occurences in the batch windowed
    count_values_windowed = product_Codes.countByValueAndWindow(60, 5)\
        .transform(lambda rdd: rdd
                   .sortBy(lambda x: -x[1]))\
        .map(lambda x: "Product counts (One minute rolling):\tValue %s\tCount %s" % (x[0], x[1]))

    # Write total product counts to stdout
    # Done with a union here instead of two separate pprint statements just to make it cleaner to display
    count_this_batch.union(count_windowed).pprint()

    # Write product counts to stdout
    count_values_this_batch.pprint(5)
    count_values_windowed.pprint(5)

    return ssc


if __name__ == '__main__':
    ssc = StreamingContext.getOrCreate(
        '/tmp/checkpoint_v01', lambda: createContext())
    ssc.start()
    ssc.awaitTermination()
