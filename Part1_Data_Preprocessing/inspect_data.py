import pandas as pd

file_path = 'University_Management_Curation_Project.xlsx'
try:
    xl = pd.ExcelFile(file_path)
    print("Sheets in the excel file:")
    print(xl.sheet_names)
    
    for sheet in xl.sheet_names:
        print(f"\n--- Sheet: {sheet} ---")
        df = xl.parse(sheet)
        print("Columns:")
        print(df.columns.tolist())
        print("Shape:", df.shape)
        print("First row:", df.head(1).to_dict(orient='records'))
except Exception as e:
    print("Error reading excel file:", e)
