import os




DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "chatbi_mvp"),
    "charset": "utf8mb4"
}


LLM_CONFIG = {
    "api_key": os.getenv("DASHSCOPE_API_KEY"),
    "model": os.getenv("LLM_MODEL", "qwen3.8-max"),
    "temperature": 0.1,
    "max_tokens": 1000
}