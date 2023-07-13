# -*- coding: utf8 -*-

import sys
import requests
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import json
import io
from streamlit_option_menu import option_menu
from utils.vis import graph_visual

st.set_page_config(layout="wide")

def load_image(img_path):
    img = Image.open(img_path)
    return img

st.markdown("""
<style>
.center {
    text-align: center; 
    font-size:250% !important;
}
</style>
""", unsafe_allow_html=True)

#--File Path--------------------------------------------------------------------------------------------------------------
img_path = 'image/'
img1_path = img_path+'part1_img1.PNG'
img2_path = img_path+'part3_img1.PNG'
img3_path = img_path+'part3_img2.PNG'
img4_path = img_path+'part3_img3.PNG'
img5_path = img_path+'part3_img4.PNG'

#----------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------
abstr_text = '''
            Scenegraph Generation은 Image 및 Video 에서의 Scene에 대하여 이미지 내의 Object를 추출하고 \n
            Object간의 관계를 추출하여 Scene Graph SPO를 생성할 수 있는 기술이다. 함께 살펴보도록 하자 
             '''

#----------------------------------------------------------------------------------------------------------------

def Intro():
    st.markdown('<h1 class ="center"> Image에서 Scene Graph 생성 </h1>', unsafe_allow_html=True)
    st.write("")
    st.subheader("Intro\n")
    st.markdown('#### Scene Graph Generation은 Image 및 Video 에서의 Scene에 대하여 이미지 내의 Object를 추출하고 \
                \n #### Object간의 관계를 추출하여 Scene Graph SPO를 생성할 수 있는 기술입니다. \
                \n #### 함께 SceneGraph 생성에 대해 알아볼까요?', unsafe_allow_html=True)
    
       
    st.markdown("___")

    
    img1 = load_image(img1_path)
    st.image(img1, width=1000)
    st.markdown("___")

    
    
def Explanation():   
    st.markdown('<h1 class ="center"> Image에서 Scene Graph 생성 </h1>', unsafe_allow_html=True)
    st.write("")
    st.subheader('Background')
    st.write("")
    st.write('''
            Classification에서 부터 Detection, Segmentation, 그리고 최근에는 Captioning, Question Answering 등 \n
            Vision과 Language를 결합하는 high-level의 recognition task에 이목이 쏠리고 있습니다. \n
            이러한 고수준의 recognition task를 해결하기 위해서는 객체 인식 정도를 넘어서서, \n
            Object가 어떤 속성을 지니는지, object간의 어떤 상호작용이 있는지를 이해해야 합니다.\n
            이러한 문제를 해결하기 위해 scene graph를 도입할 수 있으며, 이러한 총체적인 정보들을 graph의 형태로 정의할 수 있습니다.\n
            하지만, bounding box, object label, relationship label 등 데이터를 만드는 것이 매우 까다로울것 같습니다. \n
            그래서 새롭게 등장한 연구 영역이 scene graph generation입니다.
            ''')    
    st.markdown("___")
    st.markdown('### 1.Node(Object) 탐지'  )
    st.write("")
    st.write("""
            객체 감지는 이미지나 비디오에서 객체를 식별하고 찾을 수 있게 해주는 컴퓨터 비전 기술입니다. \n
            이러한 객체 감지를 사용하여 장면의 객체를 식별하고 계산하고 정확한 위치를 결정합니다. \n 
            그리고 객체를 추적하는 동시에 레이블을 정확하게 지정할 수 있습니다.
            """)
    img2 = load_image(img2_path)
    st.image(img2, width=600,caption ='그림1. Mask R-CNN detecting bounding boxes and labels of objects')        
    st.write("""
            해변을 유유히 걷고 있는 그림1을 함께 살펴보시죠  \n 
            객체 감지를 사용하면 발견된 사물의 유형을 즉시 분류하는 동시에 이미지 내에서 사물의 인스턴스를 찾을 수 있습니다.
            """)
    st.markdown("___")    
    st.markdown('### 2.Edge(Relation) 예측'  )
    st.write("")
    st.write("""
            개체가 노드로 주어지면 Scene Graph Generation 모델을 적용하여 두 노드 간의 관계를 Edge로 예측합니다.
            """)
    img3 = load_image(img3_path)
    st.image(img3, width=600,caption ='그림2. Scene graph generated after node and edge predictions')           
    st.write("""
            예를 들어, "has","behind", "on" 등은 그림 2의 노드들에 대한 각 관계로 예측될 수 있습니다. \n
            예측된 노드와 엣지로 예시의 Scene 에 대한 SceneGraph를 구성할 수 있습니다.  
            """)
    st.markdown("___")    
    st.markdown('### 3.Scene Graph 예측')
    st.write("")
    st.write("""
            아래의 그림3은 스마트폰을 사용하는 모습을 SceneGraph 생성하는 예시입니다. \
            \n 각각의 객체를 잘 인식하고 객체의 label을 잘 예측하는 것을 확인할 수 있습니다.
            """)  
    col_1, col_2, = st.columns(2)
    with col_1:
        img4 = load_image(img4_path)
        st.image(img4,caption ='그림3. Scene graph generated for image')

    with col_2:
        img5 = load_image(img5_path)
        st.image(img5,caption ='그림4. Relationship labels for image')
    st.write("""
            그림4와 같이 방향이 지정된 엣지 레이블을 예측할 수 있으며, 각각의 모델의 예측점수도 함께 구할 수 있습니다. \
            \n (Phone)-[in]->(hand)의 관계 예측이 가장 높은 점수를 가지는 것을 확인할 수 있습니다. 
            """)

