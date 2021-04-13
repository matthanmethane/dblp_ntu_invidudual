from os import error
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import networkx as nx
import numpy as np
import seaborn as sns
from preprocessing import ret_graph_network_year, ret_nodes,get_properties_yearly, yearly_diff,init_collab, find_pos_with_pid, find_area_with_pid, find_name_with_pid, find_man_with_pid, ret_graph_cent,get_coworker_dict_cent, draw_heatmap, centrality_top_venue_dataframe, centrality_top_venue_scatter
from faculty import load_faculty_xml, get_xml_link
from pandasgui import show
WINDOW_SIZE = "300x900"
BTN_WIDTH = "300"
BTN_HEIGHT = "10"
BG_COLOR = "#BDBDBD"

window = tk.Tk()
window.geometry(WINDOW_SIZE)
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Excel files","*.xlsx*"),("all files","*.*")))
    if("Faculty" in filename):
        global faculty_path 
        faculty_path = filename
        label_file_explorer.configure(text="Please load Top.xlsx", fg='black')
    elif("Top" in filename):
        global top_path 
        top_path = filename
        label_file_explorer.configure(text="All files loaded! Click Initilize!", fg='black')
    else:
        label_file_explorer.configure(text="Please select the correct file!", fg='red')

def init_file():
    try:
        if(faculty_path is None or top_path is None):
            messagebox.showerror("File Error!","Please load both Faculty.xlsx and Top.xlsx")
        else:
            #get_xml_link(faculty_path)
            load_faculty_xml(faculty_path)
            get_coworker_dict_cent()
            init_collab()
            messagebox.showinfo("Complete!","Initialization Finished! Click Next to continue")
            return
    except Exception as e:
        messagebox.showerror("File Error!","Please load both Faculty.xlsx and Top.xlsx")
        print(e)
