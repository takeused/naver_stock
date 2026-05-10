import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import date
from config import CATEGORY_URLS, MAJOR_BROKERS, TOP_N_PER_CATEGORY

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SESSION = requests.Session()
SESSION.verify = False
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})

# 세션 쿠키 초기화 — 메인 페이지 먼저 방문
def _init_session():
    try:
        SESSION.get("https://finance.naver.com/", timeout=10)
    except Exception:
        pass

_init_session()


def _parse_views(text: str) -> int:
    try:
        return int(text.replace(",", "").strip())
    except (ValueError, AttributeError):
        return 0


def _score(views: int, max_views: int, broker: str) -> float:
    normalized = (views / max_views * 100) if max_views > 0 else 0
    bonus = 30 if broker in MAJOR_BROKERS else 0
    return normalized + bonus


def _fetch_page(url: str, page: int) -> BeautifulSoup:
    resp = SESSION.get(
        url,
        params={"page": page},
        headers={"Referer": "https://finance.naver.com/research/"},
        timeout=15,
    )
    resp.raise_for_status()
    resp.encoding = "euc-kr"
    return BeautifulSoup(resp.text, "lxml")


def get_today_reports(category: str, url: str) -> list[dict]:
    today = date.today().strftime("%y.%m.%d")
    reports = []
    page = 1

    while True:
        soup = _fetch_page(url, page)
        rows = soup.select("table.type_1 tr, table.tb_type1 tr")

        found_today = False
        stop = False

        for row in rows:
            cols = row.select("td")
            if not cols:
                continue

            date_text = cols[-2].get_text(strip=True) if len(cols) >= 2 else ""
            if not date_text:
                continue

            if date_text == today:
                found_today = True
                title_tag = row.select_one("td.title a, td.tit a, td a")
                if not title_tag:
                    continue

                title = title_tag.get_text(strip=True)

                # PDF 링크 탐색
                pdf_tag = row.select_one("a[href*='.pdf'], a[href*='pdf']")
                pdf_url = pdf_tag["href"] if pdf_tag else ""

                # 증권사 (3번째 td)
                broker_tag = row.select_one("td:nth-child(3)")
                broker = broker_tag.get_text(strip=True) if broker_tag else ""

                # 조회수 (마지막 td)
                views = _parse_views(cols[-1].get_text(strip=True)) if len(cols) >= 1 else 0

                reports.append({
                    "category": category,
                    "title": title,
                    "broker": broker,
                    "views": views,
                    "pdf_url": pdf_url,
                    "date": date_text,
                })

            elif date_text < today:
                # 오늘보다 이전 날짜가 나오면 더 이상 찾을 필요 없음
                stop = True
                break

        if stop:
            break

        next_page = soup.select_one("a.pgR, td.pgR a")
        if not next_page:
            break
        page += 1

    return reports


def select_top_reports(reports: list[dict]) -> list[dict]:
    if not reports:
        return []

    max_views = max(r["views"] for r in reports) if reports else 1
    for r in reports:
        r["score"] = _score(r["views"], max_views, r["broker"])

    return sorted(reports, key=lambda r: r["score"], reverse=True)[:TOP_N_PER_CATEGORY]


def collect_all_reports() -> list[dict]:
    selected = []
    for category, url in CATEGORY_URLS.items():
        print(f"[크롤링] {category} ...")
        try:
            reports = get_today_reports(category, url)
            print(f"  → 오늘 리포트 {len(reports)}개 수집")
            top = select_top_reports(reports)
            selected.extend(top)
        except Exception as e:
            print(f"  [오류] {category}: {e}")
    return selected


if __name__ == "__main__":
    reports = collect_all_reports()
    print(f"\n선별된 리포트 총 {len(reports)}개:")
    for r in reports:
        print(f"  [{r['category']}] {r['title']} | {r['broker']} | 조회수 {r['views']} | 점수 {r['score']:.1f}")
