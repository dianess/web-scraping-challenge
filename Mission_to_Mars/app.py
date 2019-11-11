from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Create connection variable
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"


# Pass connection to the pymongo instance.
mongo = PyMongo(app)


# Define the routes
# The home page
@app.route('/')
def index():

    # Find one record of data from the mongo database
    mars = mongo.db.items.find_one()

    # Return template and data
    return render_template('index.html', mars=mars)

# Route that will trigger the scrape function
@app.route('/scrape')
def scraper():

    # Run the scrape function
    mars = mongo.db.items
    mars_data = scrape_mars.scrape()

    # Update the Mongo Database using update and upsert=True with new mars_data
    mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")
    # return index()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
