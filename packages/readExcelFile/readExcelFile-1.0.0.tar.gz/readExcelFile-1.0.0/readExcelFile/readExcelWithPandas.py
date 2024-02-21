import pandas as pd
import warnings

# Disable all warnings
warnings.filterwarnings("ignore")


def readExcelWithPandas(excel_file_path):
    data = pd.read_excel(excel_file_path)
    return data


