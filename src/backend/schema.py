from typing import TYPE_CHECKING, Protocol

import strawberry
from strawberry.types import Info

from backend.service import get_books

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
        books = await get_books(db=info.context.db, author_ids=author_ids, search=search, limit=limit)
        return [
            Book(title=book['title'], author=Author(name=book['author']['name']))
            for book in books
        ]


schema = strawberry.Schema(query=Query)
