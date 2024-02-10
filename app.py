from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tierlist.db'
db = SQLAlchemy(app)

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
        # ตรวจสอบการล็อกอิน
        # ในที่นี้ให้เราสมมติว่าล็อกอินสำเร็จเสมอ
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    tiers = Tier.query.all()
    return render_template('home.html', tiers=tiers)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # ทำการสมัครสมาชิก
        # ในที่นี้เราสมมติว่าการสมัครสมาชิกสำเร็จเสมอ
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/checkin')
def checkin():
    # ตรวจสอบการเช็คอิน
    # ในที่นี้เราสมมติว่าผู้ใช้ทำการเช็คอินสำเร็จเสมอ
    return redirect(url_for('home'))

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
