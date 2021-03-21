import pandas as pd
from faculty import get_xml_link,load_faculty_xml,Faculty
from bs4 import BeautifulSoup
from math import log
from scipy.optimize import curve_fit
import numpy as np
import re
import lxml
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.figure import Figure

from pandasgui import show

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
        if(faculty.pid == pid):
            return faculty.name

#Function to return list of all Faculty class
def get_faculty_list():
    faculty_list = []
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt","r")
    pid_list = file.readlines()
    pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]
    for idx, df_line in df.iterrows():
        faculty = Faculty(df_line["Faculty"],pid_list_rstrip[idx],df_line["Position"],df_line["Gender"],df_line["Management"],df_line["Area"])
        faculty_list.append(faculty)
    return faculty_list

#Function to get pid: coworker Dictonary and create file 'Weighted_collab.txt'
def get_coworker_dict():
    faculty_list = get_faculty_list()
    coauthor_dict = {}
    pid_strings = [faculty.pid for faculty in faculty_list]
    with open("weighted_collab.txt","w", encoding='utf-8') as f:
        for pid_string in pid_strings:
            file = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding='utf-8') 
            content = BeautifulSoup(file,"lxml")
            file.close()
            coauthor_pane = content.find("coauthors")
            coauthors = coauthor_pane.findAll("na")
            coauthor_pid_list = []
            for coauthor in coauthors:
                try:
                    if coauthor["pid"] in pid_strings:
                        collab_pid = coauthor["pid"]
                        author_pane = content.findAll("author",{"pid":coauthor["pid"]})
                        no_collab = len(author_pane)
                        f.write(f"{pid_string}\t{collab_pid}\t{no_collab}\n")
                        print(f"Writing... {pid_string} {collab_pid} {no_collab}")
                except Exception as e:
                    print(e)
                    continue
            coauthor_dict[pid_string] = coauthor_pid_list
    return(coauthor_dict)

def ret_graph():  
    try:
        with open("weighted_collab.txt","r", encoding='utf-8') as f:
            G = nx.read_weighted_edgelist(f)
    except:
        G = ""
    return G


#Function to get pid: Area Dictionary
def get_area_dict():
    faculty_list = get_faculty_list()
    
    area_dict = {}
    for faculty in faculty_list:
        area_dict[faculty.pid] = faculty.area

    return(area_dict)

#Function to create a heatmap Graph
def draw_heatmap(G, measures, measure_name, node_bool = True):
    pos = nx.spring_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, node_size=250,
                                    cmap = plt.cm.plasma,
                                    node_color = list(measures.values()),
                                    nodelist=list(measures.keys()))
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    labels = nx.draw_networkx_labels(G, pos)
    if(node_bool):
        edges = nx.draw_networkx_edges(G, pos)
    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis("off")
    plt.show()


#Function to create an Excel file of all centralities
def centrality_to_excel(G):
    #Get values of Centrality
    deg_cen = nx.degree_centrality(G)
    eigen_cen = nx.eigenvector_centrality(G)
    betweeness_cen = nx.betweenness_centrality(G)
    #Extract list to append
    eigen_cen_vals = [eigen_cen[key] for key in eigen_cen]
    betweeness_cen_vals = [betweeness_cen[key] for key in betweeness_cen]
    #Create a Centrality Table
    df_cen = pd.DataFrame.from_dict(deg_cen.items())
    df_cen.columns = ['ID','Degree Centrality']
    df_cen['Eigenvector Centrality'] = eigen_cen_vals
    df_cen['Betweenness Centrality'] = betweeness_cen_vals
    print(df_cen)
    df_cen.to_excel("Centrality.xlsx")  

#Function to return a DataFrame of each Centrality
def centrality_to_dataframe(G, cen_type="all"):
    if(cen_type == "all"):
        #Get values of Centrality
        deg_cen = nx.degree_centrality(G)
        eigen_cen = nx.eigenvector_centrality(G)
        betweeness_cen = nx.betweenness_centrality(G)
        #Extract list to append
        eigen_cen_vals = [eigen_cen[key] for key in eigen_cen]
        betweeness_cen_vals = [betweeness_cen[key] for key in betweeness_cen]
        #Create a Centrality Table
        df_cen = pd.DataFrame.from_dict(deg_cen, orient='index')
        df_cen.columns = ['Degree Centrality']
        df_cen['Eigenvector Centrality'] = eigen_cen_vals
        df_cen['Betweenness Centrality'] = betweeness_cen_vals
        sort_df_cen = df_cen.sort_values(by = ["Degree Centrality"], ascending=[False])
        return sort_df_cen
    elif(cen_type == "degree"):
        #Get values of Centrality
        deg_cen = nx.degree_centrality(G)
        #Create sorted Degree Centrality Table
        df_deg_cen = pd.DataFrame.from_dict(deg_cen, orient='index')
        df_deg_cen.columns = ['Degree Centrality']
        sort_df_deg_cen = df_deg_cen.sort_values(by = ['Degree Centrality'],ascending=[False])
        return(sort_df_deg_cen)
    elif(cen_type == "eigenvector"):
        #Get values of Centrality
        eigen_cen = nx.eigenvector_centrality(G)
        #Create sorted Eigenvector Centrality Table
        df_eigen_cen = pd.DataFrame.from_dict(eigen_cen, orient='index')
        df_eigen_cen.columns = ['Eigenvector Centrality']
        sort_df_eigen_cen = df_eigen_cen.sort_values(by = ['Eigenvector Centrality'],ascending=[False])
        return(sort_df_eigen_cen)
    elif(cen_type == "betweenness"):
        #Get values of Centrality
        betweeness_cen = nx.betweenness_centrality(G)
        #Create sorted Betweeness Centrality Table
        df_betweeness_cen = pd.DataFrame.from_dict(betweeness_cen, orient='index')
        df_betweeness_cen.columns = ['Betweenness Centrality']
        sort_df_betweeness_cen = df_betweeness_cen.sort_values(by = ['Betweenness Centrality'],ascending=[False])
        return(sort_df_betweeness_cen)
    else:
        return None

