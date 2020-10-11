import pandas as pd
from os import walk
import glob
import csv


def exel2csv():
	files = glob.glob("..\..\..\Airlines\YourBoardingPassDotAero\*.xlsx")
	
	print(files)
	
	index = 0
	
	for i in files:
		read_file = pd.read_excel (i)
		strfile = str(index) + '.csv'
		read_file.to_csv (strfile, index = None, header=True)
		index += 1


def deleteCommas(line):
	lineout = []
	amountCommas = 0
	word = ''
	index_tmp = ''
	for i in line:
		if i == ',':
			lineout.append(word)
			word = ''
			index_tmp = i
		if i == '\n':
			lineout.append(word)
			break
		if index_tmp == i:
			continue
		else:
			word += i
			index_tmp = ''
	
	lineout2 = []
	for i in range(len(lineout)):
		if "Unnamed" in lineout[i] or lineout[i] == '':
			continue
		
		else:
			lineout2.append(lineout[i])
	return lineout2
		


dictList = []
dictInfoTicket = {'Id' : 0, 'SEQUENCE': 0, 'Sex' : '', 'First Name' : '', 'Last Name' : '',  'Y' : '', 'Flight' : '', 'Departure' : '', 'Arrival' : '', 'Gate' : 0, 'AirportIdD' : '',
					'AirportIdA' : '', 'Date' : '', 'Time' : '', 'OperatorInfo' : '', 'Info' : '', 'Seat' : '', 'PNR' : '', 'E-TICKET' : ''}


filesCSV = glob.glob("*.csv")
amount = 1

for file in filesCSV:
	with open(file) as csv_file:
		line1	= deleteCommas(csv_file.readline())
		line2	= deleteCommas(csv_file.readline())
		line3	= deleteCommas(csv_file.readline())
		line4	= deleteCommas(csv_file.readline())
		line5	= deleteCommas(csv_file.readline())
		line6	= deleteCommas(csv_file.readline())
		line7	= deleteCommas(csv_file.readline())
		line8	= deleteCommas(csv_file.readline())
		line9	= deleteCommas(csv_file.readline())
		line10	= deleteCommas(csv_file.readline())
		line11	= deleteCommas(csv_file.readline())
		line12	= deleteCommas(csv_file.readline())
		line13	= deleteCommas(csv_file.readline())
		line14	= deleteCommas(csv_file.readline())
		
		sqplace = 0
		for i in range(len(line1)):
			if "SEQUENCE" in line1[i]:
				sqplace = i
				break
			else:
				continue
	
		dictInfoTicket['SEQUENCE'] = line1[sqplace + 1]
		dictInfoTicket['Sex'] = line3[0]
		
		place2 = line3[1].find(' ')
		
		dictInfoTicket['Id'] = amount
		dictInfoTicket['First Name'] = line3[1][:place2]
		dictInfoTicket['Last Name'] = line3[1][place2 + 1:]
		dictInfoTicket['Y'] = line3[2]
		dictInfoTicket['Flight'] = line5[0]
		dictInfoTicket['Departure'] = line5[1]
		dictInfoTicket['Arrival'] = line5[2]
		if len(line7) == 4:
			dictInfoTicket['Gate'] = None
			dictInfoTicket['AirportIdD'] = line7[1]
			dictInfoTicket['AirportIdA'] = line7[3]
		if len(line7) == 5:
			dictInfoTicket['Gate'] = line7[1]
			dictInfoTicket['AirportIdD'] = line7[2]
			dictInfoTicket['AirportIdA'] = line7[4]
		
		
		dictInfoTicket['Date'] = line9[0]
		dictInfoTicket['Time'] = line9[2]
		dictInfoTicket['OperatorInfo'] = line9[3]
		if len(line11) == 2:
			dictInfoTicket['Info'] = line11[0]
			dictInfoTicket['Seat'] = None
		if len(line11) == 3:
			dictInfoTicket['Info'] = line11[0]
			dictInfoTicket['Seat'] = None
		dictInfoTicket['PNR'] = line13[1]
		dictInfoTicket['E-TICKET'] = line13[3]
	
		#print(dictInfoTicket)
	
	dictList.append(dictInfoTicket)
	dictInfoTicket = {'Id' : 0, 'SEQUENCE': 0, 'Sex' : '', 'First Name' : '', 'Last Name' : '',  'Y' : '', 'Flight' : '', 'Departure' : '', 'Arrival' : '', 'Gate' : 0, 'AirportIdD' : '',
						'AirportIdA' : '', 'Date' : '', 'Time' : '', 'OperatorInfo' : '', 'Info' : '', 'Seat' : '', 'PNR' : '', 'E-TICKET' : ''}
	amount += 1
	

with open('Tickets.txt', mode='w',  newline='') as tickets_file:
	fieldnames = ['Id', 'SEQUENCE', 'Sex', 'First Name', 'Last Name',  'Y', 'Flight', 'Departure', 'Arrival', 'Gate', 'AirportIdD',
					'AirportIdA', 'Date', 'Time', 'OperatorInfo', 'Info', 'Seat', 'PNR', 'E-TICKET']

	writer = csv.DictWriter(tickets_file, fieldnames=fieldnames, delimiter=';', quotechar='"')
	
	writer.writeheader()
	
	for i in dictList:
		writer.writerow(i)
	




