from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '02c4e75b494eafafb778726c93c11bf5'

from DayInReview import routes