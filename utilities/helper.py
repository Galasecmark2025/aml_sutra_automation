import mysql.connector


server = "160.30.125.196,10222"
username = "ComtekAdmin"
password = "ComTek@dm!n123"

host, port = server.split(",")

try:
    print("Trying to connect...")
    print(repr(username))
    print(repr(password))

    conn = mysql.connector.connect(
        host=host.strip(),
        port=int(port.strip()),
        user=username.strip(),
        password=password.strip(),
        connection_timeout=15,

        # optional SSL handling
        ssl_disabled=True
    )

    print("Connected!")

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    print(cursor.fetchone()[0])

except Exception as e:
    print("Full error:")
    print(repr(e))