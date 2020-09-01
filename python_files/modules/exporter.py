import os
import csv
import datetime
import pytz

def export_to_zip():
  pass

def save_to_csv(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)

  writer.writerow(["site", "title", "company", "location", "salary", "link"])

  for job in jobs:
    writer.writerow(list(job.value()))
  return


def create_dir(dir_name):
  try:
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
  except OSError:
    print(f"{dir_name} is already exist")


def create_dir_name():
  PREFIX = "jobs_at_"
  now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d_%H%M%S")[2:]

  return f"{PREFIX}{now}"