import mysql.connector

# Establish the connection
conn = mysql.connector.connect(
    host='localhost',
    user='yourusername',
    password='yourpassword',
    database='yourdatabase'
)

# Create a cursor object
cursor = conn.cursor()

# Create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL
)
'''
cursor.execute(create_table_query)

# Insert data
insert_data_query = '''
INSERT INTO users (name, age)
VALUES (%s, %s)
'''
user_data = ('Alice', 30)
cursor.execute(insert_data_query, user_data)
conn.commit()

# Query data
query_data = 'SELECT * FROM users'
cursor.execute(query_data)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Update data
update_data_query = '''
UPDATE users
SET age = %s
WHERE name = %s
'''
new_age = 31
username = 'Alice'
cursor.execute(update_data_query, (new_age, username))
conn.commit()

# Delete data
delete_data_query = '''
DELETE FROM users
WHERE name = %s
'''
username_to_delete = 'Alice'
cursor.execute(delete_data_query, (username_to_delete,))
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

