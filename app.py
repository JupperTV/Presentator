"""Run this to start the server"""

import flask

from typing import Final
from uuid import uuid4 as newUUID

app = flask.Flask(__name__)

# This is the name for the cookie used to indentify which secondary
# screen to display.
# The value of the cookie is a randomly generated uuid.
COOKIE: Final[str] = "JuppersPresentator"

TEMPLATE_FOLDER: Final[str] = "templates"

# Generate a uuid first
@app.route("/", methods=["GET"])
def index():
    cookieValue = flask.request.cookies.get(COOKIE)
    if cookieValue:  # if cookie is truthy
        return flask.redirect(
                flask.url_for(
                    "mainPresent",
                    presentationid=cookieValue))
    return flask.redirect(flask.url_for("newUser"))


@app.route("/new", methods=["GET"])
def newUser():
    newid = str(newUUID())
    response = flask.make_response(
            flask.render_template(
                "new.html",
                presentationId=newid))
    response.set_cookie(key=COOKIE, value=newid)
    return response


@app.route("/mainPresent/<presentationid>", methods=["GET"])
def mainPresent(presentationid: str):
    print("mainpresent:", presentationid)
    return flask.render_template(
            "mainPresentator.html",
            presentationId=presentationid,
            url = f"{flask.request.host_url}secondPresent/{presentationid}/")

@app.route("/secondPresent/<presentationid>", methods=["GET"])
def secondPresent(presentationid: str):
    print("secondpresent:", presentationid)
    return flask.render_template(
            "secondPresentator.html",
            presentationId=presentationid)

if __name__ == "__main__":
    app.run(port=80, debug=True)

