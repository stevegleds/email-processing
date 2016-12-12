import re
myboxfile = 'D:\python-code\mailbox\emailcomplaints.mbox'
print("filename is: ", myboxfile)
myfile = open(myboxfile, 'r', encoding='utf-8')
mytext = myfile.read()
match = re.findall(r'To: [\w\.-]+@[\w\.-]+', mytext)
count = 0
ignore = 0
for i in match:
    if 'amazonses' in i or 'pcspeedup' in i or 'broadbandspeedchecker' in i :
        ignore += 1
    else:
        count += 1
        print(count, i)
print('We found ', count, 'email addresses and ignored', ignore)
