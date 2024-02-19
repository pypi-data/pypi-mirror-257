import pytest
from query import connectby
from pyspark.sql import SparkSession

CHILD_COLUMN = 'COST_CENTER_ID'
PARENT_COLUMN = 'COST_CENTER_PARENT_ID'


@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.getOrCreate()


def test_query(spark):
    schema = 'COST_CENTER_ID string, COST_CENTER_PARENT_ID string, NAME string'
    cost_centers = \
        [[1, None, 'Ontario'],
         [11, 1, 'Ontario11'],
         [2, None, 'Quebec2']
         ]
    df = spark.createDataFrame(cost_centers, schema=schema)

    df2 = df.transform(connectby, child_column=CHILD_COLUMN, parent_column=PARENT_COLUMN)
    df2.show()

    assert df2.count() == 4
