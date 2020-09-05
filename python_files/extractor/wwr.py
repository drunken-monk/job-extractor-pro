import requests
from bs4 import BeautifulSoup


def extract_jobs_wwr(item):
  SITE_NAME = "weworkremotely"
  title = item.find("span", {"class": "title"})
  if title == None:
    return None
  title = item.find("span", {"class": "title"}).get_text(strip=True)
  company = item.find("span", {"class": "company"}).get_text(strip=True)
  try:
    company_anchor = item.select_one("li > a")["href"]
    company_anchor = f"https://weworkremotely.com{company_anchor}"
  except:
    company_anchor = "No Link"
  try:
    location = item.find("span", {"class": "region company"}).get_text(strip=True)
  except:
    location = "Anywhere"
  salary = "not opened"

  return {
    "site": SITE_NAME,
    "title": title,
    "company": company,
    "location": location,
    "salary": salary,
    "link": company_anchor
  }

def extract_wwr_htmls(url):
  jobs_wwr = []

  response = requests.get(url)
  soup = BeautifulSoup(response.text, "html.parser")
  contents = soup.find("div", {"id": "job_list"})
  items = contents.find_all("li")

  for item in items:
    refined = extract_jobs_wwr(item)
    if refined != None:
      jobs_wwr.append(refined)
  return jobs_wwr


def get_jobs_wwr(keyword, desire_pages = None):
  # this site does not have pages.
  url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}&utf8=%E2%9C%93"

  jobs = extract_wwr_htmls(url)
  return jobs