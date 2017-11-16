from flask import Blueprint, jsonify
import praw
import random

random_meme = Blueprint('random_meme', __name__, url_prefix='/random_meme')

reddit = None
subreddits = ['me_irl', 'meirl']


def configure_reddit(client_id, client_secret, username):
    """
    Call before using other methods in this
    """
    global reddit
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent='web:meme_messenger:v1.0(by /u/%s)' % username
    )


@random_meme.route('/')
def get_random_meme():
    posts = []
    for post in reddit.subreddit(random.choice(subreddits)).hot(limit=50):
        posts.append(post)
    return jsonify({"url": random.choice(posts).url})
