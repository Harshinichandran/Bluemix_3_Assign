import os
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
# import memcache
# import pickle as cPickle
import random
import redis

app = Flask(__name__,template_folder="static")
# memc = memcache.Client(['127.0.0.1:11211'])
R_SERVER=redis.StrictRedis(host="localhost",port=6379)
#########################################################################################################################
@app.route('/')
def home():
   return render_template('index.html')
#=======================================================================================================================#

@app.route('/createtable', methods=['POST'])
def createtable():
   conn = sql.connect('Assign3.db')
   csvf = pd.read_csv("equake.csv",encoding = "ISO-8859-1")
   start_time = time.time()
   csvf[['date', 'time']] = csvf['time'].str.split('T', expand=True)
   csvf['time'] = csvf['time'].str.split('.').str[0]
   # R_SERVER.set("key", csvf.to_msgpack(compress='zlib'))
   csvf.to_sql('Earthquake3', conn, if_exists='replace', index=False)
   msg="Table created successfully"
   end_time = time.time()
   time_diff = end_time - start_time
   print(csvf)
   return render_template('index.html',msg=msg,timediff=time_diff)


#=======================================================================================================================#
#
@app.route('/Magnitude', methods=['POST'])
def Magnitude():

    #====================================================================================
    con = sql.connect("Assign3.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    print(R_SERVER)
    result = R_SERVER.get("key")
    # result=result.decode('utf-8')
    print(result)
    print("I am before if")
    if not result:
        cur.execute('SELECT mag FROM EarthQuake3 where mag > ?', (request.form.get('magnitude'),))
        result = cur.fetchall()
        print("I am inside if")
        print(result)
        print('Went inside...')
        key="key"
        R_SERVER.set(key,result)

    return render_template('index.html', rows=result)

#
#
# #=======================================================================================================================#
@app.route('/random', methods=['POST'])
def randomFunc():
    magnitude = []
    count = request.form['count']
    # magnituderange = float(magnituderange)
    con = sql.connect("Assign3.db")
    start_time = time.time()
    con.row_factory = sql.Row
    cur = con.cursor()
    for i in range(1, int(count) + 1):
        rand = random.randrange(0, 100)
        mag = int(rand)
        cur.execute('SELECT locationSource FROM Earthquake3 where depth>= ?',(mag,))
        magdata = cur.fetchall()
    end_time = time.time()
    time_diff = end_time - start_time


    count = 0
    for row in magdata:
        count = count + 1
        magnitude.append("LocationSource:" + row[0])
    return render_template('index.html', counter2=count, result2=magnitude, totaltimer=time_diff)

#=======================================================================================================================#
@app.route('/rdis', methods=['POST'])
def rdis():

        return render_template('index.html')
#========================================================================================================================#


PORT = int(os.getenv('PORT', '8080'))
if __name__ == '__main__':
    app.run(debug = True, port=int(PORT))