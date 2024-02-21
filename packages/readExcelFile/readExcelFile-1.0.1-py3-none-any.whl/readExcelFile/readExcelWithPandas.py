import pandas as pd
import warnings

# Disable all warnings
warnings.filterwarnings("ignore")


def readExcelWithPandas(excelFilePath):
    """
    Read data from an Excel file using pandas library and return it as a DataFrame.

    Args:
        excelFilePath (str): The file path of the Excel file.

    Returns:
        DataFrame: A DataFrame containing data from the Excel file.
    """
    try:
        # Attempt to read the Excel file
        data = pd.read_excel(excelFilePath)
        return data
    except Exception as e:
        # Handle any exceptions that occur during execution
        print(f"An error occurred: {e}")
        return None
