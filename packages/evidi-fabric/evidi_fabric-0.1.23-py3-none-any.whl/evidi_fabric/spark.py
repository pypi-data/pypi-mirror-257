import logging
from pyspark.conf import SparkConf
from pyspark.sql.session import SparkSession

from evidi_fabric.config import settings

logging.getLogger(__name__)


def get_or_create_spark() -> SparkSession:
    """Gets a spark session and returns it unless it already exists.

    This function is used to start a spark session and return it. It is used
    to avoid creating multiple spark sessions. In Databricks, this function
    simply returns the existing spark session.

    Returns:
        SparkSession: Spark session
    """
    logging.info("Getting or creating spark session")

    conf = SparkConf()
    try:
        conf.set("spark.jars.packages", ",".join(settings.packages))
    except AttributeError:
        pass

    try:
        conf.set("spark.driver.memory", settings.spark.driver.memory)
    except AttributeError:
        conf.set("spark.driver.memory", "8g")
    conf.set("spark.driver.maxResultSize", "4g")
    conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    conf.set("spark.sql.debug.maxToStringFields", "1000")  # to avoid warning
    conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    
    try:
        conf.set('spark.sql.session.timeZone', settings.spark.sql.session.timeZone)
    except:
        conf.set('spark.sql.session.timeZone', 'UTC')

    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    return spark


if __name__ == "__main__":
    spark = get_or_create_spark()
    print('Done')
