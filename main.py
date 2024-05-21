from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label="Cafe name", validators=[DataRequired()])
    location = StringField(label="Cafe Location on Google Maps (URL)" ,
                           validators=[DataRequired(), URL(message="Please enter a valid URL.")])
    opening_time = StringField(label="Opening Time e.g. 8AM")
    closing_time = StringField(label="Closing Time e.g. 5:30PM")

    coffee_rating = SelectField(
        label="Coffee Rating",
                                choices=['✘','☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'],
                                validators=[DataRequired()])

    wifi_rating = SelectField(
        label="WIFI Strength Rating",
    choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
    validators=[DataRequired()])

    num_sockets = SelectField(
        label="Power Socket Availability",
    choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
    validators=[DataRequired()])

    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit() and request.method == 'POST':
        print("True")
        with open(file='cafe-data.csv', mode='a', encoding='utf-8', newline='\n') as csv_file:
            cafe   = form.cafe.data
            location = form.location.data
            open_time = form.opening_time.data
            close_time = form.closing_time.data
            coffee_rating = form.coffee_rating.data
            wifi_rating = form.wifi_rating.data
            availability = form.num_sockets.data
            writer = csv.writer(csv_file, delimiter=',')
            csv_file.write('\n')
            writer.writerow(
                [cafe, location, open_time, close_time,
                 coffee_rating, wifi_rating, availability])
        return render_template("index.html")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open(file='cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
