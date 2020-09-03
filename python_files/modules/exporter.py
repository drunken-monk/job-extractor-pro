import os
import csv
import datetime
import pytz

DIR_OUTPUT = "outputs"

def analyze_jobs_by_site(jobs):
  job_statistic = {}
  labeled_jobs = {}
  for job in jobs:
    source_site = job.get("site")
    if source_site not in job_statistic:
      job_statistic[source_site] = 1
      labeled_jobs[source_site] = [job]
    else:
      job_statistic[source_site] = job_statistic.get(source_site) + 1
      labeled_jobs[source_site].append(job)
  print(job_statistic)
  return job_statistic, labeled_jobs


def save_to_csv(jobs):
  if create_dir(DIR_OUTPUT):
    dir_name = f"{DIR_OUTPUT}/{create_output_name()}.csv"
    print(dir_name)
    file = open(f"{dir_name}", mode="w")
    writer = csv.writer(file)
    writer.writerow(["site", "title", "company", "location", "salary", "link"])
    for job in jobs:
      writer.writerow(list(job.values()))
    return dir_name


def create_dir(dir_name):
  try:
    if not os.path.exists(dir_name):
      os.mkdir(dir_name)
    return True
  except OSError:
    print(f"{dir_name} is already exist")
    return False


def create_output_name():
  PREFIX = "jobs_at_"
  now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d_%H%M%S")[2:]

  return f"{PREFIX}{now}"


def get_time_stamp():
  PREFIX = ""
  now = datetime.datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y%m%d_%H%M%S")[2:]

  return f"{PREFIX}{now}"