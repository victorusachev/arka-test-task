from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from databases import Database


async def get_books(
        db: 'Database',
        author_ids: list[int] | None = None,
        search: str | None = None,
        limit: int | None = None,
) -> list[dict]:
    if limit == 0:
        return []

    query, params = construct_query_with_params(author_ids=author_ids, search=search, limit=limit)
    rows = await db.fetch_all(query=query, values=params)

    return [
        {'title': row['title'], 'author': {'name': row['author_name']}}
        for row in rows
    ]


def construct_query_with_params(
        author_ids: list[int] | None = None,
        search: str | None = None,
        limit: int | None = None,
) -> tuple[str, dict[str, str]]:
    params: dict[str, Any] = {}
    where_conditions = []
    if author_ids:
        where_conditions.append("authors.id = ANY(:author_ids)")
        params["author_ids"] = author_ids
    if search:
        where_conditions.append("(books.title ILIKE :search OR authors.name ILIKE :search)")
        params["search"] = f"%{search}%"

    where_clause = ''
    if where_conditions:
        where_clause = 'WHERE ' + (' AND '.join(where_conditions))

    limit_clause = ''
    if limit is not None:
        limit_clause = "LIMIT :limit"
        params["limit"] = limit

    query = f"""
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id
{where_clause}
ORDER BY authors.name, books.title
{limit_clause}
"""

    return query, params
