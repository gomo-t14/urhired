import asyncio
import json
import argparse
import os
import sys
import django
from playwright.async_api import async_playwright
from asgiref.sync import sync_to_async
from libretranslatepy import LibreTranslateAPI
import time



# Set up Django environment to interface script with django 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urhired.settings')
django.setup()

#lets setup the libretranslateapi


from spiders.models import Job

job_data = []



def parse_salary(employment_types):
    if not employment_types:
        return []
    return [
        f"{t.get('from')} - {t.get('to')} {t.get('currency')}"
        for t in employment_types if t.get("from") and t.get("to")
    ]

def parse_employment(employment_types):
    if not employment_types:
        return []
    return [t.get("type") for t in employment_types if t.get("type")]

def create_check_json(industry):
    async def check_json(response):
        if 'offers' in response.url and 'page=' in response.url:
            try:
                if response.status != 200:
                    print(f"Bad response {response.status} from {response.url}")
                    return
                data = await response.json()
                offers = data.get("data", [])

                for job in offers:
                    # Directly save API data to model without translation
                    remuneration = parse_salary(job.get("employmentTypes"))
                    employment_type = parse_employment(job.get("employmentTypes"))
                    requirements = (job.get("requiredSkills") or []) + [
                        lang.get("code") for lang in job.get("languages", []) if lang.get("code")
                    ]

                    job_instance = Job(
                        job_id=job.get("guid"),
                        Industry=industry,
                        #Title=await translate_text(job.get("title")),
                        Title=job.get("title"),
                        Company=job.get("companyName"),
                        Location=job.get("city"),
                        #Remuneration=", ".join(remuneration) if remuneration else None,
                        Type_of_Work=job.get("workingTime"),
                        Experience=job.get("experienceLevel"),
                        Employment_type=", ".join(employment_type) if employment_type else None,
                        Operating_mode=job.get("workplaceType"),
                        Requirements=", ".join(requirements) if requirements else None, 
                        Url=job.get('slug'),
                    )
                    #job_instance.save()
                    #job_data.append(jobinstance)
                    await sync_to_async(job_instance.save)()
                    await sync_to_async(job_data.append)(job_instance)

            except Exception as e:
                print(f"Failed to parse JSON from {response.url}: {e}")
    return check_json

async def run(url, industry):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(url, timeout=60000)

        try:
            await page.wait_for_selector("#cookiescript_accept", timeout=5000)
            await page.click("#cookiescript_accept")
            print("Cookie prompt accepted.")
        except:
            print("No cookie prompt appeared.")

        page.on("response", create_check_json(industry))

        # Scroll down 3 times with wait, triggering API calls
        for _ in range(3):
            await page.keyboard.press("End")
            await page.wait_for_timeout(7000)

        await browser.close()

    return job_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape job data from JustJoin.it and RocketJobs.pl")
    parser.add_argument("--url", required=True, help="The URL to scrape")
    parser.add_argument("--industry", required=True, help="Industry designation for the job data")
    args = parser.parse_args()

    results = asyncio.run(run(args.url, args.industry))
    print(f"\nCollected {len(results)} job offers.\n")
    for item in results[:3]:
        print({
            "job_id": item.job_id,
            "Title": item.Title,
            "Company": item.Company,
            "Location": item.Location,
            "Url": item.Url
        })
