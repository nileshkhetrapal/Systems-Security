from flask import Flask, render_template, request
import mysql.connector

db = mysql.connector.connect(
  host="10.0.6.10",
  port="3356",
  user="chat_app",
  password="chat_app",
  database="chat_app"
)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

import transformers



@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    pipe = transformers.pipeline('text-generation', model='gpt2')
    bot_output = pipe(user_input, max_length=60, num_return_sequences=1)[0]['generated_text']
    cursor = db.cursor()
    #This code creates an SQL query to insert the `user_input` and `bot_output` values into a table called `chat_history` in the `chat_app` database, and then executes the query using the `cursor.execute()` method. Finally, it commits the changes to the database using the `db.commit()` method.
    sql = "INSERT INTO chat_history (user_input, bot_output) VALUES (%s, %s)"
    values = (user_input, bot_output)
    cursor.execute(sql, values)
    db.commit()
    return bot_output

@app.route('/history')
def history():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chat_history")
    results = cursor.fetchall()
    return render_template('history.html', results=results)
