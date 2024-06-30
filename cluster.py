from extract_abstract import extract_abstract
import pandas as pd

def process_papers(excel_path):
    df = pd.read_excel(excel_path)

    for index, row in df.iterrows():
        name = row['Name']
        doi = row['DOI']

        res = extract_abstract(doi)
        df.at[index, 'Abstract'] = res

    df.to_excel('updated_excel_file.xlsx', index=False)

if __name__ == "__main__":
    excel_path = 'Green Energy Papers Database.xlsx'

    # Data Preprocessing:
    process_papers(excel_path) 

    # Vectorisation Clustering:

    # Visualisation:

    # Output Generation:
