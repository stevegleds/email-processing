'''
Creates file containing emails from main file not contained in secondary file.
This takes two files all_emails and sent_emails and returns new file with emails in sent_emails removed from all_emails file
Specify the two source files and the output file at the start
'''
import csv
import os
all_emails_filename = 'sendgrid_suppression_bounces161216_emailsonly.csv'  # this is full list of subscribers from OpenEMM
sent_emails_filename = 'bounced_emails.csv'  # these are emails that we have sent already. Need to remove from the list
output_filename = 'sendgrid_net_bounces.csv'

all_emails_file = os.path.join('', all_emails_filename)
sent_emails_file = os.path.join('', sent_emails_filename)
output_file = os.path.join('', output_filename)
all_emails_list = []
sent_emails_list = []

print("filenames are: ", sent_emails_file, all_emails_file)

#  Create set of all_emails
with open(all_emails_file, 'r', encoding='utf-8') as fa:
    for line in fa:
        all_emails_list.append(line[1:-2].lower())
print('all email sample:', all_emails_list[13], 'has', len(all_emails_list[13]), 'chars')
all_emails_set = set(all_emails_list)  # Remove duplicates
print('Total number of subscribers is:', len(all_emails_set))

#  Create set of sent emails
with open(sent_emails_filename, 'r', encoding='utf-8') as fs:
    for line in fs:
        sent_emails_list.append(line[0:-1].lower())
print('sent emails sample', sent_emails_list[13], 'has', len(sent_emails_list[13]), 'chars')
sent_emails_set = set(sent_emails_list)  # Remove duplicates
print('Total sent emails: ', len(sent_emails_set))

#  Create list from set of emails not sent
unsent_emails_set = all_emails_set - sent_emails_set
print('Total unsent emails:', len(unsent_emails_set))

#  Create csv file of unsent emails
unsent_emails_list = list(unsent_emails_set)
unsent_emails_list.insert(0, 'email')  # Add title to first row for import
#  Write unsent email address to output file
output_file = open(output_file, "w", newline='', encoding='utf-8')  # newline = '' to prevent blank lines being inserted
wr = csv.writer(output_file, quoting=csv.QUOTE_ALL)
for email in unsent_emails_list:
    wr.writerow([email])
output_file.close()