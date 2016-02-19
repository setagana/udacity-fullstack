from restaurantApp import app
from flask import render_template, url_for, request, redirect, flash, jsonify

from restaurantApp.forms import restaurantForm

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
 
# from database_setup import *

# engine = create_engine("sqlite:///restaurantmenu.db")

# Base.metadata.bind = engine
 
# DBSession = sessionmaker(bind=engine)

# session = DBSession()

@app.route("/")
@app.route("/restaurants/")
def restaurantList():
	#Get all restaurants from DB and store as "restaurants"
	# return render_template("restaurants.html", restaurants=restaurants)
	return render_template("restaurants.html")

@app.route("/restaurants/<int:restaurant_id>/menu/")
def restaurantMenu(restaurant_id):
	#Get restaurant from database by ID and store as "restaurant"
	#Get courses from database by restaurant and store as "courses"
	#Get menu items by restaurant and by course and store as "[coursename]Items"
	# return render_template("restaurantMenu.html", restaurant=restaurant)
	return render_template("restaurantMenu.html")

@app.route("/restaurants/add", methods=["GET","POST"])
def newRestaurant():
	form = restaurantForm()
	if form.validate_on_submit():
		#Add restaurant to DB
		#Flash message
		return redirect(url_for("restaurantList"))
	else:
		return render_template("newRestaurant.html", form=form)

@app.route("/restaurants/<int:restaurant_id>/edit/", methods=["GET","POST"])
def editRestaurant(restaurant_id):
	#Get restaurant from DB and store as "restaurant"
	if request.method == "POST":
		# Commit changes to DB
		# flash message
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("editRestaurant.html", restaurant=restaurant)
		return render_template("editRestaurant.html")

@app.route("/restaurants/<int:restaurant_id>/delete/", methods=["GET","POST"])
def deleteRestaurant(restaurant_id):
	#Get restaurant from DB and store as restaurantToDelete
	if request.method == "POST":
		#Remove restaurantToDelete from DB, flash message
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("deleteRestaurant.html", restaurant=restaurantToDelete)
		return render_template("deleteRestaurant.html")

@app.route("/restaurants/<int:restaurant_id>/menu/add/", methods=["GET", "POST"])
def newMenuItem(restaurant_id):
	if request.method == "POST":
		#Create new menu item with data from form
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		# return render_template("newMenuItem.html", restaurant_id=restaurant_id)
		return render_template("newMenuItem.html")

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/", methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == "POST":
		# Commit menu item changes to DB
		# Flash message	
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		# return render_template("editMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, i=menuItem)
		return render_template("editMenuItem.html")

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/", methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
	deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == "POST":
		# Commit menu item deletion to DB
		# Flash messages
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		# return render_template("deleteMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
		return render_template("deleteMenuItem.html")

# #Making an API Endpoint (GET request)
# @app.route("/restaurants/<int:restaurant_id>/menu/JSON")
# def restaurantListJSON(restaurant_id):
# 	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
# 	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
# 	return jsonify(MenuItems=[i.serialize for i in items])

# #Making an API endpoint for a single menu item (GET request)
# @app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON")
# def menuItemJSON(restaurant_id, menu_id):
# 	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
# 	return jsonify(MenuItem=menuItem.serialize)