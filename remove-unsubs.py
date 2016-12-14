import re
import csv
import pandas as pd
import os
new_emails_filename = 'new.csv'
new_emails_file = os.path.join('', new_emails_filename)
previous_emails_filename = "prev.csv"
previous_emails_file = os.path.join('', previous_emails_filename)
previous_emails_only = []
new_emails_only =[]
print("filenames are: ", new_emails_file, previous_emails_file)

def parse(raw_file, delimiter):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter #TODO add default arg : ','
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    # open csv file
    opened_file = open(raw_file, newline='', encoding='utf-8')
    # read csv file
    csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
    # csv_data object is now an iterator meaning we can get each element one at a time

    # build data structure to return parsed data
    parsed_data = []  # this list will store every row of data
    fields = csv_data.__next__()  # this will be the column headers; we can use .next() because csv_data is an iterator
    print(fields)
    for row in csv_data:
        if row[1] == "":  # there is no text in the runner field so no data to process
            pass
        else:
            parsed_data.append(dict(zip(fields, row)))  # Creates a new dict item for each row with col header as key and stores in a list
        #  racer_count += 1  # This is number of racers not races
    print("data list is: ", parsed_data)
    print("Type of parsed_data is: ", type(parsed_data))
    # close csv file
    opened_file.close()
    return parsed_data

previous_emails_list = parse(previous_emails_file, ',')
for contact in previous_emails_list:
    previous_emails_only.append(contact['email'].lower())

print('previous emails are:', previous_emails_only)

new_emails_list = parse(new_emails_file, ',')
for contact in new_emails_list:
    new_emails_only.append(contact['email'].lower())

def create_new_subcribers(newsub_set, new_emails_list):
    newsub_details = []
    print('new emails list is:', new_emails_list)
    print(type(new_emails_list))
    for contact in new_emails_list:
        if contact['email'] in newsub_set:
            newsub_details.append(contact['countrycode'] + ',' + contact['language']+ ',' + contact['email']+ ',' + contact['firstname']+ ',' + contact['lastname'])


    print(type(newsub_details))
    return newsub_details
# with open(new_emails_file, 'r', encoding='utf-8') as fa:
#     for line in fa:
#         new_emails_list.append(line.lower())

new_emails_only = list(set(new_emails_only))  # Remove duplicates
print('Current list has:', len(new_emails_only), 'emails')

# with open(previous_emails_file, 'r', encoding='utf-8') as fp:
#     for line in fp:
#         previous_emails_list.append(line)

previous_emails_only = list(set(previous_emails_only))  # Remove duplicates
print('The previous list had: ',len(previous_emails_only), 'emails.')
for e in range(1,10):
    print('previous email sample:', e, previous_emails_only[e])

current_set = set(new_emails_only)
previous_set = set(previous_emails_only)
unsub_set = previous_set - current_set
newsub_set = current_set - previous_set
print('current set is:', len(current_set), 'previous set was: ', len(previous_set), 'and there are these unsubs:', len(unsub_set))
print(len(unsub_set))
print('they are:', unsub_set)
print('new subscribers are:', newsub_set)
newsub_details = create_new_subcribers(newsub_set, new_emails_list)
print('new sub details are: ', newsub_details)
emailsfile = open('new_subscribers.csv', "w", newline='', encoding='utf-8') # newline = '' to prevent blank lines being inserted
wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
for contact in newsub_details:
   wr.writerow([contact])
emailsfile.close()

# TODO tidy up code.
# TODO export unsubscribers to csv file
# TODO add comments