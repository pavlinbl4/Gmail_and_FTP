# из отчета TASS извлекает период отчета
import openpyxl


def get_report_date(file_way):
    wb = openpyxl.load_workbook(file_way)
    sheet = wb.active
    report_date = sheet.cell(row=5, column=3).value
    return report_date   # январь 2022 года


