import aiohttp
import bs4
import re


async def get_programathor_links():
    jobs_url = 'https://programathor.com.br/jobs'
    base_url = 'https://programathor.com.br'

    print('\nBuscando vaga em PROGRAMATHOR')
    async with aiohttp.ClientSession() as request:
        async with request.get(jobs_url) as resp:
            resp.raise_for_status()
            html = await resp.text()

            links = []
            soup = bs4.BeautifulSoup(html, 'html.parser')
            urls = soup.find_all('a')
            urls = list(filter(lambda x: x.get('href') != None, urls))
            urls = list(filter(lambda x: re.search('/jobs/', x.get('href'))
                        and not re.search('/jobs/page/', x.get('href')), urls))

            if urls:
                for url in urls:
                    url = url.get('href')
                    url = base_url + url
                    links.append(url)

            return links
