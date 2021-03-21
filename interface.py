from os import error
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import networkx as nx
from preprocessing_mine import ret_graph,get_coworker_dict, draw_heatmap, centrality_top_venue_dataframe, centrality_top_venue_scatter
from faculty import load_faculty_xml, get_xml_link
from pandasgui import show

window = tk.Tk()
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
            get_coworker_dict()
            messagebox.showinfo("Complete!","Initialization Finished! Click Next to continue")
            return
    except Exception as e:
        messagebox.showerror("File Error!","Please load both Faculty.xlsx and Top.xlsx")
        print(e)

def excellency():
    excellency_gui = Toplevel(main)
    G = ret_graph()
    
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

    degree_cen_btn = tk.Button(excellency_gui, text ="Degree", command = lambda: open_centrality("degree"))
    eigenvector_cen_btn = tk.Button(excellency_gui, text ="Eigenvector", command = lambda: open_centrality("eigenvector"))
    betweenness_cen_btn = tk.Button(excellency_gui, text ="Betweenness", command = lambda: open_centrality("betweenness"))
    dataframe_btn = tk.Button(excellency_gui, text="View Dataframe", command= lambda: open_cent_dataframe("dummy"))
    scatter_btn = tk.Button(excellency_gui, text="View Scatter Plot", command = lambda: open_scatter("Degree"))


    degree_cen_btn.pack(side='top')
    eigenvector_cen_btn.pack(side='top')
    betweenness_cen_btn.pack(side='top')
    dataframe_btn.pack(side='top')
    scatter_btn.pack(side='top')
    tk.Button(excellency_gui, text="Exit", command = excellency_gui.destroy).pack(side='bottom')


def loadMain():
    global main
    MsgBox = tk.messagebox.askquestion ('Go to main','Are you sure you initialized the files?',icon = 'warning')
    if MsgBox == 'yes':
        main= Toplevel(window)
        tk.Button(main, text="NTU SCSE Network", command = exit).pack(side='top')
        tk.Button(main, text="Collaboration", command = exit).pack(side='top')
        tk.Button(main, text="Excellency", command = excellency).pack(side='top')
        tk.Button(main, text="New Faculty Recommendation", command = exit).pack(side='top')
        tk.Button(main, text="Exit", command = main.destroy).pack(side='bottom')
    



get_file_btn  = tk.Button(window, text ="Load File", command = browseFiles)
# Create a File Explorer label
label_file_explorer = Label(window, 
                            text = "Please load Faculty.xlsx",
                            width = 100, height = 4, 
                            fg = "black")
init_btn = tk.Button(window, text="Initialize files", command = init_file)
go_main_btn = tk.Button(window, text="Next", command = loadMain)


get_file_btn.pack(side='top')
label_file_explorer.pack(side='top')
init_btn.pack(side='top')
go_main_btn.pack(side='top')
tk.Button(window,text="Exit",command=exit).pack(side='bottom')

window.mainloop()