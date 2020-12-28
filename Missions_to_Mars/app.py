#!pip install Flask-PyMongo (this bridges Flask and PyMongo)

# Create a route called "/scrape" that imports scrape_mars.py, and store the returned value in Mongo as a dictionary
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

# Import script to run in the /scrape route
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/scrape_mars_db"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find record of data from the mongo database and set it to a variable
    mars_facts_var = mongo.db.scrape_mars.find_one()

    news_title = mars_facts_var["latest_news"]
    news_p = mars_facts_var["latest_news_paragraph"]
    featured_img_url = mars_facts_var["current_featured_image_url"]
    mars_facts_table = mars_facts_var["mars_facts"]
    mars_hemispheres_dict = mars_facts_var["mars_hemispheres_urls"]

    # Return template and data
    return render_template("index.html",
                            news_title=news_title,
                            news_p=news_p,
                            featured_img_url=featured_img_url,
                            mars_facts_table=mars_facts_table,
                            mars_hemispheres_dict=mars_hemispheres_dict)

@app.route("/scrape")
def scrape():
    scrape_data= scrape_mars.scrape()
    mongo.db.scrape_mars.update({}, scrape_data, upsert=True)
    
    # Redirect back to homepage
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)