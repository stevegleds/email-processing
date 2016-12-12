import re
import csv
import os
bounces_filename = 'bounces.mbox'  # this is a test file
bounces_file = os.path.join('', bounces_filename)
print("filename is: ", bounces_file)
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
emailsfile = open('bounced_emails.csv', 'w', newline='')
wr = csv.writer(emailsfile, quoting=csv.QUOTE_ALL)
for email in emails:
    wr.writerow([email])
emailsfile.close()