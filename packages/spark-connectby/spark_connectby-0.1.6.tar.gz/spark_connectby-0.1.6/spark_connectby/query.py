from pyspark.sql import DataFrame

from spark_connectby.connectby_query import ConnectByQuery


def connectby(df: DataFrame, prior: str, to: str,
              start_with: [] = None, level_col: str = 'level') -> DataFrame:
    query = ConnectByQuery(df, prior, to, start_with, level_col)

    return query.get_result_df()

DataFrame.connectby = connectby