*** "$ pip install -r requirements.txt" before opening the GUI ***

Guide for GUI:

1. Click Load File Button
	\n Upload your Faculty.xlsx
	\n Upload your Top.xlsx
2. Click Initialize files
	\n This will create all the txt/xml needed for the program to run
3. Click Next Button
	\n Make sure that files are initialized

\n\n\n\n






1. get_coworker_dict()
	This will create "weighted_collab.txt" which contains edges of the graph
2. ret_graph():
	This will read the "weighted_collab.txt" and return the NetworkX Graph
3. centrality_to_excel(G)
	This will create an Excel file of all centralities 
4. centrality_to_dataframe(G,cen_type)
	This will return a Pandas DataFrame for the input Centrality
	['all,'degree','eigenvector','betweenness']
5. no_top_venue_dataframe
	This will return a Pandas DataFrame of Number in top venues
6. centrality_top_venue_dataframe(G)
	This will return a Pandas DataFrame of Centralities and Number in top venues 
7. centrality_top_venue_scatter(G, cen_type)
	This will plot a scatter plot between Centrality and Number in top venue
