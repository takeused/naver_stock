import httpx
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, FLASH_MODEL, PRO_MODEL

_http = httpx.Client(verify=False)
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(httpx_client=_http),
)

HAIKU_SYSTEM = "당신은 증권사 리서치 리포트를 분석하는 전문가입니다. 핵심만 간결하게 요약합니다."

SONNET_SYSTEM = """당신은 주식시장 전문 애널리스트입니다.
여러 증권사 리포트 요약을 종합 분석하여 투자자에게 실용적인 인사이트를 제공합니다.
단순 나열이 아닌 패턴 파악과 재해석에 집중합니다."""


def summarize_report(report: dict) -> str:
    title = report.get("title", "")
    broker = report.get("broker", "")
    category = report.get("category", "")
    text = report.get("text", "")

    if not text:
        return f"[{category}] {title} ({broker}) — PDF 텍스트 추출 불가"

    prompt = f"""{HAIKU_SYSTEM}

다음 증권사 리포트를 150자 이내로 요약하세요.
조건:
- 핵심 주장 1줄
- 구체적 수치나 종목이 있으면 반드시 포함
- 150자 이내

리포트 제목: {title}
증권사: {broker}
카테고리: {category}

본문:
{text[:3000]}"""

    try:
        resp = client.models.generate_content(model=FLASH_MODEL, contents=prompt)
        return resp.text.strip()
    except Exception as e:
        print(f"  [Gemma Flash 오류] {title}: {e}")
        return f"[{category}] {title} ({broker}) — 요약 실패"


def summarize_all(reports: list[dict]) -> list[str]:
    summaries = []
    total = len(reports)
    for i, report in enumerate(reports, 1):
        print(f"  [Flash 요약 {i}/{total}] {report.get('title', '')[:30]}...")
        summary = summarize_report(report)
        summaries.append(f"[{report['category']}] {report['title']} ({report['broker']})\n{summary}")
    return summaries


def generate_insight(summaries: list[str]) -> str:
    combined = "\n\n".join(f"{i+1}. {s}" for i, s in enumerate(summaries))

    prompt = f"""{SONNET_SYSTEM}

다음은 오늘 발행된 증권사 리포트 요약입니다. 종합 분석하여 아래 형식으로 인사이트를 작성하세요.

리포트 요약:
{combined}

출력 형식 (이모지 포함, 각 섹션 명확히 구분):

🔥 오늘의 핵심 (3줄)
→ 여러 리포트에서 겹치거나 임팩트 큰 시장 메시지

📊 주목 테마
→ 반복 언급된 섹터/테마 2~3개, 주목 이유 포함

💎 주목 종목 (최대 5개)
→ 여러 리포트 언급 + 모멘텀 + 수급 흐름 기준 선별

⚠️ 리스크 요인
→ 리포트들이 경고하는 리스크"""

    try:
        resp = client.models.generate_content(model=PRO_MODEL, contents=prompt)
        return resp.text.strip()
    except Exception as e:
        print(f"  [Gemma Pro 오류]: {e}")
        return "종합 인사이트 생성 실패"


if __name__ == "__main__":
    sample_reports = [
        {
            "category": "종목분석",
            "title": "삼성전자 — HBM 수주 확대 기대",
            "broker": "삼성증권",
            "text": "삼성전자의 HBM3E 12단 제품이 엔비디아 퀄 테스트를 통과하면서 2025년 하반기 대규모 공급 계약이 예상된다. 목표주가 110,000원으로 상향 조정. 반도체 업황 회복과 함께 주가 re-rating 가능성 높다.",
        },
        {
            "category": "산업분석",
            "title": "2차전지 산업 — 전고체 전환 가속",
            "broker": "미래에셋증권",
            "text": "토요타와 삼성SDI의 전고체 배터리 양산 일정이 앞당겨지면서 2027년 상용화 가능성이 대두. 에너지 밀도 400Wh/kg 달성 시 EV 시장 판도 변화 예상. 소재주 수혜 집중.",
        },
    ]
    summaries = summarize_all(sample_reports)
    print("\n=== 1차 Flash 요약 ===")
    for s in summaries:
        print(s)
        print()
    print("\n=== 2차 Pro 인사이트 ===")
    insight = generate_insight(summaries)
    print(insight)
