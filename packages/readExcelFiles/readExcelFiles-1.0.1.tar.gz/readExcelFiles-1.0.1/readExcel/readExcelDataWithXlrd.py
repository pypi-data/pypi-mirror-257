import xlrd

"""
    Read data from an Excel file using xlrd library and return it as a list of rows.

    Args:
        file_path (str): The file path of the Excel file.
        sheet_name (str): The name of the worksheet. Default is 'Sheet1'.

    Returns:
        list: A list containing rows of data from the specified worksheet.
    """


def readExcelDataWithXlrd(excel_file_path, sheet_name='Sheet1'):
    workbook = xlrd.open_workbook(excel_file_path)
    worksheet = workbook.sheet_by_name(sheet_name)

    data = []
    for row_idx in range(worksheet.nrows):
        row_data = []
        for col_idx in range(worksheet.ncols):
            row_data.append(worksheet.cell_value(row_idx, col_idx))
        data.append(row_data)

    return data


# Example usage:
excel_file = r"D:\python-work\python-core\read-file\file\xls\murali.xls"
result = readExcelDataWithXlrd(excel_file)
print(result)
