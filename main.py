import os
from flask import Flask, render_template, redirect, request
#from python_files.extractor.indeed import get_jobs_indeed
#from python_files.extractor.so import get_jobs_so
from python_files.extractor.site_integration import get_jobs
from python_files.modules.exporter import save_to_csv, export_to_zip


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
    from_caeche = db.get(keyword)
    if from_caeche:
      jobs = from_caeche
    else:
      jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
  else:
    return redirect("/")
  return render_template("report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"]
  )

@app.route("/export-csv")
def csv_exporter():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    jobs = db.get(keyword)
    save_to_csv(jobs)
    return "csv"
  else:
    return redirect("/")

@app.route("/export-zip")
def zip_exporter():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    jobs = db.get(keyword)
    export_to_zip(jobs)
    return "zip"
  else:
    return redirect("/")

#os.system("pkill -9 python")
app.run(host="0.0.0.0")