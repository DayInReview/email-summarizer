from flask import render_template, url_for, flash, redirect, request
from DayInReview import app
from DayInReview.forms import DisplayForm

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")

@app.route("/display", methods=['GET', 'POST'])
def display():
    form = DisplayForm()
    if form.validate_on_submit():
        flash('this works')
    return render_template("display.html", title="Display", form=form)