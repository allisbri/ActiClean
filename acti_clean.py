import csv
from shutil import copyfile
import os

# Remove rows where NaN exists in active or daily
    # what about rows where daily has NaN, from 'date' on, currently these are deleted
# Replace all of the NaN’s with blank cells
# Remove where %invalid is greater than 50 (?)
# For sleep intervals, copy and paste row data (?)

file_path = 'C:\\Users\\a\\Desktop\\CES_07302018.csv'
new_file_path = 'C:\\Users\\a\\Desktop\\test_CES_07302018.csv'
interval_type_col = 4
onset_latency_col = 22
percent_invalid_sw = 21
active_interval = 'ACTIVE'
daily_interval = 'DAILY'
excluded_interval = 'EXCLUDED'
count = 0

with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)
    with open(new_file_path, 'w', encoding='utf-8-sig', newline='') as new_csv:
        csv_writer = csv.writer(new_csv)

        for row in csv_reader:
            print(count)
            print(row)
            if len(row) >= interval_type_col and \
                    (row[interval_type_col] == daily_interval or row[interval_type_col] == active_interval):
                    print(row)
                    if row[onset_latency_col] != 'NaN':
                        csv_writer.writerow(row)
            elif count <= 0:
                csv_writer.writerow(row)
            elif len(row) < 22 or float(row[percent_invalid_sw]) < 50:
                col_count = 0
                r = row.copy()
                for col in row:
                    if col == 'NaN':
                        r[col_count] = ''

                    col_count = col_count + 1
                print("printing r")
                print(r)
                csv_writer.writerow(r)
            count = count + 1

