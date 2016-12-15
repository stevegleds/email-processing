import re
import csv
import os
import datetime
old_file = False
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

def get_emails(source_file, output_file):
    count = 0
    countbrackets = 0
    countrecipients = 0
    ignore = 0
    emails = []
    with open(source_file, 'r', encoding='utf-8') as fb:
        for line in fb:
            match = re.findall(r'To: [\w\.-]+@[\w\.-]+', line)
            for i in match:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if count <10 :
                        print(i, i[4:])
                    emails.append(i[4:])
                    count += 1
            matchbracket = re.findall(r'To: <[\w\.-]+@[\w\.-]+', line)
            for i in matchbracket:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if countbrackets < 10:
                        print(i, i[5:])
                    emails.append(i[5:])
                    countbrackets += 1
            matchrecipient = re.findall(r'rfc822; [\w\.-]+@[\w\.-]+', line)
            for i in matchrecipient:
                if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i:
                    ignore += 1
                else:
                    if countrecipients < 10:
                        print('RFC recipient found:', i, i[8:])
                    emails.append(i[8:])
                    countrecipients += 1
        print('We found ', count + countbrackets + countrecipients, 'email addresses and ignored', ignore)
        emails = list(set(emails))  # Remove duplicates
        print('We removed ', count + countbrackets + countrecipients - len(emails), 'duplicates' )
        emails.insert(0, 'email')  # Add title to first row for import
        emailsfile = open(output_file, 'w', newline='')
        wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
        for email in emails:
            wr.writerow([email])
        emailsfile.close()

process_sourcefile(bounces_input_filename, old_file)
get_emails(bounces_input_filename, bounces_output_filename)
process_sourcefile(complaints_input_filename, old_file)
get_emails(complaints_input_filename, complaints_output_filename)
