"""Custom data types used in the plugin"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DBConnectionSettings:
    """FAA DOF database connection details"""
    host: str
    database: str
    user: str
    password: str
