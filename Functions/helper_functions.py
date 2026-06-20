# import libraries
from pyspark.sql.functions import when, col, coalesce, raise_error, lit
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType

def apply_schema(df: DataFrame, schema: StructType, fillnull: bool = False) -> DataFrame:

    schema_columns = [(when(col(x.name).isNotNull(), coalesce(col(x.name).cast(x.dataType), raise_error(f"Cannot cast column '{x.name}' to '{x.dataType}'"))).otherwise(col(x.name).cast(x.dataType))).alias(x.name) if x.name.upper() in (c.upper() for c in df.columns) else lit(None).cast(x.dataType).alias(x.name) for x in schema.fields]

    df = df.select(*schema_columns)

    # Fill Nulls
    if fillnull == True:
        df = df.na.fill("UNDEF",[x[0] for x in df.dtypes if x[1] == "string"])
        df = df.na.fill(0,[x[0] for x in df.dtypes if ("decimal" in x[1]) or (x[1] in ("double", "float", "int", "bigint", "smallint"))])

    return df
