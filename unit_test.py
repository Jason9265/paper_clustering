from extract_abstract import extract_abstract
from vectorise_clustering import vectorise_clustering

def test_extra():
    url = 'http://dx.doi.org/10.1109/ACCESS.2018.2885083'
    abstract = extract_abstract(url)
    print(abstract) 

def test_clustering():
    vectorise_clustering('updated_excel_file.xlsx', 12, False)

test_clustering()
