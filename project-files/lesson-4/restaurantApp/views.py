from restaurantApp import app
from flask import render_template, url_for, request, redirect, flash, jsonify

from restaurantApp.forms import restaurantForm
from restaurantApp.forms import menuItemForm

from restaurantApp.database_setup import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurantApp/app.db")

Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)

session = DBSession()

from decimal import *
getcontext().prec = 2

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
	courseList = ["Snacks","Starters","Mains","Sides","Desserts","Aperitifs"]
	menuItems = [["Gruyere and white truffle maccarons","Crispy chicken skins"],["Pennette Formaggi","Calamari","Risotto Mio","Garlic Bread with Mozarella"],["Calzone Diavolo","Pennette Formaggi","Nicoise Salad","Pennette Bolognese"],["Coleslaw","Broccolini","Mixed Salad","Potato Nocciola"],["Treacle tart cheesecake","Vanilla cheesecake","Honeycomb Cream Slice"],["Coffee","Tea","Whiskey","Brandy"]]
	return render_template("restaurantMenu.html", courseList=courseList, menuItems=menuItems)

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
	form = restaurantForm()
	if form.validate_on_submit():
		# Commit changes to DB
		# flash message
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("editRestaurant.html", restaurant=restaurant)
		return render_template("editRestaurant.html", form=form)

@app.route("/restaurants/<int:restaurant_id>/delete/", methods=["GET","POST"])
def deleteRestaurant(restaurant_id):
	#Get restaurant from DB and store as restaurantToDelete
	if request.method == "POST":
		#Remove restaurantToDelete from DB, flash message
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("deleteRestaurant.html", restaurant=restaurantToDelete)
		return render_template("deleteRestaurant.html")

@app.route("/restaurants/<int:restaurant_id>/menu/add/", methods=["GET","POST"])
def newMenuItem(restaurant_id):
	form = menuItemForm()
	if request.method == "POST":
		convertedPrice = int(Decimal(form.price.data) * 100)
		newItem = MenuItem(name = form.dishName.data, course = form.course.data, description = form.dishDescription.data, price = convertedPrice, restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		#Flash message
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		courseList = ["Snacks","Starters","Mains","Sides","Desserts","Aperitifs"]
		return render_template("newMenuItem.html", restaurant_id=restaurant_id, form=form, courseList=courseList)

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/", methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
	# menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	form = menuItemForm()
	if form.validate_on_submit():
		# Commit menu item changes to DB
		# Flash message	
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		# return render_template("editMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, i=menuItem)
		courseList = ["Snacks","Starters","Mains","Sides","Desserts","Aperitifs"]
		return render_template("editMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, form=form, courseList=courseList)

# Task 3: Create a route for deleteMenuItem function here

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/", methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
	# deletedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == "POST":
		# Commit menu item deletion to DB
		# Flash messages
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant_id))
	else:
		# return render_template("deleteMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
		return render_template("deleteMenuItem.html", restaurant_id=restaurant_id)

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