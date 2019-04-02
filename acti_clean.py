import csv
from tkinter import filedialog

# Remove rows where NaN exists in active or daily
    # what about rows where daily or active has NaN, from 'date' on, currently these are deleted
# Replace all of the NaN’s with blank cells
# Remove where %invalid is greater than 50 (?)
# For sleep intervals, copy and paste row data (?)

# file_path = 'C:\\Users\\a\\Desktop\\CES_07302018.csv'
# new_file_path = 'C:\\Users\\a\\Desktop\\test_CES_07302018.csv'
interval_type_col = 4
onset_latency_col = 22
percent_invalid_sw_col = 21
active_interval = 'ACTIVE'
daily_interval = 'DAILY'
excluded_interval = 'EXCLUDED'
count = 0


def get_file_location_from_user_selection():
    filename = filedialog.askopenfilename(filetypes=[(".csv", ".csv")])
    return filename


def list_string_equals(string_list, index_to_check, string_to_check_for):
    if len(string_list) >= (index_to_check + 1):
        if string_list[index_to_check] == string_to_check_for:
            return True
    return False


def replace_string_in_list(string_list, string_to_replace, string_to_insert):
    c = 0
    r = row.copy()
    for s in string_list:
        if s == string_to_replace:
            r[c] = string_to_insert
        c = c + 1
    return r


file_path = get_file_location_from_user_selection()
new_file_path = file_path.replace(".csv", "_clean.csv")
with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)
    with open(new_file_path, 'w', encoding='utf-8-sig', newline='') as new_csv:
        csv_writer = csv.writer(new_csv)
        print('test')
        for row in csv_reader:
            print(count)
            print(row)
            print('test2')
            if count <= 0:
                csv_writer.writerow(row)
            # exclude rows that have NaN for active interval or daily interval at onset_latency_col
            elif list_string_equals(row, interval_type_col, active_interval) \
                    or list_string_equals(row, interval_type_col, daily_interval):
                    print(row)
                    if row[onset_latency_col] != 'NaN':
                        csv_writer.writerow(row)
            # replace all cases of NaN with blank cells and write rows that have less length
            elif len(row) <= (percent_invalid_sw_col + 1):
                new_row = replace_string_in_list(row, 'NaN', '')
                csv_writer.writerow(new_row)
            # replace all cases of NaN with blank cells and exclude rows that have less than 50 percent invalid sw
            elif float(row[percent_invalid_sw_col]) < 50:
                new_row = replace_string_in_list(row, 'NaN', '')
                csv_writer.writerow(new_row)
            count = count + 1

