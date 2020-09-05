from python_files.extractor.so import get_jobs_so
from python_files.extractor.wwr import get_jobs_wwr
from python_files.extractor.remoteok import get_jobs_remoteok
from python_files.extractor.indeed import get_jobs_indeed


DICT_IDX_SITES = {
  0: ["stack overflow", get_jobs_so],
  1: ["wwr", get_jobs_wwr],
  2: ["remoteok", get_jobs_remoteok],
  3: ["indeed", get_jobs_indeed],
}


def get_jobs(keyword, sites, desire_pages = None):
  jobs = {
    "all_jobs": []
  }
  for site_idx in sites:
    site_jobs = DICT_IDX_SITES[site_idx][1](keyword, desire_pages)
    jobs[DICT_IDX_SITES[site_idx][0]] = site_jobs
    jobs["all_jobs"] += site_jobs
  
  return jobs