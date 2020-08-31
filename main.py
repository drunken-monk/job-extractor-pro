import os
from flask import Flask, render_template, redirect, request
#from python_files.extractor.indeed import get_jobs_indeed
#from python_files.extractor.so import get_jobs_so
from python_files.extractor.site_integration import get_jobs
from python_files.modules.exporter import expert_to_zip


os.system("clear")

DESIRE_PAGES = 1
SELECTED_SITES = [0]

jobs = []
caeche = {}

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
    from_caeche = caeche.get(keyword)
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

@app.route("/export")
def exporter():
  return "This is exporter"

#os.system("pkill -9 python")
app.run(host="0.0.0.0")