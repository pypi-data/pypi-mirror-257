import xlwings as xw


def is_valid_value(value):
    if value is None:
        return False
    if isinstance(value, str) and value.strip().isalnum():
        return False
    return True


def readFilesWithXlwings(excel_file_path):
    # Load the Excel file
    wb = xw.Book(excel_file_path)

    # Reference the active sheet
    sheet = wb.sheets.active
    data = sheet.used_range.value  # Get all values from the used range of the sheet
    data = [[item for item in row if is_valid_value(item)] for row in data if any(is_valid_value(item) for item in row)]

    # Print the filtered data
    for row in data:
        print(row)

    # Close the Excel workbook
    wb.close()




