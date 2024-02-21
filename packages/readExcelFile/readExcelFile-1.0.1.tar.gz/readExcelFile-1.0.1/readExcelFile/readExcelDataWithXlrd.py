import xlrd

import warnings

# Disable all warnings
warnings.filterwarnings("ignore")


def readExcelDataWithXlrd(excelFilePath, sheetName='Sheet1'):
    """
        Read data from an Excel file using xlrd library and return it as a list of rows.

        Args:
            excelFilePath (str): The file path of the Excel file.
            sheetName (str): The name of the worksheet. Default is 'Sheet1'.

        Returns:
            list: A list containing rows of data from the specified worksheet.
        """
    try:
        workbook = xlrd.open_workbook(excelFilePath)
        worksheet = workbook.sheet_by_name(sheetName)

        data = []
        for row_idx in range(worksheet.nrows):
            row_data = []
            for col_idx in range(worksheet.ncols):
                row_data.append(worksheet.cell_value(row_idx, col_idx))
            data.append(row_data)

        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
