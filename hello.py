import os
import re
from datetime import datetime

from flask import Flask, flash, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email


def is_uoft_email(email):
    email_regex = r'^\S+@(\S*\.|)utoronto\.\S+$'

    # Since Match objects are not JSON Serializable, cast to boolean before returning
    return re.match(email_regex, email) is not None


def handle_updated_field(form, session, field_name):
    old_field = session.get(field_name)
    if old_field and old_field != form.data.get(field_name):
        flash("Looks like you've changed your {}!".format(field_name))
    session[field_name] = form.data.get(field_name)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = EmailField("What is your UofT Email address?", validators=[
                       DataRequired(), Email()])
    submit = SubmitField('Submit')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        handle_updated_field(form, session, 'name')
        handle_updated_field(form, session, 'email')

        session['is_uoft_email'] = is_uoft_email(form.email.data)
        return redirect(url_for('index'))

    return render_template(
        "index.html",
        form=form,
        name=session.get('name'),
        email=session.get('email'),
        is_uoft_email=session.get('is_uoft_email')
    )


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", name=name, current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)
