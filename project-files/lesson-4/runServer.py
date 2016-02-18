from restaurantApp import app

if __name__ == "__main__":
	app.secret_key = "gRJ5Jl41uVifVCfICzYYsIci7cer01gP"
	app.debug = True
	app.run(host = "0.0.0.0", port = 5000)