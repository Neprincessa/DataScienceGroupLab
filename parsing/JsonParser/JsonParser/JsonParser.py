import json
import csv

#handle = open("../../Airlines/FrequentFlyerForum-Profiles.json")

with open("..\..\..\Airlines\FrequentFlyerForum-Profiles.json") as json_file:
    data = json.load(json_file)

Registered_Flights = []
NickName           = []
Travel_Documents   = []
Sex                = []
Loyality_Programm  = []
Real_Name          = []
airpots            = {}
DataAboutFlights   = []
PersonIdFlight     = []
PersonIdInfoFlight = []

#for i in data['Forum Profiles']:
#    print(i)

list1 = data['Forum Profiles'][0]


for i in range(len(data['Forum Profiles'])):
    tmp = data['Forum Profiles'][i]
    passports = []

    for k in tmp['Travel Documents']:
        for j in k:
            passports.append(k[j]) 
            if(len(passports) >= 2):
                print('2')
 
    names = list(tmp['Real Name'].values())

    Registered_Flights.append(tmp['Registered Flights'])
    NickName.append(tmp['NickName']) 
            
    Travel_Documents.append(passports)  
    Sex.append(tmp['Sex'])           
    Loyality_Programm.append(tmp['Loyality Programm'])
    
    Real_Name.append(names)    




PersonId = 0

for j in Registered_Flights:
    tmpList2 = []
    PersonId += 1
    for i in j:
        tmp_i = i.copy()
        tmp_i.pop('Arrival')
        tmp_i.pop('Departure')
        #tmpList2 = list(tmp_i.values())
        amountKeys = 0
        
        if list(i['Arrival'].values()) not in list(airpots.values()):
            airkeys = list(airpots.keys())
            amountKeys1 = len(airkeys) + 1
            if len(airkeys) > 0:
                airpots[str(amountKeys1)] = list(i['Arrival'].values())
            if len(airkeys) == 0:
                airpots['1'] = list(i['Arrival'].values())
        else:
            for k in airpots:
                if list(i['Arrival'].values()) == airpots[k]:
                    amountKeys1 = int(k)
                    break

        if list(i['Departure'].values()) not in list(airpots.values()):
            airkeys = airpots.keys()
            if len(airkeys) > 0:
                amountKeys2 = len(airkeys) + 1
                airpots[str(amountKeys2)] = list(i['Departure'].values())
            if len(airkeys) == 0:
                airpots['1'] = list(i['Departure'].values())
        else:
            for k in airpots:
                if list(i['Departure'].values()) == airpots[k]:
                    amountKeys2 = int(k)
                    break

        Flight = [PersonId, amountKeys1, amountKeys2]
        InfoFlight = [PersonId, list(tmp_i.values())]
        PersonIdFlight.append(Flight)
        PersonIdInfoFlight.append(InfoFlight)
        tmpList2.append((amountKeys1, amountKeys2))
        tmpList2.append(list(tmp_i.values()))
        
    
    DataAboutFlights.append(tmpList2)
    tmpList2 = []
          
PersonalIdLoyalty = []
PersonId = 0

for i in Loyality_Programm:
    PersonId += 1
    for j in i:
        LoyaltyInfo = list(j.values())
        PersonalIdLoyaltyInfo = [PersonId]
        
        for k in LoyaltyInfo:
            k = k.replace(" ", "")
            PersonalIdLoyaltyInfo.append(k)
        
        PersonalIdLoyalty.append(PersonalIdLoyaltyInfo)
        



headerPersonalIdLoyalty = ['PersonId', 'Type', 'Abbr', 'LoyaltyId']

with open('PersonalIdLoyalty.csv', mode='w', newline='') as PersonalIdLoyalty_file:
    PersonalIdLoyalty_writer = csv.writer(PersonalIdLoyalty_file, delimiter=';')

    PersonalIdLoyalty_writer.writerow(headerPersonalIdLoyalty)
    for k in PersonalIdLoyalty:
        PersonalIdLoyalty_writer.writerow(k)


headerPersonIdFlight = ['PersonId', 'Arrival', 'Departure']

with open('PersonIdFlight.csv', mode='w', newline='') as PersonIdFlight_file:
    PersonIdFlight_writer = csv.writer(PersonIdFlight_file, delimiter=';')

    PersonIdFlight_writer.writerow(headerPersonIdFlight)
    for k in PersonIdFlight:
        PersonIdFlight_writer.writerow(k)


headerPersonIdInfoFlight = ['PersonId', 'Date', 'Codeshare', 'Flight']

with open('PersonIdInfoFlight.csv', mode='w', newline='') as PersonIdInfoFlight_file:
    PersonIdInfoFlight_writer = csv.writer(PersonIdInfoFlight_file, delimiter=';')

    PersonIdInfoFlight_writer.writerow(headerPersonIdInfoFlight)
    for k in PersonIdInfoFlight:
        PersonIdInfoFlightInfo = [k[0]]
        for i in k[1]:
            PersonIdInfoFlightInfo.append(i)
        PersonIdInfoFlight_writer.writerow(PersonIdInfoFlightInfo)


headerPersonalInformation = ['PersonId', 'NickName', 'Travel_Documents', 'Sex', 'First Name', 'Last Name']

with open('PersonalInformation.csv', mode='w', newline='') as PersonalInformation_file:
    PersonalInformation_writer = csv.writer(PersonalInformation_file, delimiter=';')

    PersonalInformation_writer.writerow(headerPersonalInformation)
    for i in range(len(NickName)):
        PersonalInformationInfo = [i+1]

        if NickName[i] == None:
            PersonalInformationInfo.append('')
        else:
            PersonalInformationInfo.append(NickName[i])
        if Travel_Documents[i][0] == None:
            PersonalInformationInfo.append('')
        else:
            PersonalInformationInfo.append(Travel_Documents[i][0])
        if Sex[i] == None:
            PersonalInformationInfo.append('')
        else:
            PersonalInformationInfo.append(Sex[i])
        if Real_Name[i][0] == None:
            PersonalInformationInfo.append('')
        else:
            PersonalInformationInfo.append(Real_Name[i][0])
        if Real_Name[i][1] == None:
            PersonalInformationInfo.append('')
        else:
            PersonalInformationInfo.append(Real_Name[i][1])

        PersonalInformation_writer.writerow(PersonalInformationInfo)


print(Registered_Flights[0])

print(len(airpots))
print(len(Registered_Flights))
print(len(NickName))
print(len(Travel_Documents))
print(len(Sex))
print(len(Loyality_Programm))
print(len(Real_Name))


#print(data['Forum Profiles'][15]['NickName'])
#print(len(data['Forum Profiles'][0]['Registered Flights']))
#print(data.keys())
