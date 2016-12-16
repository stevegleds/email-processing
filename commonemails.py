import os
import datetime

bounced_emails_filename = 'emails.csv'
sent_emails_filename = 'dec5_send_list.txt'
print("filenames are: ", bounced_emails_filename, sent_emails_filename)

bounced_emails_list = []
sent_emails_list = []
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

process_sourcefile(bounced_emails_filename, old_file)
with open(bounced_emails_filename, 'r', encoding='utf-8') as f:
    for line in f:
        bounced_emails_list.append(line)

bounced_emails_list = list(set(bounced_emails_list))  # Remove duplicates
print('Bounced emails : ', len(bounced_emails_list))

with open(sent_emails_filename, 'r', encoding='utf-8') as f:
    for line in f:
        sent_emails_list.append(line)

sent_emails_list = list(set(sent_emails_list))  # Remove duplicates
print('Emails sent: ', len(sent_emails_list))

bounced_set = set(bounced_emails_list)
sent_set = set(sent_emails_list)
overlap_set = sent_set & bounced_set
print('Emails sent and bounced:', len(overlap_set))