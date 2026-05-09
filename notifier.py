import os
from datetime import date
from config import OUTPUT_DIR


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


def notify(insight: str, reports: list[dict]) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    filepath = os.path.join(OUTPUT_DIR, f"브리핑_{today}.md")

    content = _build_markdown(insight, reports)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  [저장 완료] {filepath}")
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
