from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

@app.route('/')
def main_page():
	"""
	Loads main page
	"""
	return render_template('base_page.html')

if __name__ == "__main__":
	app.run()
