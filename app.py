import mysql.connector
from flask import Flask, request, render_template
app = Flask(__name__)

# MySQL database configuration
user = 'root'
password = 'nilesh'
host = 'localhost'
database = 'chatbot'
table_name = 'messages'
# Connect to the MySQL server
conn = mysql.connector.connect(user=user, password=password, host=host)

# Create the database
cur = conn.cursor()
try:
 cur.execute(f"CREATE DATABASE {database}")
except:
 pass

# Connect to the new database
#conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
#table_name = 'messages'
print("Connected to database '{}'".format(database))
# Check if the table already exists
cur.execute("USE {}".format(database))
cur.execute("SHOW TABLES LIKE '{}'".format(table_name))
result = cur.fetchone()

if result:
    print("Table '{}' already exists".format(table_name))
else:
    # Create the table
    cur.execute("""CREATE TABLE messages (
                   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                   message VARCHAR(255),
                   response VARCHAR(255)
                )""")
    print("Table '{}' created successfully".format(table_name))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the message from the form
        message = request.form['message']
        response_text = 'I don\'t know what to say'

        # Save the message and response to the database
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (message, response) VALUES (%s, %s)", (message, response_text))
        conn.commit()
        cur.close()

    # Get all messages and responses from the database
    cur = conn.cursor()
    cur.execute("SELECT message, response FROM messages")
    messages = cur.fetchall()
    cur.close()

    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
