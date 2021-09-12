from flask import Flask, redirect, url_for, render_template, request, session
from flask.helpers import flash
from flask_mail import Mail, Message  # pip install flask-mail
from flask_sqlalchemy import SQLAlchemy  # pip install flask-sqlalchemy
from datetime import datetime
from flask_admin import Admin  # pip install flask-admin
from flask_admin.contrib.sqla import ModelView
# WEB SERVER GATEWAY INTERFACE #pip install pymysql
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_article'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)
admin = Admin(app)
mail = Mail(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime)
    slug = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Names %r>' % self.title


class Service_client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.Integer, nullable=True)
    modele = db.Column(db.Integer)
    date_ = db.Column(db.DateTime, default=datetime.utcnow)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin.add_view(SecureModelView(Posts, db.session))
admin.add_view(SecureModelView(Service_client, db.session))


@app.errorhandler(404)  # invalid url
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)  # Internal Server Error
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/welcomeadmin", methods=["GET", "POST"])
def LoginAdmin():
    return render_template('adminlogin.html')


@app.route("/post/<string:slug>")
def post(slug):
    post = Posts.query.filter_by(slug=slug).one()
    return render_template('post.html', post=post)


@app.route("/post")
def article():
    posts = Posts.query.all()
    return render_template('article.html', posts=posts)


@app.route("/service", methods=["GET", "POST"])
def service():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        date_ = request.form.get("date_")
        modele = request.form.get("modele")
        client = Service_client(name=name, email=email,
                                phone=phone, date_=date_, modele=modele)
        db.session.add(client)
        db.session.commit()
        flash("your request have been sent")
    return render_template('service.html')


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        msg = Message(
            subject=f"Mail from {name}", body=f"Name:{name} \n E-Mail:{email} \n Phone:{phone} \n\n\n {message}", sender=email, recipients=['maslernono@gmail.com'])
        mail.send(msg)
        flash('Your Message have been sent successfully')
        return render_template('contact_us.html', succeed=True)
    return render_template('contact_us.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'Noussair' and request.form.get('password') == 'IDSD2021':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', failed=True)
    return render_template('login.html')


@property
def password(self):
    raise AttributeError('password is not readable attribute')


@password.setter
def password(self, password):
    self.password_hash = generate_password_hash(password)


def password(self, password):
    return check_password_hash(self.password_hash)


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(port=50, debug=True)
