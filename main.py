from langchain_community.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import streamlit as st
from newspaper import Article
import requests
from dotenv import load_dotenv
import os 
load_dotenv()

HuggingFaceHub_key=os.getenv("HuggingFaceHub_key")

os.environ["HUGGINGFACEHUB_API_TOKEN"]=HuggingFaceHub_key

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}
def fetch_article(arctile_url,headers=headers):
  session = requests.Session()
  try  :
    res=session.get(arctile_url,headers=headers,timeout=10)
    if res.status_code==200 :
      article = Article(arctile_url)
      article.download()
      article.parse()
      st.write("Articel Title:",article.title)
  except Exception as e:
    st.write("Error while fetching ",e)
  return article
def Summarize(arctile_url):
  article=fetch_article(arctile_url) 
  llm=HuggingFaceHub(
    repo_id="facebook/bart-large-cnn", model_kwargs={"temperature":0.5,"max_length":130}
    )
  template = """Summarize the following article.
  Title: {article_title}
  {article_text}
  """
  prompt=PromptTemplate(
    input_variables=["article_title","article_text"],
    template=template
  )
  return llm.invoke(prompt.format(article_title=article.title,article_text=article.text))
st.set_page_config(page_title='Article Summurizer', page_icon = "📰", layout = 'wide', initial_sidebar_state = 'auto')
st.title("Summarize your article")
user_prompt = st.text_input("Enter your article URL")

if st.button("Summurize") and user_prompt:
    with st.spinner("Generating..."):
        output =Summarize(user_prompt)
        st.write(output)
