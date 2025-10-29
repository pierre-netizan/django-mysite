# utils/db.py
from django.conf import settings

def schema_table(table_name: str) -> str:
    """
    返回带 schema 的表名：'"mysite"."posts"'
    """
    return f'"{settings.DB_SCHEMA}"."{table_name}"'





