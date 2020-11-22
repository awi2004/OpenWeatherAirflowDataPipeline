import psycopg2


def make_database():
    # declaring variables
    conn = ''

    try:
        conn = psycopg2.connect(database="postgres", user="postgres", password="test123", host="127.0.0.1", port="5432")
        cursor = conn.cursor()
        print("Connected to database successfully. . .")

        # sql statement to create table
        create_table = """CREATE TABLE IF NOT EXISTS weather_table
                (
                    city         TEXT, 
                    country      TEXT,
                    latitude     REAL,
                    longitude    REAL,
                    todays_date  DATE,
                    humidity     REAL,
                    pressure     REAL,
                    min_temp     REAL,
                    max_temp     REAL,
                    temp         REAL,
                    weather      TEXT
                );
                """
        # executing sql statement
        cursor.execute(create_table)
        conn.commit()
        print("Table created successfully . . .")

        conn.close()
        #cursor.close()
        print("Connection closed . . . ")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to database : ", error)


# executing python code
if __name__ == "__main__":
    make_database()