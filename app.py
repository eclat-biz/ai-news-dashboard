import streamlit as st
import feedparser
import urllib.parse
from datetime import datetime

# ページ設定
st.set_page_config(
    page_title="AI ニュース収集ダッシュボード",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# プロフェッショナル・モダンデザインのカスタムCSS
st.markdown("""
<style>
    /* 全体の背景: シンプルで清潔感のあるグレーホワイト */
    .main {
        background-color: #f4f7f9;
        color: #333;
    }
    
    /* ヘッダーデザイン: シンプルかつプロフェッショナル */
    .dashboard-header {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        color: #1a73e8; /* コーポレートブルー */
        margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e4e8;
    }
    
    /* ニュースカードのデザイン: モダンなフラットデザイン */
    .news-card-link {
        text-decoration: none !important;
        color: inherit !important;
        display: block;
        margin-bottom: 20px;
    }
    
    .news-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #e0e4e8;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease-in-out;
    }
    
    /* カードのホバー効果: 浮き上がりと色の変化 */
    .news-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(26, 115, 232, 0.1);
        border-color: #1a73e8;
    }
    
    .news-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1a73e8;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    
    .news-date {
        font-size: 0.85rem;
        color: #70757a;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
    }
    
    .news-summary {
        font-size: 0.95rem;
        color: #3c4043;
        margin-bottom: 10px;
        line-height: 1.6;
    }
    
    .read-more-btn {
        display: inline-block;
        margin-top: 5px;
        color: #1a73e8;
        font-weight: bold;
        font-size: 0.9rem;
    }

    /* サイドバーのカスタマイズ */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e4e8;
    }
    [data-testid="stSidebar"] .sidebar-content {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def fetch_google_news(query):
    """Google News RSSからニュースを取得する"""
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=ja&gl=JP&ceid=JP:ja"
    feed = feedparser.parse(url)
    return feed.entries

# サイドバー設定
st.sidebar.title("🔍 検索設定")
query = st.sidebar.text_input("キーワードを入力", value="Artificial Intelligence")
st.sidebar.markdown("---")
st.sidebar.info("Google News の RSS を使用して、指定したキーワードに関する最新情報を取得します。")

# メインコンテンツ
st.markdown(f"""
    <div class="dashboard-header">
        <h1 style="margin:0;">📰 AI ニュース収集ダッシュボード</h1>
        <p style="margin-top:10px; color:#5f6368;">「<b>{query}</b>」に関する最新ニュースを一覧表示します</p>
    </div>
""", unsafe_allow_html=True)

# ニュース取得
with st.spinner('情報を取得しています...'):
    news_items = fetch_google_news(query)

if not news_items:
    st.warning("ニュースが見つかりませんでした。別のキーワードで試してみてください。")
else:
    # ニュースをカード型で表示
    for item in news_items[:20]:
        try:
            date_str = item.published
            dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
            formatted_date = dt.strftime('%Y年%m月%d日 %H:%M')
        except:
            formatted_date = item.published
        
        # summaryから余計なHTMLを簡易的に除去
        summary_text = item.summary.split('<')[0] if '<' in item.summary else item.summary
        if not summary_text.strip():
            summary_text = "この記事の概要は、リンク先の元記事にてご確認ください。"

        st.markdown(f"""
        <a href="{item.link}" target="_blank" class="news-card-link">
            <div class="news-card">
                <div class="news-title">{item.title}</div>
                <div class="news-date">📅 更新日時: {formatted_date}</div>
                <div class="news-summary">{summary_text}</div>
                <div class="read-more-btn">元記事を詳しく読む ➜</div>
            </div>
        </a>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center style='color:#5f6368;'>© 2025 AI News Dashboard - Professional Edition</center>", unsafe_allow_html=True)
