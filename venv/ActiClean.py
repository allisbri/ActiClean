import csv
import openpyxl
import os

wb = openpyxl.Workbook()
ws = wb.active

with open('C:\\Users\\a\\Desktop\\PTSD_03162018.csv') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        ws.append(row)

wb.save('C:\\Users\\a\\Desktop\\file.xlsx')

os.chdir('C:\\Users\\a\\Desktop')
wb = openpyxl.load_workbook('file.xlsx')