def Practice():
    st.markdown('<h1 class ="center"> Image에서 Scene Graph 생성 </h1>', unsafe_allow_html=True)
    st.write("")
    st.subheader("Let's practice")
    
    image_file = None
    pred_button = None
    df = None
    
    def image_extraction(img):
        resp = requests.post("http://112.221.131.146:1650/predict", files={"file": img})
        js=resp.json()
        return pd.DataFrame(js)
    

    col_1, col_2, col_3, col_4 = st.columns([4.8, 0.2, 4.8, 0.2])
    with col_1:
        st.markdown("#### 이미지를 업로드 해보세요. SceneGraph 생성을 할 수 있습니다.")
        uploadbtn = st.button("Upload Image")
        
        if "uploadbtn_state" not in st.session_state:
            st.session_state.uploadbtn_state = False

        if uploadbtn or st.session_state.uploadbtn_state:
            st.session_state.uploadbtn_state = True
            image_file = st.file_uploader("버튼을 누르거나, 사진을 마우스로 옮겨 사진을 업로드 해주세요.", type=["jpg", "jpeg","png","svg"])
        
    with col_3:
        if image_file:
            st.markdown("#### SceneGraph 생성을 해보세요.")
            file = image_file
            pred_button = st.button("Scene Graph Detection")
            bytes_data = image_file.getvalue()
            st.image(bytes_data, caption='Upload Image')
            df = image_extraction(image_file)
           
            
            if pred_button:
                st.session_state.predbtn_state = True
    
    st.markdown("___")

    col_1, col_2, col_3, col_4 = st.columns([4.8, 0.2, 4.8, 0.2])

    with col_1:
        if not pred_button or "predbtn_state" not in st.session_state :
            st.session_state.predbtn_state = False

        if st.session_state.predbtn_state: 
            with st.spinner('Wait for it...'):
                st.markdown("#### SceneGraph 모델의 생성 결과입니다.")
                st.dataframe(df)

    with col_3:
        if not pred_button or  "predbtn_state" not in st.session_state:
            st.session_state.predbtn_state = False
            
        if st.session_state.predbtn_state: 
            with st.spinner('Wait for it...'):
                st.markdown("#### SceneGraph를 시각화 합니다.")
                graph_visual(df,'SUBJECT','OBJECT','PREDICATE')


def main() :

        
    selected_menu = option_menu(
        None, 
        ["Intro","Explanation", "Practice"], 
        icons = ['bookmark-check', 'file-play-fill'], 
        menu_icon = "cast", 
        default_index = 0, 
        orientation = "horizontal",
        styles = {"container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"font-size": "21px"},
        "nav-link": {"font-size": "19px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#007AFF",}})

    if selected_menu == "Intro":
        Intro()
    if selected_menu == 'Explanation':
        Explanation()
    if selected_menu == "Practice":
        Practice() 
  


        
        

    
if __name__ == "__main__" :
    main()
    


# st.set_page_config(
#     page_title="SCENE GRAPH TUTORIAL",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )
