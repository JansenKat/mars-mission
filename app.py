from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/')
def home():
    return

@app.route('/scrape')
def scrape():
    return


if __name__ == "__main__":
    app.run(debug=True)