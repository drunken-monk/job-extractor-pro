import requests
from bs4 import BeautifulSoup

#LIMIT = 50
#DESIRE_KEYWORD = "python"
#URL = ""

def get_indeed_pages(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  pages = pagination.find_all("a")
  spans = []
  for page in pages[:-1]:
      spans.append(int(page.string))
  max_page = max(spans)

  return max_page

def extract_jobs_indeed(html_indeed):
  SITE_NAME = "indeed"

  title = html_indeed.find("h2", {"class": "title"})
  title = title.find("a")["title"]
  company = html_indeed.find("span", {"class": "company"})
  company_anchor = company.find("a")
  if company_anchor is not None:
      company = str(company_anchor.string)
  else:
      company = str(company.string)
  company = company.strip()
  location = html_indeed.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  salary = html_indeed.find("span", {"class": "salaryText"})
  salary = salary.string if salary is not None else "not opened"
  job_id = html_indeed["data-jk"]

  return {
    "site": SITE_NAME,
    "title": title,
    "company": company,
    "location": location,
    "salary": salary,
    "link": f"https://www.indeed.com/viewjob?jk={job_id}"
  }

def extract_indeed_htmls(last_page, url, LIMIT):
  jobs_indeed = []
  for page in range(last_page):
    print(f"=============== indeed: {page+1}page ===============")

    response = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})

    for result in results:
      jobs_indeed.append(extract_jobs_indeed(result))
  
  return jobs_indeed

def get_jobs_indeed(keyword, desire_pages = None):
  LIMIT = 50
  url = f"https://www.indeed.com/jobs?as_and={keyword}&sort=&limit={LIMIT}"

  last_page = get_indeed_pages(url) if desire_pages is None else desire_pages
  jobs = extract_indeed_htmls(last_page, url, LIMIT)
  return jobs