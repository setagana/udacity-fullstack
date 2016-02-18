from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import *

class webserverHandler(BaseHTTPRequestHandler):
	"""docstring for web"""
	def do_GET(self):
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' name='testFormHello' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "&#161Hola!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind=engine)
				session = DBSession()

				restaurantList = session.query(Restaurant).all()

				output = ""
				output += "<html><body>"

				for restaurant in restaurantList:
					output += "<h2>%s</h2>" % restaurant.name
					output += "<h3><a href='/restaurants/%d/edit'>Edit</a></h3>" % restaurant.id
					output += "<h3><a href='/restaurants/%d/delete'>Delete</a></h3>" % restaurant.id
					output += "<br />"
			
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path == "/restaurants/new":
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Please tell us the name of your restaurant:</h2><input name='restaurant' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/edit"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				this_URL = self.path
				restaurant_id = int(this_URL[13:self.path.rfind('/')])

				output = ""
				output += "<html><body>"
				output += "<h1>So, you'd like to make some changes?</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='%s'><h2>Please tell us the new name of your restaurant:</h2><input name='new_name' type='text' ><input name='restaurant_id' type='hidden' value='%d'><input type='submit' value='Submit'></form>" % (this_URL, restaurant_id)
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/delete"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				this_URL = self.path
				restaurant_id = int(this_URL[13:self.path.rfind('/')])

				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind=engine)
				session = DBSession()

				restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).one()

				output = ""
				output += "<html><body>"
				output += "<h1>Are you sure you want to delete your restaurant?</h1>"
				output += "<form method='POST' enctype='multipart/form-data' action='%s'><h2>We're sad to see you go. Please confirm you'd like to delete %s from the database: </h2><input name='restaurant_id' type='hidden' value='%d'><input type='submit' value='Delete'></form>" % (this_URL, restaurant_to_delete.name, restaurant_id)
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return


		except IOError:
			self.send_error(404, "File Note Found %s" % self.path)
	
	def do_POST(self):
		try:
			if self.path.endswith('/hello'):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += "<h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]

				output += "<form method='POST' enctype='multipart/form-data' name='testFormPost' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
			if self.path == '/restaurants/new':
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					restaurant_name = fields.get('restaurant')

				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind=engine)
				session = DBSession()

				newRestaurant = Restaurant(name=restaurant_name[0])
				session.add(newRestaurant)
				session.commit()

				output = ""
				output += "<html><body>"
				output += "<h2>Thanks for registering your restaurant<h2>"
				output += "<h4>%s has been added to our database.</h4>" % restaurant_name[0]
				output += "</body></html>"

				self.wfile.write(output)
				print output

			if self.path.endswith('/edit'):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					new_name = fields.get('new_name')
					restaurant_id = fields.get('restaurant_id')

				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind=engine)
				session = DBSession()

				restaurant_to_update = session.query(Restaurant).filter_by(id=restaurant_id[0]).one()
				restaurant_to_update.name = new_name[0]
				session.add(restaurant_to_update)
				session.commit()

				output = ""
				output += "<html><body>"
				output += "<h2>Thanks for updating your restaurant<h2>"
				output += "<h4>Our records now show your restaurant's name is: %s.</h4>" % new_name[0]
				output += "</body></html>"

				self.wfile.write(output)
				print output

			if self.path.endswith('/delete'):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
				if ctype == 'multipart/form-data':
					fields = cgi.parse_multipart(self.rfile, pdict)
					restaurant_id = fields.get('restaurant_id')

				engine = create_engine('sqlite:///restaurantmenu.db')
				Base.metadata.bind = engine
				DBSession = sessionmaker(bind=engine)
				session = DBSession()

				restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id[0]).one()

				session.delete(restaurant_to_delete)
				session.commit()

				output = ""
				output += "<html><body>"
				output += "<h2>Your restaurant has been deleted<h2>"
				output += "<h4>We have removed your restaurant from the database. Goodbye.</h4>"
				output += "</body></html>"

				self.wfile.write(output)
				print output
		except:
			pass	

def main():
	try:
		port = 8080
		server = HTTPServer(('',port), webserverHandler)
		print "Web server running on port %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print "^C entered, stopping web server..."
		server.socket.close()

if __name__ == '__main__':
	main()