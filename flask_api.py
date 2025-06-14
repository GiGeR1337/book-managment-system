import pandas as pd
from flask import Flask, request, jsonify

from logger_config import *
from data_persistence import load_data, save_data

logger = logging.getLogger(__name__)
app = Flask(__name__)
data = load_data()


@app.route('/books', methods=['GET'])
def get_all_books():
    logger.info("GET /books")
    return data.to_json(orient='records')


@app.route('/books/author/<author_name>', methods=['GET'])
def get_books_by_author(author_name):
    logger.info("GET /books/author/%s", author_name)
    result = data[data['author'].str.contains(author_name, case=False, na=False)]
    return result.to_json(orient='records')


@app.route('/books/title_contains/<word>', methods=['GET'])
def get_books_by_title_word(word):
    logger.info("GET /books/title_contains/%s", word)
    result = data[data['title'].str.contains(word, case=False, na=False)]
    return result.to_json(orient='records')


@app.route('/books', methods=['POST'])
def add_book():
    global data
    book = request.get_json()
    logger.info("POST /books: adding %s", book)
    data = pd.concat([data, pd.DataFrame([book])], ignore_index=True)
    save_data(data)
    return jsonify({"message": "Book added."}), 201


if __name__ == "__main__":
    app.run(debug=True)
