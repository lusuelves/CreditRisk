#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:06:36 2020

@author: luciasuelves
"""

from flask import Flask, request
from prediction import predict

app = Flask(__name__)


@app.route('/')
def hello():
    return """
            <h1> Risky Credit </h1>
            <form action="/answer" method="post">
                        Loan quantity: <input type="int" name="loan">  <br />
                        Mortgage due: <input type="int" name="mortdue">  <br />
                        Home value: <input type="int" name="value">  <br />

            <label>Reason:</label>
                <select name='reason'>
                  <option value="HomeImp">Home improvement</option>
                  <option value="DebtCon">Debbt consolidation</option>
                </select><br>
            <label>Choose a job:</label>
                <select name='job'>
                  <option value="Mgr">Mgr</option>
                  <option value="Office">Office</option>
                  <option value="Sales">Sales</option>
                  <option value="Self">Self</option>
                  <option value="Other">Other</option>
                </select><br>
                        Years you have been working:<input type="int" name="yoj">  <br />
                        Derogacy: <input type="int" name="derog">  <br />
                        Delinquency: <input type="int" name="delinq">  <br />
                        Clage: <input type="int" name="clage">  <br />
                        Ninq: <input type="int" name="ninq">  <br />
                        Clno: <input type="int" name="clno">  <br />
                        Debt-income: <input type="int" name="debtinc">
            <input type="submit" name= "form" value="Submit" />
            </form>
            """
            
@app.route('/answer',methods=['POST'])
def response():
    variables = ['loan','mortdue','value','reason','job','yoj','derog','delinq',
                 'clage','ninq','clno','debtinc']
    params = [request.form[var] for var in variables]
    response = predict(params)
    answer = ''
    if response == 1:
        return """
                We can not give you the loan, but we could give you some tips
                """
    else:
        return 'Congrats you are apt for the loan'
            
app.run("0.0.0.0", 5000, debug=True)