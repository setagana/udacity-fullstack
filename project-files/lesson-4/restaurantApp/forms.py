from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, URL, Regexp

class restaurantForm(Form):
	name = StringField("Name", validators=[DataRequired()])
	address = StringField("Address", validators=[DataRequired()])
	city = StringField("City", validators=[DataRequired()])
	postCode = StringField("ZIP/Post code", validators=[DataRequired()])
	phone = StringField("Phone number", validators=[DataRequired()])
	website = StringField("Website", validators=[URL()])

class menuItemForm(Form):
	dishName = StringField("Dish name", validators=[DataRequired()])
	dishDescription = StringField("Description")
	course = StringField("Course", validators=[DataRequired()])
	price = StringField("Price", validators=[DataRequired(), Regexp("^(?!0+$)\d{0,5}(.\d{1,2})?$",message="That doesn't look like a valid number")])