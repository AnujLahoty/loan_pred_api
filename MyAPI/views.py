from django.shortcuts import render
from . forms import ApprovalForm
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from django.core import serializers
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from . models import approvals
from . serializers import approvalsSerializers
import pickle
import joblib
import json
import numpy as np
from sklearn import preprocessing
import pandas as pd
import joblib
from django.contrib import messages
from keras import backend as K

# Create your views here.

@api_view(["POST"])
def api_req_pred(request):
	try:
		mydata=request.data
		mdl = joblib.load('MyAPI/loan_model.pkl')
		scalers = joblib.load('MyAPI/scalers.pkl')
		unit=np.array(list(mydata.values()))
		unit=unit.reshape(1,-1)
		X=scalers.transform(unit)
		y_pred=mdl.predict(X)
		y_pred=(y_pred>0.58)
		newdf=pd.DataFrame(y_pred, columns=['Status'])
		newdf=newdf.replace({True:'Approved', False:'Rejected'})
		print(newdf)
		loan_status = str(newdf['Status'][0])
		return Response('Your Status is {}'.format(loan_status))
	except ValueError as e:
		return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
    
def approveReject(df):
    try:
        dtest = df
        dtest.drop('csrfmiddlewaretoken', axis=1, inplace=True)
        dtest.drop('firstname', axis=1, inplace=True)
        dtest.drop('lastname', axis=1, inplace=True)
        print(dtest)
        mdl = joblib.load('MyAPI/loan_model.pkl')
        scalers = joblib.load('MyAPI/scalers.pkl')
        ml_model_ordered_features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
       'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
       'Loan_Amount_Term', 'Credit_History', 'Property_Area_Rural',
       'Property_Area_Semiurban', 'Property_Area_Urban']
        dtest['Gender'] = dtest['Gender'].map({'Female':0,'Male':1})
        dtest['Married'] = dtest['Married'].map({'No':0, 'Yes':1}).astype(np.int)
        dtest['Dependents'] = dtest['Dependents'].fillna( dtest['Dependents'].dropna().mode().values[0]).astype(np.int)
        dtest['Education'] = dtest['Education'].map({'Not Graduate':0, 'Graduate':1}).astype(np.int)
        dtest['Self_Employed'] = dtest['Self_Employed'].map({'No':0, 'Yes':1})
        dtest['Gender'] = dtest['Gender'].fillna( dtest['Gender'].dropna().mode().values[0]).astype(np.int)
        dtest['Self_Employed'] = dtest['Self_Employed'].fillna( dtest['Self_Employed'].dropna().mode().values[0])
        dtest['LoanAmount'] = dtest['LoanAmount'].fillna( dtest['LoanAmount'].dropna().mode().values[0])
        dtest['Loan_Amount_Term'] = dtest['Loan_Amount_Term'].fillna( dtest['Loan_Amount_Term'].dropna().mode().values[0])
        dtest['Credit_History'] = dtest['Credit_History'].fillna( dtest['Credit_History'].dropna().mode().values[0])
        dtest['ApplicantIncome'] = dtest['ApplicantIncome'].astype(np.int)
        dtest['CoapplicantIncome'] = dtest['CoapplicantIncome'].astype(np.int)
        dtest['LoanAmount'] = dtest['LoanAmount'].astype(np.int)
        dtest['Loan_Amount_Term'] = dtest['Loan_Amount_Term'].astype(np.int)
        dtest['Credit_History'] = dtest['Credit_History'].astype(np.int)
        
        columns_after_dummies = ['Property_Area_Rural', 'Property_Area_Semiurban', 'Property_Area_Urban']
        X = pd.get_dummies(dtest)
        for i in columns_after_dummies:
            if i in X:
                pass
            else:
                X[i] = 0
        X = X[ml_model_ordered_features]
        print(X.columns)
        print(len(X.columns))
        print(X.head())
        X = scalers.transform(X)
        print("Input data to model", X)
        y_pred = mdl.predict(X)
        print("Model's predicted prob", y_pred)
        y_pred = (y_pred>0.1)
        new_df = pd.DataFrame(y_pred, columns=['Status'])
        print(new_df)
        new_df = new_df.replace({True: 'Approved', False: 'Rejected'})
        K.clear_session()
        return (new_df.values[0][0])
    except (TypeError,ValueError) as e:
        return (e.args)

def cxcontact(request):
    if request.method =='POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            print("Form is valid!")
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            Dependents = form.cleaned_data['Dependents']
            ApplicantIncome = form.cleaned_data['ApplicantIncome']
            CoapplicantIncome = form.cleaned_data['CoapplicantIncome']
            LoanAmount = form.cleaned_data['LoanAmount']
            Loan_Amount_Term = form.cleaned_data['Loan_Amount_Term']
            Credit_History = form.cleaned_data['Credit_History']
            Gender = form.cleaned_data['Gender']
            Married = form.cleaned_data['Married']
            Education = form.cleaned_data['Education']
            Self_Employed = form.cleaned_data['Self_Employed']
            Property_Area = form.cleaned_data['Property_Area']
            myDict = (request.POST).dict()
            df = pd.DataFrame(myDict, index=[0])
            answer = approveReject(df)
            print(answer)
            if int(df['LoanAmount']) < 25000:
                messages.success(request, 'Application Status: {}'.format(answer))
            else:
                messages.success(request, 'Invalid: Your Loan Amount Exceeds $25000 Limit')

    form = ApprovalForm()

    return render(request, 'myform/cxform.html', {'form': form})