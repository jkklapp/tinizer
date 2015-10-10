from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack

import pickledb as db

from floo import Floo

from urlparse import urlparse

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
    original_url = request.form["original_url"]
    parsed_url = urlparse(original_url)
    is_valid_url = bool(parsed_url.scheme)
    if not is_valid_url:
        return render_template('400.html'), 400
    tiny_url = db.get("next_url")
    db.set(tiny_url, original_url)
    db.set("next_url", get_next_url(tiny_url))
    return render_template('index.html', tinized_url=urlize(tiny_url))

@app.route("/<tiny_url>")
def untinize(tiny_url):
    original_url = db.get(tiny_url)
    if not original_url:
        return render_template('404.html'), 404
    else:
        return redirect(original_url, code=302)

def get_first_url():
    return counter.initial()

def get_next_url(current_url):
    return counter.inc(current_url)

def urlize(url):
    return request.url_root + url

if __name__ == "__main__":
    # Characters valid of a shor URL
    counter = Floo("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=")
    db = db.load('tinize.db', True)
    n_urls = db.get("next_url")
    if not n_urls:
        db.set("next_url", get_first_url())
    app.debug = True
    app.run()
