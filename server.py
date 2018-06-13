import os
# try:
#   from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
#   from SocketServer import TCPServer as Server
# except ImportError:
#   from http.server import SimpleHTTPRequestHandler as Handler
#   from http.server import HTTPServer as Server
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
import time
import random



# httpd = Server(("", PORT), Handler)
# try:
#   print("Start serving at port %i" % PORT)
#   httpd.serve_forever()
# except KeyboardInterrupt:
#   pass
app = Flask(__name__,template_folder="static")

#########################################################################################################################
@app.route('/')
def home():
   return render_template('index.html')
#=======================================================================================================================#

@app.route('/createtable', methods=['POST'])
def createtable():
   conn = sql.connect('Assign3.db')
   csvf = pd.read_csv("all_month.csv",encoding = "ISO-8859-1")
   start_time = time.time()
   csvf[['date', 'time']] = csvf['time'].str.split('T', expand=True)
   csvf['time'] = csvf['time'].str.split('.').str[0]
   csvf.to_sql('Earthquake3', conn, if_exists='replace', index=False)
   msg="Table created successfully"
   end_time = time.time()
   time_diff = end_time - start_time
   print(csvf)
   return render_template('index.html',msg=msg,timediff=time_diff)

#=======================================================================================================================#

@app.route('/Magnitude', methods=['POST'])
def Magnitude():
    Magnitude = request.form['Region']
    con = sql.connect("Assign3.db")
    start_time = time.time()
    con.row_factory = sql.Row
    cur = con.cursor()
    # cur.execute('SELECT REGION,DIVISION,STATE,STNAME,POPESTIMATE2001 FROM Census where REGION = ?', (Region,))
    cur.execute('SELECT Date,mag FROM EarthQuake3 where mag > ?', (Magnitude,))
    rows = cur.fetchall()
    end_time = time.time()
    time_diff = end_time - start_time
    count = 0
    for row in rows:
        count = count + 1
        # magnitude.append("mag:" + row[0])

    return render_template('index.html', counter=count, rows=rows,timediff=time_diff)
#=======================================================================================================================#
@app.route('/random', methods=['POST'])
def randomFunc():
    magnitude = []
    count = request.form['count']
    # magnituderange = float(magnituderange)
    con = sql.connect("Assign3.db")
    start_time = time.time()
    con.row_factory = sql.Row
    cur = con.cursor()

    start_time = time.time()
    for i in range(1, int(count) + 1):
        rand = random.randrange(0, 100)
        mag = int(rand)
        cur.execute('SELECT place FROM Earthquake3 where depth>= ?',(mag,))
    end_time = time.time()
    time_diff = end_time - start_time
    magdata = cur.fetchall()

    count = 0
    for row in magdata:
        count = count + 1
        magnitude.append("Place:" + row[0])
    return render_template('index.html', countr2=count, resu2=magnitude, totaltimer=time_diff)

# httpd = Server(("", PORT), Handler)
# try:
#   print("Start serving at port %i" % PORT)
#   httpd.serve_forever()
# except KeyboardInterrupt:
#   pass
PORT = int(os.getenv('PORT', 5000))
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=int(PORT))
	# app.run(debug = True)
# httpd.server_close()