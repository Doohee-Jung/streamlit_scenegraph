import numpy as np
import pandas as pd
from streamlit_agraph import agraph,Node,Edge
from streamlit_agraph import Config as aconfig

def graph_visual(df,src,dst,rel,width=500,height=500):
    config = aconfig(width=width, 
            height=height,
            #   graphviz_layout=layout,
            directed=True,
            nodeHighlightBehavior=True, 
            highlightColor="#F7A7A6",
            collapsible=True,
            node={'labelProperty':'label'},
            maxZoom=2,
            minZoom=0.1,
            staticGraphWithDragAndDrop=False,
            staticGraph=False,
            initialZoom=1
            ) 

    nodes= set(df[src].values)|set(df[dst].values)
    nodes = [Node(id=i, label=i,color="#DBEBC2") for i in nodes]
    edges = [Edge(source=i, target=k,label=j,color="#F7A7A6",arrows_to=True) for i,j,k in zip(df[src],df[rel],df[dst])]
    return agraph(nodes,edges,config)
