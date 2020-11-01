from flask import Flask, render_template, request
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "squad.runtimeterror@gmail.com",
    MAIL_PASSWORD = "RUNTIMEterror"
)
mail = Mail(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1:3307/RuntimeTerror"
db = SQLAlchemy(app)

class ContactMe(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    message = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(10), nullable=True)

@app.route('/', methods = ['GET', 'POST'])
def home():
    x = ['squad.runtimeterror@gmail.com']
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = ContactMe(name = name, email = email, phone = phone, message = message, date = datetime.now())
        db.session.add(entry)
        db.session.commit()
        mail.send_message('New message from ' + name, sender=email, recipients=x, body=message + '\n' + email + '\n' + phone)
        return render_template('contact.html')
    return render_template('index.html')


@app.route('/contact', methods=['GET', 'POST'])
def Contact():

    return render_template('index.html')


app.run(debug=True)
