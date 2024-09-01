from contextlib import asynccontextmanager
from functools import partial
from typing import AsyncGenerator

import strawberry
from databases import Database
from fastapi import FastAPI
from strawberry.types import Info
from strawberry.fastapi import BaseContext, GraphQLRouter

from settings import Settings


CONN_TEMPLATE = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


class Context(BaseContext):
    db: 'Database'

    def __init__(self, db: 'Database') -> None:
        super().__init__()
        self.db = db


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
        info: Info[Context, None],
        author_ids: list[int] | None = [],
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        # TODO:
        # Do NOT use dataloaders
        await info.context.db.execute("select 1")
        return []


schema = strawberry.Schema(query=Query)


@asynccontextmanager
async def lifespan(app: FastAPI, db: Database) -> AsyncGenerator:
    async with db:
        yield
    await db.disconnect()


def create_app() -> FastAPI:
    settings = Settings()  # type: ignore[call-arg]
    db_url = CONN_TEMPLATE.format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        host=settings.DB_SERVER,
        name=settings.DB_NAME,
    )
    db = Database(db_url)

    app = FastAPI(lifespan=partial(lifespan, db=db))

    graphql_app = GraphQLRouter(
        schema,
        context_getter=partial(Context, db),  # type: ignore[var-annotated]
    )

    app.include_router(graphql_app, prefix="/graphql")
    return app
