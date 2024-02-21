from datetime import datetime, date

from pyspark.sql import SparkSession


def print_hi(name):
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    spark = SparkSession.builder.getOrCreate()

    df = spark.createDataFrame([
        (1, 2., 'string1', date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
        (2, 3., 'string2', date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
        (3, 4., 'string3', date(2000, 3, 1), datetime(2000, 1, 3, 12, 0))
    ], schema='a long, b double, c string, d date, e timestamp')


    df.show(truncate=False)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
