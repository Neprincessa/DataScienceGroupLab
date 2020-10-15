import postgresql
import postgresql.driver as pg_driver
import psycopg2

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
		fist_name varchar(25) not null,
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
	
	COPY "AirlinesData"(uid, fist_name, last_name, cards_type, card_number, bonus_program, activities_type, activity_type, code, date, departure, arrival, fare)
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


create_tables_copy_data(db, path)

