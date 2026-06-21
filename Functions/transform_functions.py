# import libraries
from pyspark.sql.functions import col, lit, current_timestamp, to_date, left, avg, stddev, when, coalesce, raise_error
from pyspark.sql.types import StructType
from pyspark.sql import DataFrame

def create_missing_records(df: DataFrame) -> DataFrame:

    timestamp = df.select("timestamp").distinct()
    turbine = df.select("turbine_id").distinct()
    cross_df = timestamp.crossJoin(turbine)

    missing_df = (
                cross_df.alias("c")
                        .join(df.alias("b"), ["timestamp", "turbine_id"], "left_anti")
                        .select(*[col(f"c.{x}") if x in cross_df.columns else (lit(current_timestamp()).alias(x) if x == "import_timestamp" else lit(None).cast(df.schema[x].dataType).alias(x)) for x in df.columns])
                )

    final_df = (
                df.union(missing_df)
                        .withColumn("date", to_date(left("timestamp", lit(10)), "yyyy-MM-dd"))
                        .withColumn("timestamp", col("timestamp").cast("timestamp"))
                )

    return final_df

def add_anomaly(df: DataFrame) -> DataFrame:

    summary_df = (
                df
                .groupBy("date", "turbine_id")
                .agg(avg("power_output").alias("avg_power_output"),
                    stddev("power_output").alias("stddev_power_output"))
                )

    # Joins anomaly_df to gold_df
    final_df = (
                df.alias("i")
                    .join(summary_df.alias("u"), ["date", "turbine_id"])
                    .select("i.*", "u.avg_power_output", "u.stddev_power_output")
            )

    # Identifies anomaly
    final_df = final_df.withColumn("anomaly", (col("power_output") < col("avg_power_output") - col("stddev_power_output") * lit(2)) | (col("power_output") > col("avg_power_output") + col("stddev_power_output") * lit(2)))

    return final_df

def apply_schema(df: DataFrame, schema: StructType) -> DataFrame:

    schema_columns = [
        (
        coalesce(col(x.name), lit(f"{x.metadata['default']}"))
        if "default" in x.metadata
            else col(x.name)
        ).cast(x.dataType).alias(x.name)
        if x.name.upper() in (c.upper() for c in df.columns)
            else lit(None).cast(x.dataType).alias(x.name)
        for x in schema.fields
    ]

    df = df.select(*schema_columns)

    return df
