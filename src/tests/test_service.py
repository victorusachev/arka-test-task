from backend.service import construct_query_with_params


def test_construct_query_with_params_no_params():
    expected_query = """
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id

ORDER BY authors.name, books.title
    """
    expected_params = {}

    query, params = construct_query_with_params()

    assert query.strip() == expected_query.strip()
    assert params == expected_params


def test_construct_query_with_params_author_ids():
    author_ids = [1, 2, 3]
    expected_query = """
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id
WHERE authors.id = ANY(:author_ids)
ORDER BY authors.name, books.title
    """
    expected_params = {"author_ids": author_ids}

    query, params = construct_query_with_params(author_ids=author_ids)

    assert query.strip() == expected_query.strip()
    assert params == expected_params


def test_construct_query_with_params_search():
    search = "Some search"
    expected_query = """
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id
WHERE (books.title ILIKE :search OR authors.name ILIKE :search)
ORDER BY authors.name, books.title
    """
    expected_params = {"search": f"%{search}%"}

    query, params = construct_query_with_params(search=search)

    assert query.strip() == expected_query.strip()
    assert params == expected_params


def test_construct_query_with_params_limit():
    limit = 5
    expected_query = """
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id

ORDER BY authors.name, books.title
LIMIT :limit
"""
    expected_params = {"limit": limit}

    query, params = construct_query_with_params(limit=limit)

    assert query.strip() == expected_query.strip()
    assert params == expected_params


def test_construct_query_with_params_all():
    """Тест: вызов функции с заданными параметрами author_ids, search и limit."""
    author_ids = [1, 2]
    search = "Test search"
    limit = 10
    expected_query = """
SELECT authors.name AS author_name, books.title
FROM books
JOIN authors ON books.author_id = authors.id
WHERE authors.id = ANY(:author_ids) AND (books.title ILIKE :search OR authors.name ILIKE :search)
ORDER BY authors.name, books.title
LIMIT :limit
"""
    expected_params = {
        "author_ids": author_ids,
        "search": f"%{search}%",
        "limit": limit
    }

    query, params = construct_query_with_params(author_ids=author_ids, search=search, limit=limit)

    assert query.strip() == expected_query.strip()
    assert params == expected_params
