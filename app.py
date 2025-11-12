from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime, date
from sqlalchemy.orm import joinedload
#from flask_compress import Compress

from models import db, User, Ticket

app = Flask(__name__)
#Compress(app)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zombiepark.db'

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    template = "admin_home.html" if (current_user.is_authenticated and current_user.role == "admin") else "index.html"
    return render_template(template)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed_pw = generate_password_hash(password, method="pbkdf2:sha256")
        new_user = User(username=username, password_hash=hashed_pw)

        db.session.add(new_user)
        db.session.commit()

        flash("Реєстрація успішна! Увійдіть у систему.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            if user.role == "admin":
                return redirect(url_for("admin_home"))
            else:
                return redirect(url_for("home"))  # Можна змінити на сторінку замовлення квитків
        else:
            flash("Невірний логін або пароль.")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/admin_home")
@login_required
def admin_home():
    if current_user.role != "admin":
        return "Доступ заборонено!", 403
    return render_template("admin_home.html")

@app.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
    if request.method == "POST":
        visit_date_str = request.form.get("visit_date")
        ticket_type = request.form.get("ticket_type", "standard")
        quantity = int(request.form.get("quantity", 1))  # кількість з форми

        try:
            visit_date = datetime.strptime(visit_date_str, "%Y-%m-%d").date()
        except Exception:
            flash("Невірний формат дати.", "danger")
            return redirect(url_for("tickets"))

        if visit_date < date.today():
            flash("Дата не може бути в минулому.", "warning")
            return redirect(url_for("tickets"))

        ticket_prices = {"standard": 100, "vip": 200}
        total_price = ticket_prices.get(ticket_type, 100) * quantity

        ticket = Ticket(
            user_id=current_user.id,
            event_date=visit_date,
            ticket_type=ticket_type,
            price=total_price
        )
        db.session.add(ticket)
        db.session.commit()
        flash(f"Квитки успішно заброньовано! Сума: {total_price} грн", "success")
        return redirect(url_for("my_tickets"))

    return render_template("tickets.html")

@app.route("/my_tickets")
@login_required
def my_tickets():
    tickets = Ticket.query.options(joinedload(Ticket.owner)).order_by(Ticket.created_at.desc()).all()
    return render_template("my_tickets.html", tickets=tickets)

@app.route("/admin/tickets")
@login_required
def admin_tickets():
    if current_user.role != "admin":
        return "Доступ заборонено!", 403
    tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template("admin_tickets.html", tickets=tickets)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
