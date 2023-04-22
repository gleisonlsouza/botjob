import asyncio
import aiohttp
import bs4
import re

from links.programathor import get_programathor_links


async def get_html(link: str):
    async with aiohttp.ClientSession() as request:
        async with request.get(link) as resp:
            resp.raise_for_status()

            return await resp.text()


def get_job_info(html: str):
    soup = bs4.BeautifulSoup(html, "html.parser")

    company: str = soup.css.select_one('.wrapper-content-job-show')
    title: str = soup.css.select_one(' .wrapper-header-job-show > .container')
    job: str = soup.css.select_one(' .line-height-2-4')
    link: str = soup.find('meta', {'property': 'og:url'})
    result: str = ""

    company = company.get_text().replace('\n', '').strip()
    title = title.get_text().replace('\n', '').strip()
    job = re.sub('\n\s*\n', '\n\n', job.get_text())
    link = link.get('content')

    result = company + title + job + link

    print(4*'\n')
    print(result)


async def print_jobs():
    print('Buscando vagas, por favor aguarde...')
    see_all = False
    tasks = []
    links = await asyncio.create_task(get_programathor_links())

    for link in links:
        tasks.append(asyncio.create_task(get_html(link)))

    for task in tasks:
        html = await task

        job_info = get_job_info(html)

        if job_info:
            print(job_info)

        if not see_all:
            i = input("\nPressione Enter para continuar ou A para ver todas...: ")
            see_all = i == 'a' or i == 'A'


def main():
    asyncio.run(print_jobs())


if __name__ == '__main__':
    main()
