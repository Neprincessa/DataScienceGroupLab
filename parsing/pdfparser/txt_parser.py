import csv
import re
from datetime import date, time

# exist_categories = ["FROM", "TO",  "Validity Days Dep", "Time",
#                     "Arr", "Time", "Flight Aircraft Travel", "Time"]


# categories = ["from_city", "from_country", "from_aeroport", "to_city", "to_country",
#               "to_aeroport", "days", "depTime", "arrTime", "flight", "aircraft", "travelTime"]


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def date_parse(str_date):
    res = re.match(r'(\d\d) (\w\w\w) - (\d\d) (\w\w\w)', str_date)
    if res != None:
        if res.group(4) == months[0]:
            return date(2018, months.index(res.group(2)) + 1, int(res.group(1))), date(2019, months.index(res.group(4)) + 1, int(res.group(3)))
        return date(2018, months.index(res.group(2)) + 1, int(res.group(1))), date(2018, months.index(res.group(4)) + 1, int(res.group(3)))


def get_from_to(data):
    tmp = []
    tmp_str = data.split(':')[1].replace(' \n', '')
    airport = tmp_str[-4:]
    tmp_str = tmp_str.replace(airport, '')
    if tmp_str.find(',') == -1:
        country = ''
    else:
        if len(tmp_str.split(', ', 2)) == 1:
            country = tmp_str.split(', ', 2)[0].replace(',', '')
        else:
            country = tmp_str.split(', ', 2)[1]
    city = tmp_str.split(', ', 2)[0].replace(' ', '')
    return [city, country, airport]


if __name__ == '__main__':
    input_file = open('Skyteam_Timetable.txt', 'r')
    csv_file = open('report.csv', 'w', newline='')
    spamwriter = csv.writer(csv_file, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["from_city", "from_country", "from_aeroport", "to_city", "to_country",
                         "to_aeroport", "days", "depTime", "arrTime", "flight", "aircraft", "travelTime"])

    next_str = ''
    for line in input_file:
        if 'FROM' in line or new_str != '':
            data_from = get_from_to(line.strip())
            for new_line in input_file:
                if 'TO' in new_line:
                    data_to = get_from_to(new_line.strip())
                elif 'Consult' in new_line or 'Validity Days Dep' in new_line or 'Operated by' in new_line or 'Time' in new_line or 'Arr' in new_line or 'Flight Aircraft Travel' in new_line or 'Time' in new_line:
                    pass
                elif 'FROM' in new_line:
                    new_str = new_line
                    break
                elif len(new_line) != 2 and new_line.strip() != '':
                    trip = new_line.strip().split(' ')
                    # print('TT ', trip)
                    time = date_parse(new_line)
                    if time == None:
                        time_from, time_to = None, None
                    else:
                        time_from = time[0]
                        time_to = time[1]
                    # if '"' in trip[10]:
                    #     print(new_line)
            spamwriter.writerow(data_from + data_to +
                                [time_from, time_to]+[''.join(trip[5:len(trip)-6])]+[trip[6], trip[7]]+[trip[8], trip[9], trip[10]])
