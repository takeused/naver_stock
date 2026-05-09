from apscheduler.schedulers.blocking import BlockingScheduler
from main import run

scheduler = BlockingScheduler(timezone="Asia/Seoul")

# 평일(월~금) 오전 9시 30분 실행
scheduler.add_job(run, "cron", day_of_week="mon-fri", hour=9, minute=30)

if __name__ == "__main__":
    print("스케줄러 시작 — 평일 09:30 자동 실행 대기 중 (종료: Ctrl+C)")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("스케줄러 종료")
