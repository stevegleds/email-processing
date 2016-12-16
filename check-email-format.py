import re
import csv
import os
import datetime
old_file = False  # Used to test if we are using an out of date file. This means we have forgotten to copy the new gmail export file mbox.
# Specify just the filenames. Process_sourcefile() will deal with paths and also check if the files are up to date.
email_input_filename = 'sendgrid_suppression_bounces161216_emailsonly.csv'
email_output_filename = 'emails-checked.csv'

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
        if response != 'Y':
            raise SystemExit

process_sourcefile(email_input_filename, old_file)

def check_email_format(source_file, output_file):
    # Parameters are the source file .mbox and the output file .csv
    # The files are created from within the function so there is no output from the function
    # These counters are used to report the number of emails found
    count = 0
    emails_checked = 0
    ignore = 0
    emails = []
    # Using 'with open' because the source files can be very large and cause memory errors
    # Uses RE to identify patterns for emails such as 'To: email..'; 'To: <email ...'; 'RFC Recipient'
    # These are the formats found in the mbox files.
    # 10 emails are printed from each RE to check that emails are being parsed correctly.
    with open(source_file, 'r', encoding='utf-8') as f:
        for line in f:
            if count < 10:
                print(line)
            emails_checked += 1
            match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', line)
            if match == None :
                pass
            elif match.group()[:3] == 'www':
                print('www', match.group())
            else:
                count += 1
                if count < 10:
                    print(match.group())
                emails.append(match.group())
        print('We found ', count, 'valid email addresses and ignored', emails_checked - count)
        emails = list(set(emails))  # Remove duplicates
        emails.insert(0, 'email')  # Add title to first row for import
        emailsfile = open(output_file, 'w', newline='')  # newline='' is to stop blank lines being inserted in csv file.
        wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
        for email in emails:
            wr.writerow([email])
        emailsfile.close()

check_email_format(email_input_filename, email_output_filename)

