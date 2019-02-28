"""Reusable sqlite-backed Node container(s)."""
from ..exceptions import NodeNotFound


class ReadOnlyNode:
    def __init__(self, _sqlitegraph=None, *args, **kwargs):
        self.sqlitegraph = _sqlitegraph

    def __getitem__(self, key):
        return self.sqlitegraph.get_node(key)

    def __contains__(self, key):
        try:
            self[key]
        except NodeNotFound:
            return False
        return True

    def __iter__(self):
        query = self.sqlitegraph.conn.execute("SELECT _key FROM nodes")
        return (row[0] for row in query)

    def __len__(self):
        query = self.sqlitegraph.conn.execute("SELECT count(*) FROM nodes")
        return query.fetchone()[0]


# TODO: use Mapping (mutable?) abstract base class for dict-like magic
class Node(ReadOnlyNode):
    def clear(self):
        # FIXME: make this do something
        pass

    def __setitem__(self, key, ddict):
        if key in self:
            self.sqlitegraph.update_node(key, ddict)
        else:
            self.sqlitegraph.add_node(key, ddict)


def node_factory_factory(sqlitegraph, readonly=False):
    """Creates factories of DB-based Nodes.

    :param sqlitegraph: Graph database object.
    :type sqlitegraph: entwiner.GraphDB

    """

    def node_factory():
        return Node(_sqlitegraph=sqlitegraph)

    def readonly_node_factory():
        return ReadOnlyNode(_sqlitegraph=sqlitegraph)

    if readonly:
        return readonly_node_factory
    else:
        return node_factory
