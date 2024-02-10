from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tierlist.db'
db = SQLAlchemy(app)

class Tier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        tier = request.form['tier']
        new_tier = Tier(name=name, category=category, tier=tier)
        db.session.add(new_tier)
        db.session.commit()
        return redirect(url_for('index'))
    tiers = Tier.query.all()
    return render_template('index.html', tiers=tiers)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    tier = Tier.query.get_or_404(id)
    if request.method == 'POST':
        tier.name = request.form['name']
        tier.category = request.form['category']
        tier.tier = request.form['tier']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', tier=tier)

@app.route('/delete/<int:id>')
def delete(id):
    tier = Tier.query.get_or_404(id)
    db.session.delete(tier)
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
