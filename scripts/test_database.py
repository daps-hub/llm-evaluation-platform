from sqlalchemy import text

from app.database.connection import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user")
        )

        database_name, database_user = result.one()

        print(f"Database: {database_name}")
        print(f"User: {database_user}")
        print("PostgreSQL connection successful.")


if __name__ == "__main__":
    main()