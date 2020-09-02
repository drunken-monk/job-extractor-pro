import os
import csv
import datetime
import pytz

def export_to_zip():
  pass

def save_to_csv(jobs):
  file = open("jobs.csv", mode="w")
  writer = csv.writer(file)
  print("before write")
  writer.writerow(["site", "title", "company", "location", "salary", "link"])
  print("after write")
  for job in jobs:
    print(job)
    writer.writerow(list(job.values()))
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