from typing import Any, Awaitable, Callable, Dict, List, Union

import python_query.utils as utils
from python_query.query import Query
from python_query.query_options import QueryOptions
from python_query.types import TData, TQueryKey, TQueryOptions


class QueryCache:
    def __init__(
            self,
            default_options: TQueryOptions = QueryOptions()) -> None:
        self.__queries: Dict[str, Query[Any]] = {}
        self.__default_options = default_options

    def __getitem__(self, key: TQueryKey) -> Query[Any]:
        return self.get_query(key)

    def __setitem__(self,
                    key: TQueryKey,
                    value: Callable[[],
                                    Union[Awaitable[TData],
                                          TData]]) -> None:
        self.add_query(key, value)

    def add_query(self,
                  key: TQueryKey,
                  fn: Callable[[],
                               Union[Awaitable[TData],
                                     TData]]) -> None:
        query: Query[TData] = Query(key, fn, self.__default_options)
        self.__queries[query.get_hash()] = query

    def get_query(self, key: TQueryKey) -> Query[object]:
        return self.__queries[utils.hash_query_key(key)]

    def get_queries_not_exact(self, key: TQueryKey) -> List[Any]:
        return [
            query for query in self.__queries.values() if query.matches_key(
                key, False)]

    async def get_query_data_async(self, key: TQueryKey) -> Any:
        return await self[key].fetch_async()
