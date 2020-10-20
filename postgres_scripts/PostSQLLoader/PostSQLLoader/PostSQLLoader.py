import postgresql
import postgresql.driver as pg_driver
import psycopg2
import requests, json
from transliterate import translit, get_available_language_codes
import cyrtranslit
from datetime import date


import sys

handleSettings = open("Settings.txt")
Settings = handleSettings.readline()[:-1]
path = handleSettings.readline()[:-1]
db = postgresql.open(Settings)

def create_tables_copy_data(db_in, path_in):

	path = path_in
	
	scr1 = """
	create table "AirlinesData"
	(
		uid varchar(9) not null,
		first_name varchar(25) not null,
		last_name varchar(25) not null,
		cards_type varchar(8) not null,
		card_number varchar(12),
		bonus_program varchar(30),
		activities_type varchar(8),
		activity_type varchar(6),
		code varchar(10),
		date date,
		departure varchar(3),
		arrival varchar(3),
		fare varchar(6)
	);
	
	COPY "AirlinesData"(uid, first_name, last_name, cards_type, card_number, bonus_program, activities_type, activity_type, code, date, departure, arrival, fare)
	FROM '{}PointzAggregator-AirlinesData.csv'
	DELIMITER ';'
	CSV HEADER;
	""".format(path)
	
	scr2 = """
	CREATE TABLE public."BoardingData"
	(
	    first_name VARCHAR(30) NULL,
	    second_name VARCHAR(30) NULL,
	    last_name VARCHAR(30) NULL,
	    sex VARCHAR(30) NULL,
	    birth_date VARCHAR(30) NULL,
	    passenger_document VARCHAR(30) NULL,
	    booking_code VARCHAR(30) NULL,
	    ticket_number VARCHAR(30) NULL,
	    baggage VARCHAR(30) NULL,
	    dep_date DATE NULL,
	    dep_time TIME NULL,
	    flight_number VARCHAR(30) NULL,
	    codesh VARCHAR(30) NULL,
	    dest_city VARCHAR(30) NULL
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."BoardingData"
	    OWNER to postgres;
	COPY "BoardingData"(first_name, second_name, last_name, sex, birth_date, passenger_document, booking_code, ticket_number, baggage, dep_date, dep_time, flight_number, codesh, dest_city)
	FROM '{}BoardingData.csv'
	DELIMITER ';'
	CSV HEADER;
	""".format(path)
	
	
	scr3 = """
	CREATE TABLE public."ForumPersonalInformation" (
		person_id INTEGER NOT NULL,
		nickname VARCHAR(30) NULL,
		passenger_document VARCHAR(30) NULL,
		sex VARCHAR(30) NULL,
		first_name VARCHAR(30) NULL,
		last_name VARCHAR(30) NULL,
		PRIMARY KEY (person_id)
	
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."ForumPersonalInformation"
	    OWNER to postgres;
	
	COPY "ForumPersonalInformation"(person_id, nickname, passenger_document, sex, first_name, last_name)
	FROM '{}PersonalInformation.csv'
	DELIMITER ';'
	CSV HEADER;
	
	
	
	CREATE TABLE public."ForumAirport" (
		airport_id INTEGER NOT NULL,
		name VARCHAR(30) NULL,
		abbr VARCHAR(30) NULL,
		country VARCHAR(30) NULL,
		PRIMARY KEY (airport_id)
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."ForumAirport"
	    OWNER to postgres;
	
	COPY "ForumAirport"(airport_id, name, abbr, country)
	FROM '{}airports.csv'
	DELIMITER ';'
	CSV HEADER;
	
	
	CREATE TABLE public."ForumPersonalIdLoyalty" (
		person_id INTEGER NOT NULL,
		type VARCHAR(30) NULL,
		abbr VARCHAR(30) NULL,
		loyality_id INTEGER NULL,
		CONSTRAINT fk_person_id
		 FOREIGN KEY (person_id)
		 REFERENCES public."ForumPersonalInformation"(person_id)
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."ForumPersonalIdLoyalty"
	    OWNER to postgres;
	
	COPY "ForumPersonalIdLoyalty"(person_id, type, abbr, loyality_id)
	FROM '{}PersonalIdLoyalty.csv'
	DELIMITER ';'
	CSV HEADER;
	
	CREATE TABLE public."ForumPersonIdInfoFlight" (
		person_id INTEGER NOT NULL,
		date DATE NULL,
		codesh VARCHAR(30) NULL,
		flight_number VARCHAR(30) NULL,
		CONSTRAINT fk_person_id
		 FOREIGN KEY (person_id)
		 REFERENCES public."ForumPersonalInformation"(person_id)
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."ForumPersonIdInfoFlight"
	    OWNER to postgres;
	
	COPY "ForumPersonIdInfoFlight"(person_id, date, codesh, flight_number)
	FROM '{}PersonIdInfoFlight.csv'
	DELIMITER ';'
	CSV HEADER;
	
	CREATE TABLE public."ForumPersonIdFlight" (
		person_id INTEGER NOT NULL,
		dep_airport_id INTEGER NOT NULL,
		dest_airport_id INTEGER NOT NULL,
		CONSTRAINT fk_person_id
		 FOREIGN KEY (person_id)
		 REFERENCES public."ForumPersonalInformation"(person_id),
		CONSTRAINT fk_dep_airport_id
		 FOREIGN KEY (dep_airport_id)
		 REFERENCES public."ForumAirport"(airport_id),
		CONSTRAINT fk_dest_airport_id
		 FOREIGN KEY (dest_airport_id)
		 REFERENCES public."ForumAirport"(airport_id)
	)
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."ForumPersonIdFlight"
	    OWNER to postgres;


    COPY "ForumPersonIdFlight"(person_id, dep_airport_id, dest_airport_id)
	FROM '{}PersonIdFlight.csv'
	DELIMITER ';'
	CSV HEADER;	
	""".format(path, path, path, path, path)
	
	scr4 = """
	create table "Report"
	(
		from_city varchar(50) not null,
		from_country varchar(25),
		from_airport varchar(3) not null,
		to_city varchar(25) not null,
		to_country varchar(25) not null,
		to_airport varchar(3) not null,
		date_from date not null,
		date_to date not null,
		days varchar(50) not null,
		"depTime" time not null,
		"arrTime" time not null,
		flight varchar(10) not null,
		aircraft varchar(3) not null,
		"travelTime" varchar(10) not null
	);
	
	COPY "Report"(from_city, from_country, from_airport, to_city, to_country, to_airport, date_from, date_to, days, "depTime", "arrTime", flight, aircraft, "travelTime")
	FROM '{}report.csv'
	DELIMITER ';'
	CSV HEADER;
	""".format(path)
	
	
	scr5 = """ 
	CREATE TABLE "Sirena-export-fixed"(
		PaxName varchar(60) not null,
		PaxBirthDate varchar(10),
		DepartDate date not null,
		DepartTime time not null,
		ArrivalDate date not null,
		ArrivalTime time not null,
		FlightCodeSh varchar(10) not null,
		From_ varchar(3) not null,
		Dest varchar(3) not null,
		Code_e_Ticket varchar(22) not null,
		TravelDoc varchar(11) not null,
		Seat varchar(3),
		Meal varchar(4),
		TrvCls_Fare char not null,
		Baggage varchar(20),
		PaxAdditionalInfo varchar(20),
		AdditionalInfo varchar(15),
		AgentInfo varchar(50)
	);
	
	COPY "Sirena-export-fixed"(paxname, paxBirthDate, DepartDate, DepartTime, ArrivalDate, ArrivalTime, FlightCodeSh, From_, Dest, Code_e_Ticket, TravelDoc, Seat, Meal, TrvCls_Fare, Baggage, PaxAdditionalInfo, AdditionalInfo, AgentInfo)
	FROM '{}Sirena-export-fixed.csv'
	DELIMITER ';'
	CSV HEADER;
	""".format(path)
	
	
	
	scr6 = """
	CREATE TABLE public."SkyTeamExchange" (
		dep_date DATE NULL,
		flight_number VARCHAR(30) NULL,
		dep_code VARCHAR(30) NULL,
		status VARCHAR(30) NULL,
		dest_code VARCHAR(30) NULL,
		someinfo VARCHAR(30) NULL,
		travel_class CHAR NULL,
		fare VARCHAR(30) NULL
	)
	
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."SkyTeamExchange"
	    OWNER to postgres;

	COPY "SkyTeamExchange"(dep_date, flight_number, dep_code, status, dest_code, someinfo, travel_class, fare)
	FROM '{}ymlCSV.csv'
	DELIMITER ',';

	""".format(path)

	
	scr8 = """
	CREATE TABLE public."YourBoardingPassDotAero" (
		uid INTEGER NOT NULL,
		sequence INTEGER NULL,
		sex VARCHAR(30) NULL,
		first_name VARCHAR(30) NULL,
		last_name VARCHAR(30) NULL,
		Y_info VARCHAR(30) NULL,
		flight_number VARCHAR(30) NULL,
		dep_city VARCHAR(30) NULL,
		dest_city VARCHAR(30) NULL,
		gate VARCHAR(30) NULL,
		dest_code VARCHAR(30) NULL,
	        dep_code VARCHAR(30) NULL,
	        dep_date DATE NULL,
		dep_time TIME NULL,
		operator_info VARCHAR(30) NULL,
		info VARCHAR(100) NULL,
		seat VARCHAR(30) NULL,
		PNR VARCHAR(30) NULL,
		ticket_number VARCHAR(30) NULL
	)
	
	WITH (
	    OIDS = FALSE
	)
	TABLESPACE pg_default;
	
	ALTER TABLE public."YourBoardingPassDotAero"
	    OWNER to postgres;

	COPY "YourBoardingPassDotAero"(uid,	sequence, sex, first_name, last_name, Y_info, flight_number, dep_city, dest_city, gate, dest_code, dep_code, dep_date, dep_time, operator_info, info, seat, PNR, ticket_number)
	FROM '{}Tickets.csv'
	DELIMITER ';'
	CSV HEADER;
	""".format(path)
	
	db_in.execute(scr1)
	db_in.execute(scr2)
	db_in.execute(scr3)
	db_in.execute(scr4)
	db_in.execute(scr5)
	db_in.execute(scr6)
	db_in.execute(scr8)

