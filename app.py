from flask import Flask, jsonify, request
from scrape_mars import scrape
import pymongo

app = Flask(__name__)

CONN = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONN)
db = client.mars_db

@app.route('/')
def home():
    result = db.mars_collection.find_one()
    return render_template("index.html",result=result)

@app.route('/scrape')
def scrape_route():
    result = scrape()
    db.mars_collection.insert_one(result)
    return


if __name__ == "__main__":
    app.run(debug=True)