#Function to get DataFrame of Professor and number of Publications in the Top Venues
def no_top_venue_dataframe():
    VENUE_DICT = {
        "Data Management" : "sigmod",
        "Data Mining" : "kdd",
        "Information Retrieval" : "sigir",
        "Computer Vision" : "cvpr",
        "AI/ML" : "nips",
        "Computer Networks" : "sigcomm",
        "Cyber Security" : "ccs",
        "Software Engg" : "icse",
        "Computer Architecture" : "isca",
        "HCI" : "chi",
        "Distributed Systems" : "podc",
        "Computer Graphics" : "siggraph",
        "Bioinformatics" : "recomb",
        "Multimedia" : "mm"
    }
    VENUE_LIST = [VENUE_DICT[key] for key in VENUE_DICT]
    CONFERENCE_NAME = {
        "sigmod" : "SIGMOD Conference",
        "kdd" : "KDD",
        "sigir" : "SIGIR",
        "cvpr" : "CVPR",
        "nips" : "NeurIPS",
        "sigcomm" : "SIGCOMM",
        "ccs" : "CCS",
        "icse" : "ICSE",
        "isca" : "ISCA",
        "chi" : "CHI",
        "podc" : "PODC",
        "siggraph" : "SIGGRAPH" , #contain SIGGRAPH without @
        "recomb" : "RECOMB",
        "mm" : "ACM Multimedia",
    }

    faculty_list = get_faculty_list()
    area_list = get_area_dict()

    #TODO: The venues should match with the professor's respective subject
    faculty_venue_dict = {}
    pid_strings = [faculty.pid for faculty in faculty_list]
    for pid_string in pid_strings:
        file = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding='utf-8') 
        content = BeautifulSoup(file,"lxml")
        file.close()
        publications_pane = content.find_all("inproceedings")
        venue_list = []
        for publications in publications_pane:
            #Check if the publication is a workshop or not
            publication_booktitle = publications.find("booktitle").get_text()
            #Add to list if it is a conference, Must exclude workshops
            publication = publications["key"]
            publication_split = publication.split('/')
            publication_venue = publication_split[1]    
            if(publication_venue == VENUE_DICT[area_list[pid_string]]):
                if(publication_venue == "siggraph" and publication_booktitle == CONFERENCE_NAME[publication_venue] and not("\@" in publication_booktitle)):
                    venue_list.append(publication_venue)
                elif(publication_booktitle == CONFERENCE_NAME[publication_venue]):
                    venue_list.append(publication_venue)
        faculty_venue_dict[pid_string] = venue_list

    faculty_venue_no_dict = {}
    for key in faculty_venue_dict:
        faculty_venue_no_dict[key] = len(faculty_venue_dict[key])

    df = pd.DataFrame.from_dict(faculty_venue_no_dict, orient='index')
    df.columns = ["No.Publication in Top Venue"]
    sorted_df = df.sort_values(by = ['No.Publication in Top Venue'],ascending=[False])
    return sorted_df

#Function to return dataframe of all centralities and number of pulications in top venue
def centrality_top_venue_dataframe(G):
    df_centrality = centrality_to_dataframe(G)
    df_top_venue = no_top_venue_dataframe()
    df_centrality["No.Publication in Top Venue"] = df_top_venue["No.Publication in Top Venue"]
    df_centrality = df_centrality.rename(index = lambda x: find_name_with_pid(x))
    return(df_centrality)
#Function to show graph between centrality and number of pulications in top venue
def centrality_top_venue_scatter(G, cen_type):
    df = centrality_top_venue_dataframe(G)
    plt.scatter(df[f'{cen_type} Centrality'], df['No.Publication in Top Venue'])
    plt.title(f"{cen_type} Centrality VS No. Publication")
    plt.xlabel(f"{cen_type} Centrality")
    plt.ylabel("Number of Publication in Top Venue ")
    plt.show()
    
# node_dict = get_coworker_dict()
# G = nx.Graph(node_dict)


#centrality_top_venue_dataframe(G).to_excel("Centrality_Top_Venue.xlsx")


G = ret_graph()


    