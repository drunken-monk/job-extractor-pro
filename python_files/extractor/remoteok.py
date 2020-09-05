import requests
from bs4 import BeautifulSoup


def extract_jobs_remoteok(item):
  SITE_NAME = "remoteok"
  id = item["data-id"]
  item = item.find("td", {"class": "company position company_and_position_mobile"})
  if id == None:
    return None
  title = item.find("h2").get_text(strip=True)
  company = item.find("h3").get_text(strip=True)
  try:
    company_anchor = f"https://remoteok.io/l/{id}"
  except:
    company_anchor = "No Link"
  try:
    location = item.find("span", {"class": "location"}).get_text(strip=True)
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


def extract_remoteok_htmls(url):
  jobs_remoteok = []
  result = requests.get(url)

  soup = BeautifulSoup(result.text, "html.parser")
  contents = soup.find("table", {"id": "jobsboard"})
  items = contents.find_all("tr", {"class": "job"})

  for item in items:
    refined = extract_jobs_remoteok(item)
    if refined != None:
      jobs_remoteok.append(refined)
  return jobs_remoteok


def get_jobs_remoteok(keyword, desire_pages = None):
  # this site does not have pages.
  url = f"https://remoteok.io/remote-{keyword}-jobs"

  jobs = extract_remoteok_htmls(url)
  return jobs