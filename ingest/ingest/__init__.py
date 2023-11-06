import psycopg2
import asyncio

# dbname should be the same for the notifying process
conn = psycopg2.connect(
    host="localhost", dbname="example", user="example", password="example"
)

cursor = conn.cursor()
cursor.execute("LISTEN match_updates;")
conn.commit()


def handle_notify():
    conn.poll()
    for notify in conn.notifies:
        print(notify.payload)
    conn.notifies.clear()


loop = asyncio.get_event_loop()
loop.add_reader(conn, handle_notify)
loop.run_forever()
