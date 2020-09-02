import os
from flask import Flask, render_template, redirect, request
#from python_files.extractor.indeed import get_jobs_indeed
#from python_files.extractor.so import get_jobs_so
from python_files.extractor.site_integration import get_jobs
from python_files.modules.exporter import save_to_csv, export_to_zip, get_time_stamp


os.system("clear")

DESIRE_PAGES = 1
SELECTED_SITES = [0]

jobs = []
db = {}

def chk_keyword_in_db(keyword):
  try:
    if not keyword:
      raise Exception()
    keyword = keyword.lower()
    jobs = db.get(keyword)
    if not jobs:
      raise Exception()
    return True
  except:
    return False

#======================================
app = Flask("Job-Extractor-Pro")

@app.route("/")
def root():
  return render_template("index.html")

@app.route("/archive")
def archive():
  return "This is archive"

@app.route("/report")
def report():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    from_db = db.get(keyword)
    if from_db:
      time_stamp = from_db["time_stamp"]
      #jobs_from_db = from_db["db_jobs"]
      jobs = from_db["db_jobs"]
    else:
      time_stamp = get_time_stamp()
      jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
      db[keyword] = {
        "time_stamp": time_stamp,
        "db_jobs": jobs
      }
  else:
    return redirect("/")
  return render_template("report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp
  )


@app.route("/update")
def update():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    time_stamp = get_time_stamp()
    jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
    db[keyword] = {
        "time_stamp": time_stamp,
        "db_jobs": jobs
      }
    
  else:
    return redirect("/")
  return render_template("report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp
  )


@app.route("/export-csv")
def csv_exporter():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    from_db = db.get(keyword)
    time_stamp = from_db["time_stamp"]
    jobs = from_db["db_jobs"]["all_jobs"]
    save_to_csv(jobs)
    return "export csv"
  else:
    return redirect("/")

@app.route("/export-zip")
def zip_exporter():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    from_db = db.get(keyword)
    time_stamp = from_db["time_stamp"]
    jobs = from_db["db_jobs"]["all_jobs"]
    export_to_zip(jobs)
    return "export zip"
  else:
    print("not")
    return redirect("/")

#os.system("pkill -9 python")
app.run(host="0.0.0.0")