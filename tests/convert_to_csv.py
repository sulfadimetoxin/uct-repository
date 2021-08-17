from openpyxl import load_workbook
import csv

wb = load_workbook(filename='sample_data/Result_40.xlsx', read_only=True)
sh = wb.active
with open('students_data.csv', 'w', newline="") as f:
    c = csv.writer(f)
    for r in sh.rows:
        c.writerow([cell.value for cell in r])

wb.close()
