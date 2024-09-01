from typing import TYPE_CHECKING, Protocol

import strawberry
from strawberry.types import Info

if TYPE_CHECKING:
    from databases import Database


class _Context(Protocol):
    db: 'Database'

    def __init__(self, db: 'Database') -> None:
        pass


@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    title: str
    author: Author


@strawberry.type
class Query:
    @strawberry.field
    async def books(
        self,
        info: Info[_Context, None],
        author_ids: list[int] | None = [],
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        # TODO:
        # Do NOT use dataloaders
        await info.context.db.execute("select 1")
        return []


schema = strawberry.Schema(query=Query)
