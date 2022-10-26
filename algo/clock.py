from apscheduler.schedulers.blocking import BlockingScheduler
import WebScraperV2.py
sched = BlockingScheduler()
scrapper = WebScrapperV2.ScrapeLazada()
@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')   
    scrapper.scrape()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()