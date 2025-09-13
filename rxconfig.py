import os
import reflex as rx
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
DB_CONFIG = os.getenv("DB_CONFIG")

config = rx.Config(
    app_name="dashboard_tutorial",
    db_url=DB_CONFIG,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
#engine = create_engine("mariadb+pymysql://user:pass@some_mariadb/dbname?charset=utf8mb4")