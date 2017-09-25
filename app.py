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

@app.route('/account/<username>')
def account_page(username):
    """
    Loads account page
    """
    #Obtain the user's information somehow and package it in a dictonary
    #Get it from the db based on a session token?
    return render_template('account_page.html', username=username)

if __name__ == "__main__":
    app.run()
