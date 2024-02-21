#from pyspark.sql import SparkSession

#from com.phida.main import logging

#spark = (SparkSession.builder
#         .getOrCreate())

#logger = logging.Log4j(spark)

###############Above lines are commented and Below lines are added by Shilton#########
import pyspark
import base64
from pyspark.sql import SparkSession
from com.phida.main import logging

with open("/mnt/secrets/azure-secret.txt", "rb") as file:
    storage_account_key = file.read().strip()

decoded_key = base64.b64decode(storage_account_key).decode("utf-8")

spark = SparkSession.builder \
    .appName("SilverMerge4") \
    .config('spark.jars.packages', 'org.apache.hadoop:hadoop-azure:3.3.1') \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("fs.azure.account.auth.type.eabase.dfs.core.windows.net", "SharedKey") \
    .config("fs.azure.account.key.eabase.dfs.core.windows.net", decoded_key) \
    .getOrCreate()

logger = logging.Log4j(spark)