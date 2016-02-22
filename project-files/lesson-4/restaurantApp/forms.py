from flask_wtf import Form
from wtforms import TextField, validators

class restaurantForm(Form):
	name = TextField("Name", [validators.InputRequired()])
	address = TextField("Address", [validators.InputRequired()])
	city = TextField("City", [validators.InputRequired()])
	postCode = TextField("ZIP/Post code", [validators.InputRequired()])
	phone = TextField("Phone number", [validators.InputRequired()])
	website = TextField("Website", [validators.URL()])

class menuItemForm(Form):
	dishName = TextField("Dish name", [validators.InputRequired()])
	dishDescription = TextField("Description")
	course = TextField("Course",[validators.InputRequired()])
	price = TextField("Price", [validators.InputRequired()])