#TODO: Put your network property of SCSE here
def network_scse():
    network_gui = Toplevel(main)
    network_gui.geometry(WINDOW_SIZE)
    nodes = ret_nodes()
    def get_yr_network(dummy):
        for i in range(2000,2022,1):
            G = ret_graph_network_year(yr_input = i)
            plt.subplot(6,4,i-1999)
            plt.gca().set_title(f'Year {i}')
            nx.draw(G,node_size =5)
        plt.show()
    def get_yr_df(dummy):
        df = get_properties_yearly(nodes)
        df_dif = yearly_diff(df,N=1)
        show(df_dif)
    get_yr_network_btn = tk.Button(network_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH, text ="Open Yearly Network", command = lambda: get_yr_network("dummy"))
    get_yr_network_btn.pack(side='top')
    get_yr_df_btn = tk.Button(network_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH, text ="Open Yearly DataFrame", command = lambda: get_yr_df("dummy"))
    get_yr_df_btn.pack(side='top')
    tk.Button(network_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Exit", command = network_gui.destroy).pack(side='bottom')

#Collaboration functions here
def collab():
    collab_gui = Toplevel(main)
    collab_gui.geometry(WINDOW_SIZE)
    def rank_collab(dummy):
        G = nx.Graph()
        with open("edge_list.txt", "r") as f:
            for line in f:
                a, b = line.split()
                n1 = find_pos_with_pid(a)
                n2 = find_pos_with_pid(b)

                G.add_node(n1)
                G.add_node(n2)

                if G.has_edge(n1, n2):
                    # Increase weight by 1
                    G[n1][n2]['weight'] += 1
                else:
                    # new edge. add with weight = 1
                    G.add_edge(n1, n2, weight=1)
        # Plot Heatmap
        nodes = G.nodes()
        A = nx.to_numpy_array(G, nodelist=nodes)
        sns.heatmap(A, annot=True, xticklabels=nodes, yticklabels=nodes,cmap="Blues")
        plt.show()
        plt.savefig("rank_collab_heatmap.png")
        
        # Plot Network Graph
        pos = nx.spring_layout(G, seed=7)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw(G, pos, with_labels=True)
        plt.show()
        plt.savefig("rank_collab_nwGraph.png")

    def management_collab(dummy):
        G = nx.Graph()
        with open("edge_list.txt", "r") as f:
            for line in f:
                a, b = line.split()
                n1 = find_man_with_pid(a)
                n2 = find_man_with_pid(b)

                G.add_node(n1)
                G.add_node(n2)

                if G.has_edge(n1, n2):
                    # Increase weight by 1
                    G[n1][n2]['weight'] += 1
                else:
                    # new edge. add with weight = 1
                    G.add_edge(n1, n2, weight=1)
        # Plot Network Graph
        pos = nx.spring_layout(G, seed=7)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw(G, pos, with_labels=True)
        plt.show()
        #plt.savefig("man_collab_nwGraph.png")

    def area_collab(dummy):
        G = nx.Graph()
        with open("edge_list.txt", "r") as f:
            for line in f:
                a, b = line.split()
                n1 = find_area_with_pid(a)
                n2 = find_area_with_pid(b)

                G.add_node(n1)
                G.add_node(n2)

                if G.has_edge(n1, n2):
                    # Increase weight by 1
                    G[n1][n2]['weight'] += 1
                else:
                    # new edge. add with weight = 1
                    G.add_edge(n1, n2, weight=1)
        # Plot Heatmap
        degrees = G.degree()
        nodes = G.nodes()
        A = nx.to_numpy_array(G, nodelist=nodes)
        sns.heatmap(A, annot=True, xticklabels=nodes, yticklabels=nodes,cmap="Blues")
        plt.show()
        #plt.savefig("area_collab_heatmap.png")

        # Plot Network Graph
        pos = nx.spring_layout(G, seed=7)
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        n_color = np.asarray([degrees[n] for n in nodes])
        nx.draw(G, pos=pos, with_labels=True, node_color=n_color, node_size=300, cmap=plt.cm.Blues)
        sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=4, vmax=13))
        plt.colorbar(sm)
        plt.show()
        # plt.savefig("area_collab_nwGraph.png")

    #Buttons for collaboration
    rank_collab_btn = tk.Button(collab_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Rank Colloboration", command = lambda: rank_collab("dummy"))
    mngmt_collab_btn = tk.Button(collab_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Management Collaboration", command = lambda: management_collab("dummy"))
    area_collab_btn = tk.Button(collab_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Betweenness Collaboration", command = lambda: area_collab("dummy"))
    #Placement of buttons
    rank_collab_btn.pack(side='top')
    mngmt_collab_btn.pack(side='top')
    area_collab_btn.pack(side='top')
    tk.Button(collab_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Exit", command = collab_gui.destroy).pack(side='bottom')

def excellency():
    excellency_gui = Toplevel(main)
    excellency_gui.geometry(WINDOW_SIZE)
    G = ret_graph_cent()
    
    def open_centrality(cent_type):
        if(cent_type == "degree"):
            draw_heatmap(G,nx.degree_centrality(G),"Degree Centrality")
        elif(cent_type == "eigenvector"):
            draw_heatmap(G,nx.eigenvector_centrality(G),"Betweenness Centrality")
        elif(cent_type == "betweenness"):
            draw_heatmap(G,nx.betweenness_centrality(G),"Betweenness Centrality")

    def open_cent_dataframe(dummy):
        df = centrality_top_venue_dataframe(G)
        show(df)
    def open_scatter(cen_type):
        centrality_top_venue_scatter(G,cen_type)

    degree_cen_btn = tk.Button(excellency_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Degree", command = lambda: open_centrality("degree"))
    eigenvector_cen_btn = tk.Button(excellency_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Eigenvector", command = lambda: open_centrality("eigenvector"))
    betweenness_cen_btn = tk.Button(excellency_gui,bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH, text ="Betweenness", command = lambda: open_centrality("betweenness"))
    dataframe_btn = tk.Button(excellency_gui,bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH, text="View Dataframe", command= lambda: open_cent_dataframe("dummy"))
    scatter_btn = tk.Button(excellency_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="View Scatter Plot", command = lambda: open_scatter("Degree"))


    degree_cen_btn.pack(side='top')
    eigenvector_cen_btn.pack(side='top')
    betweenness_cen_btn.pack(side='top')
    dataframe_btn.pack(side='top')
    scatter_btn.pack(side='top')
    tk.Button(excellency_gui, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Exit", command = excellency_gui.destroy).pack(side='bottom')

#TODO: Put your faculty recommendation functions here
def recommend():
    recommend = Toplevel(main)


def loadMain():
    global main
    MsgBox = tk.messagebox.askquestion ('Go to main','Are you sure you initialized the files?',icon = 'warning')
    if MsgBox == 'yes':
        main= Toplevel(window)
        main.geometry(WINDOW_SIZE)
        tk.Button(main, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="NTU SCSE Network", command = network_scse).pack(side='top')
        tk.Button(main, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Collaboration", command = collab).pack(side='top')
        tk.Button(main, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Excellency", command = excellency).pack(side='top')
        tk.Button(main, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="New Faculty Recommendation", command = recommend).pack(side='top')
        tk.Button(main, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Exit", command = main.destroy).pack(side='bottom')
    



get_file_btn  = tk.Button(window, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text ="Load File", command = browseFiles)
# Create a File Explorer label
label_file_explorer = Label(window, 
                            text = "Please load Faculty.xlsx",
                            width = 100, height = 4, 
                            fg = "black")
init_btn = tk.Button(window, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Initialize files", command = init_file)
go_main_btn = tk.Button(window, bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Next", command = loadMain)


get_file_btn.pack(side='top')
label_file_explorer.pack(side='top')
init_btn.pack(side='top')
go_main_btn.pack(side='top')
tk.Button(window,bg=BG_COLOR,height = BTN_HEIGHT, width = BTN_WIDTH,text="Exit",command=exit).pack(side='bottom')

window.mainloop()