import os
import csv
import datetime
import pytz

DIR_OUTPUT = "outputs"

def analyze_jobs_by_site(jobs):
  job_statistic = {}
  labeled_jobs = {}
  labeled_jobs["all"] = []
  print(len(jobs))
  for job in jobs:
    source_site = job.get("site")
    if source_site not in labeled_jobs:
      labeled_jobs[source_site] = [job]
    else:
      labeled_jobs[source_site].append(job)
    labeled_jobs["all"].append(job)
    
  for key, val in labeled_jobs.items():
    job_statistic[key] = len(val)
  #print(labeled_jobs)
  return job_statistic, labeled_jobs


def save_to_csv(jobs, file_name=None):
  if create_dir(DIR_OUTPUT):
    if file_name == None:
      file_name = f"{create_output_name()}.csv"
    dir_name = f"{DIR_OUTPUT}/{file_name}.csv"
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