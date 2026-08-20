from app.database.connection import get_connection


def main():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()

                print("✅ Database connection successful!")
                print(f"PostgreSQL: {version[0]}")

    except Exception as e:
        print("❌ Database connection failed!")
        print(e)


if __name__ == "__main__":
    main()