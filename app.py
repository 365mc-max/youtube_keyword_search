import streamlit as st
from datetime import datetime, date, timedelta, timezone

# ----------------- 페이지 기본 설정 -----------------
st.set_page_config(
    page_title="YouTube Shorts Trend Hub",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------- 컬러풀 & 생동감 넘치는 CSS 스타일링 -----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
    }

    /* 전체 배경 오로라 블러 효과 */
    .stApp {
        background: radial-gradient(circle at 10% 10%, rgba(255, 0, 51, 0.08) 0%, transparent 40%),
                    radial-gradient(circle at 90% 20%, rgba(255, 94, 0, 0.06) 0%, transparent 45%),
                    radial-gradient(circle at 50% 80%, rgba(255, 46, 99, 0.05) 0%, transparent 50%),
                    #ffffff;
        color: #1e1e24;
    }

    /* 상단 히어로 헤더 */
    .hero-container {
        text-align: center;
        padding: 35px 10px 20px 10px;
    }
    .badge-pill {
        display: inline-block;
        background: linear-gradient(135deg, rgba(255,0,0,0.1), rgba(255,100,0,0.1));
        border: 1px solid rgba(255,0,0,0.25);
        color: #e60000;
        font-weight: 700;
        font-size: 13px;
        padding: 6px 16px;
        border-radius: 999px;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        line-height: 1.2;
        background: linear-gradient(120deg, #111111 20%, #FF0033 60%, #FF6B00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    .hero-desc {
        font-size: 15px;
        color: #636e72;
        font-weight: 500;
        margin-bottom: 20px;
    }

    /* 상단 필터 제어 패널 */
    .filter-wrapper {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 0, 51, 0.18);
        border-radius: 20px;
        padding: 24px 28px;
        box-shadow: 0 10px 30px -10px rgba(255, 0, 0, 0.08);
        margin-bottom: 25px;
    }

    /* 랭킹 카드 */
    .rank-card {
        background: #ffffff;
        border-radius: 18px;
        border: 1px solid #f0f0f5;
        padding: 16px 22px;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .rank-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(255, 0, 51, 0.12);
        border-color: rgba(255, 0, 51, 0.3);
    }

    /* 랭킹 뱃지 */
    .rank-badge {
        font-size: 24px;
        font-weight: 900;
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #fdf2f2;
        color: #ff0033;
        flex-shrink: 0;
    }
    .rank-top1 {
        background: linear-gradient(135deg, #FF0033, #FF4500);
        color: white;
        box-shadow: 0 4px 12px rgba(255, 0, 51, 0.35);
    }
    .rank-top2 {
        background: linear-gradient(135deg, #FF3366, #FF6600);
        color: white;
        box-shadow: 0 4px 12px rgba(255, 51, 102, 0.3);
    }
    .rank-top3 {
        background: linear-gradient(135deg, #FF6B4A, #FFA033);
        color: white;
        box-shadow: 0 4px 12px rgba(255, 107, 74, 0.25);
    }

    /* 썸네일 */
    .thumb-wrap {
        width: 110px;
        height: 140px;
        border-radius: 14px;
        overflow: hidden;
        flex-shrink: 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }
    .thumb-wrap img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* 텍스트 메타 정보 */
    .meta-content {
        flex: 1;
        min-width: 0;
    }
    .meta-title {
        font-size: 17px;
        font-weight: 700;
        color: #111;
        text-decoration: none;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        margin-bottom: 8px;
    }
    .meta-title:hover {
        color: #FF0033;
    }
    .meta-sub {
        font-size: 13px;
        color: #888;
        display: flex;
        gap: 12px;
        align-items: center;
    }
    .channel-name {
        font-weight: 600;
        color: #333;
        background: #f5f6f8;
        padding: 3px 10px;
        border-radius: 6px;
    }

    /* 통계치 */
    .stat-container {
        text-align: right;
        flex-shrink: 0;
        padding-left: 15px;
    }
    .stat-label {
        font-size: 12px;
        color: #888;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .stat-value {
        font-size: 22px;
        font-weight: 900;
        color: #FF0033;
        letter-spacing: -0.5px;
    }

    /* 조회 버튼 스타일 */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF0033 0%, #FF4500 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        font-size: 16px;
        padding: 14px 28px;
        width: 100%;
        box-shadow: 0 6px 20px rgba(255, 0, 51, 0.35);
        transition: all 0.2s ease;
        margin-top: 10px;
    }
    div.stButton > button:first-child:hover {
        box-shadow: 0 8px 25px rgba(255, 0, 51, 0.5);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- 사이드바 설정 -----------------
with st.sidebar:
    st.markdown("### ⚙️ 대시보드 환경설정")
    API_KEY = st.text_input("YouTube Data API Key", type="password", help="키가 없으면 데모 데이터로 즉시 동작합니다.")
    st.markdown("---")
    st.markdown("🔴 **YouTube Shorts Radar**<br>지정 기간 & 키워드 랭킹 탐색기", unsafe_allow_html=True)

# ----------------- 헤더 섹션 -----------------
st.markdown("""
<div class="hero-container">
    <div class="badge-pill">⚡ REAL-TIME CALENDAR FILTER</div>
    <div class="hero-title">YouTube Shorts Trends & Ranking</div>
    <div class="hero-desc">캘린더에서 시작일과 종료일을 직접 지정하여 특정 기간의 바이럴 쇼츠를 분석하세요.</div>
</div>
""", unsafe_allow_html=True)

# ----------------- 상단 필터 패널 (캘린더 직접 지정 통합) -----------------
today = date.today()
default_start = today - timedelta(days=30)

with st.container():
    st.markdown("<div class='filter-wrapper'>", unsafe_allow_html=True)
    
    # 1행: 키워드, 국가, 정렬 기준, 조회 개수
    row1_c1, row1_c2, row1_c3, row1_c4 = st.columns([1.6, 1, 1, 1])

    with row1_c1:
        st.markdown("**🔍 검색 키워드**")
        keyword = st.text_input("검색 키워드", value="챌린지", label_visibility="collapsed")

    with row1_c2:
        st.markdown("**🌏 대상 국가**")
        country_map = {
            "한국 🇰🇷": "KR",
            "미국 🇺🇸": "US",
            "일본 🇯🇵": "JP",
            "대만 🇹🇼": "TW",
            "전세계 🌐": ""
        }
        country_selected = st.selectbox("대상 국가", list(country_map.keys()), index=0, label_visibility="collapsed")
        region_code = country_map[country_selected]

    with row1_c3:
        st.markdown("**📊 정렬 기준**")
        sort_option = st.selectbox("정렬 기준", ["조회수 순위", "좋아요 순위", "댓글 순위"], index=0, label_visibility="collapsed")

    with row1_c4:
        st.markdown("**🔢 추출 개수**")
        max_results = st.slider("추출 개수", min_value=5, max_value=50, value=10, label_visibility="collapsed")

    st.markdown("<hr style='margin: 12px 0 16px 0; border: none; border-top: 1px dashed rgba(255,0,0,0.15);'>", unsafe_allow_html=True)

    # 2행: 캘린더 날짜 범위 선택 (시작일 ~ 종료일)
    row2_c1, row2_c2 = st.columns([1.5, 2.5])
    
    with row2_c1:
        st.markdown("**📅 업로드 기간 (캘린더 선택)**")
        date_range = st.date_input(
            "기간 선택",
            value=(default_start, today),
            max_value=today,
            label_visibility="collapsed",
            help="캘린더 달력에서 시작 날짜와 종료 날짜를 차례로 클릭하세요."
        )

    # 선택된 날짜 파싱
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range
    elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
        start_date = date_range[0]
        end_date = date_range[0]
    else:
        start_date = default_start
        end_date = today

    with row2_c2:
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        st.caption(f"📌 선택된 기간: **{start_date.strftime('%Y년 %m월 %d일')} ~ {end_date.strftime('%Y년 %m월 %d일')}** 업로드 영상 필터링")

    # 조회 실행 버튼
    search_clicked = st.button("🔥 캘린더 기간 내 쇼츠 트렌드 분석하기", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- 데이터 수집/필터링 로직 -----------------
def get_mock_data():
    return [
        {
            "id": "1",
            "title": "소주과일 석류과일! 🍓 #한호흡챌린지 근데 누구세요..?",
            "channelTitle": "박다혜dahye",
            "publishedAt": "2026-08-05",
            "thumbnail": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=500&auto=format&fit=crop",
            "views": 190540834,
            "likes": 4200000,
            "comments": 23000,
            "url": "https://www.youtube.com"
        },
        {
            "id": "2",
            "title": "Who Can Save Her Cooking? 🚑💀🍲 #shorts #funny",
            "channelTitle": "CuRe 구래",
            "publishedAt": "2026-07-17",
            "thumbnail": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=500&auto=format&fit=crop",
            "views": 157263715,
            "likes": 3100000,
            "comments": 15000,
            "url": "https://www.youtube.com"
        },
        {
            "id": "3",
            "title": "The girl ate all the apples 🍎😋 #shorts #trend",
            "channelTitle": "Mert Boo",
            "publishedAt": "2026-07-20",
            "thumbnail": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500&auto=format&fit=crop",
            "views": 118117353,
            "likes": 2800000,
            "comments": 9400,
            "url": "https://www.youtube.com"
        },
        {
            "id": "4",
            "title": "Impossible Trick Shot Challenge Part 4 🎯🔥",
            "channelTitle": "Trickster Studio",
            "publishedAt": "2026-07-12",
            "thumbnail": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&auto=format&fit=crop",
            "views": 84210000,
            "likes": 1950000,
            "comments": 5800,
            "url": "https://www.youtube.com"
        }
    ]

def fetch_shorts(api_key, query, region, s_date, e_date, sort_metric, limit):
    from googleapiclient.discovery import build
    youtube = build("youtube", "v3", developerKey=api_key)
    
    # 캘린더 시작일(00:00:00 UTC) ~ 종료일(23:59:59 UTC)을 ISO8601 포맷으로 변환
    published_after = datetime.combine(s_date, datetime.min.time()).replace(tzinfo=timezone.utc).isoformat()
    published_before = datetime.combine(e_date, datetime.max.time()).replace(tzinfo=timezone.utc).isoformat()

    search_kwargs = {
        "q": f"{query} #shorts",
        "part": "id,snippet",
        "maxResults": limit,
        "type": "video",
        "videoDuration": "short",
        "publishedAfter": published_after,
        "publishedBefore": published_before
    }
    if region:
        search_kwargs["regionCode"] = region

    search_res = youtube.search().list(**search_kwargs).execute()
    video_ids = [it["id"]["videoId"] for it in search_res.get("items", []) if "videoId" in it.get("id", {})]
    
    if not video_ids:
        return []

    stats_res = youtube.videos().list(part="snippet,statistics", id=",".join(video_ids)).execute()

    items = []
    for it in stats_res.get("items", []):
        st_data = it.get("statistics", {})
        sn_data = it.get("snippet", {})
        items.append({
            "id": it["id"],
            "title": sn_data.get("title", ""),
            "channelTitle": sn_data.get("channelTitle", ""),
            "publishedAt": sn_data.get("publishedAt", "")[:10],
            "thumbnail": sn_data.get("thumbnails", {}).get("high", {}).get("url") or sn_data.get("thumbnails", {}).get("medium", {}).get("url", ""),
            "views": int(st_data.get("viewCount", 0)),
            "likes": int(st_data.get("likeCount", 0)),
            "comments": int(st_data.get("commentCount", 0)),
            "url": f"https://www.youtube.com/shorts/{it['id']}"
        })

    # 정렬 기준 반영
    if sort_metric == "조회수 순위":
        items.sort(key=lambda x: x["views"], reverse=True)
    elif sort_metric == "좋아요 순위":
        items.sort(key=lambda x: x["likes"], reverse=True)
    elif sort_metric == "댓글 순위":
        items.sort(key=lambda x: x["comments"], reverse=True)

    return items

# ----------------- 데이터 실행 및 결과 렌더링 -----------------
results = []
if search_clicked:
    if not API_KEY:
        st.toast("💡 데모 모드로 전환되어 샘플 랭킹 데이터를 표시합니다!", icon="✨")
        results = get_mock_data()
    else:
        with st.spinner("🚀 지정한 기간의 쇼츠 트렌드를 스캔하는 중..."):
            try:
                results = fetch_shorts(
                    API_KEY, 
                    keyword, 
                    region_code, 
                    start_date, 
                    end_date, 
                    sort_option, 
                    max_results
                )
            except Exception as e:
                st.error(f"데이터 수집 중 오류: {e}")
else:
    results = get_mock_data()

# ----------------- 랭킹 리스트 출력 -----------------
if results:
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; align-items:flex-end; margin: 30px 0 16px 0;'>
        <div>
            <span style='font-size:22px; font-weight:800; color:#111;'>🏆 인기 쇼츠 TOP 랭킹</span>
            <span style='font-size:14px; color:#888; margin-left:10px;'>키워드: <b>'{keyword}'</b> | {country_selected}</span>
        </div>
        <div style='font-size:14px; color:#FF0033; font-weight:700; background:rgba(255,0,51,0.06); padding:6px 14px; border-radius:8px;'>
            📅 {start_date} ~ {end_date}
        </div>
    </div>
    """, unsafe_allow_html=True)

    for idx, v in enumerate(results, start=1):
        badge_class = "rank-badge rank-top1" if idx == 1 else ("rank-badge rank-top2" if idx == 2 else ("rank-badge rank-top3" if idx == 3 else "rank-badge"))
        metric_val = v["views"] if sort_option == "조회수 순위" else (v["likes"] if sort_option == "좋아요 순위" else v["comments"])
        metric_title = sort_option.replace(" 순위", "")

        card_html = f"""
        <div class="rank-card">
            <div class="{badge_class}">{idx}</div>
            <div class="thumb-wrap">
                <img src="{v['thumbnail']}" alt="Thumbnail" />
            </div>
            <div class="meta-content">
                <a href="{v['url']}" target="_blank" class="meta-title">{v['title']}</a>
                <div class="meta-sub">
                    <span class="channel-name">📺 {v['channelTitle']}</span>
                    <span>📅 {v['publishedAt']}</span>
                </div>
            </div>
            <div class="stat-container">
                <div class="stat-label">{metric_title}</div>
                <div class="stat-value">+{metric_val:,}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
elif search_clicked:
    st.info("해당 기간 및 키워드 조건에 부합하는 쇼츠 영상이 없습니다. 날짜 범위를 넓혀보세요.")