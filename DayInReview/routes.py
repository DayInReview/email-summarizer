from flask import render_template, url_for, flash, redirect, request
from DayInReview import app
from DayInReview.forms import DisplayForm
from DayInReview.read_emails import read_emails

@app.route("/")
@app.route("/home")
def home():
    form = DisplayForm()
    return render_template("home.html", title="Home", form=form)

@app.route("/display", methods=['GET', 'POST'])
def display():
    form = DisplayForm()
    read_emails(form.email.data, form.password.data, 1)
    return render_template("display.html", title="Display", form=form)