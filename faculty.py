from bs4.element import ContentMetaAttributeValue
import pandas as pd
import requests
from bs4 import BeautifulSoup    
import lxml     

class Faculty:
    def __init__(self, name, pid, position, gender, management, area):
        self.name = name
        self.pid = pid
        self.position = position
        self.gender = gender
        self.management = management
        self.area = area
    def __str__(self) :
        return(f"{self.name}:{self.pid}")
    def __repr__(self) :
        return(f"{self.name},{self.pid},{self.position},{self.gender},{self.management},{self.area}")
    def get_name_with_pid(self,pid):
        if(self.pid == pid):
            return self.name
        else:
            return None
            



#Retrieve link for individual's XML information
def get_xml_link():
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["DBLP"])
    for index,row in df.iterrows():
        for link in row:
            r = requests.get(link)
            redirect_link = r.url
            xml_link = redirect_link.replace("html","xml")
            if("dblp.uni-trier.de" in xml_link):
                xml_new_link = xml_link.replace("dblp.uni-trier.de","dblp.org")
            else:
                xml_new_link = xml_link
            f = open("xml_link.txt","a")
            f.write(xml_new_link+'\n')
            f.close()
            print(xml_new_link)

#Download XML of individual's DBLP
def load_faculty_xml():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("xml_link.txt","r")
    xml_links = file.readlines()
    file.close()
    
    for idx, df_line in df.iterrows():
        xml_link_request = requests.get(xml_links[idx].rstrip())
        content = BeautifulSoup(xml_link_request.content,"lxml")
        author = content.find("author")["pid"]
        author_file = str(author).replace("/","_")
        #with open(r"faculty_xml/"+author_file+".xml","w", encoding='utf-8') as file:
            #file.write(str(content))
        #For testing purpose
        with open("pid.txt",'a') as file:
            file.write(author_file+'\n')
        print(author_file)
        faculty = Faculty(df_line["Faculty"],author_file,df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        print(faculty)
        faculty_list.append(faculty)
    return faculty_list




    

    

