import tkinter as tk
import matplotlib.pyplot as plt
import networkx as nx
from preprocessing_mine import ret_graph,get_coworker_dict, draw_heatmap, centrality_top_venue_dataframe, centrality_top_venue_scatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandasgui import show



window = tk.Tk()

G = ret_graph()
get_coworker_dict()

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

degree_cen_btn = tk.Button(window, text ="Degree", command = lambda: open_centrality("degree"))
eigenvector_cen_btn = tk.Button(window, text ="Eigenvector", command = lambda: open_centrality("eigenvector"))
betweenness_cen_btn = tk.Button(window, text ="Betweenness", command = lambda: open_centrality("betweenness"))
dataframe_btn = tk.Button(window, text="View Dataframe", command= lambda: open_cent_dataframe("dummy"))
scatter_btn = tk.Button(window, text="View Scatter Plot", command = lambda: open_scatter("Degree"))


degree_cen_btn.pack(side='top')
eigenvector_cen_btn.pack(side='top')
betweenness_cen_btn.pack(side='top')
dataframe_btn.pack(side='top')
scatter_btn.pack(side='top')

window.mainloop()