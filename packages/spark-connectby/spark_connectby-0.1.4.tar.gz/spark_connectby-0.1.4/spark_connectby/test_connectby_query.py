import timeit

import pytest
from pyspark.sql import SparkSession

from connectby_query import Node, ConnectByQuery, LEVEL_COLUMN

CHILD_COLUMN = 'COST_CENTER_ID'
PARENT_COLUMN = 'COST_CENTER_PARENT_ID'


@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.getOrCreate()


@pytest.fixture(scope="module")
def df_big(spark):
    schema = f'{CHILD_COLUMN} string, {PARENT_COLUMN} string, NAME string'
    cost_centers = \
        [[1, None, 'Ontario'],
         [2, None, 'Quebec'],
         [11, 1, 'Ontario11'],
         [12, 1, 'Ontario12'],
         [111, 11, 'Ontario111'],
         [112, 11, 'Ontario112'],
         [121, 12, 'Ontario121'],
         [21, 2, 'Quebec21']
         ]
    cost_centers_df = spark.createDataFrame(cost_centers, schema=schema)
    return cost_centers_df


@pytest.fixture(scope="module")
def df_small(spark):
    schema = f'{CHILD_COLUMN} string, {PARENT_COLUMN} string, NAME string'
    cost_centers = \
        [[1, None, 'Ontario'],
         [11, 1, 'Ontario11'],
         [12, 1, 'Ontario12'],
         [111, 11, 'Ontario111']
         ]
    return spark.createDataFrame(cost_centers, schema=schema)


@pytest.fixture(scope="module")
def df_tiny(spark):
    schema = 'COST_CENTER_ID string, COST_CENTER_PARENT_ID string, NAME string'
    cost_centers = \
        [[1, None, 'Ontario'],
         [11, 1, 'Ontario11'],
         [2, None, 'Quebec2']
         ]
    return spark.createDataFrame(cost_centers, schema=schema)


def test_2_roots(df_big):
    root_list = [Node.for_root('1'), Node.for_root('2')]
    query = ConnectByQuery(df_big, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert result_df.count() == 8


def test_start_with_middle_node(df_big):
    a_node = [Node.for_root('11')]
    query = ConnectByQuery(df_big, CHILD_COLUMN, PARENT_COLUMN, start_with=a_node)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert result_df.count() == 3


def test_simple(df_small):
    root_list = [Node.for_root('1')]
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert result_df.count() == 4
    assert LEVEL_COLUMN in result_df.columns


def test_simple_all_data(df_small):
    root_list = [Node.for_root('1')]
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    all_data = query.all_data
    print(all_data)

    assert len(all_data) == 4


def test_simple_children_filter(df_small):
    root_list = [Node.for_root('1')]
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    children = query.children_with_parent('1')
    print(children)

    assert len(children) == 2


def test_default_root(df_tiny):
    query = ConnectByQuery(df_tiny, CHILD_COLUMN, PARENT_COLUMN)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert result_df.count() == 4


def test_level_column(df_small):
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert LEVEL_COLUMN in result_df.columns


def test_level_column_new(df_small):
    new_level_column = 'COST_CENTER_LEVEL'
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, level_column=new_level_column)

    result_df = query.get_result_df()
    print()
    result_df.show(truncate=False)

    assert new_level_column in result_df.columns


def test_input_extra_root(df_small):
    root_list = [Node.for_root('1'), Node.for_root('2')]
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    result_df = query.get_result_df()

    print()
    result_df.show(truncate=False)

    assert result_df.count() == 4


def test_leaf(df_small):
    start_time = timeit.default_timer()

    root_list = [Node.for_root('111')]
    query = ConnectByQuery(df_small, CHILD_COLUMN, PARENT_COLUMN, start_with=root_list)

    result_df = query.get_result_df()

    print()
    result_df.show(truncate=False)

    print(f'spent in seconds): {timeit.default_timer() - start_time}')
    assert result_df.count() == 1


def test():
    pass
