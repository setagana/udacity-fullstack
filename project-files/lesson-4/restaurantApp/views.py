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
	restaurantResults = session.query(Restaurant).all()
	return render_template("restaurants.html", restaurantResults = restaurantResults)

@app.route("/restaurants/<int:restaurant_id>/menu/")
def restaurantMenu(restaurant_id):
	#Get restaurant from database by ID and store as "restaurant"
	#Get courses from database by restaurant and store as "courses"
	#Get menu items by restaurant and by course and store as "[coursename]Items"
	# return render_template("restaurantMenu.html", restaurant=restaurant)
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	courseQuery = session.query(MenuItem.course).filter_by(restaurant_id = restaurant_id).distinct()
	courseList = [result[0] for result in courseQuery]
	menuItems = []
	for course in courseList:
		itemsQuery = session.query(MenuItem).filter_by(course = course)
		menuItems.append(itemsQuery)
	return render_template("restaurantMenu.html", restaurant=restaurant, courseList=courseList, menuItems=menuItems)

@app.route("/restaurants/add", methods=["GET","POST"])
def newRestaurant():
	form = restaurantForm()
	if form.validate_on_submit():
		newRestaurant = Restaurant(name = form.name.data, address = form.address.data, city = form.city.data, postcode = form.postCode.data, phone = form.phone.data, website = form.website.data)
		session.add(newRestaurant)
		session.commit()
		#Flash message
		return redirect(url_for("restaurantList"))
	else:
		return render_template("newRestaurant.html", form=form)

@app.route("/restaurants/<int:restaurant_id>/edit/", methods=["GET","POST"])
def editRestaurant(restaurant_id):
	restaurantToEdit = session.query(Restaurant).filter_by(id = restaurant_id).one()
	form = restaurantForm()
	if form.validate_on_submit():
		restaurantToEdit.name = form.name.data
		restaurantToEdit.address = form.address.data
		restaurantToEdit.city = form.city.data
		restaurantToEdit.postcode = form.postCode.data
		restaurantToEdit.phone = form.phone.data
		restaurantToEdit.website = form.website.data
		session.add(restaurantToEdit)
		session.commit()
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("editRestaurant.html", restaurant=restaurant)
		return render_template("editRestaurant.html", form=form, restaurantToEdit = restaurantToEdit)

@app.route("/restaurants/<int:restaurant_id>/delete/", methods=["GET","POST"])
def deleteRestaurant(restaurant_id):
	restaurantToDelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		session.query(MenuItem).filter_by(restaurant_id = restaurant_id).delete()
		session.delete(restaurantToDelete)
		session.commit()
		#flash message
		return redirect(url_for("restaurantList"))
	else:
		# return render_template("deleteRestaurant.html", restaurant=restaurantToDelete)
		return render_template("deleteRestaurant.html", restaurantToDelete=restaurantToDelete)

@app.route("/restaurants/<int:restaurant_id>/menu/add/", methods=["GET","POST"])
def newMenuItem(restaurant_id):
	form = menuItemForm()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if form.validate_on_submit():
		convertedPrice = int(Decimal(form.price.data) * 100)
		newItem = MenuItem(name = form.dishName.data, course = form.course.data, description = form.dishDescription.data, price = convertedPrice, restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		#Flash message
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant.id))
	else:
		courseQuery = session.query(MenuItem.course).filter_by(restaurant_id = restaurant.id).distinct()
		courseList = [result[0] for result in courseQuery]
		return render_template("newMenuItem.html", restaurant=restaurant, form=form, courseList=courseList)

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/", methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	form = menuItemForm()
	if form.validate_on_submit():
		menuItem.name = form.dishName.data
		menuItem.course = form.course.data
		menuItem.description = form.dishDescription.data

		convertedPrice = int(Decimal(form.price.data) * 100)
		menuItem.price = convertedPrice

		session.add(menuItem)
		session.commit()
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant.id))
	else:
		courseQuery = session.query(MenuItem.course).filter_by(restaurant_id = restaurant.id).distinct()
		courseList = [result[0] for result in courseQuery]
		return render_template("editMenuItem.html", restaurant=restaurant, menuItem = menuItem, form=form, courseList=courseList)

@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/", methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	if request.method == "POST":
		session.delete(itemToDelete)
		session.commit()
		# Flash messages
		return redirect(url_for("restaurantMenu", restaurant_id=restaurant.id))
	else:
		# return render_template("deleteMenuItem.html", restaurant_id=restaurant_id, menu_id=menu_id, item=deletedItem)
		return render_template("deleteMenuItem.html", restaurant=restaurant, menu_id=menu_id, itemToDelete = itemToDelete)

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