def getGenders(names):
	url = ""
	cnt = 0
	if not isinstance(names,list):
		names = [names,]
	
	for name in names:
		if url == "":
			url = "name[0]=" + name
		else:
			cnt += 1
			url = url + "&name[" + str(cnt) + "]=" + name
		

	req = requests.get("https://api.genderize.io?" + url)
	results = json.loads(req.text)
	
	retrn = []
	for result in results:
		if result["gender"] is not None:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			if len(results) > 1:
				continue
			if len(results) == 1:
				retrn.append((u'None',u'0.0',0.0))
	return retrn


def find_sex(first_name_in, second_name_in):
	lst = [first_name_in, second_name_in]
	return getGenders(lst)


def get_collapsed(db_in):
	handleCollapsed = open("collapsed_data.txt")
	collapsed_data = []
	
	ans = db_in.query("""SELECT "case", first_name, last_name FROM public.yourboardingpassdotaero_good;""")
	for sex, first, second in ans:
		rt = find_sex(first, second)
		if len(rt) > 0:
			if type(rt) == list:
				sum = 0
				count = len(rt)
				for i in rt:
					sum += i[1]
				if rt[0] == None:
					cl_data = [sex, first, second, float(sum / count)]
					handleCollapsed.write(str(cl_data))
					collapsed_data.append(cl_data)
				if (float(sum / count) < 0.95):
					cl_data = [sex, first, second, float(sum / count)]
					handleCollapsed.write(str(cl_data))
					collapsed_data.append(cl_data)
			else:
				if (rt[1] < 0.95):
					cl_data = [sex, first, second, rt[1]]
					handleCollapsed.write(str(cl_data))
					collapsed_data.append(cl_data)
		else:
			cl_data = [sex, first, second, 0]
			collapsed_data.append(cl_data)
	
	with open("collapsed_data.txt", newline='') as fl:
		for i in collapsed_data:
			fl.write(str(i) + '\n')



