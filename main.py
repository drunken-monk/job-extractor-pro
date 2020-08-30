import os
from flask import Flask, render_template
from python_files.extractor.indeed import get_jobs_indeed
from python_files.extractor.so import get_jobs_so
from python_files.modules.exporter import expert_to_zip

os.system("clear")

dict_idx_sites = {
  0: ["indeed", get_jobs_indeed],
  1: ["stack overflow", get_jobs_so]
}

DESIRE_KEYWORD = "AI"
DESIRE_PAGES = 1
SELECTED_SITES = [0, 1]

jobs = []
'''
for site_idx in SELECTED_SITES:
  jobs += dict_idx_sites[site_idx][1](DESIRE_KEYWORD, DESIRE_PAGES)


for job in jobs:
  print(job,"\n")
'''
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
  return "This is report"

@app.route("/export")
def exporter():
  return "This is exporter"

app.run(host="0.0.0.0")