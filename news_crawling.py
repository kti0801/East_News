
# 설치해야 할 라이브러리
# !pip install google.generativeai
# !pip install selenium
# !pip install webdriver_manager


from bs4 import BeautifulSoup
import time
 
from selenium import webdriver
from selenium.webdriver.common.by import By
from google.generativeai.types import HarmCategory, HarmBlockThreshold

options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
# options.add_argument('headless') # headless 모드 설정 -> 해당 옵션 적용 시 PDF 다운 불가
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox') 


driver = webdriver.Chrome()
# wait seconds...
driver.implicitly_wait(3)


def main_news(n=3):
    news_title = []
    news_contents = []
    i = 1

    driver.get('https://www.yna.co.kr/theme/headlines-history')
    time.sleep(3)

    while True:
        driver.find_element(By.CSS_SELECTOR, f'#container > div > div:nth-child(2) > section > div > ul > li:nth-child({i}) > div > div.news-con > a > strong').click()
        time.sleep(3)

        # 1. 셀레니움으로 html가져오기
        html_source = driver.page_source
        # 2. bs4로 html 파싱
        soup = BeautifulSoup(html_source, 'html.parser')
        time.sleep(0.5)

        title = soup.select_one('#articleWrap > div.content03 > header > h1').get_text().strip()
        paragraphs = soup.select('#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p')
        full_text = ' '.join(paragraph.get_text().strip() for paragraph in paragraphs)

        news_title.append(title)
        news_contents.append(full_text)

        driver.back()

        i += 1

        if i == n+1:
            break
    
    return news_title, news_contents



def tag_news(input, n=3):
    query = str(input)
    news_title = []
    news_contents = []
    i = 1
    
    driver.get(f'https://www.yna.co.kr/{query}/index?site=navi_{query}_depth01')
    time.sleep(3)

    while True:
        driver.find_element(By.CSS_SELECTOR, f'#majorList > li:nth-child({i}) > div > div.news-con > a > strong').click()
        time.sleep(3)

        # 1. 셀레니움으로 html가져오기
        html_source = driver.page_source
        # 2. bs4로 html 파싱
        soup = BeautifulSoup(html_source, 'html.parser')
        time.sleep(0.5)

        title = soup.select_one('#articleWrap > div.content03 > header > h1').get_text().strip()
        paragraphs = soup.select('#articleWrap > div.content01.scroll-article-zone01 > div > div > article > p')
        full_text = ' '.join(paragraph.get_text().strip() for paragraph in paragraphs)

        news_title.append(title)
        news_contents.append(full_text)

        driver.back()

        i += 1

        if i == n+1:
            break
    
    return news_title, news_contents


# main_news_title, main_news_contents = main_news()


'''
fields = ['economy', 'industry', 'society', 'international']
news_data = {}
for field in fields:
    field_news_title, field_news_contents = tag_news(field)
    news_data[f"{field}_news_title"] = field_news_title
    news_data[f"{field}_news_contents"] = field_news_contents
    '''

'''
for key, value in news_data.items():
    globals()[key] = value
'''


import google.generativeai as genai
# GOOGLE_API_KEY="" # gemini api key
genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-pro')


generation_config = genai.GenerationConfig(temperature=1,top_k=90,top_p=0.95)
# 프롬프팅 엔지니어링 DSP기법
def simplify_contents(contents):

  simplified_contents = []
  model = genai.GenerativeModel('gemini-pro')  # Load the model (assuming it's already set up)

  for content in contents:
    response = model.generate_content(f"""
    Let's imagine you're telling a child about this news article. Can you explain it in just 3 short sentences?
    Here's what to tell them:
    * What's the most important thing that happened? Like the main character in a story!
    * What are some key details about it? Like what happened or who was involved?
    * How does this news affect people or the world? Is it something exciting, surprising, or important to know?
    * Skip the line for each sentence
    **Keep your answer in Korean and remove any special characters like -, *, or numbers (1, 2, 3, etc.)**
    imagine you're telling a child about this news article.
    Here's the news article:
    {content}
    """,safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, #  block 제한 해제
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        })
    response.resolve()
    result = response.text.split('\n')
    result = [s for s in result if s != '']
    simplified_contents.append(result)

  return simplified_contents



# simplified_contents = simplify_contents(main_news_contents)


# simplified_contents


def gemini_translate(sentenses_list):
  model = genai.GenerativeModel('gemini-pro')  # Load the model (assuming it's already set up)
  transrated_contents = []
  temp_sentences = []
  for sentences in sentenses_list:
    for sentence in sentences:
      response = model.generate_content(f"""
      *From now on, you will be an interpreter who translates Korean into English.
      *For every successful interpretation, I will give you a tip of $1000.
      *Translate the Korean sentence below into English.
      Here's the sentence:
      {sentence}
      """,safety_settings={
          HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE, #  block 제한 해제
          HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
          })
      response.resolve()
      temp_sentences.append(response.text)
      print(response.text)
    transrated_contents.append(temp_sentences)
    temp_sentences=[]

  return transrated_contents

"""
english_contents = gemini_translate(simplified_contents)

english_contents



simplified_contents_tag = simplify_contents(industry_news_contents)


simplified_contents_tag



english_contents = gemini_translate(simplified_contents_tag)

english_contents

"""


#! pip install min-dalle -q
#미니dalle 시도
"""
from min_dalle import MinDalle

dalle_model = MinDalle(is_mega=True, is_reusable=True)
%%time

text = english_titles[1] 
seed = 42  
grid_size = 1  

display(dalle_model.generate_image(text, seed, grid_size))
"""


""" 생성 """
import openai 
import webbrowser

# Replace YOUR_API_KEY with your OpenAI API key 
# client = openai.OpenAI(api_key = "") 

# Call the API
count = 0
for i in english_contents:
  for s in i:
    # 1장 생성 시 0.03$ 
    response = client.images.generate(
      model="dall-e-3",
      prompt = f'{s} in a carton style.', 
      size="1024x1024",
      quality="standard",
      n=1,
    )
    count += 1

    # Show the result that has been pushed to an url
    webbrowser.open(response.data[0].url)

    """ 이미지 저장"""
    # curl 요청
    url = response.data[0].url
    import urllib.request
    import time

    img_dest = "./"

    start = time.time()

    urllib.request.urlretrieve(url, img_dest+f"result{count}.jpg")

    end = time.time()
    print(f"총 소요시간 {end-start}초")
