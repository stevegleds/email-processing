"""
Identifies new and deleted subscribers by comparing previous subscriber list with latest subscriber list
new_links_filename is a list of inbound urls
old_links_filename is list of urls that have been previously checked
Add the required filename for old nad new links
add name for merged output file that contains merged info from old to new links file
"""
import csv
import os

new_links_filename = 'referring_page.csv'
old_links_filename = "old_links.csv"
new_links_file = os.path.join('data', new_links_filename)
old_links_file = os.path.join('data', old_links_filename)
print("filenames are: ", new_links_file, old_links_file)
updated_links_filename = 'updated_referral_links.csv'
old_urls_only = []
new_urls_only = []


def parse(raw_file, delimiter):
    """
    :param raw_file: probably csv file
    :param delimiter: specify delimiter #TODO add default arg : ','
    :return: parsed data list of dictionaries
    Parses a raw CSV file to a JSON-line object.
    18 October 2018 had ro remove encoding='utf-8' for one of the files I processed. Added it back
    """
    # open csv file
    with open(raw_file, newline='', encoding='utf-8') as opened_file:
        # read csv file
        csv_data = csv.reader(opened_file, delimiter=delimiter)  # first delimiter is csv.reader variable name
        # csv_data object is now an iterator meaning we can get each element one at a time
        # build data structure to return parsed data
        parsed_data = []  # this list will store every row of data
        fields = csv_data.__next__()
        # this will be the column headers; we can use .next() because csv_data is an iterator
        print(fields)
        fields[0] = 'Host'
        print(fields)
        for row in csv_data:
            if row[0] == "":  # there is no text field so no data to process
                pass
            else:
                parsed_data.append(dict(zip(fields, row)))
                # Creates a new dict item for each row with col header as key and stores in a list
            #  racer_count += 1  # This is number of racers not races
        # close csv file
        opened_file.close()
        return parsed_data


# create list containing only urls
old_links_list = parse(old_links_file, ',')
#  print('Old links list:', old_links_list)
for link in old_links_list:
    old_urls_only.append(link['Host'].lower())
#  print('previous urls are:', old_urls_only)

# create list containing new urls
new_links_list = parse(new_links_file, ',')
for link in new_links_list:
    new_urls_only.append(link['Host'].lower())


def create_new_links(old_list, new_list):
    # Creates new list of dictionaries with found field with full details
    new_links_details = []
    new_links_details.append('Host' + ',' + 'Last crawled' + ',' + 'Found?' + ',' + 'old_link' + ','
                             + 'disavow' + ',' + 'comment' + ',' + 'classification')

    for url in new_list:
        found = 'Not Found'
        old_link = ""
        disavow = ""
        comment = ""
        classification = ""
        if ',' in url['Host']:
            url['Host'] = url['Host'].replace(',', '_sgxyz_')
        for link in old_list:
            if link['Host'] in url['Host']:
                found = "Found"
                old_link = link['Host']
                disavow = link['Disavow']
                comment = link['Comment']
                classification = link['Classification']
        new_links_details.append(url['Host'] + ',' + found + ',' + old_link + ','
                                  + disavow + ',' + comment + ',' + classification)
    return new_links_details


print('Current list has:', len(new_urls_only), 'urls')
print('The previous list had: ', len(old_urls_only), 'links')
for e in range(1, 10):
    print('previous links sample:', e, old_urls_only[e])
    print('new links sample:', e, new_urls_only[e])


def create_file(output_file, urls):
    updated_links_file = open(output_file, "w", newline='', encoding='utf-8')
    # newline = '' to prevent blank lines being inserted
    wr = csv.writer(updated_links_file, quoting=csv.QUOTE_ALL)
    for url in urls:
        wr.writerow([url])
    updated_links_file.close()


updated_links = create_new_links(old_links_list, new_links_list)
print(updated_links)
create_file(updated_links_filename, updated_links)


