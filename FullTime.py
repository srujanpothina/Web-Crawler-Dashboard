# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from scrapy.shell import inspect_response
import re
import urllib3
from bs4 import BeautifulSoup
import pypyodbc

db = pypyodbc.connect('Driver={SQL Server Native Client 11.0};'

                      'Server=(localdb)\MSSQLLocalDB;'

                      'Database=HR Recruiting DB;')

cursor = db.cursor()

skillarray= ['java','ruby','nodejs','c#','c++','tsql','.net','python','algorithm','jsp','j2ee','t-sql','ios','android','javascript','rest','soap','servicenow','hybris','websphere','angularjs','aws']

class Jobs:
    title=""
    company=""
    url = ""
    location=""
    salary=""
    summary=""
    max_sal=0
    min_sal=0
    skills = ""

    def __init__(self,title,url,company,location,salary,summary,max_sal,min_sal,skills):
        self.title=title
        self.url=url
        self.company=company
        self.location=location
        self.salary=salary
        self.summary=summary
        self.max_sal=max_sal
        self.min_sal = min_sal
        self.skills=skills

class FulltimeSpider(scrapy.Spider):
    name = 'FullTime'
    allowed_domains = ['www.glassdoor.com/index.htm']
    start_urls = (
        'https://www.glassdoor.com/Job/us-software-engineer-jobs-SRCH_IL.0,2_IN1_KO3,20.htm?fromAge=7&jobType=fulltime',
    )

    count = 0
    url = ""
    columns = ['Job_Title','URL','Job Type','Company','City','State','Minimum Salary','Maximum Salary','Skills']
    titles = []
    ur = []
    companies = []
    city = []
    state = []
    salaries = []
    max_sal=[]
    min_sal = []
    skills = []
    counter = 0
    def parse(self, response):

        jobs = response.xpath('//*[@class="jlGrid hover"]/li')

        job_details = []

        for job in jobs:

            title =  job.xpath('.//*[@class="flexbox"]/div/a/text()').extract()
            urlls = job.xpath('.//*[@class="flexbox"]/div/a/@href').extract()
            uls = str(response.urljoin(str(urlls[0])))
            company = job.xpath('.//*[@class="flexbox empLoc"]/div/text()').extract()
            salary =  job.xpath('.//*[@class="green small"]/text()').extract()
            max_sal,min_sal=0,0

            if len(salary)<1:
                salary = 0
                pass
            else:
                #print("salary--"+str(salary))
                if "per" in str(salary):
                    sals = re.findall('\d+', str(salary))
                    #print("salaries--"+sals)
                    min_sal,max_sal=int(sals[0])*40*4*12,int(sals[1])*40*4*12
                elif "k" in str(salary):
                    sals = re.findall('\d+', str(salary))
                    min_sal, max_sal = int(sals[0]) * 1000, int(sals[1]) * 1000
                    print(sals)
                elif "week" in str(salary):
                    sals = re.findall('\d+', str(salary))
                    min_sal, max_sal = int(sals[0]) * 4 * 12, int(sals[1]) * 4 * 12
                else:
                    min_sal, max_sal=0,0

            location = job.xpath('.//*[@class="subtle loc"]/text()').extract()
            lists = Jobs(title,uls,company,location,salary," ",max_sal,min_sal,"")
            job_details.append(lists)

        self.count = self.count + 1
        
        for i in range(0,len(job_details)):
            self.titles.append(str(job_details[i].title[0]))
            self.companies.append(str(job_details[i].company[0])[:-3])
            self.ur.append(str(job_details[i].url))
            loca = str(job_details[i].location[0]).split(',')
            if(len(loca) > 1):
                self.city.append(str(loca[0]))
                self.state.append(str(loca[1]))
            else:
                self.city.append("")
                self.state.append("")
            #print(type(job_details[i].salary))
            '''   if(job_details[i].salary > 0):
                self.salaries.append(str(job_details[i].salary[0]))
            else:
                self.salaries.append("")
            '''
            #self.salaries.append(job_details[i].salary[0])

            self.max_sal.append(job_details[i].max_sal)

            self.min_sal.append(job_details[i].min_sal)


            http = urllib3.PoolManager()
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            page = http.request('GET', job_details[i].url, headers={'User-Agent': 'Mozilla/5.0'})

            soup = BeautifulSoup(page.data, 'html.parser')
            job_desc = soup.find('div', attrs={'class': 'jobDescriptionContent desc module pad noMargBot'})
            job_desc_lower = str(job_desc).lower()
            #print(job_desc_lower)

            skillset = []

            for i in range(len(skillarray)):
                if (skillarray[i] in job_desc_lower):
                    skillset.append(skillarray[i])

            skillstring = ','.join(skillset)
            self.skills.append(skillstring)

        #rules = (Rule(SgmlLinkExtractor(allow=[

        plink = response.xpath('.//*[@class="pageNavBar noMargBot"]/div/ul/li/a/@href').extract()
        if(self.count == 1):
            Exact_URL = response.urljoin(plink[0])
        elif(self.count == 2):
            self.url = plink[1]
            Exact_URL = response.urljoin(plink[1])
        else:    
            strr = str(self.url.replace('IP'+str(self.count), 'IP'+ str(self.count + 1)))
            self.url = strr
            Exact_URL = response.urljoin(strr)    
        if(self.count < 1):
            yield scrapy.Request(Exact_URL,dont_filter=True)
        else:
            #print(len(titles))
            print(len(self.max_sal))
            print(len(self.min_sal))

            SQLCommand = ("INSERT INTO [dbo].[Jobs] "

                          "([job_title],[job_type],[company],[city],[state],[minimum_salary],[maximum_salary],[url],[skills])"

                          "VALUES (?,?,?,?,?,?,?,?,?)")

            for i in range(0,len(self.titles)):

                Values = [self.titles[i],"Full Time",self.companies[i],self.city[i],self.state[i],self.min_sal[i],self.max_sal[i],self.ur[i],self.skills[i]]
                cursor.execute(SQLCommand, Values)
                db.commit()
                '''
                cursor.execute("select max(id) from Jobs")
                job_id = (cursor.fetchone())

                my_list = self.skills[i].split(",")
                print(my_list)
                if(len(my_list)>0):
                    print(len(my_list))
                    cursor1 = db.cursor()
                    for j in my_list:

                        vals=[j]
                        query="select id from skills where skill_name=?"
                        cursor1.execute(query,vals)

                        skill_id = (cursor1.fetchone())
                        print("Skills---"+str(j) + str(skill_id))
                        query = "INSERT INTO [dbo].[skill_mapping] values(?,?)"
                        vals=[skill_id,job_id]
                        cursor1.execute(query,vals)
                        db.commit()
                db.commit()
                '''

            db.close()
            raw_data={'Job_Title':self.titles,
                      'URL':self.ur,
                      'Job Type':"Full Time",
                      'Company':self.companies,
                      'City':self.city,
                      'State':self.state,
                      #'Salary':self.salaries,
                      'Minimum Salary':self.min_sal,
                      'Maximum Salary':self.max_sal,
                      'Skills': self.skills
            }    
            df=pd.DataFrame(raw_data,columns=self.columns)
            if(df.to_csv('JobList_FullTimeNew.csv',mode='a', index=False)):
                print("Success")      


