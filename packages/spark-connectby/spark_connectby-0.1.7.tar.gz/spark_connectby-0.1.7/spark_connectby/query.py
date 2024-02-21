from typing import Union, List

from pyspark.sql import DataFrame

from spark_connectby.connectby_query import ConnectByQuery, Node


def connectby(df: DataFrame, prior: str, to: str,
              start_with: Union[List[str], str] = None, level_col: str = 'level') -> DataFrame:
    if start_with is None:
        top_nodes = None
    elif isinstance(start_with, list):
        top_nodes = [Node.for_root(i) for i in start_with]
    else:
        top_nodes = [Node.for_root(start_with)]

    query = ConnectByQuery(df=df, child_column=prior, parent_column=to, start_with=top_nodes, level_column=level_col)

    return query.get_result_df()

DataFrame.connectby = connectby