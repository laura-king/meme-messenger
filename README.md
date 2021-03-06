# Meme Messenger

## Requirements:

Python 3.6+

Node.js 6.11+

## Setup:

### Installing libraries:

```bash
$ pip3 install -r requirements.txt
$ npm install -g bower
$ bower install
```
### Setting up Google OAuth for the server:

Follow [this guide](https://developers.google.com/identity/protocols/OAuth2#basicsteps) (just the basic steps section) by Google for setting up OAuth for Google+

In your `Authorized JavaScript origins` put: `http://[your application ip/domain]:[port]`

In your `Authorized redirect URIs` put: `http://[your application ip/domain]:[port]` and  `http://[your application ip/domain]:[port]/auth/authorized`

Use the `Client ID` and `Client secret` from that page in your server's configuration file

### Setting up a Reddit account for the server:

Create a [Reddit](https://www.reddit.com) account

Navigate to the [app setup page](https://www.reddit.com/prefs/apps/) and create an app that is a **script** with a redirect uri that is your application's base uri

Add your client id (under "personal use script"), secret, and Reddit username to the configuration file

### Configuring the server:

Copy the `app.cfg.template` file and rename it to `app.cfg`

Enter the `app.cfg` file in your favorite editor and change these settings to configure the server

| Setting name                   | Details                                  |
| ------------------------------ | :--------------------------------------- |
| SERVER_NAME                    | URL the server is to run on in format `[ip]:[port]`, defaults to `localhost:8080` |
| DEBUG                          | Flag to enable or disable Flask debug mode, more details [here](http://flask.pocoo.org/docs/0.12/quickstart/#debug-mode), defaults to `False`, **do not set to `True` in a production environment** |
| SECRET_KEY                     | Secret key for the Flask application, needed for sessions to keep users logged in, look [here](http://flask.pocoo.org/docs/0.12/quickstart/#sessions) for details on sessions and generating your secret key |
| GOOGLE_OAUTH_CLIENTID          | The Client ID provided to you from the Google OAuth client credential manager, required for the application |
| GOOGLE_OAUTH_SECRET            | The Client secret provided to you from the Google OAuth client credential manager |
| SQLALCHEMY_DATABASE_URI        | The location of the database for the application, defaults to an SQLite3 database in the base directory called "meme.db" |
| SQLALCHEMY_TRACK_MODIFICATIONS | Toggle weather or not SQLAlchemy will detect modifications on objects and emit signals for a change, defaults to `False` as it is not needed for the application |
| REDDIT_CLIENT_ID               | The client id given for the Reddit account used to search for random memes |
| REDDIT_CLIENT_SECRET           | The secret given for the Reddit account used to search for random memes |
| REDDIT_USERNAME                | the username for the Reddit account used to search for random memes, **do not include the '/u/'** |

Extra configuration settings for libraries used can be found here:

[Flask](http://flask.pocoo.org/docs/0.12/config/)

[Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/config/)

### Initializing the database schema:

The database schema is automatically generated off of the models in the `app.py` file, run

```bash
$ python3 init-db.py #or just `python app.py` depending on how you have python set up on your system
```

## Running the server:

in the base directory, run

```bash
$ export FLASK_APP=app.py #only first time in that terminal session
$ flask run
```
or

**Dependencies:**
```bash
$ python3 app.py
```

- Python 3.6
- Flask

**Contact Info:**

Laura King - lxk3301@rit.edu

Adam Kuhn - ark9719@rit.edu

Mackenzie Bowe - mmb8830@rit.edu

Bill Tarr - wet1177@rit.edu

Melissa Laskowski - mxl7583@rit.edu
