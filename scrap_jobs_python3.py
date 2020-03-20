from bs4 import BeautifulSoup as bs
from requests import get

all_jobs = []
jobs_page = "True"
base_url = "https://www.pyjobs.com.br"
jobs_url_initial = f'{base_url}/jobs'
corrent_page_number = 1
jobs_url_page = f'{jobs_url_initial}/?page={corrent_page_number}'


def next_page():
    global corrent_page_number
    corrent_page_number += 1

    if(corrent_page_number <= number_pages):
        jobs_url_page = f'{jobs_url_initial}/?page={corrent_page_number}'
        jobs_page = get(jobs_url_page)
        print(f"Proxima Página: {jobs_url_page}")
        return(jobs_page)
    else:
        print("Não existe mais páginas!")
        return False



def get_dados(boxes):
    print("Pegando Dados...")
    for box in boxes:
        link = box.find('a')['href']
        job_page_detail = get(f'{base_url}{link}')
        bs_page_detail = bs(job_page_detail.text, 'html.parser')
        bs_page_data = bs_page_detail.find_all('ul')[1].find_all('li')
        title_job = bs_page_detail.find('h2')

        data = {
            "url": bs_page_detail.url,
            "title": title_job.text,
            "company": bs_page_data[0].text,
            "salary": bs_page_data[1].text,
            "state": bs_page_data[2].text,
            "place": bs_page_data[3].text,
            "level": bs_page_data[4].text,
            "isRemote": bs_page_data[5].text
        }

        all_jobs.append(data)
    print("Dados obtidos!\n")
    return all_jobs

def page_bs(page):
    bs_page = bs(job_page_initial.text, "html.parser")
    boxes = bs_page.find_all("div", {"class": "col-md-4"})
    return boxes

#PRIMEIRA PÁGINA
print(f"Primeira página: {jobs_url_page}")
job_page_initial = get(jobs_url_page)
bs_page = bs(job_page_initial.text, "html.parser")
number_pages = len(bs_page.find('ul', {'class': 'pagination'}).find_all('a'))
boxes = bs_page.find_all("div", {"class": "col-md-4"})
get_dados(boxes)

#PROXIMAS PÁGINAS
while (jobs_page):
    jobs_page = next_page()
    if (jobs_page):
        boxes = page_bs(jobs_page)
        get_dados(boxes)
    else:
        break


arquivo = open("jobs.txt", "w")
for job in all_jobs:
    arquivo.write(f"{job['title']}\n")
    arquivo.write(f"{job['company']}\n")
    arquivo.write(f"{job['state']}\n")
    arquivo.write(f"{job['place']}\n")
    arquivo.write(f"{job['level']}\n")
    arquivo.write(f"{job['salary']}\n")
    arquivo.write(f"{job['isRemote']}\n")
    arquivo.write(f"{job['url']}\n")
    arquivo.write('\n \n')

arquivo.close()
print("Dados salvos em jobs.txt")
