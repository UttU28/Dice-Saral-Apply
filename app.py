import schedule
from time import sleep
from scrapeData import scrapeTheJobs
# from applyJobs import applyTheJobs

def job():
    # applyTheJobs()
    # sleep(1 * 60)
    scrapeTheJobs()

job()
schedule.every(20).minutes.do(job)
# Run indefinitely
while True:
    schedule.run_pending()
    sleep(1)