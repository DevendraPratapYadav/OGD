import json
import MySQLdb as SQL
import nnr as NNR
import findCorr as FCOR
import itertools

from flask import Flask, render_template, redirect, url_for, request
from flask import make_response
from flask_cors import CORS
from collections import OrderedDict

#print list vertically
def printV(lst):
    for x in lst:
        print x;

app = Flask(__name__)
CORS(app)

# @app.after_request
# def add_headers(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   return response

@app.route("/")
def home():
	return "Hello World"

@app.route("/index")
def base():
	return "Greetings Wanderer !!!"

@app.route('/login',methods=['GET','POST'])
def login():
	message = None

	if request.method == 'POST':
		datafromjs = request.form['mydata']

		jsonObj = {'result' : "Python Connected"}

		resp = make_response( json.dumps(jsonObj) )
		resp.headers['Content-Type'] = "application/json"
		return resp

	return render_template('login.html',message='')

@app.route('/getTableNames',methods=['POST'])
def getTableNames():
	print "___________________________________________________"
	
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd');
	cursor = db.cursor();
	metaDataset = "Datasets";
	cursor.execute("select Name from "+"`"+metaDataset+"`");
	numrows = int(cursor.rowcount);
	table = [];

	for i in range(numrows):
		row = cursor.fetchone();
		if row :
			table.append(row);
	
	print table;
	
	results = {"result":table};
	
	json_results = json.dumps(results)
	resp = make_response(json.dumps(json_results))
	resp.headers['Content-Type'] = "application/json"
	cursor.close();
	
	return resp;

@app.route('/loadTable',methods=['POST'])
def loadTable():
	datasetName = request.json["input"];
	# request.form['dataFromJs'];
	# Connect to the MySQL database
	# print "*****************************";
	# print dataFromJS;
	# print "*****************************";

	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd')
	
	cursCol = db.cursor();
	cursCol.execute("SHOW columns FROM `" + datasetName + "`")
	colNames = [column[0] for column in cursCol.fetchall()]
	strColNames = "";
	for i in xrange(0,len(colNames)):
		if i < len(colNames)-1:
			strColNames+=colNames[i]+"|";
		else:
			strColNames+=colNames[i];
	cursCol.close();
	
	# Creation of a cursora
	cursor = db.cursor()

	# Execution of a SQL statement
	cursor.execute("select * from `"+datasetName+"`")

	# Get the total number of rows
	numrows = int(cursor.rowcount)

	table = []
	# table = [i[0] for i in cursor.description]

	# Get and display the rows one at a time
	for i in range(numrows):
		row = cursor.fetchone()
		if row:
			table.append(row)
	cursor.close();

	filename = "data.txt"

	# Write all data to a file
	file_descriptor = open(filename, "w")

	# Converts Table to String
	text_data = convert_table_to_text(table, '\n', '|')

	cursor2 = db.cursor();
	cursor2.execute("select * from `"+datasetName+"`");
	desc = cursor2.description;
	print desc;
	results = [OrderedDict(itertools.izip([col[0] for col in desc], row)) for row in cursor2.fetchall()]

	print results;

	cursor3 = db.cursor();
	commd = "SELECT table_comment FROM information_schema.tables WHERE table_name = '"+datasetName+"'";
	print commd;
	cursor3.execute(commd);
	desc3 = cursor3.description;
	results3 = [dict(itertools.izip([col[0] for col in desc3], row)) for row in cursor3.fetchall()]
	comment = results3[0]['table_comment'];

	# text_data = comment[1:-1] +"\n"+ text_data;
	comment = comment.replace(" ", "|")
	text_data = strColNames +"\n"+ comment[1:-1] +"\n"+ text_data;

	file_descriptor.write(text_data)
	file_descriptor.close()

	json_results = json.dumps(results)
	resp = make_response(json.dumps(json_results))
	resp.headers['Content-Type'] = "application/json"
	# response = Flask.jsonify({'result': json_results})
	# response.headers.add('Access-Control-Allow-Origin', '*')
	# return resp

	# applyML(table)
	return resp

@app.route('/getUserData',methods=['POST'])
def getUserData():
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd');
	cursor = db.cursor();
	tableName = "User History";
	userId = request.json["input"];
	query = "select * from " + "`" + tableName + "` " + "where ID = '" + userId+"'";
	print query;
	cursor.execute(query);
	numrows = int(cursor.rowcount);
	table = [];
	
	for i in range(numrows):
		row = cursor.fetchone();
		if row:
			table.append(row);
	
	print table;
	
	results = {"result": table};
	
	json_results = json.dumps(results)
	resp = make_response(json.dumps(json_results))
	resp.headers['Content-Type'] = "application/json"
	cursor.close();
	
	return resp;

@app.route('/saveUserData',methods=['POST'])
def saveUserData():
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd');
	cursor = db.cursor();
	tableName = "User History";
	userData = json.dumps(request.json["input"]);
	userId = request.json["id"];
	
	cursor.execute("INSERT INTO " + "`" + tableName + "`" + " VALUES (NULL, %s, NULL, %s)", (userId, str(userData)))

	numrows = int(cursor.rowcount);
	table = [];
	
	for i in range(numrows):
		row = cursor.fetchone();
		if row:
			table.append(row);
	
	print table;
	
	results = {"result": table};
	
	json_results = json.dumps(results)
	resp = make_response(json.dumps(json_results))
	resp.headers['Content-Type'] = "application/json"
	db.commit();
	cursor.close();
	
	return resp;

