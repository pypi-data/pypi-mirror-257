# spark-connectby
Spark currently does not support hierarchy query `connect by` as of version 3.5.0. 
And there is a [PR](https://github.com/apache/spark/pull/40744) opened to support recursive CTE query. But that is not available yet.  

This is an attempt to add `connectby` method to [DataFrame](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html)

# Concept 
Hierarchy query is one of the important feature that many traditional relational databases, such as Oracle, DB2, My SQL, 
Snowflake, [Redshift](https://docs.aws.amazon.com/redshift/latest/dg/r_CONNECT_BY_clause.html), etc.,
would support directly or alternatively by using recursive CTE. 

Example in Redshift:
```sql
select id, name, manager_id, level
from employee
start with emp_id = 1
connect by prior emp_id = manager_id;
```

With this library, we can use `connectby()` on `Dateframe`:
```python
from spark_connectby.query import connectby
from pyspark.sql import SparkSession

schema = 'emp_id string, manager_id string, name string'
data = [[1, None, 'Carlos'],
        [11, 1, 'John'],
        [111, 11, 'Jorge'],
        [112, 11, 'Kwaku'],
        [113, 11, 'Liu']
        ]
df = spark.createDataFrame(data, schema)
df2 = df.connectby(prior='emp_id', to='manager_id', start_with='1')
df2.show()
```
With result:
```
+------+-----+----------+------+
|emp_id|level|manager_id|  name|
+------+-----+----------+------+
|     1|    1|      null|Carlos|
|    11|    2|         1|  John|
|   111|    3|        11| Jorge|
|   112|    3|        11| Kwaku|
|   113|    3|        11|   Liu|
+------+-----+----------+------+
```

# Installation
Python Version >= 3.7 
```
$ pip install --upgrade spark-connectby
```

# Usage
```python
from spark_connectby.query import connectby

df = ...

df2 = df.connectby(prior='emp_id', to='manager_id', start_with='1')   # start_with `emp_id` as 1

df2 = df.transform(connectby, prior='emp_id', to='manager_id', start_with='1')   # or by using df.transform() method

df2 = df.connectby(prior='emp_id', to='manager_id')   # without start_with, it will go through each node

df2 = df.connectby(prior='emp_id', to='manager_id', level_col='the_level')  # level column name other than `level`

df2 = df.connectby(prior='emp_id', to='manager_id', start_with=['1', '2'])  # start_with a list of top nodes ids. 

```


