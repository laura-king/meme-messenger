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
    #See if this user is the user looking
    #Check to see if a user exists with that name
    existing_user=True
    user_data = {"username":username}
    if existing_user:
        #Temp List for now
        blocked = ['BigJim', 'Jerkface420', 'GuyFerrari']
        #Obtain the user's information somehow and package it in a dictonary
        user_data.update({"blocked_users": blocked, "privacy":'friends'})
    return render_template('account_page.html', user_data=user_data, existing_user=existing_user)

if __name__ == "__main__":
    app.run()
