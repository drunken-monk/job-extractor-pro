import requests
from bs4 import BeautifulSoup

def get_so_pages(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)
  except:
    return None

def extract_jobs_so(html_so):
  SITE_NAME = "stack_overflow"
  title = html_so.find("h2").find("a")["title"]
  company, location = html_so.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True).strip("-").strip(" \r").strip("\n")
  job_id = html_so["data-jobid"]
  
  additionals = html_so.find_all("div", {"class":"fs-caption"})
  salary = "not supported"
  
  return {
    "site": SITE_NAME,
    "title": title,
    "company": company,
    "location": location,
    "salary": salary,
    "link": f"https://stackoverflow.com/jobs/{job_id}"
  }


def extract_so_htmls(last_page, url):
  jobs_so = []
  for page in range(last_page):
    print(f"========== SO: {page+1}page ==========")
    response = requests.get(f"{url}&pg={page+1}")
    soup = BeautifulSoup(response.text, "html.parser")
    try:
      results = soup.find_all("div", {"class": "-job"})
    except:
      return []
      
    for result in results:
      job = extract_jobs_so(result)
      jobs_so.append(job)

  return jobs_so


def get_jobs_so(keyword, desire_pages = None, is_remote = "true"):
  url = f"https://stackoverflow.com/jobs?q={keyword}&sort=i&r={is_remote}"
  last_page = get_so_pages(url) if desire_pages is None else desire_pages
  if last_page != None:
    jobs_so = extract_so_htmls(last_page, url)
    return jobs_so
  else:
    return []