def insert_mergering_data(db_in):
	
	scr1 = """ 
create table public."BufferPerson"
(
	person_id SERIAL,
	first_name varchar(25) null,
	last_name varchar(25) null,
	passenger_document VARCHAR(30) NULL,
	PRIMARY KEY(person_id)
);

INSERT INTO 
 public."BufferPerson" (first_name, last_name, passenger_document)
SELECT DISTINCT 
 BD.first_name, 
 BD.last_name,
 BD.passenger_document
FROM 
 public."BoardingData" BD
FULL OUTER JOIN
(SELECT DISTINCT
  paxname,
  null,
  traveldoc
 FROM
  public."Sirena-export-fixed") as S
ON
 BD.passenger_document = S.traveldoc;

DELETE FROM public."BufferPerson" WHERE (first_name IS NULL AND last_name IS NULL);

INSERT INTO 
 public."BufferPerson" (first_name, last_name)
SELECT DISTINCT 
 AD.first_name, 
 AD.last_name
FROM 
 public."AirlinesData" AS AD
WHERE
 first_name != AD.first_name
 AND last_name != AD.last_name
 AND AD.first_name IS NOT NULL
 AND AD.last_name IS NOT NULL;


INSERT INTO 
 public."BufferPerson" (first_name, last_name)
SELECT DISTINCT 
 FPI.first_name, 
 FPI.last_name
FROM 
 public."ForumPersonalInformation" AS FPI
WHERE
 first_name != FPI.first_name
 AND last_name != FPI.last_name
 AND FPI.first_name IS NOT NULL
 AND FPI.last_name IS NOT NULL;

INSERT INTO 
 public."BufferPerson" (first_name, last_name)
SELECT DISTINCT 
 YBPDA.first_name, 
 YBPDA.last_name
FROM 
 public."YourBoardingPassDotAero" AS YBPDA
WHERE
 first_name != YBPDA.first_name
 AND last_name != YBPDA.last_name
 AND YBPDA.first_name IS NOT NULL
 AND YBPDA.last_name IS NOT NULL;


SELECT * FROM public."BufferPerson";
"""

	
	scr2 = """ 
create table public."BufferMatchingPersonFlight"(
	ticket_number VARCHAR(30) NOT NULL,
	passenger_document VARCHAR(30) NOT NULL
);

TRUNCATE public."BufferMatchingPersonFlight";

INSERT INTO 
 public."BufferMatchingPersonFlight"
SELECT DISTINCT 
 BD.ticket_number,
 BD.passenger_document
FROM 
 public."BoardingData" as BD
WHERE
 BD.ticket_number IS NOT NULL
 AND BD.ticket_number != 'Not presented'
 AND BD.passenger_document IS NOT NULL;
 
INSERT INTO 
 public."BufferMatchingPersonFlight"
SELECT DISTINCT 
 S.code_e_ticket,
 S.traveldoc
FROM 
 public."Sirena-export-fixed" as S
WHERE
 S.code_e_ticket NOT IN (SELECT ticket_number FROM public."BufferMatchingPersonFlight")
 AND S.code_e_ticket IS NOT NULL
 AND S.code_e_ticket != 'Not presented'
 AND S.traveldoc IS NOT NULL; 

SELECT * FROM public."BufferMatchingPersonFlight";
"""

	

	scr3 = """ 
create table public."BufferFlightsTMP1"
(
	flight_id SERIAL,
	ticket_number VARCHAR(30) NULL,
	flight_number VARCHAR(30) NULL, 
	dep_city VARCHAR(30) NULL,
	dest_city VARCHAR(30) NULL,
	dep_date DATE NULL,
	travel_class VARCHAR(30) NULL,
	baggage VARCHAR(30) NULL	
);

create table public."BufferFlightsTMP2"
(
	flight_id SERIAL,
	ticket_number VARCHAR(30) NULL,
	flight_number VARCHAR(30) NULL, 
	dep_city VARCHAR(30) NULL,
	dest_city VARCHAR(30) NULL,
	dep_date DATE NULL,
	travel_class VARCHAR(30) NULL,
	baggage VARCHAR(30) NULL	
);


create table public."BufferFlights"
(
	flight_id SERIAL,
	ticket_number VARCHAR(30) NULL,
	flight_number VARCHAR(30) NULL, 
	dep_city 	VARCHAR(30) NULL,
	dest_city VARCHAR(30) NULL,
	dep_date DATE NULL,
	travel_class VARCHAR(30) NULL,
	baggage VARCHAR(30) NULL,
	PRIMARY KEY (flight_id)
);

TRUNCATE public."BufferFlightsTMP1";
TRUNCATE public."BufferFlightsTMP2";
TRUNCATE public."BufferFlights";

INSERT INTO 
 public."BufferFlightsTMP1" (ticket_number, flight_number, dep_city,
			dest_city, dep_date, travel_class)
SELECT DISTINCT 
 YBPDA.ticket_number, 
 YBPDA.flight_number,
 initcap(YBPDA.dep_city),
 initcap(YBPDA.dest_city),
 YBPDA.dep_date,
 YBPDA.Y_info
FROM 
 public."YourBoardingPassDotAero" as YBPDA;


INSERT INTO 
 public."BufferFlightsTMP1" (ticket_number, dep_city,
			dest_city, dep_date, travel_class)
SELECT DISTINCT 
 S.Code_e_Ticket, 
 S.From_,
 S.Dest,
 S.DepartDate,
 S.TrvCls_Fare
FROM 
 public."Sirena-export-fixed" as S
WHERE
 S.Code_e_Ticket NOT IN (SELECT ticket_number FROM public."BufferFlightsTMP1");
 
INSERT INTO 
 public."BufferFlightsTMP1" (ticket_number, flight_number,
			dest_city, dep_date)
SELECT DISTINCT 
 ticket_number,
 flight_number,
 dest_city,
 dep_date
FROM 
 public."BoardingData" as BD
WHERE
 BD.ticket_number NOT IN (SELECT ticket_number FROM public."BufferFlightsTMP1");

INSERT INTO 
 public."BufferFlightsTMP2" (ticket_number, flight_number, dep_city,
							dest_city, dep_date, travel_class, baggage)
SELECT DISTINCT 
 tmpBF.ticket_number, 
 tmpBF.flight_number, 
 tmpBF.dep_city,
 tmpBF.dest_city,
 tmpBF.dep_date, 
 tmpBF.travel_class,
 BD.baggage
FROM 
 (SELECT DISTINCT
  ticket_number,
  baggage
 FROM public."BoardingData") as BD
 RIGHT JOIN
  public."BufferFlightsTMP1" as tmpBF
 ON
  tmpBF.ticket_number=BD.ticket_number;


INSERT INTO 
 public."BufferFlights" (ticket_number, flight_number, dep_city,
						dest_city, dep_date, travel_class, baggage)
SELECT DISTINCT 
 tmpBF.ticket_number, 
 tmpBF.flight_number, 
 tmpBF.dep_city,
 tmpBF.dest_city,
 tmpBF.dep_date, 
 tmpBF.travel_class,
 S.baggage
FROM 
 (SELECT DISTINCT
  code_e_ticket,
  baggage
 FROM public."Sirena-export-fixed") as S
 RIGHT JOIN
  public."BufferFlightsTMP2" as tmpBF
 ON
  S.code_e_ticket=tmpBF.ticket_number;
  
DELETE FROM public."BufferFlights" WHERE ticket_number='Not Presented';
DROP TABLE  public."BufferFlightsTMP1";
DROP TABLE  public."BufferFlightsTMP2";

SELECT * FROM public."BufferFlights";
"""

	db_in.execute(scr3)
	db_in.execute(scr2)
	db_in.execute(scr1)
	
