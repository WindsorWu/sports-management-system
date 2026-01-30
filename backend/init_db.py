"""
数据库初始化脚本
自动创建sports数据库
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """初始化数据库"""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root'),
            port=int(os.getenv('DB_PORT', '3306')),
            charset='utf8mb4'
        )

        with connection.cursor() as cursor:
            # 创建数据库
            db_name = os.getenv('DB_NAME', 'sports')
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"[SUCCESS] Database '{db_name}' created successfully!")

        connection.close()
        print("[SUCCESS] Database initialization completed!")

    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}")
        raise

if __name__ == '__main__':
    init_database()
