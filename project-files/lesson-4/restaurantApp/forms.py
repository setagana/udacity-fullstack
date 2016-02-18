from flask_wtf import Form
from wtforms import TextField, validators

class restaurantForm(Form):
	address = TextField("Address", [validators.InputRequired()])
	city = TextField("City", [validators.InputRequired()])
	postCode = TextField("ZIP/Post code", [validators.InputRequired()])
	phone = TextField("Phone number", [validators.InputRequired()])
	website = TextField("Website", [validators.URL()])