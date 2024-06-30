import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Remove unnecessary words
def preprocess_text(text, use_stemming=False, use_lemmatization=True):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d', ' ', text)
    
    # Remove stopwords
    tokens = word_tokenize(text)
    additional_words = {'sdg', 'sib', 'ee', 'ion', 'production', 'resource', 'review', 'grid', 'step', 'location', 'abc', 'result', 'good', 'swarm', 'rul', 'iran', 'service', 'scale', 'facilitating', 'soc', 'chmmc', 'sb', 'anfis', 'ruo', 'intermediate', 'ev', 'vspc', 'control', 'array', 'cu', 'dot', 'imaging', 'remarkable', 'mg', 'problem', 'operating', 'operational', 'tob', 'wound', 'od', 'pda', 'ppy', 'mof', 'ag', 'technology', 'fault', 'smart', 'sample', 'learning', 'learning', 'error', 'model', 'heuristic', 'time', 'year', 'method', 'collaboration', 'china', 'production', 'commodity', 'bp', 'emd', 'inaekf', 'identification', 'soc', 'estimation', 'input', 'monetary', 'wholesale', 'production', 'period', 'market', 'analysis', 'return', 'hydrocarbon', 'industry', 'explosion', 'pt', 'como', 'ngnf', 'encapsulated', 'shell', 'gb', 'field', 'v3', 'vector', 'v3s', 'rvv', 'basic', 'technique', 'tracking', 'mppt', 'focv', 'moo', 'site', 'active', 'activation', 'impact', 'analysis', 'photocatalytic', 'production', 'application', 'protection', 'document', 'faults', 'bess', 'able', 'micro', 'response', 'demand', 'optimization', 'component', 'dimensional', 'grade', 'mass', 'era', 'merra', 'reanalysis', 'measurement', 'year', 'tio', 'nh', 'tp', 'cm', 'µg', 'ahead', 'day', 'dispatch', 'multiple', 'uncertainty', 'anode', 'cycle', 'volume', 'ml', 'eh', 'risk', 'fcpp', 'drps', 'pevs', 'bond', 'efficiency', 'actively', 'term', 'film', 'surface', 'passed', 'use', 'india', 'real', 'solution', 'line', 'innovation', 'taxation', 'demonstration'}

    stop_words = set(stopwords.words('english'))
    stop_words.update(additional_words)
    tokens = [word for word in tokens if word not in stop_words]
    
    if use_stemming:
        tokens = [stemmer.stem(word) for word in tokens]
    elif use_lemmatization:
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

    processed_text = ' '.join(tokens)
    
    return processed_text

def extract_abstract(url):
    options = uc.ChromeOptions()
    # if use headless, the website will block request as bot
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        abstract_div = soup.find('div', class_=lambda x: x in ['article-section__content', 'abstract author', 'html-p', 'article_abstract-content', 'c-article-section__content', 'abstract-text row g-0', 'section-paragraph', 'article-text wd-jnl-art-abstract cf', 'hlFld-Abstract', 'capsule__text'])
        if abstract_div:
            abstract_text = abstract_div.get_text(strip=True)
        else:
            abstract_role = soup.find('div', attrs={"role": "paragraph"})
            if abstract_role:
                abstract_text = abstract_role.get_text(strip=True)
            else:
                return "NOT FOUND"

        abstract_text = preprocess_text(abstract_text)
        return abstract_text

    finally:
        driver.quit()
