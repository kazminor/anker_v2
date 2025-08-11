# database/postgres_connector.py
import psycopg2
from psycopg2 import Error

class PostgresConnector:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self, host, port, dbname, user, password):
        try:
            self.connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS mining_dataset (
                    id SERIAL PRIMARY KEY,
                    depth FLOAT,
                    rock_strength FLOAT,
                    humidity FLOAT,
                    fracture FLOAT,
                    width FLOAT,
                    location TEXT,
                    roof_type TEXT,
                    displacement FLOAT,
                    support_type TEXT,
                    anchor_step FLOAT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def add_dataset(self, data):
        try:
            for param_name, value in data.items():
                if param_name not in [
                    'depth', 'rock_strength', 'humidity', 'fracture', 'width',
                    'location', 'roof_type', 'displacement', 'support_type', 'anchor_step'
                ]:
                    self.cursor.execute("""
                        SELECT column_name 
                        FROM information_schema.columns 
                        WHERE table_name = 'mining_dataset' AND column_name = %s
                    """, (param_name,))
                    if not self.cursor.fetchone():
                        column_type = 'FLOAT' if isinstance(value, (int, float)) else 'TEXT'
                        self.cursor.execute(f"""
                            ALTER TABLE mining_dataset
                            ADD COLUMN {param_name} {column_type}
                        """)
                        self.connection.commit()

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO mining_dataset ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, list(data.values()))
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error adding data to dataset: {e}")
            self.connection.rollback()
            return False

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()