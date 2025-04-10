"""Database utils to perform CRUD operations"""
from __future__ import annotations

import logging
from typing import Any

import psycopg2
from psycopg2.extras import DictCursor

from .errors import DBConnectionError


class DBUtils:

    """Handle database CRUD operations"""

    def __init__(self,
                 host: str,
                 database: str,
                 user: str,
                 password: str) -> None:
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self._connection = None

    def connect(self) -> None | Exception:
        """Connect to the database"""
        try:
            self._connection = psycopg2.connect(
                host=self._host,
                database=self._database,
                user=self._user,
                password=self._password
            )
            return None
        except Exception as e:
            logging.error("Database connection error: %s", e)
            raise DBConnectionError(e) from e

    def select(self, query: str) -> dict[Any, Any]:
        """Execute select query"""
        if not self._connection:
            self.connect()

        with self._connection as conn:
            cur = conn.cursor(cursor_factory=DictCursor)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()

        return data
