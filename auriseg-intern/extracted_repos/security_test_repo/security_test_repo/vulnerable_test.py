import os
import sqlite3

DB_PASSWORD = "admin123"

def login(username):
query = (
"SELECT * FROM users "
f"WHERE username = '{username}'"
)

```
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute(query)

return cursor.fetchall()
```

def run_ping(host):
os.system("ping " + host)

