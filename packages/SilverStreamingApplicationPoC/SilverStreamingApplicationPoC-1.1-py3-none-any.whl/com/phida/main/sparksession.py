#from pyspark.sql import SparkSession

#from com.phida.main import logging

#spark = (SparkSession.builder
#         .getOrCreate())

#logger = logging.Log4j(spark)

###############Above lines are commented and Below lines are added by Shilton#########
import pyspark
from pyspark.sql import SparkSession
from com.phida.main import logging
spark = SparkSession.builder \
    .appName("SilverMerge4") \
    .config('spark.jars.packages', 'org.apache.hadoop:hadoop-azure:3.3.1') \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("fs.azure.account.auth.type.eabase.dfs.core.windows.net", "SharedKey") \
    .config("fs.azure.account.key.eabase.dfs.core.windows.net", 
            "0/lxarMjHfeZHZPwMhvv6YHv3U/NsYvqQSAW79Kt6y8dIk9v8yvPHG/emRaVdmm+CEXPRrRr1Ra6+AStxbObeQ==") \
    .getOrCreate()
logger = logging.Log4j(spark)