@app.route('/runMLComponentFromHistory',methods=['POST'])
def runMLComponentFromHistory():
	print request.json["input"];
	sessionData = json.loads(request.json["input"][3])
	print "sessionData";
	print sessionData;
	datasetName = sessionData[1];
	
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd')
	
	cursCol = db.cursor();
	cursCol.execute("SHOW columns FROM `" + datasetName + "`")
	colNames = [column[0] for column in cursCol.fetchall()]
	strColNames = "";
	for i in xrange(0,len(colNames)):
		if i < len(colNames)-1:
			strColNames+=colNames[i]+"|";
		else:
			strColNames+=colNames[i];
	cursCol.close();
	
	cursor = db.cursor()
	
	# Execution of a SQL statement
	cursor.execute("select * from `" + datasetName + "`")
	
	# Get the total number of rows
	numrows = int(cursor.rowcount)
	
	table = []
	
	for i in range(numrows):
		row = cursor.fetchone()
		if row:
			table.append(row)
	cursor.close();
	
	filename = "data_history.txt"
	
	# Write all data to a file
	file_descriptor = open(filename, "w")
	
	# Converts Table to String
	text_data = convert_table_to_text(table, '\n', '|')
	
	cursor2 = db.cursor();
	cursor2.execute("select * from `" + datasetName + "`");
	desc = cursor2.description;
	print desc;
	results = [OrderedDict(itertools.izip([col[0] for col in desc], row)) for row in cursor2.fetchall()]
	
	print results;
	
	cursor3 = db.cursor();
	commd = "SELECT table_comment FROM information_schema.tables WHERE table_name = '" + datasetName + "'";
	print commd;
	cursor3.execute(commd);
	desc3 = cursor3.description;
	results3 = [dict(itertools.izip([col[0] for col in desc3], row)) for row in cursor3.fetchall()]
	comment = results3[0]['table_comment'];
	
	comment = comment.replace(" ", "|")
	text_data = strColNames +"\n"+ comment[1:-1] + "\n" + text_data;
	file_descriptor.write(text_data)
	file_descriptor.close()
	
	rec_data = sessionData[2]
	# print rec_data[2]
	
	inp = map(int, rec_data[0])
	out = map(int, rec_data[1])
	
	param = [map(int, x) for x in sessionData[3]];
	
	print "**********************************\n"
	print inp
	print out
	print param
	print "**********************************\n"
	# response = NNR.apply_regression('data.txt')
	
	result = NNR.apply_regression('data_history.txt', inp, out, param);
	
	print result;
	
	print "***************";
	
	str_arr = [];
	str_iar = [];
	
	for i in xrange(0, len(result)):
		str_iar = [];
		for j in xrange(0, len(result[i])):
			str_iar.append(str(result[i][j]));
		str_arr.append(str_iar);
	
	printV(str_arr);
	
	print "***************"
	jsonObj = {'result': str_arr}
	resp = make_response(json.dumps(jsonObj))
	resp.headers['Content-Type'] = "application/json"
	return resp

@app.route('/runCorrComponent',methods=['GET','POST'])
def runCorrComponent():
	colSelection = request.json["input"];
	print colSelection;
	result = FCOR.findCorrelation('data.txt', colSelection[0], colSelection[1])
	
	print "***************"
	jsonObj = {'result': [0,1,2]}
	resp = make_response(json.dumps(jsonObj))
	resp.headers['Content-Type'] = "application/json"
	return resp

@app.route('/runMLComponent',methods=['GET','POST'])
def mlCompoenent():
	rec_data = request.json['input']
	# print rec_data[2]

	inp = map(int,rec_data[0])
	out = map(int,rec_data[1])

	param = [ map(int,x) for x in rec_data[2]];

	print "**********************************\n"
	print inp
	print out
	print param
	print "**********************************\n"
	# response = NNR.apply_regression('data.txt')

	result = NNR.apply_regression('data.txt',inp,out,param);
	
	print result;
	
	print "***************";
	
	str_arr = [];
	str_iar = [];

	for i in xrange(0,len(result)):
		str_iar = [];
		for j in xrange(0,len(result[i])):
			str_iar.append(str(result[i][j]));
		str_arr.append(str_iar);

	printV(str_arr);

	print "***************"
	jsonObj = {'result': str_arr}
	resp = make_response(json.dumps(jsonObj))
	resp.headers['Content-Type'] = "application/json"
	return resp

def convert_table_to_text(table,row_sep,col_sep):

	text_data = ""

	for (i, row) in enumerate(table):
		for (j, value) in enumerate(row):
			if j == len(row)-1:
				text_data += str(value)
			else:
				text_data += str(value) + col_sep
	
		text_data += row_sep

	return text_data


if __name__ == "__main__":
	app.run(debug=False)