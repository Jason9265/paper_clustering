import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

        return abstract_text

    finally:
        driver.quit()
