# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 00:43:56 2020

@author: MEI
"""

import urllib
import re   
from bs4 import BeautifulSoup  
from distutils.filelist import findall  
import pandas as pd
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Connection': 'keep-alive',
    'cookie':'session-id=261-2473042-2808111; x-wl-uid=1njcCicPXIWr8rHydIJmX7x/0xd/I6M/11uV5RZaOx4GF5tCfke7Mtigfp5arDPwhYyNnSmY6lX8=; ubid-acbuk=261-1769644-8565630; i18n-prefs=GBP; session-token=hQkHQgqOjm/alyAZi83gvuq03ERWD+UmLmZv1BhISbrqRcrIwFdby+1KVTHxQicQdnezpK9A3rIt5zmRn+5iMhYjPuD4BaQgqqc/V1LQFTJfp8Iaqi5NIl59OQI5o4Rz42W5QtInNLoXdodMQl7UpX6+fNDzqJ3boCJyY+xc3GQSlgDq2jDLxToyrKDbhW8F; session-id-time=2082758401l; csm-hit=adb:adblk_no&t:1594156358910&tb:4PBGCATE5HSJKZEWSPP9+s-V7QMSYNHCBHBWN2PZRMJ|1594156358908'
    
}



def amazon(barcode,description):    #get price from amazon
    try:
        #barcode='DFR550Z'
        
        #req = urllib.request.Request('https://www.amazon.co.uk/s?k={}'.format(barcode))
        aaa=requests.get('https://www.amazon.co.uk/s?k={}'.format(barcode),headers=headers)
        #page = urllib.request.urlopen(req)     
        #contents = page.read() 

        contents=aaa.text   
        soup = BeautifulSoup(contents, 'html5lib')  
        #lxml  
        price = soup.find_all("span",{"class":"a-offscreen"})
        text =soup.find_all("span",{"class":"a-size-medium a-color-base a-text-normal"})
     
        for x,y in zip(text,price):
            if fuzz.token_set_ratio(x,description)>40:# fuzzy matching products
                return [y.get_text(),'https://www.amazon.co.uk/s?k={}'.format(barcode)]

       
        return None
    except:
        return None
     
#amazon('P-65919','5555')    

'''
def toolstation(barcode):    
    try:
        page = urllib.request.urlopen('https://www.toolstation.com/search?q={}'.format(barcode))      
        contents = page.read()     
        soup = BeautifulSoup(contents, 'html.parser')     
        span = soup.find_all("span",{"class": "sp-price f-medium notranslate"})
        return span[0].get_text()
    except:
        return 'Null'
    
toolstation('PTC20%20-%20MAKITA%20%20CIRCULAR%20SAW%20CORDLESS%20136MM%2018V%20LI-ION%20-%20BODY%20ONLY') 


'''
def screwfix(barcode):    #get price from screwfix
    #barcode='PTC20+-+MAKITA+RECIPROCATING'
    try:
        page = urllib.request.urlopen('https://www.screwfix.com/search?search={}'.format(barcode))      
        contents = page.read()     
        soup = BeautifulSoup(contents, 'html.parser')     
        span = soup.find_all(id="product_list_price_1")
        return span[0].get_text()
    except:
        return 'Null'



def diy(barcode):    
    barcode='MAKITA+DOUBLE+TORSON+BIT+PZ2'
    try:
        page = urllib.request.urlopen('https://www.diy.com/search?term={}'.format(barcode))      
        contents = page.read()     
        soup = BeautifulSoup(contents, 'html.parser')     
        span = soup.find_all("div",{"class": "_9fa73251 _34fa7e6a e5c240b1 _98551c89"})
        return span[0].get_text()
    except:
        return 'Null'


total=[]

def price(barcode):
    pricelist=[]
    a=amazon(barcode)
    
    pricelist.append(a)
    #pricelist.append(b)
    #pricelist.append(c)
    total.append(pricelist)
    return pricelist

#d=price('DHP482RTWJ')

#file=pd.read_csv('C:/AWAD/sample.csv')
a=0
'''
for i in file['SupplierProductCode']:
    print (a)
    p=price(i)
    print(p)
    
    a=a+1
    
ccc=pd.DataFrame(total)    
ddd=ccc[0]
'''


if __name__ == '__main__':    
    main()
    

  


    
    
    