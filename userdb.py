import sqlite3

# Connect to db
conn = sqlite3.connect('users.db')
# Create cursor
c = conn.cursor()
# Create user table
c.execute('''CREATE TABLE users (hash text, name text, gender text)''')
# Commit changes
conn.commit()
# Close connection
conn.close()