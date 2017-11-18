import xlrd
import readFromCSV as rfc

def printV(data):
    for x in data:
        print x;

def exportFunctionFromExcel(filename):
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_name(filename.split('.')[0])
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]

    for i in xrange(1,len(data)):
        data[i][0] = float(data[i][0].split("-")[0]);

    data[0][0] = 'YEAR';
    return data;

def exportFromCSV(filename):
   data = rfc.load_all(filename);
