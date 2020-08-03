# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 20:11:18 2020

@author: MEI
"""
import json
import threading
import requests
import pandas as pd
import jinja2
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from summerproject import amazon
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
from flask import Flask, jsonify,request,send_file,render_template,make_response,redirect,url_for,Blueprint


engine = ()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PERMANENT_SESSION_LIFETIME']=10  
db = SQLAlchemy(app)   



@app.route("/compare",methods=['get','POST'])
def compare():
     return render_template('compare.html')

@app.route("/",methods=['get','POST'])
def index():
     return render_template('compare.html')

 
 
@app.route("/up",methods=['get','POST'])#receive upload file and insert the data to database
def up():
     f = request.files['file']
     f1=pd.read_csv(f)        
     f1.to_sql( "productlist", engine, if_exists='replace')
     return '{"code": 0 }'
     
    
@app.route("/products",methods=['get','POST'])# return the products detail as json format
def products():   
    #df=pd.read_csv('c:/AWAD/sample.csv')
    #print(request.values.get("page"))
    page = int(request.values.get("page"))-1
    start=page*10
    
    
    
    df=pd.read_sql('select * from productlist limit %i,10'%(start),engine)
    #df=df.head(5)
    df=df.to_json(orient='records')
    df=json.loads(df)
   
    
    result={"code":0,"msg":"","count":1000,"data":df}
    result=json.dumps(result)
    return  result

@app.route("/productslist",methods=['get','POST'])#return products name in order to display them in the ComboBox
def productslist():   

    df=pd.read_sql('select * from productlist',engine)
    
    df['text']=list(df['SupplierProductCode'])
    df['id']=list(df['SupplierProductCode'])
    del df['GPHProductCode']
    del df['SupplierProductCode']
    del df['BarCode']
    del df['Description']
    del df['GPH_RRP']
    #df=df.head(5)
    df=df.to_json(orient='records')
    return  df
    

@app.route('/price/<item>')    
def price(item):
    
    price1=amazon(item)
    return price1


@app.route('/data.json',methods=['get','POST'])    
def data():
   
    result=[{'Mancode':'P-44046','GHPCode':'MAK19006','Description':'MAKITA DRILL & BIT SET 216PC','price':'29.99','price1':'53.95','price2':'28.95','price3':'29.99'}]
    result=json.dumps(result)
    return result


@app.route('/data.json1/<item>',methods=['get','POST'])    #return price of product in special format
def data1(item):
    try:
    #item='A-85771'
        data=pd.read_sql('''select Description,GPH_RRP from table_name where SupplierProductCode='%s' '''%(item),engine)
        Description=str(data['Description'][0])
        GPH_RRP=str(data['GPH_RRP'][0])
        a=amazon(item,Description)
        print(a)
        if float(GPH_RRP)>float(a[0][1:]):
            
            col1='green'
        else:
            col1='red'
                         
        result=[{'Mancode':item,'GHPCode':item,'Description':Description,'price':GPH_RRP,'price1':a[0],'col1':col1,'link1':a[1],}]
        result=json.dumps(result)
        return result
    except:
         
        result=[{'Mancode':item,'GHPCode':item,'Description':Description,'price':GPH_RRP,'price1':'Null','link1':'Null',}]
        result=json.dumps(result)
        return result

 
@app.route('/data.json000/<item>',methods=['get','POST'])  #to overcome block from amazon
def t(item):
    #item='A-85771'
    aaa=requests.get('http://39.106.15.45/data.json1/{}'.format(item))
    contents=aaa.text
    
    return contents


@app.route('/upload',methods=['get','POST'])    
def upload():
    
     return render_template('upload.html')
 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('upload.html'), 404

@app.errorhandler(500)
def internal_error(error):

    return render_template('compare.html'), 500    
    
    
     

if __name__ == '__main__':
    #app.run(host='127.0.0.1',port=9000,debug=True,threaded=True)#参数
    app.run(host='0.0.0.0',port=8080,threaded=True)


