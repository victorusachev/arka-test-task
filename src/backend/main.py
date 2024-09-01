from contextlib import asynccontextmanager
from functools import partial
from typing import AsyncGenerator

from databases import Database
from fastapi import FastAPI
from strawberry.fastapi import BaseContext, GraphQLRouter

from backend.schema import schema
from backend.settings import Settings


class Context(BaseContext):
    db: 'Database'

    def __init__(self, db: 'Database') -> None:
        super().__init__()
        self.db = db


@asynccontextmanager
async def lifespan(app: FastAPI, db: Database) -> AsyncGenerator:
    async with db:
        yield
    await db.disconnect()


def make_db_url(settings: Settings) -> str:
    url_template = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    return url_template.format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        port=settings.DB_PORT,
        host=settings.DB_SERVER,
        name=settings.DB_NAME,
    )


def create_app() -> FastAPI:
    settings = Settings()  # type: ignore[call-arg]
    db_url = make_db_url(settings)
    db = Database(db_url)

    app = FastAPI(lifespan=partial(lifespan, db=db))

    graphql_app = GraphQLRouter(
        schema,
        context_getter=partial(Context, db),  # type: ignore[var-annotated]
    )

    app.include_router(graphql_app, prefix="/graphql")
    return app
