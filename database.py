import pymysql
from typing import Tuple, List
from config import DB_CONFIG


class DatabaseClient:
    """MySQL 数据库客户端"""

    def __init__(self):
        self.config = DB_CONFIG

    def execute(self, sql: str) -> Tuple[List[str], list[tuple]]:
        """执行 SQL 并返回结果"""
        conn = pymysql.connect(**self.config)

        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                columns = [desc[0] for desc in cursor.description] if cursor.description else []
                results = cursor.fetchall()

                return columns, results
        finally:
            conn.close()

    def validate_connection(self) -> bool:
        """验证数据库连接是否正常"""
        try:
            conn = pymysql.connect(**self.config)
            conn.close()
            return True
        except Exception:
            return False