#insert_mergering_data(db)

def translitData(db_in):
	scr1 = """
	create table public."TRANSLITNAMES"
	(
		name_id SERIAL,
		rusName VARCHAR(30),
		transNameFirst VARCHAR(30), 
		transNameLast VARCHAR(30),
	);
	"""	
	
	#db_in.execute(scr1)
	
	scr2 = """ SELECT DISTINCT paxname FROM public."Sirena-export-fixed"; """
	
	ans = db_in.query(scr2)
	i = 1	

	for name in ans:
		try:
			strName = name[0]
			#out_data = translit(strName, 'ru', reversed=True)
			out_data = cyrtranslit.to_latin(strName, 'ru')
			first_name = ''
			midleName = ''
			LastName = ''
				
			with open("out.txt", 'a') as file:
				LastName = out_data[0:out_data.find(' ')]
				out_data = out_data[out_data.find(' ') + 1 : ]
				place = out_data.find(' ')
				if(place < 0):
					first_name = out_data
				else:
					first_name = out_data[0:out_data.find(' ')]
				out_data = out_data[out_data.find(' ') + 1 : ]
				midleName = out_data
				out_str = str(i) + ';' + LastName.upper() + ';' + first_name.upper() + ';' + midleName.upper() + '\n'
				file.write(out_str)
			i += 1

		except Exception as e:
			with open("collapsed_data.txt", 'a') as f2:
				file.write("HARD TO UNDERSTAND: " + name + ' ' + str(i) + '\n')
			print("HARD TO UNDERSTAND: " + name + ' ' + str(i))
			i += 1
			continue
	


