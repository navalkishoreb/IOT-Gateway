from flask import Flask,render_template,url_for,redirect,session,flash
from flask_script import Manager 
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import os.path

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
#https://www.grc.com/passwords.htm
app.config["SECRET_KEY"]="qzAbKOkhmFvNVlejBqXImtwIzlngugUPlXpHg1WOoj7EUMxE47ISEFVtAnCVfqo"
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///"+os.path.join(base_dir,"data.sqlite")
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)



class LoginForm(FlaskForm):
	username = StringField("Username: ",validators=[Required()])
	password = PasswordField("Password: ",validators=[Required()])
	submit = SubmitField("Login")

"""user_sensors = db.Table("user_sensors",
		db.Column("username" , db.String(64), db.ForeignKey("users.username"), nullable = False), 
		db.Column("sensor_id", db.String(8), db.ForeignKey("sensor_data.sensor_id"), nullable = False),
		db.PrimaryKeyConstraint("username","sensor_id")
		)
"""

class User(db.Model):
	__tablename__	= "users"
	username = db.Column(db.String(64),primary_key = True, index = True)
	password = db.Column(db.String(64), nullable = False)
	is_logged_in = db.Column(db.Boolean , nullable = False, default = False)
	sensors = db.relationship("SensorData", backref = "users")
	def __repr__(self):
		userData = "user-> %r : password-> %r : is_logged_in-> %r " % (self.username, self.password, self.is_logged_in)
		return userData

class SensorData(db.Model):
	__tablename__ = "sensor_data"
	sensor_id = db.Column(db.String(8), index = True)
	topic = db.Column(db.Text ,unique = True)
	read_write = db.Column(db.Integer)
	owner = db.Column(db.String(64), db.ForeignKey("users.username"), nullable = False)

	__table_args__ = (db.CheckConstraint("read_write>=1 and read_write <=2", name ="check_read_write"),
	db.PrimaryKeyConstraint("sensor_id","owner"),{})

	def __repr__(self):
		sensorData = "sensor_id %r : owner %r : topic %r : read_write %r " % (self.sensor_id, self.owner, self.topic, self.read_write)
		return sensorData


@app.route("/",methods=["GET","POST"])
def homePage():
	loginForm = LoginForm()
	if loginForm.validate_on_submit():
		old_name = session.get("username")
		if old_name is not None and old_name != loginForm.username.data:
			flash("It seems you have changed your name.")
		session["username"] = loginForm.username.data
		loginForm.username.data = ""
		return redirect(url_for("homePage"))
	return render_template("homePage.html", current_time = datetime.utcnow(), form = loginForm, name = session.get("username"))

@app.route("/user/<name>")
def userPage(name):
	return render_template("userPage.html",username = name)


@app.errorhandler(404)
def pageNotFound(e):
	return render_template("404.html"),404

@app.errorhandler(500)
def internalServerError(e):
	return render_template("500.html"),500





if __name__ == "__main__":
	manager.run()

