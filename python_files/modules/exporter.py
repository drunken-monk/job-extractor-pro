import os
import csv
import datetime
import pytz
import shutil
import zipfile

DIR_OUTPUT = "outputs"

def analyze_jobs_by_site(jobs):
  job_statistic = {}
  for job in jobs:
    source_site = job.get("site")
    if source_site not in job_statistic:
      job_statistic[source_site] = 1
    else:
      job_statistic[source_site] = job_statistic.get(source_site) + 1
  print(job_statistic)
  return job_statistic


def export_to_zip(jobs):
  dir_name = f"{DIR_OUTPUT}/{create_output_name()}"
  print(dir_name)
  dict_csv = {}
  if create_dir(dir_name):
    for job in jobs:
      source_site = job.get("site")
      print(source_site)
      if source_site not in dict_csv:
        file = open(f"{dir_name}/{source_site}.csv", mode="w")
        file = open(f"{dir_name}/README.txt", mode="w")
        writer = csv.writer(file)
        dict_csv[source_site] = {
          "file": file,
          "writer": writer,
        }
        dict_csv[source_site]["writer"].writerow(["site", "title", "company", "location", "salary", "link"])
      dict_csv[source_site]["writer"].writerow(list(job.values()))
    
    zf = zipfile.ZipFile(f"{DIR_OUTPUT}/{dir_name}.zip", "w")
    for dirname, subdirs, files in os.walk(f"{dir_name}"):
      zf.write(dirname)
      for filename in files:
        zf.write(os.path.join(dirname, filename))
    zf.close()
    print(zf)
    return zf


def save_to_csv(jobs):
  if create_dir(DIR_OUTPUT):
    dir_name = f"{DIR_OUTPUT}/{create_output_name()}.csv"
    print(dir_name)
    file = open(f"{dir_name}", mode="w")
    #file = open(f"{DIR_OUTPUT}/{dir_name}.csv", mode="w")
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