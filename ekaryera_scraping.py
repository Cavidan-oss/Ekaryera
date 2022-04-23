import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime as dt




class File_Handler(object):
    
    def change_dir_to(self,path):

        if os.path.exists(os.path.join(os.getcwd(), path)):

            os.chdir(path)
            return True

        return False

    def create_folder(self, folder_name, mode = 0o666):

        
        path = os.path.join(os.getcwd(), folder_name)
        os.mkdir(path, mode)
        
        if os.path.exists(folder_name):
            return True

        return False
    
    

def get_soup(url):
    
    while True:
        try:
            request=requests.get(url)
            break
        
        except:
            print("Error Occured. Reconnecting!!!!")
    
    content=request.content

    soup=BeautifulSoup(content, 'html.parser')
    
    return soup


def background_data(url):
    
    detailed_response = get_soup(url)    
    detailed_data= detailed_response.find('div', {"class" : "job-details"})
    
    detailed_data = list(filter(lambda x:x,detailed_data.text.split('\n')))
    
    money_date = detailed_response.find('ul', {"class" : "tags-jobs"})
    money_date = list(filter(lambda x:x ,[i.text.strip('\n ') for i in money_date]))[1:3]
    
    
    is_melumat, telebler, pul, son_tarix = ":".join(detailed_data[0:2]), ":".join(detailed_data[2:]), money_date[0], money_date[1]
    
    
    return is_melumat, (' ').join(telebler.split('\xa0')), pul.split(":")[-1].strip(' '), son_tarix.split(":")[-1].strip(' ')




def get_data(soup):
    global run
    
    datas = soup.find_all("div", {"class" : 'job-listing wtabs'})
    
    if len(datas)<100:
        run = False
    
    for data in datas:
        
        new_data = list(filter(lambda x : x,data.text.strip('\n ').split('\n')))
        if len(new_data)<5:
            title, loc, time,exp = new_data 
            company = "Bilinmir"
        else:
            title, company,loc, time,exp = new_data 
    
        
        test_data = data.find('a')
        link = test_data.get('href')
        
        
        info, demand, salary, date = background_data(link)
        
        job_id = link.split('/')[-1]
        
        yield  job_id, title, company, loc, time, exp.split(":")[-1].strip(' '), info, demand, salary, date
    

run = True



def main(file_name, scratch = True, defualt_path = r'C:\Users\Cavidan\Desktop\Codees\Ekaryera'):
    
    count = 0
    os.chdir(defualt_path)

    now = dt.now()
    folder_name = now.strftime("%B_%d(%Y)")
    file = File_Handler()    
    file.change_dir_to('Data')
    
    if not os.path.exists(folder_name):
        file.create_folder(folder_name)
        
    file.change_dir_to(folder_name) 
        
   
    if scratch:
        f  =open(file_name, 'w')
        f.write(' ')
    
    
    file = open(file_name, 'a', encoding = 'utf-8')
    
    while run:
        soup = get_soup(f'https://ekaryera.az/vakansiyalar?page={count}')
        count +=1
        
        for data in get_data(soup):
    
            job_id, title, company, loc, time, exp, info, demand, salary, date = data
            info = info.replace('|', 'or')
            demand = demand.replace('|', 'or')        
            length = len((f"{job_id}|{title}|{company}|{loc}|{time}|{exp}|{info}|{demand}|{salary}|{date}" + "\n").split('|'))
            
            print(length)
            
            
            
            if length==10:
                file.write(f"{job_id}|{title}|{company}|{loc}|{time}|{exp}|{info}|{demand}|{salary}|{date}" + "\n")
            
            else:
                print(f"{job_id}|{title}|{company}|{loc}|{time}|{exp}|{info}|{demand}|{salary}|{date}" + "\n")
                
                
            
    file.close()
  


# df = pd.read_csv("Book2.csv", encoding = 'ISO-8859-1')

# column_names =  ["index", "Job_ID", 'Job_Name', 'Company', 'Location', 'Experience', 'Additional Info', 'Requirements', 'Salary', 'Last_day_to_sumbit']
# new_df = pd.read_excel("cavab.xlsx", names = column_names)    

    


main('test.csv')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    