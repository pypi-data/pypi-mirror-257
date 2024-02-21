import xlwings as xw

import warnings

# Disable all warnings
warnings.filterwarnings("ignore")


def isValidValue(value):
    """
    Check if a value is valid.

    Args:
        value: The value to be checked.

    Returns:
        bool: True if the value is valid, False otherwise.
    """
    if value is None:
        return False
    if isinstance(value, str) and value.strip().isalnum():
        return False
    return True


def readFilesWithXlwings(excelFilePath):
    """
    Read data from an Excel file using xlwings library and print filtered data.

    Args:
        excelFilePath (str): The file path of the Excel file.
    """

    workbook  = None
    try:
        # Load the Excel file
        workbook = xw.Book(excelFilePath)

        # Reference the active sheet
        sheet = workbook.sheets.active
        data = sheet.used_range.value  # Get all values from the used range of the sheet
        # Filter and print the data
        filtered_data = [[item for item in row if isValidValue(item)] for row in data if
                         any(isValidValue(item) for item in row)]
        for row in filtered_data:
            print(row)

    except Exception as e:
        # Handle any exceptions that occur during execution
        print(f"An error occurred: {e}")

    finally:
        # Close the Excel workbook
        if 'workbook' in locals():
            workbook.close()
