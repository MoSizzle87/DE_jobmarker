from pathlib import Path
import datetime
import logging
import sys
import asyncio
from scrap_wttj.constants import (JOBS, RACINE_URL, TOTAL_PAGE_SELECTOR, JOB_LINK_SELECTOR,
                                  CONTRACT_INFO_SELECTOR,
                                  COMPANY_INFO_SELECTOR, CONTRACT_SELECTORS, COMPANY_SELECTORS, SKILLS_DICT,
                                  JOB_DESCRIPTION_SELECTOR)
from playwright.async_api import async_playwright
from scrap_wttj.data_extraction import extract_links, get_contract_elements, get_company_elements, get_job_skills, \
    get_raw_description
from scrap_wttj.pagination_functions import get_total_pages, get_html
from scrap_wttj.file_operations import save_file

# Setup logging
current_dir = Path(__file__).resolve().parent
logging.basicConfig(level=logging.INFO, filename=f'{current_dir}/app.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


async def generate_job_search_url(job, page_number):
    return f"https://www.welcometothejungle.com/fr/jobs?query={job.replace(' ', '%20')}&page={page_number}&aroundQuery=worldwide"


async def scrape_job_offers(browser, job, page_number):
    job_search_url = await generate_job_search_url(job, page_number)
    page = await browser.new_page()
    job_links = await extract_links(page, job_search_url, JOB_LINK_SELECTOR)
    job_offers = []

    for link in job_links:
        complete_url = f'{RACINE_URL}{link}'
        html = await get_html(complete_url)
        if html:
            job_offer = {
                'source': "welcometothejungle",
                **await get_contract_elements(html, CONTRACT_INFO_SELECTOR, CONTRACT_SELECTORS),
                'company_data': await get_company_elements(html, COMPANY_INFO_SELECTOR, COMPANY_SELECTORS),
                'skills': await get_job_skills(html, JOB_DESCRIPTION_SELECTOR, SKILLS_DICT),
                'description': await get_raw_description(html, JOB_DESCRIPTION_SELECTOR)
            }
            job_offers.append(job_offer)

    await page.close()  # Fermer la page après avoir terminé
    return job_offers


def make_hashable(data):
    """
    Recursively convert a complex data structure into an immutable form that can be used as a set element.

    Args:
    data (any): The data to convert to an immutable form. Can be a list, dict, or basic data type.

    Returns:
    tuple: An immutable representation of the input data.
    """
    if isinstance(data, dict):
        return tuple((key, make_hashable(value)) for key, value in sorted(data.items()))
    elif isinstance(data, list):
        return tuple(make_hashable(item) for item in data)
    else:
        return data


async def main():
    unique_job_offers = []
    seen_job_offers = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for job in JOBS:
            baseurl = await generate_job_search_url(job, 1)
            total_pages = await get_total_pages(baseurl, TOTAL_PAGE_SELECTOR)
            for page_number in range(1, total_pages + 1):
                job_offers = await scrape_job_offers(browser, job, page_number)
                for job_offer in job_offers:
                    hashable_job_offer = make_hashable(job_offer)
                    if hashable_job_offer not in seen_job_offers:
                        unique_job_offers.append(job_offer)
                        seen_job_offers.add(hashable_job_offer)

        await browser.close()  # Fermer le navigateur après avoir terminé

    week_number = datetime.datetime.now().isocalendar()[1]
    save_file(unique_job_offers, f'wttj_database_{week_number}.json')


if __name__ == "__main__":
    asyncio.run(main())
