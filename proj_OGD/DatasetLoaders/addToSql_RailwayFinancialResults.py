import xlrd
import MySQLdb as SQL
import readFromCSV as rfc

def save_to_database(table,datasetPath,datasetName,datasetExtension,columnDataTypes):
	# Connect to the MySQL database
	db = SQL.connect(host='localhost', user='root', passwd='', db='ogd')

	# Creation of a cursor
	cursor = db.cursor()

	# Execution of a SQL statement
	# cursor.execute("select * from mortality")
	createCommand = "CREATE TABLE " +"`"+datasetName+"`"+"( Entry int NOT NULL AUTO_INCREMENT PRIMARY KEY,";

	for i in xrange(0,len(columnDataTypes)):
		createCommand += "`"+table[0][i]+"`"+" "+columnDataTypes[i]+" ,";
	createCommand = createCommand[0:-1] + ")";

	print createCommand

	# cursor.execute("CREATE TABLE Annual_Survey_Of_Datasets( year varchar(255) NOT NULL PRIMARY KEY, rate varchar(255) )");
	cursor.execute(createCommand);

	for i in xrange(1,len(table)):
		insertCommand = "";
		insertCommand = "insert into "+"`"+datasetName+"`"+" values(NULL,";

		for j in range(0,len(table[i])):
			if str(table[i][j])!= 'NA':
				insertCommand += str(table[i][j])+","
			else:
				insertCommand += "NULL"+","
		insertCommand = insertCommand[0:-1]+")";

		print insertCommand;
		cursor.execute(insertCommand);
		# cursor.execute("insert into "+datasetName+"values"+"(\"%s\", \"%s\")" % (table[i][0], table[i][1]))
		db.commit();

def printV(data):
	for x in data:
		print x;

def exportFromExcel(filename):
	book = xlrd.open_workbook(filename);
	sheet = book.sheet_by_name(filename.split('.')[0]);
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

	for i in xrange(1, len(data)):
		data[i][0] = float(data[i][0].split("-")[0]);

	data[0][0] = 'YEAR';

	return data;

datasetPath = "C:\Users\SnehilAmeta\PycharmProjects\proj_OGD\Datasets\RailwayFinancialResults_inCrores.csv";
datasetName = "RailwayFinancialResults_inCrores";
datasetExtension = ".csv";

data = rfc.load_all(datasetPath);
data = data.transpose();

for i in xrange(1,len(data)):
	data[i][0] = data[i][0].split("-")[0];

# data[0][0] = "Year";
printV(data);

columnDataTypes = [];

for i in xrange(0,len(data[0])):
	columnDataTypes.append("double(50,5)");

save_to_database(data,datasetPath,datasetName,datasetExtension,columnDataTypes);