import os
from flask import Flask, render_template, redirect, request, send_file
from python_files.extractor.site_integration import get_jobs
from python_files.modules.exporter import save_to_csv, analyze_jobs_by_site, get_time_stamp

os.system("clear")

DESIRE_PAGES = None
SELECTED_SITES = [0, 1, 2, 3]

jobs = []
db = {}
labeled_db = {}

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

app = Flask("Job-Extractor-Pro")


@app.route("/")
def root():
  return render_template("index.html")


@app.route("/report")
def report():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    from_db = db.get(keyword)
    if from_db:
      time_stamp = from_db["time_stamp"]
      jobs = from_db["db_jobs"]
    else:
      time_stamp = get_time_stamp()
      jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
      db[keyword] = {
        "time_stamp": time_stamp,
        "db_jobs": jobs
      }
    is_item = False if len(jobs["all_jobs"]) < 1 else True
  else:
    return redirect("/")
  return render_template("report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp,
  is_item=is_item
  )


@app.route("/s-report")
def s_report():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    from_db = db.get(keyword)
    if from_db:
      time_stamp = from_db["time_stamp"]
      jobs = from_db["db_jobs"]
    else:
      time_stamp = get_time_stamp()
      jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
      db[keyword] = {
        "time_stamp": time_stamp,
        "db_jobs": jobs
      }
    is_item = False if len(jobs["all_jobs"]) < 1 else True
  else:
    return redirect("/")
  return render_template("s-report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp,
  is_item=is_item
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
    is_item = False if len(jobs["all_jobs"]) < 1 else True
  else:
    return redirect("/")
  return render_template("report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp,
  is_item=is_item
  )


@app.route("/s-update")
def s_update():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    time_stamp = get_time_stamp()
    jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
    db[keyword] = {
      "time_stamp": time_stamp,
      "db_jobs": jobs
    }
    is_item = False if len(jobs["all_jobs"]) < 1 else True
  else:
    return redirect("/")
  return render_template("s-report.html", 
  searchBy=keyword,
  length=len(jobs["all_jobs"]),
  jobs=jobs["all_jobs"],
  time_stamp=time_stamp,
  is_item=is_item
  )


@app.route("/export-all")
def csv_exporter():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    from_db = db.get(keyword)
    time_stamp = from_db["time_stamp"]
    jobs = from_db["db_jobs"]["all_jobs"]
    file = save_to_csv(jobs)

    return send_file(
      file,
      mimetype='text/csv',
      attachment_filename=f"all_{keyword}_{time_stamp}.csv",
      as_attachment=True,
      cache_timeout=0
    )
  else:
    return redirect("/")


@app.route("/export-selection")
def export_selection():
  keyword = request.args.get("keyword")
  if chk_keyword_in_db(keyword):
    from_db = db.get(keyword)
    time_stamp = from_db["time_stamp"]
    jobs = from_db["db_jobs"]["all_jobs"]
    job_statistic, labeled_db[keyword] = analyze_jobs_by_site(jobs)

    return render_template("export.html",
    keyword=keyword,
    time_stamp=time_stamp,
    job_statistic=job_statistic,
  )
  else:
    return redirect("/")


@app.route("/update-db")
def update_db():
  keyword = request.args.get("keyword")
  if keyword:
    keyword = keyword.lower()
    time_stamp = get_time_stamp()
    jobs = get_jobs(keyword, SELECTED_SITES, DESIRE_PAGES)
    db[keyword] = {
      "time_stamp": time_stamp,
      "db_jobs": jobs
    }
    job_statistic, labeled_db[keyword] = analyze_jobs_by_site(jobs["all_jobs"])
    
  else:
    return redirect("/")
  return render_template("export.html",
    keyword=keyword,
    time_stamp=time_stamp,
    job_statistic=job_statistic,
  )


@app.route("/export-separately")
def export_seperately():
  keyword = request.args.get("keyword")
  site = request.args.get("site")
  time_stamp = request.args.get("time_stamp")
  
  jobs = labeled_db.get(keyword)[site]
  file = save_to_csv(jobs, f"{site}_{time_stamp}")

  return send_file(
    file,
    mimetype='text/csv',
    attachment_filename=f"{site}_{keyword}_{time_stamp}.csv",
    as_attachment=True,
    cache_timeout=0
  )

app.run(host="0.0.0.0", debug=True)