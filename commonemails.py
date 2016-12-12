import re
import csv
bounced_emails = 'D:\python-code\mailbox\emails.csv'
sent_emails = 'D:\python-code\mailbox\dec5_send_list.txt'
bounced_emails_list = []
sent_emails_list = []
print("filenames are: ", bounced_emails, sent_emails)

with open(bounced_emails, 'r', encoding='utf-8') as f:
    for line in f:
        bounced_emails_list.append(line)

bounced_emails_list = list(set(bounced_emails_list))  # Remove duplicates
print(len(bounced_emails_list))

with open(sent_emails, 'r', encoding='utf-8') as f:
    for line in f:
        sent_emails_list.append(line)

sent_emails_list = list(set(sent_emails_list))  # Remove duplicates
print(len(sent_emails_list))

bounced_set = set(bounced_emails_list)
sent_set = set(sent_emails_list)
overlap_set = sent_set & bounced_set
print(len(overlap_set))