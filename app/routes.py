from flask import render_template, flash, redirect, request
from app import app
from app.forms import LoanForm
import pandas as pd
import sys

def college_score(institution):


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/types')
def types():
    return render_template('types.html')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    form = LoanForm()
    if request.method == 'POST':
        institution=request.form['institution']
        career=request.form['career']
        income=request.form['income']
        race=request.form['race']
        gender=request.form['gender']
        cost=request.form['cost']
        expected=request.form['expected']
        actual=request.form['actual']
        dependency=request.form['dependency']

    if form.validate_on_submit():
        flash('Displaying {} {} {} {}'.format(
            institution, career, income, race))
        print(institution, career, income, race, file=sys.stderr)
    return render_template('calc.html', form=form)
