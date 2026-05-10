import os
import requests
from datetime import date
from config import OUTPUT_DIR, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def _build_markdown(insight: str, reports: list[dict]) -> str:
    today = date.today().strftime("%Y년 %m월 %d일")
    lines = [
        f"# 📈 {today} 증권사 리포트 브리핑",
        "",
        f"> 카테고리별 상위 리포트 {len(reports)}개 분석",
        "",
        "---",
        "",
        insight,
        "",
        "---",
        "",
        "## 📋 분석 대상 리포트 목록",
        "",
    ]

    current_category = None
    for r in reports:
        if r["category"] != current_category:
            current_category = r["category"]
            lines.append(f"### {current_category}")
        lines.append(f"- **{r['title']}** — {r['broker']} (조회수 {r['views']:,})")

    return "\n".join(lines)


def send_telegram_push(content: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("  [알림] 텔레그램 Token/Chat ID가 설정되지 않아 푸시 알림을 생략합니다.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # 텔레그램 메시지 길이 제한(4096자)을 고려하여 4000자씩 분할 전송
    max_length = 4000
    chunks = [content[i:i+max_length] for i in range(0, len(content), max_length)]
    
    for i, chunk in enumerate(chunks):
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "disable_web_page_preview": True
        }
        try:
            resp = requests.post(url, json=payload, timeout=10)
            resp.raise_for_status()
            print(f"  [푸시 완료] 텔레그램 전송 성공! ({i+1}/{len(chunks)})")
        except Exception as e:
            print(f"  [푸시 실패] 텔레그램 전송 오류: {e}")
            if hasattr(resp, "text"):
                print(f"  [에러 상세]: {resp.text}")


def notify(insight: str, reports: list[dict]) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    filepath = os.path.join(OUTPUT_DIR, f"브리핑_{today}.md")

    content = _build_markdown(insight, reports)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [저장 완료] {filepath}")

    # 텔레그램 전송
    send_telegram_push(content)

    return filepath


if __name__ == "__main__":
    sample_insight = """🔥 오늘의 핵심
→ 반도체 HBM 수요 확대 기대감 지속
→ 2차전지 소재주 주목

📊 주목 테마
→ AI 인프라: 데이터센터 투자 증가
→ 방산: 수출 계약 확대

💎 주목 종목
→ 삼성전자, SK하이닉스, LG에너지솔루션

⚠️ 리스크 요인
→ 미국 금리 인하 지연 가능성"""

    sample_reports = [
        {"category": "종목분석", "title": "삼성전자 HBM 수주 확대", "broker": "삼성증권", "views": 1200},
        {"category": "산업분석", "title": "2차전지 전고체 전환", "broker": "미래에셋증권", "views": 980},
    ]

    path = notify(sample_insight, sample_reports)
    print(f"파일 확인: {path}")
