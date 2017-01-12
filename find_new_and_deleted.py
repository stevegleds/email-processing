'''
Identifies new and deleted subscribers by comparing previous subscriber list with latest subscriber list
new_emails_filename is the latest export from openemm
previous_emails_filename is the previous export
Add the required filename for deleted and new_sub files
Open new subscriber csv file and convert to table before sending.
'''
import csv
import os

new_emails_filename = 'pcsu-softcity-emails-170109.csv'
previous_emails_filename = "pcsu-softcity-emails-161128.csv"
deleted_emails_filename = 'deleted_emails.csv'
new_sub_emails_filename = 'new_subs_details.csv'

new_emails_file = os.path.join('data', new_emails_filename)
previous_emails_file = os.path.join('data', previous_emails_filename)
deleted_emails_file = os.path.join('data', deleted_emails_filename)
new_sub_emails_file = os.path.join('data', new_sub_emails_filename)
print("filenames are: ", new_emails_file, previous_emails_file, deleted_emails_file, new_sub_emails_file)

previous_emails_only = []
new_emails_only =[]
unsubscribed_emails = []

def parse(raw_file, delimiter):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter #TODO add default arg : ','
    :return: parsed data
    Parses a raw CSV file to a JSON-line object.
    """
    # open csv file
    with open(raw_file, newline='', encoding='utf-8') as opened_file:
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
        # close csv file
        opened_file.close()
        return parsed_data

# create list containing only email addresses
previous_emails_list = parse(previous_emails_file, ',')
for contact in previous_emails_list:
    previous_emails_only.append(contact['email'].lower())
print('previous emails are:', previous_emails_only)

# create list containing new email addresses
new_emails_list = parse(new_emails_file, ',')
for contact in new_emails_list:
    new_emails_only.append(contact['email'].lower())


def create_new_subscribers(newsub_set, new_emails_list):
    # Creates new list with full details
    newsub_details = []
    for contact in new_emails_list:
        if contact['email'] in newsub_set:
            newsub_details.append(contact['countrycode'] + ',' + contact['language']+ ',' + contact['email']+ ',' + contact['firstname']+ ',' + contact['lastname'])
    return newsub_details

new_emails_only = list(set(new_emails_only))  # Remove duplicates
print('Current list has:', len(new_emails_only), 'emails')


previous_emails_only = list(set(previous_emails_only))  # Remove duplicates
print('The previous list had: ',len(previous_emails_only), 'emails.')
for e in range(1,10):
    print('previous email sample:', e, previous_emails_only[e])

current_set = set(new_emails_only)
previous_set = set(previous_emails_only)
unsub_set = previous_set - current_set
newsub_set = current_set - previous_set
newsub_details = create_new_subscribers(newsub_set, new_emails_list)
print('current set is:', len(current_set), 'previous set was: ', len(previous_set), 'and there are these unsubs:', len(unsub_set))
print('Contacts to be deleted: ', len(unsub_set))
print('Contacts to be added: ', len(newsub_set))
def create_file(output_file, contacts):
    emailsfile = open(output_file, "w", newline='', encoding='utf-8')
    # newline = '' to prevent blank lines being inserted
    wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
    for contact in contacts:
        wr.writerow([contact])
    emailsfile.close()

create_file(new_sub_emails_file, newsub_details)
create_file(deleted_emails_file, unsub_set)


