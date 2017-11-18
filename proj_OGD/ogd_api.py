import requests
import MySQLdb as SQL

def write_whole_txt(req_data):
	f = open("data_whole.txt", "w")

	for i in range(len(req_data)):
		if i == 0:
			for j in req_data[i].keys():
				f.write(j)
				f.write("    ")
			f.write("\n")
		for j in req_data[i].keys():
			f.write(req_data[i][j])
			f.write("    ")
		f.write("\n")

def write_relevant_txt(table):
	f = open("data.txt", "w")

	for i in range(len(table)):
		f.write(str(table[i][0])+'\t'+table[i][1])
		if i != len(table)-1:
			f.write('\n')

def load_dataset():
	URL = "https://api.data.gov.in/resource/2f58bb45-5855-4c48-97cc-16904c0036df?format=json&api-key=579b464db66ec23bdd0000012788980d190e4b9143557a20ef9998d9"
	PARAMS = {'limit': 1000}

	r = requests.get(url=URL, params=PARAMS)

	data = r.json()

	req_data = data['records']

	# write_to_txt(req_data)

	col_1 = []
	col_2 = []

	for i in req_data[0].keys():
		col_1.append(i)
	for i in req_data[1].values():
		col_2.append(i)

	table = []

	for i in range(len(col_1)):
		if i!= 2 and i < 20:
			table.append([str(col_1[i])[1:],str(col_2[i]) ] )

	write_whole_txt(req_data)
	write_relevant_txt(table)

	# save_to_database(table)

def save_to_database(table):
	# Connect to the MySQL database
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd')

	# Creation of a cursor
	cursor = db.cursor()

	# Execution of a SQL statement
	# cursor.execute("select * from mortality")
	# cursor.execute("CREATE TABLE imortality( year varchar(255) NOT NULL PRIMARY KEY, rate varchar(255) )");

	for i in range(len(table)):
		print ("insert into imortality values (\"%s\", \"%s\")" % (table[i][0], table[i][1]))
		cursor.execute("insert into imortality values (\"%s\", \"%s\")" % (table[i][0], table[i][1]))

	db.commit()

load_dataset()