def high_year(year):
	if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
		return True
	else:
		return False

#translitData(db)

flights = []

passData = {'FirstName' : '', 'LastName' : '', 'amountFlights' : 0, 'passDoc' : '', 'travleClass' : 0, 'foodInfo' : 0, 'depCity' : 0, 'destCity' : 0, 'date' : 0}

#classType = {'F' : 1, 'A' : 1, 'J' : 2, 'C' : 2, 'P' : 3, 'Y' : 4, 'NULL' : -1}
classType = {'FA' : 1, 'JC' : 2, 'P' : 3, 'Y' : 4, 'NULL' : -1}



def analis(db_in):
	
	scr1 = """ SELECT person_id, first_name, last_name, passenger_document
	FROM public."BufferPerson"; """
	ans = db_in.query(scr1)
		
	out_list = []

	for i in ans:
		ans1 = i
		nm1 = ans1[1]
		nm2 = ans1[2]
		psp = ans1[3]

	
		scr2 = """ Select * from "MergedData_0" where (first_name = '{}' and last_name = '{}') or (first_name = '{}' and last_name = '{}') and passenger_document = '{}'""".format(nm1, nm2, nm2, nm1, psp)

		ans2 = db_in.query(scr2)
	
		BD = []		#	день рождения
		PP = []		#	паспортные данные
		CS = []		#	класс
		ML = []		#	еда
		C1 = []		#	город отправки
		C2 = []		#	город прибытия
		DT = []		#	дата отправки
		BG = []		#	багаж

		passData2 = {'FirstName' : '', 'LastName' : '', 'amountFlights' : '', 'travleClass' : '0', 'foodInfo' : '0', 'circle' : '0', 'collapsed' : '0', 'baggage' : '0'}	#, 'depCity' : 0, 'destCity' : 0, 'date' : 0


		if len(ans2) == 0:
			continue


		passData2['FirstName'] = nm1
		passData2['LastName'] = nm2
		passData2['amountFlights'] = str(len(ans2))
		

		for row in ans2:
			BD.append(row[3])		#	день рождения
			PP.append(row[4])		#	паспортные данные
			CS.append(row[5])		#	класс
			ML.append(row[6])		#	еда
			C1.append(row[7])		#	город отправки
			C2.append(row[8])		#	город прибытия
			DT.append(row[9])		#	дата отправки
			BG.append(row[10])		#	багаж
			

		cities = []

		for city_ind in range(len(C2)):
			cities.append(C1[city_ind])
			cities.append(C2[city_ind])

		name_city = []
	
		for city in cities:
					
			if city != '':
				scr3 = """SELECT name from "ForumAirport" where	abbr = '{}' ; """.format(city)	
				ans3_city = db_in.query(scr3)
				if len(ans3_city) == 0:
					name_city.append(city)
					continue
				#print(ans3_city)
				name_city.append(ans3_city[0][0])
			
			else:
				name_city.append('')
				passData2['circle'] = '-1'	#	данные поломаны (
				#break

		
		

		#test_data = ['g1', 'g2', 'g2', 'g3', 'g3', 'g2', 'g2', 'g1', 'g5', 'g1']
		#name_city = test_data


		
		city_bits = [0 for i in range(len(name_city))]

		try:

			for city_index in range(len(name_city)):
				if city_index % 2 == 1 and city_index + 1 < len(name_city):
					if name_city[city_index] == name_city[city_index + 1]:
						city_bits[city_index + 1] = 1
					if name_city[city_index] != name_city[city_index + 1]:
						for k in range(city_index, 0, -2):
							strt = name_city[city_index]
							if k - 3 >= 0:
								if city_bits[k - 1] == 0:
									city_bits[city_index] = -1
									break		
								if name_city[k - 3] == strt and city_bits[k - 1] == 1:
									city_bits[city_index] = 2
									break
								if city_bits[k - 1] == 1:
									continue
										

						if city_bits[city_index] == 0:
							city_bits[city_index] = -1

				if city_index % 2 == 0 and city_index + 1 == len(name_city) - 1:
					if city_bits[city_index - 1] == 2 or city_bits[city_index - 1] == -1:
						city_bits[city_index] = -1
						continue
					strt = name_city[city_index + 1]
					for k in range(city_index + 1, 0, -2):
						if k - 3 >= 0:
							if name_city[k - 3] == strt and city_bits[k - 1] == 1:
								city_bits[city_index + 1] = 2
								break
							if city_bits[k - 1] == 1:
								continue
				
				
			circles = 0
			collapsed = 0

			for city in city_bits:
				if city == 2:
					circles += 1
				if city == -1:
					collapsed += 1

			
			passData2['circle'] = str(circles)
			passData2['collapsed'] = str(collapsed)
		
		except Exception as e:
				with open('collapsed_data.txt', 'a') as file_c:
					file_c.write(str(ans2) + '\n')
					file_c.write(str(name_city) + '\n')
					for pr in range(15):
						file_c.write('=')
					file_c.write('\n')
	
		

		if len(CS) == 0:
			continue
			
		classType2 = {'FA' : 0, 'JC' : 0, 'P' : 0, 'Y' : 0, 'NULL' : 0}
		classType_p = {'FA' : 0, 'JC' : 0, 'P' : 0, 'Y' : 0, 'NULL' : 0}
		amount = 0
		for j in CS:
			if j == 'A' or j == 'F':
				classType2['FA'] += 1
			if j == 'J' or j == 'C':
				classType2['JC'] += 1
			if j == 'Y':
				classType2['Y'] += 1
			if j == 'P':
				classType2['P'] += 1
			if j == '':
				classType2['NULL'] += 1
			amount += 1

		for key in classType2:
			try:
				classType_p[key] = (classType2[key] / amount)
				if classType_p[key] >= 0.5:
					#print("GOOD")
					passData2['travleClass'] = str(1)
			except Exception as e:
				print(classType2, end=' ')
				print(amount)

		bg_am = 0
		bg_w = 0
		
		for bg in BG:
			if bg != '':
				bg_am += 1
			else:
				bg_w += 1
				
		if len(BG) > 0:
			pr1 = bg_am / len(BG)
			if pr1 > 0.7:
				passData2['baggage'] = str(1)
		
		
		

		for d in ML:
			if d != '':
				passData2['foodInfo'] = str(1)


		with open("expertdata.txt", 'a') as fe:
			str_out = ''
			for key in passData2:
				str_out += passData2[key]
				str_out += ';'
			fe.write(str_out[:-1] + '\n')
	
		

analis(db)