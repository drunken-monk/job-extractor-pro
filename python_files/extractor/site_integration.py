from python_files.extractor.indeed import get_jobs_indeed
from python_files.extractor.so import get_jobs_so

DICT_IDX_SITES = {
  0: ["indeed", get_jobs_indeed],
  1: ["stack overflow", get_jobs_so]
}

def get_jobs(keyword, sites, desire_pages = None):
  jobs = {
    "all_jobs": []
  }
  for site_idx in sites:
    site_jobs = DICT_IDX_SITES[site_idx][1](keyword, desire_pages)
    jobs[DICT_IDX_SITES[site_idx][0]] = site_jobs
    jobs["all_jobs"] += site_jobs
  #jobs.add(get_jobs_indeed(keyword, desire_pages))
  #jobs.append(get_jobs_so(keyword, desire_pages))
  
  return jobs