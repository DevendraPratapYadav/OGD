import json
import MySQLdb as SQL
import nnr as NNR
import itertools

from flask import Flask, render_template, redirect, url_for, request
from flask import make_response
from flask_cors import CORS
from collections import OrderedDict

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

@app.route('/loadTable',methods=['POST'])
def loadTable():

    datasetName = request.json["input"];
    # request.form['dataFromJs'];
    # Connect to the MySQL database
    # print "*****************************";
    # print dataFromJS;
    # print "*****************************";

    db = SQL.connect(host='localhost', user='root', passwd='', db='ogd')

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
    text_data = convert_table_to_text(table, '\n', '\t')

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

    text_data = comment[1:-1] +"\n"+text_data;
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

    str_result = "<br>";

    for x in result:
        str_result+= "<br>"+str(map(int,x));

    print "***************"
    jsonObj = {'result': str_result}
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

# @app.route('/applyML',methods=['GET','POST'])
# def applyML(table):
#
#     # filename = "data.txt"
# 	#
#     # #Write all data to a file
#     # file_descriptor = open(filename, "w")
# 	#
#     # #Converts Table to String
#     # text_data = convert_table_to_text(table,'\n','\t')
# 	#
#     # file_descriptor.write(text_data)
#     # file_descriptor.close()
#
#     #Apply Regression on the data in file
#     response = NNR.apply_regression(filename)
#
#     return response

if __name__ == "__main__":
    app.run(debug=False)