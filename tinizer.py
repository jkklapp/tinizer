from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack

import pickledb as db

app = Flask(__name__)

@app.route("/")
def index():
    """Shows user the landing page, with the form to submit a new
    URL.
    """
    return render_template('index.html', url="")

@app.route("/about")
def about():
    """Shows user the about page.
    """
    return render_template('about.html', url="")

@app.route("/", methods=["POST"])
def tinize():
    """Reads from the request de original URL and generates the
    tiny url for it. Stores the data in the DB.
    """
    tiny_url = db.get("next_url")
    db.set(tiny_url, request.form["original_url"])
    db.set("next_url", get_next_url(tiny_url))
    return render_template('index.html', tinized_url=tiny_url)

def get_first_url():
    return 0

def get_next_url(current_url):
    return current_url + 1

if __name__ == "__main__":
    db = db.load('tinize.db', True)
    n_urls = db.get("next_url")
    if not n_urls:
        db.set("next_url", get_first_url())
    app.debug = True
    app.run()
