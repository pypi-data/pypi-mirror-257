# decorator to attach a function to an attribute
from functools import wraps

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import lit


def add_attr(cls):
    def decorator(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            f = func(*args, **kwargs)
            return f

        setattr(cls, func.__name__, _wrapper)
        return func

    return decorator

# custom functions
def custom(self):
    @add_attr(custom)
    def add_column3():
        return self.withColumn("col3", lit(3))

    @add_attr(custom)
    def add_column4():
        return self.withColumn("col4", lit(4))

    return custom

# add new property to the Class pyspark.sql.DataFrame
DataFrame.custom = property(custom)


schema = 'COST_CENTER_ID string, COST_CENTER_PARENT_ID string, NAME string'
cost_centers = \
    [[1, None, 'Ontario'],
     [11, 1, 'Ontario11'],
     [2, None, 'Quebec2']
     ]
spark = SparkSession.builder.getOrCreate()
df = spark.createDataFrame(cost_centers, schema=schema)

df.withColumn()
# use it
df.custom.add_column3().show()