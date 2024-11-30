from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, RadioField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# app.config['SECRET_KEY'] = 'XD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/')
def index():
    return 'Witaj w aplikacji Flask z SQLAlchemy!'

@app.route('/add_prod/<product>/<price>')
def add_prod(product, price):
    new_product = Product(name=product, price=int(price))
    db.session.add(new_product)
    db.session.commit()
    return f'Produkt {product} został dodany.'

@app.route('/prods')
def get_prods():
    prods = Product.query.all()
    prod_list = [f"{prod.id}: {prod.name} ({prod.price})" for prod in prods]
    return "<br>".join(prod_list)

@app.route('/delete_prod/<int:prod_id>')
def delete_prod(prod_id):
    prod_to_delete = Product.query.get(prod_id)
    if prod_to_delete:
        db.session.delete(prod_to_delete)
        db.session.commit()
        return f'Użytkownik o ID {prod_id} został usunięty.'
    else:
        return f'Użytkownik o ID {prod_id} nie istnieje.'

@app.route('/find/<name>')
def find(name):
    product_to_find = Product.query.filter_by(name=name).first()
    if product_to_find:
        return f'Dane produktu, które szukałeś: {product_to_find.id}: {product_to_find.name} ({product_to_find.price}).'
    else:
        return f'Produkt o nazwie "{name}" nie został znaleziony.'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

class UserInfoForm(FlaskForm):
    name = StringField('Imię', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    sumbit = SubmitField()

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = UserInfoForm()
#     if form.validate_on_submit():
#         flash(f'Imię: {form.name.data}, Email: {form.email.data}', 'success')
#         return redirect(url_for('index'))
#     return render_template('form.html', form=form)

# if __name__ == "__main__":
#     with app.app_context():
#         app.run(debug=True)


class MyForm(FlaskForm):
    name = StringField('Imię', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Data urodzenia', validators=[DataRequired()])
    profession = SelectField('Zawód', choices=[('dev', 'Programista'), ('teacher', 'Nauczyciel'), ('student', 'Student')], validators=[DataRequired()])
    student_status = RadioField('Status Studenta', choices=[('yes', 'Tak'), ('no', 'Nie')], validators=[DataRequired()])
    location = StringField('Miejsce zamieszkania', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj się')

@app.route('/form', methods=['GET', 'POST'])
def formularz():
    form = MyForm()
    if form.validate_on_submit():
        flash(f'Rejestracja zakończona sukcesem dla {form.name.data}!', 'success')
        return redirect('/form')
    return render_template('form.html', form=form)

if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)

@app.route('/submit', methods=['POST'])
def showForm():
    name = request.form.get('name')
    dob = request.form.get('dob')
    profession = request.form.get('profession')
    student_status = request.form.get('student_status')
    location = request.form.get('location')
    return render_template('submit.html', name=name, dob=dob, profession=profession, student_status=student_status, location=location)