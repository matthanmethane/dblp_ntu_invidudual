import pandas as pd
from faculty import get_xml_link,load_faculty_xml,Faculty
from bs4 import BeautifulSoup
from math import log
from scipy.optimize import curve_fit
import numpy as np
import lxml
import networkx as nx
import matplotlib.pyplot as plt
import collections

def find_name_with_pid(pid):
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
    for faculty in faculty_list:
        print(faculty)
        if(faculty.pid == pid):
            return faculty.name

def get_coworker_dict():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
    

    coauthor_dict = {}
    pid_strings = [faculty.pid for faculty in faculty_list]
    for pid_string in pid_strings:
        file = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding='utf-8') 
        content = BeautifulSoup(file,"lxml")
        file.close()
        coauthor_pane = content.find("coauthors")
        
        coauthors = coauthor_pane.findAll("na")
        coauthor_pid_list = []
        for coauthor in coauthors:
            try:
                if coauthor["pid"] in pid_list_rstrip:
                    coauthor_pid_list.append(coauthor["pid"])
            except:
                continue
        coauthor_dict[pid_string] = coauthor_pid_list

    return(coauthor_dict)

def degree_histogram(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    for key in degreeCount:
        degreeCount[key] = degreeCount[key]/(G.number_of_edges())
    deg, cnt = zip(*degreeCount.items())

    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.80, color="b")

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)

    # draw graph in inset
    plt.axes([0.4, 0.4, 0.5, 0.5])
    Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
    pos = nx.spring_layout(G)
    plt.axis("off")
    nx.draw_networkx_nodes(G, pos, node_size=20)
    nx.draw_networkx_edges(G, pos, alpha=0.4)
    plt.show()

def degree_histogram_loglog(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    degreeCountLog = {}
    for key in degreeCount:
        try:
            log_pk = log(key)
            log_k = log(degreeCount[key]/(G.number_of_edges()))
            degreeCountLog[log_pk] = log_k
        except:
            continue
    deg, cnt = zip(*degreeCountLog.items())
    plt.scatter(deg,cnt)

    z = np.polyfit(deg, cnt, 1)
    p = np.poly1d(z)
    plt.plot(deg,p(deg),"r--")



    plt.show()



node_dict = get_coworker_dict()

G = nx.Graph(node_dict)
#degree_histogram_loglog(G)
nx.draw(G)
plt.show()
