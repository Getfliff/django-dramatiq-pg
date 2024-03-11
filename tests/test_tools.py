import pytest

from django_dramatiq_pg.tools import make_url


@pytest.mark.parametrize(
    "config, expected_url",
    [
        ({}, "postgresql://"),
        (
            {
                "USER": "user",
                "PASSWORD": "password",
                "HOST": "localhost",
                "PORT": "5432",
                "OPTIONS": {"connect_timeout": 10},
                "NAME": "name",
            },
            "postgresql://user:password@localhost:5432/name?connect_timeout=10",
        ),
        (
            {"USER": "user", "HOST": "localhost", "NAME": "name"},
            "postgresql://user@localhost/name",
        ),
        (
            {"PASSWORD": "password", "HOST": "localhost", "NAME": "name"},
            "postgresql://:password@localhost/name",
        ),
        (
            {"USER": "user", "PORT": "5431", "NAME": "name"},
            "postgresql://user@:5431/name",
        ),
        (
            {
                "USER": "username",
                "PASSWORD": "password",
                "HOST": "localhost",
                "PORT": "5432",
                "NAME": "database",
            },
            "postgresql://username:password@localhost:5432/database",
        ),
        (
            {"HOST": "localhost", "PORT": "5432", "NAME": "database"},
            "postgresql://localhost:5432/database",
        ),
        (
            {
                "USER": "username",
                "PASSWORD": "password",
                "HOST": "localhost",
                "NAME": "database",
            },
            "postgresql://username:password@localhost/database",
        ),
        (
            {
                "USER": "username",
                "PASSWORD": "password",
                "PORT": "5432",
                "NAME": "database",
            },
            "postgresql://username:password@:5432/database",
        ),
        (
            {
                "USER": "username",
                "PASSWORD": "password#@|()",
                "HOST": "localhost",
                "PORT": "5432",
                "NAME": "database",
                "OPTIONS": {"sslmode": "prefer", "timezone": "UTC"},
            },
            "postgresql://username:password%23%40%7C%28%29@localhost:5432/database?sslmode=prefer&timezone=UTC",
        ),
    ],
)
def test_make_url(config, expected_url):
    assert make_url(**config) == expected_url
