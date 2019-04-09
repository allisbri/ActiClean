import csv
from tkinter import filedialog

# Remove rows where NaN exists in active or daily
    # what about rows where daily or active has NaN, from 'date' on, currently these are deleted
    # will there be rows where NaN exists only for the checked cell
# Replace all of the NaN’s with blank cells

# Remove where %invalid is greater than 50 (?)

# For sleep intervals, copy and paste row data (?)

# file_path = 'C:\\Users\\a\\Desktop\\CES_07302018.csv'
# new_file_path = 'C:\\Users\\a\\Desktop\\test_CES_07302018.csv'
interval_type_col = 4
onset_latency_col = 22
percent_invalid_sw_col = 21
start_date_col = 6
interval_num_col = 5
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
    r = string_list.copy()
    for s in string_list:
        if s == string_to_replace:
            r[c] = string_to_insert
        c = c + 1
    return r


def is_first_in_series(cur):
    if len(cur) >= (interval_num_col + 1):
        if cur[interval_num_col] == '1':
            return True
    return False


def is_last_in_series(cur, next_up, col_num):
    if len(cur) >= interval_type_col + 1:
        if not list_string_equals(cur, col_num, next_up[col_num]):
            return True
    return False


def is_first_or_last_in_series(cur, next_up, col_num):
    if is_last_in_series(cur, next_up, col_num):
        return True
    if is_first_in_series(cur):
        return True
    return False


def has_start_date(string_list):
    if len(string_list) < 7:
        return False
    if string_list[start_date_col] != 'NaN':
        return True
    return False


def write_row_without_nan(writer, string_list):
    new_row = replace_string_in_list(string_list, 'NaN', '')
    writer.writerow(new_row)


def meets_valid_sleep_wake_criteria(cur):
    if len(cur) >= (percent_invalid_sw_col + 1):
        if float(cur[percent_invalid_sw_col]) <= 50:
            return True
        else:
            return False
    else:
        return True


def row_should_be_written(cur, next_up):
    if list_string_equals(cur, interval_type_col, active_interval) or \
            list_string_equals(cur, interval_type_col, daily_interval):
        if not has_start_date(cur):
            return False
        if is_first_or_last_in_series(cur, next_up, interval_type_col):
            if meets_valid_sleep_wake_criteria(cur):
                return True
            else:
                return False
    return True


def last_row_should_be_written(cur):
    if len(cur) > 0:
        if list_string_equals(cur, interval_type_col, active_interval) or \
                list_string_equals(cur, interval_type_col, daily_interval):
            if not has_start_date(cur):
                return False
            if meets_valid_sleep_wake_criteria(cur):
                return True
    return True


def clean_actigraphy_csv(file_path):
    count = 0
    new_file_path = file_path.replace(".csv", "_clean.csv")
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(new_file_path, 'w', encoding='utf-8-sig', newline='') as new_csv:
            csv_writer = csv.writer(new_csv)
            cur = next(csv_reader)
            for row in csv_reader:
                next_up = row
                # write first row
                if count <= 0:
                    csv_writer.writerow(cur)

                elif row_should_be_written(cur, next_up):
                    write_row_without_nan(csv_writer, cur)
                    print(cur)

                cur = next_up
                count = count + 1

            # write last row
            if last_row_should_be_written(cur):
                write_row_without_nan(csv_writer, cur)


def get_removed_rows_csv(file_path):
    count = 0
    new_file_path = file_path.replace(".csv", "_removed.csv")
    with open(file_path, 'r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        with open(new_file_path, 'w', encoding='utf-8-sig', newline='') as new_csv:
            csv_writer = csv.writer(new_csv)
            cur = next(csv_reader)
            for row in csv_reader:
                next_up = row
                # write first row
                if count <= 0:
                    csv_writer.writerow(cur)

                elif not row_should_be_written(cur, next_up):
                    csv_writer.writerow(cur)
                    print(cur)

                cur = next_up
                count = count + 1

            # write last row
            if not last_row_should_be_written(cur):
                csv_writer.writerow(cur)


file_path = get_file_location_from_user_selection()
clean_actigraphy_csv(file_path)
get_removed_rows_csv(file_path)