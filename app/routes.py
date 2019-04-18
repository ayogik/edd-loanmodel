from flask import render_template, flash, redirect, request
from app import app, ge, scorecard, occupation
from app.forms import LoanForm
import pandas as pd
import sys

def college_score(institution):
    debtToEarnings = pd.Series.item(ge[ge['Institution Name'] == institution.upper()]['Debt-to-Earnings Annual Rate']) #22.5

    defaultRate = pd.Series.item(scorecard[scorecard['INSTNM'] == institution]['CDR3']) #.00699
    federalLoanStudents = pd.Series.item(scorecard[scorecard['INSTNM'] == institution]['PCTFLOAN']) #.0355
    averageCost = pd.Series.item(scorecard[scorecard['INSTNM'] == institution]['COSTT4_A']) #64400
    medianDebt = pd.Series.item(scorecard[scorecard['INSTNM'] == institution]['GRAD_DEBT_MDN']) #6100

    factors = [debtToEarnings, defaultRate, averageCost, medianDebt, federalLoanStudents]
    ranges = [{'min':0, 'max':32.31}, # debtToEarnings
                {'min':0, 'max':0.562}, # defaultRate
                {'min':4259, 'max':85308}, # averageCost
                 {'min':1262, 'max':52000}, # medianDebt
                 {'min':0, 'max':1}] # federalLoanStudents

    total = 0
    for i in range(0,4):
        if isinstance(factors[i], str):
            total += 0.5
        else:
            if i==1:
                scaled = 50*(factors[i] - ranges[i]['min'])/(ranges[i]['max'] - ranges[i]['min'])
                total += scaled
            else:
                scaled = (factors[i] - ranges[i]['min'])/(ranges[i]['max'] - ranges[i]['min'])
                total += scaled
    total += 0.5-0.5*(factors[4] - ranges[4]['min'])/(ranges[4]['max'] - ranges[4]['min'])

    return total

def personal_score(collegeScore, career, income, race, gender):
    personalIncome = pd.Series.item(occupation[occupation['OCC_TITLE'] == career]['A_MEAN'].iloc[[0]])
    variations = {'White':{'Male':1.11945,'Female':0.922821},
                    'African American':{'Male':0.838333,'Female':0.756954},
                    'Asian':{'Male':1.428603,'Female':1.102105},
                    'Hispanic':{'Male':0.796935,'Female':0.704974},
                    'Other':{'Male':1,'Female':0.8}}
    realIncome = personalIncome * variations[race][gender]
    income = int(income)

    total = 0
    if realIncome < 250000:
        total += 3*(1-realIncome/250000)
        print (total, file=sys.stderr)
    else:
        total += 0
    print (income, file=sys.stderr)
    if income < 250000:
        total += 3*(1-realIncome/250000)
    else:
        total += 0
    total += collegeScore
    return total

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
        output = college_score(institution)
        pScore = personal_score(output, career, income, race, gender)
        flash('Your Institutional, Personal Score: {}, {}'.format(output, pScore))
    return render_template('calc.html', form=form)
