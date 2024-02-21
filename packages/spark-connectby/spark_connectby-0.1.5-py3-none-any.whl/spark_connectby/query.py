from pyspark.sql import DataFrame

from spark_connectby.connectby_query import ConnectByQuery


def connectby(df: DataFrame, child_column: str, parent_column: str,
              start_with: [] = None, level_column: str = 'level') -> DataFrame:
    query = ConnectByQuery(df, child_column, parent_column, start_with, level_column)

    return query.get_result_df()