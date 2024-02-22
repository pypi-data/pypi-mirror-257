from dataclasses import dataclass

from pyspark.sql import DataFrame

ROOT_LEVEL = 1
LEVEL_COLUMN = 'LEVEL'


@dataclass
class Node:
    nid: str
    level: int

    @classmethod
    def for_root(cls, nid: str) -> 'Node':
        return cls(nid, level=ROOT_LEVEL)


class ConnectByQuery:
    def __init__(self, df: DataFrame, child_column: str, parent_column: str,
                 start_with: [Node] = None, level_column: str = LEVEL_COLUMN):
        self.df: DataFrame = df
        self.child_column = child_column
        self.parent_column = parent_column
        self.root_list: [Node] = start_with or self._default_roots()
        self.level_colum = level_column

        self._all_data: [(str, str)] = None

    @property
    def all_data(self) -> [(str, str)]:
        if self._all_data is None:
            rows = self.df.select(self.child_column, self.parent_column).collect()
            self._all_data = [(r[self.child_column], r[self.parent_column]) for r in rows]
        return self._all_data

    def children_with_parent(self, parent_id: str) -> []:
        result = list(filter(lambda d: d[1] == parent_id, self.all_data))
        return result

    def _default_roots(self) -> [Node]:
        roots = (
            self.df
            # .filter(psf.col(self.parent_column).isNull())
            .collect()
        )
        result = [Node.for_root(r[self.child_column]) for r in roots]
        assert len(result) > 0
        return result

    def get_descendants_recursive(self, node: Node) -> []:
        level = node.level + 1
        result_list = []

        direct_list = [Node(nid=c[0], level=level) for c in self.children_with_parent(node.nid)]
        indirect_list = list(map(lambda e: self.get_descendants_recursive(e), direct_list))
        descendant_list = direct_list + indirect_list

        result_list.append(descendant_list)
        return result_list

    @staticmethod
    def _flatten(nested_list):
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list += ConnectByQuery._flatten(item)
            else:
                flat_list.append(item)
        return flat_list

    def run(self) -> [Node]:
        descendants_list = list(map(lambda e: self.get_descendants_recursive(e), self.root_list))
        descendants_list_flatten = ConnectByQuery._flatten(descendants_list)

        return self.root_list + descendants_list_flatten

    def get_result_df(self) -> DataFrame:
        result_list = self.run()

        schema = f'{self.child_column} string, {self.level_colum} int'
        spark = self.df._session
        result_df = spark.createDataFrame([(r.nid, r.level) for r in result_list], schema=schema)

        result_df = result_df.join(self.df, on=self.child_column)
        return result_df
