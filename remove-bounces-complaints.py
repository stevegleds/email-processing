import re
import csv
import os
import datetime
old_file = False  # Used to test if we are using an out of date file. This means we have forgotten to copy the new gmail export file mbox.
# Specify just the filenames. Process_sourcefile() will deal with paths and also check if the files are up to date.
bounces_input_filename = 'bounces.mbox'
bounces_output_filename = 'bounces.csv'
complaints_input_filename = 'complaints.mbox'
complaints_output_filename = "complaints.csv"

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

process_sourcefile(bounces_input_filename, old_file)
process_sourcefile(complaints_input_filename, old_file)

def get_emails(source_file, output_file):
    # Parameters are the source file .mbox and the output file .csv
    # The files are created from within the function so there is no output from the function
    # These counters are used to report the number of emails found
    count = 0
    countbrackets = 0
    countrecipients = 0
    ignore = 0
    emails = []
    # Using 'with open' because the source files can be very large and cause memory errors
    # Uses RE to identify patterns for emails such as 'To: email..'; 'To: <email ...'; 'RFC Recipient'
    # These are the formats found in the mbox files.
    # 10 emails are printed from each RE to check that emails are being parsed correctly.
    with open(source_file, 'r', encoding='utf-8') as fb:
        for line in fb:
            match = re.findall(r'To: [\w\.-]+@[\w\.-]+', line)
            for i in match:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if count <10 :
                        print('To: sample\t', count, '\t\t', i, '\t', i[4:])
                    emails.append(i[4:])
                    count += 1
            matchbracket = re.findall(r'To: <[\w\.-]+@[\w\.-]+', line)
            for i in matchbracket:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if countbrackets < 10:
                        print('To: < sample\t', countbrackets, '\t', i, "\t", i[5:])
                    emails.append(i[5:])
                    countbrackets += 1
            matchrecipient = re.findall(r'rfc822; [\w\.-]+@[\w\.-]+', line)
            for i in matchrecipient:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if countrecipients < 10:
                        print('RFC recipient found:\t', countrecipients, '\t', i, '\t', i[8:])
                    emails.append(i[8:])
                    countrecipients += 1
        print('We found ', count + countbrackets + countrecipients, 'email addresses and ignored', ignore)
        emails = list(set(emails))  # Remove duplicates
        print('We removed ', count + countbrackets + countrecipients - len(emails), 'duplicates' )
        emails.insert(0, 'email')  # Add title to first row for import
        emailsfile = open(output_file, 'w', newline='')  # newline='' is to stop blank lines being inserted in csv file.
        wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
        for email in emails:
            wr.writerow([email])
        emailsfile.close()

get_emails(bounces_input_filename, bounces_output_filename)
get_emails(complaints_input_filename, complaints_output_filename)
