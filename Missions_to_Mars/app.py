#!pip install Flask-PyMongo (this bridges Flask and PyMongo)

# Create a route called "/scrape" that imports scrape_mars.py, and store the returned value in Mongo as a dictionary
from flask import Flask, render_template
from Flask-PyMongo import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongodb, create db and collection
db = client.scrape_mars_db
mars_facts = db.scrape_mars

# Route to render index.html template using data from Mongo
@app.route("/scrape")
def scrape():

    # Find record of data from the mongo database and set it to a variable
    mars_facts_var = list(mars_facts.find())

    # Return template and data
    return render_template("index.html", mars_facts=mars_facts_var )

if __name__ == "__main__":
    app.run(debug=True)