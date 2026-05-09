"""크롤러 없이 샘플 데이터로 전체 파이프라인 테스트"""
from ai_analyzer import summarize_all, generate_insight
from notifier import notify

sample_reports = [
    {
        "category": "종목분석",
        "title": "삼성전자 — HBM 수주 확대 기대",
        "broker": "삼성증권",
        "views": 1500,
        "score": 100.0,
        "text": "삼성전자의 HBM3E 12단 제품이 엔비디아 퀄 테스트를 통과하면서 2025년 하반기 대규모 공급 계약이 예상된다. 목표주가 110,000원으로 상향 조정. 반도체 업황 회복과 함께 주가 re-rating 가능성 높다.",
    },
    {
        "category": "종목분석",
        "title": "SK하이닉스 — AI 서버향 HBM 독주",
        "broker": "NH투자증권",
        "views": 1200,
        "score": 90.0,
        "text": "SK하이닉스가 HBM3E 시장의 90% 이상을 점유하며 2025년 영업이익 20조원 전망. 엔비디아 B200 탑재 공급 확정. 목표주가 280,000원 유지.",
    },
    {
        "category": "산업분석",
        "title": "2차전지 산업 — 전고체 전환 가속",
        "broker": "미래에셋증권",
        "views": 980,
        "score": 85.3,
        "text": "토요타와 삼성SDI의 전고체 배터리 양산 일정이 앞당겨지면서 2027년 상용화 가능성이 대두. 에너지 밀도 400Wh/kg 달성 시 EV 시장 판도 변화 예상. 소재주 수혜 집중.",
    },
    {
        "category": "시황정보",
        "title": "코스피 2600선 공방 — 외국인 순매수 지속",
        "broker": "KB증권",
        "views": 870,
        "score": 80.0,
        "text": "외국인이 11거래일 연속 순매수. 반도체·자동차 업종 중심. 환율 1350원대 안정화가 수급 개선 견인. 단기 저항선 2650p 돌파 여부가 관건.",
    },
    {
        "category": "경제분석",
        "title": "미 연준 동결 기조 — 하반기 인하 신호",
        "broker": "한국투자증권",
        "views": 750,
        "score": 75.0,
        "text": "FOMC 의사록에서 2025년 하반기 1~2회 인하 가능성 시사. 달러 약세 전환 시 신흥국 자금 유입 기대. 국내 채권 금리 하락 압력 예상.",
    },
]

print("=== 샘플 데이터로 전체 파이프라인 테스트 ===\n")

print("[1단계] Gemma 1차 요약")
summaries = summarize_all(sample_reports)

print("\n[2단계] Gemma 종합 인사이트")
insight = generate_insight(summaries)

print("\n[3단계] MD 파일 저장")
path = notify(insight, sample_reports)

print(f"\n완료! → {path}")
