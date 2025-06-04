import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="ESG News Finder", layout="wide")

# 模擬瀏覽器 headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

@st.cache_data
def fetch_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        st.warning(f"⚠️ 無法連線至 {url}：{e}")
        return None

def fetch_cw_news():
    url = "https://csr.cw.com.tw/"
    soup = fetch_html(url)
    news_list = []
    if soup:
        for a in soup.select("a[href^='/article/']"):
            title = a.text.strip()
            link = "https://csr.cw.com.tw" + a['href']
            if title:
                news_list.append((title, link))
    return news_list

def fetch_cna_news():
    url = "https://www.cna.com.tw/list/ahel.aspx"
    soup = fetch_html(url)
    news_list = []
    if soup:
        for div in soup.select("div.wrapper a"):
            title = div.text.strip()
            link = div['href']
            if title and link.startswith("https://"):
                news_list.append((title, link))
    return news_list

def display_news(source_name, news_list):
    st.subheader(source_name)
    if news_list:
        for title, link in news_list:
            st.markdown(f"- [{title}]({link})")
    else:
        st.info("⚠️ 找不到新聞或無法載入。")

st.title("🔍 ESG News Finder")
st.write("蒐集台灣 ESG 永續新聞網站的最新資訊")

cw_news = fetch_cw_news()
cna_news = fetch_cna_news()

col1, col2 = st.columns(2)
with col1:
    display_news("CSR@天下", cw_news)
with col2:
    display_news("中央社永續", cna_news)
