from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tierlist.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Tier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(100), nullable=False)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('home'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/home')
def home():
    tiers = Tier.query.all()
    return render_template('home.html', tiers=tiers)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('welcome'))
    return render_template('signup.html')

@app.route('/checkin')
def checkin():
    return render_template('checkin.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        tier = request.form['tier']
        new_tier = Tier(name=name, category=category, tier=tier)
        db.session.add(new_tier)
        db.session.commit()
        return redirect('/home')
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    tier_to_delete = Tier.query.get_or_404(id)
    db.session.delete(tier_to_delete)
    db.session.commit()
    return redirect('/home')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    tier = Tier.query.get_or_404(id)
    if request.method == 'POST':
        tier.name = request.form['name']
        tier.category = request.form['category']
        tier.tier = request.form['tier']
        db.session.commit()
        return redirect('/home')
    return render_template('edit.html', tier=tier)

if __name__ == '__main__':
    app.run(debug=True)
