from bs4 import BeautifulSoup
import requests
import time
import os

def find_jobs():
    print('Put some skills that you are unfamiliar with')
    unfamiliar_skill = input('>')
    print(f'Unfamiliar skill is {unfamiliar_skill}')
    
    skill_directory = f'post_{unfamiliar_skill}'
    if not os.path.exists(skill_directory):
        os.makedirs(skill_directory)

    for old_file in os.listdir(skill_directory):
        os.remove(os.path.join(skill_directory, old_file))

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=Python&txtLocation=&cboWorkExp1=0').text
    soup = BeautifulSoup(html_text, 'lxml')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.split(', ')
            header = job.find('header')
            more_info = header.h2.a['href']
            more_info_link = f'<a href="{more_info}">More Info</a>'
            if unfamiliar_skill.lower() not in [skill.lower() for skill in skills]:
                with open(f'{skill_directory}/{index}.txt', 'w') as f:
                    f.write(f'Company Name: {company_name.strip()}')
                    f.write(f'Required_skills: {", ".join(skills)}')
                    f.write(f'More Info: {more_info_link}')
                print(f'file saved {index}')

if __name__ == '__main':
    find_jobs()
    time_wait = 10
    print(f'Time waiting is {time_wait} seconds')
    time_sleep = time_wait * 1
