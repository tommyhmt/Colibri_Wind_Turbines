from pyspark.sql.functions import current_timestamp, col
from pyspark.sql import DataFrame, SparkSession
spark = SparkSession.builder.getOrCreate()

def read_csv(path) -> DataFrame:

    df = (
                spark.readStream.format("cloudFiles")
                .option("cloudFiles.format", "csv")
                .option("delimiter", ",")
                .option("inferSchema", False)
                .load(f"/mnt/{path}/")
                .withColumn("input_file_name", col("_metadata.file_path"))
                .withColumn("import_timestamp", current_timestamp())
                )

    return df
