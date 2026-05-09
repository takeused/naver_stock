from scraper import collect_all_reports
from pdf_extractor import get_report_text
from ai_analyzer import summarize_all, generate_insight
from notifier import notify


def run():
    print("=" * 50)
    print("네이버 금융 리서치 자동 브리핑 시작")
    print("=" * 50)

    # 1. 크롤링
    print("\n[1단계] 리포트 수집")
    reports = collect_all_reports()
    if not reports:
        print("오늘 리포트가 없습니다.")
        return

    # 2. PDF 텍스트 추출
    print(f"\n[2단계] PDF 텍스트 추출 ({len(reports)}개)")
    for i, report in enumerate(reports, 1):
        print(f"  [{i}/{len(reports)}] {report['title'][:30]}...")
        report["text"] = get_report_text(report.get("pdf_url", ""))

    # 3. 1차 개별 요약
    print("\n[3단계] Gemma 1차 요약")
    summaries = summarize_all(reports)

    # 4. 2차 종합 인사이트
    print("\n[4단계] Gemma 종합 인사이트 생성")
    insight = generate_insight(summaries)

    # 5. MD 파일 저장
    print("\n[5단계] MD 파일 저장")
    notify(insight, reports)

    print("\n완료!")


if __name__ == "__main__":
    run()
