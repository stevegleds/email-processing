import re
import csv
import os
import datetime
old_file = False
bounces_filename = 'bounces.mbox'  # this is a test file
bounces_file = os.path.join('', bounces_filename)
bounces_modified_date = datetime.date.fromtimestamp(os.path.getmtime(bounces_file))
print('today is:', datetime.date.today(), 'file is: ', bounces_modified_date)
if datetime.date.today() != bounces_modified_date:
    old_file = True
print("filename is: ", bounces_file, "modified on :", datetime.date.fromtimestamp(os.path.getmtime(bounces_file)))
if old_file:
    print('Your file is old, are you sure you want to continue?')
    response = input('Enter Y to continue. Any other input will quit.')
    if response != 'Y':
        raise SystemExit

output_filename = 'bounces.csv'
output_file = os.path.join('', output_filename)
count = 0
countbrackets = 0
countrecipients = 0
ignore = 0
emails = []
with open(bounces_file, 'r', encoding='utf-8') as fb:
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