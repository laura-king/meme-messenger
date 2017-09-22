from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
	"""
	Loads main page
	"""
	return render_template('base_page.html')

@app.route('/welcome')
def welcome_page():
	"""
	Loads welcome page
	"""
	return render_template('welcome.html')

@app.route('/account')
def account_page():
	"""
	Loads account page
	"""
	return render_template('account_page.html')

if __name__ == "__main__":
	app.run()
