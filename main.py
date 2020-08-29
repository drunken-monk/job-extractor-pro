from flask import Flask, render_template

app = Flask("Job-Extractor-Pro")

@app.route("/")
def root():
  return render_template("index.html")

@app.route("/report")
def report():
  return "This is report"

@app.route("/export")
def exporter():
  return "This is exporter"

app.run(host="0.0.0.0")