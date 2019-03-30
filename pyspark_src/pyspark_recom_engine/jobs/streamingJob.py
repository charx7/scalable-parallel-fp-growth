########################################################################################
#
#   file: StreamingJob.py
#
#   purpose: Creates a straming job to be submitted to the Spark cluster that receives
#            data, processes it in a given time period, and outputs the top 5
#            products being bought.
#
########################################################################################

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

    # Create a window DStream (Window Length s, Batch Interval s)
    windowed_data = parsed_Data.window(600, 10)

    # Counts the number of transactions received in the batch.
    parsed_Data.count().map(lambda x: 'Transactions in this batch: %s' % x).pprint()

    # Creates a list of the product codes
    product_Codes = windowed_data.flatMap(lambda x: x["ProductCode"])

    # Counts the ocurrences of product codes
    product_Count = product_Codes.countByValue()

    # Sorts the codes by
    sorted_product_Counts = product_Count.transform(
        (lambda foo: foo.sortBy(lambda x: -x[1])))

    # Takes only the top 5 products from the count
    top_five_products = sorted_product_Counts.transform(
        lambda rdd: sc.parallelize(rdd.take(5)))

    top_five_products.pprint()

    ssc.start()
    ssc.awaitTermination()


if __name__ == '__main__':
    main()
