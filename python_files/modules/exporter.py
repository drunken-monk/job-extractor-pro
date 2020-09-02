import os
import csv
import datetime
import pytz
import shutil

DIR_OUTPUT = "outputs"

def export_to_zip(jobs):
  dir_name = f"{DIR_OUTPUT}/{create_output_name()}"
  print(dir_name)
  if create_dir(dir_name):
    dict_csv = {}
    for job in jobs:
      source_site = job.get("site")
      print(source_site)
      if source_site not in dict_csv:
        dict_csv[source_site] = {}
        dict_csv[source_site]["file"] = open(f"{dir_name}/{source_site}.csv", mode="w")
        print(dict_csv[source_site])
        dict_csv[source_site]["writer"] = csv.writer(dict_csv[source_site]["file"])
        print(dict_csv[source_site])
        dict_csv[source_site]["writer"].writerow(["site", "title", "company", "location", "salary", "link"])
      dict_csv[source_site]["writer"].writerow(list(job.values()))
    file = shutil.make_archive(dir_name, 'zip', dir_name)
  
    return file


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