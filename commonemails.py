# Creates sets of email addresses from two files and uses set '&' to find common emails
import os
import datetime
import csv

first_filename = 'suppression_bounces161219emailsonly.csv'
second_filename = 'allsubs_nojp_3unsubs.csv'
output_file = 'common_emails.csv'
print("filenames are: ", first_filename, second_filename)

first_list = []
second_list = []
old_file = False  # Used to test if we are using an out of date file. This means we have forgotten to copy the new gmail export file mbox.
# Specify just the filenames. Process_sourcefile() will deal with paths and also check if the files are up to date.

def process_sourcefile(source_filename, old_file):
    source_file = os.path.join('', source_filename)
    source_modified_date = datetime.date.fromtimestamp(os.path.getmtime(source_file))
    print('today is:', datetime.date.today(), 'file is: ', source_modified_date)
    if datetime.date.today() != source_modified_date:
        old_file = True
    print("filename is: ", source_filename, "modified on :", datetime.date.fromtimestamp(os.path.getmtime(source_file)))
    if old_file:
        print('Your file is old, are you sure you want to continue?')
        response = input('Enter Y to continue. Any other input will quit.')
        if response.lower() != 'y':
            raise SystemExit

process_sourcefile(first_filename, old_file)
with open(first_filename, 'r', encoding='utf-8') as f:
    for line in f:
        first_list.append(line)

first_list = list(set(first_list))  # Remove duplicates
print('Bounced emails : ', len(first_list))

with open(second_filename, 'r', encoding='utf-8') as f:
    for line in f:
        second_list.append(line)

second_list = list(set(second_list))  # Remove duplicates
print('Emails sent: ', len(second_list))

first_set = set(first_list)
second_set = set(second_list)
overlap_set = second_set & first_set
print('Emails sent and bounced:', len(overlap_set))
overlap_list = list(overlap_set)
overlap_list.insert(0, 'email')  # Add title to first row for import
emailsfile = open(output_file, 'w', newline='')  # newline='' is to stop blank lines being inserted in csv file.
wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
for email in overlap_list:
    wr.writerow([email])
emailsfile.close()