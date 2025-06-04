# ESG Weekly News Collector Web App (Rewritten)

import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Define ESG-related news sources
NEWS_SOURCES = {
    "CSR@天下": "https://csr.cw.com.tw/",
    "CSRone": "https://csrone.com/",
    "ETtoday ESG": "https://esg.ettoday.net/",
    "The Guardian Environment": "https://www.theguardian.com/uk/environment",
    "CNN Climate": "https://edition.cnn.com/specials/world/cnn-climate",
    "BBC Environment": "https://www.bbc.com/news/science_and_environment",
    "中央社 健康環保": "https://www.cna.com.tw/list/ahel.aspx"
}

def fetch_page_soup(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        st.warning(f"⚠️ 無法連線至 {url}：{e}")
        return None

def extract_articles(soup, base_url, selector, max_articles=5):
    articles, seen_titles = [], set()
    for tag in soup.select(selector):
        title = tag.get_text(strip=True)
        href = tag.get('href')
        if not title or not href or title in seen_titles:
            continue
        seen_titles.add(title)
        if href.startswith('/'):
            href = base_url.rstrip('/') + href
        elif not href.startswith('http'):
            continue
        articles.append((title, href))
        if len(articles) >= max_articles:
            break
    return articles

def collect_all_news():
    collected_news = {}
    for name, url in NEWS_SOURCES.items():
        soup = fetch_page_soup(url)
        if not soup:
            collected_news[name] = []
            continue

        if "cw.com.tw" in url:
            selector = 'div.article-content a'
        elif "ettoday.net" in url:
            selector = 'div.piece h3 a'
        elif "guardian" in url:
            selector = 'a.u-faux-block-link__overlay'
        elif "cnn" in url:
            selector = 'h3.cd__headline a'
        elif "bbc" in url:
            selector = 'a.gs-c-promo-heading'
        elif "cna.com.tw" in url:
            selector = 'div.listBox a'
        elif "csrone" in url:
            selector = 'h5.card-title a'
        else:
            selector = 'a'

        collected_news[name] = extract_articles(soup, url, selector)
    return collected_news

def generate_notion_markdown(news_dict):
    today = datetime.today().strftime('%Y-%m-%d')
    md = f"## \U0001F331 ESG Weekly News Digest ({today})\n\n"
    for source, articles in news_dict.items():
        md += f"### {source}\n"
        if not articles:
            md += "- 無法取得新聞資料\n"
        else:
            for title, link in articles:
                md += f"- [{title}]({link})\n"
        md += "\n"
    return md

# Streamlit Web Interface
st.set_page_config(page_title="ESG News Collector", layout="wide")
st.title("\U0001F4EC ESG 每週新聞快報工具")

if st.button("🔍 擷取本週 ESG 新聞"):
    with st.spinner("擷取中，請稍候..."):
        news_results = collect_all_news()
        markdown_output = generate_notion_markdown(news_results)
        st.success("擷取完成！以下為可複製貼上的 Notion 格式：")
        st.code(markdown_output, language='markdown')

st.markdown("---")
st.markdown("由 Chris 設計的 ESG 新聞擷取工具，每週點一下就搞定資訊整理 🧠")
