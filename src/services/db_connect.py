import psycopg2
from decouple import config

try:
    conn_string = f"host={config('DB_HOST')} port={config('DB_PORT')} dbname={config('DB_NAME')} user={config('DB_USER')} password={config('DB_PASSWORD')}"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
except Exception as e:
    print("Error: ", e)
    conn = None
    cursor = None
