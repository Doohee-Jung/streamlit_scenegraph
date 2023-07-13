
# -*- coding: utf8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import json
import pickle as pkl
import time

from PIL import Image

import sys,os
from streamlit_option_menu import option_menu
from st_click_detector import click_detector

import warnings
warnings.filterwarnings('ignore') #경고 무시용

from utils.vis import graph_visual

st.set_page_config(layout="wide")
st.markdown("""
<style>
.center {
    text-align: center; 
    font-size:250% !important;
}
""", unsafe_allow_html=True)

def Intro():
    st.markdown('<h1 class ="center"> Scene Graph를 이용한 장면(Scene) 간 유사도 </h1>', unsafe_allow_html=True)

    det_exp = """
Scene Graph를 이용하여 이미지나 영상 간 특정 <strong>장면(scene)</strong>에 대해 객체의 
<span>행위에 대한 SPO</span>를 이용하여 <strong>유사도를 산출</strong>할 수 있습니다.<br>
이번에는 행위에 대한 SPO의 <strong>⑴빈도 기반 방법</strong>과 <strong>⑵그래프의 구조 기반 방법</strong>에 대해 설명하고, 그래프의 구조 기반 방법론을 적용하여 시연을 할 수 있습니다."""

    det_exp_font = f"""<h6 style='text-align: left;font-family : times arial; 
    line-height : 165%; font-size : 117%; font-weight : 400'>{det_exp}\n\n</h6>"""


    st.markdown("#### <h1 style='text-align: left;font-size:230%'>Intro</h1>", unsafe_allow_html=True)
    
    col1,col2 = st.columns([8.5,1])

    with col1 :
        st.markdown(det_exp_font, unsafe_allow_html=True)
        st.write("")




def Explanation():
    main_ttl = "Maximum Common Subgraph(MCS) 유사도를 이용한<br>장면(Scene) 간 유사도 설명 및 예시"
    st.markdown(f""" <h1 class ="center"> {main_ttl} </h1>""", unsafe_allow_html=True)
    det_exp = """
이번에는 <strong>⑴빈도 기반 방법</strong>과 <strong>⑵그래프의 구조 기반 방법</strong> 두 가지의 유사도 설명방법을 기술하고,
그래프의 구조적 특징을 이용하여 장면 간 <strong>핵심행위</strong>를 파악하기 용이한 <strong>MCS 유사도 방법론</strong>을 이용한 장면 간 유사도의 설명과 예시를 자세히 소개합니다.<br><br>"""

    det_exp_font = f"""<h6 style='text-align: left; font-family : times arial; 
    line-height : 165%; font-size : 117%; font-weight : 400'>{det_exp}\n\n</h6>"""
    
    st.markdown("#### <h1 style='text-align: left; font-size:230%'>Explanation</h1>", 
    unsafe_allow_html=True)
    st.write("")
    
    col1,col2 = st.columns([5,1])

    with col1 :
        st.markdown(det_exp_font, unsafe_allow_html=True)
        st.write("")
    st.markdown("___")



    st.markdown("""## <h1 style='text-align: left; font-size:180%'>☑ 장면의 SPO를 통한 유사도 산출방법</h1>""", 
    unsafe_allow_html=True)
    img_1 = 'image/part2_img_1_1.PNG'
    img1 = Image.open(img_1)
    st.write("""
이미지나 영상의 장면에서 객체 및 객체의 상태나 행위를 관계로 추출할 수 있습니다.\n
이러한 객체나 관계는 그래프의 노드 혹은 엣지로 모델링 하여 **Scene Graph**로 표현할 수 있습니다.""")


    col1, col2, col3, col4 = st.columns([4.8, 0.2, 4.8, 0.2])
    
    with col1:
        title1 = "SPO 빈도 기반 장면 간 유사도 산출"
        st.markdown(f"#### <h1 style='text-align: left; font-size:150%'>{title1}</h1>",
        unsafe_allow_html=True)
        img_1 = 'image/part2_img_1_1.PNG'
        img1 = Image.open(img_1)
        img1.resize((600, 400))
        
        st.image(img1, width = 450)
    with col3:
        title1 = "동형 그래프 구조적 특성에 따른 유사도 산출"
        st.markdown(f"#### <h1 style='text-align: left; font-size:140%'>{title1}</h1>",
        unsafe_allow_html=True)
        img_2 = 'image/part2_img_1_2.PNG'
        img2 = Image.open(img_2)
        img2.resize((600, 400))
        st.write("\n")
        st.text("")
        st.text("")        

        st.image(img2, width = 450)
    
    
    col5, col6, col7, col8 = st.columns([4.8, 0.2, 4.8, 0.2])
    with col5:
        st.write("\n")
        st.write("\n")
        img1_text = """
<strong style=" font-size : 110%">• SPO 빈도 기반 장면 간 유사도 산출</strong><br>
 <strong>동일 이미지(노드)</strong> 내 두개의 <strong>동일한 객체(명사노드)</strong>가 포함<br>
 <strong>두개의 객체(명사노드)</strong>간 <strong>관계(술어엣지)</strong>가 존재<br><br>
<strong style="font-size : 110%">• 가중치 부여</strong><br>
 <strong>1)가중치를 동일하게 1(빈도 수)로 부여</strong><br>
혹은 <strong>2)특정 행위에 대한 SPO에 가중치 부여</strong><br>"""
        img1_text_html = f"""
<h6 style='text-align: left; font-family : times arial; line-height : 200%; 
font-size : 90%; font-weight : 300'>{img1_text}\n\n</h6>"""
        st.markdown(img1_text_html, unsafe_allow_html=True)
        st.text("")
    with col7:
        st.write("\n")
        st.write("\n")
        img2_text = """
<strong style="font-size : 110%"> 그래프 구조적 특성 기반 Maximum Common Subgraph(MCS) 유사도 산출</strong><br>
 두 그래프 간 겹치는 <strong>가장 큰 부분 그래프의 <i>비율</i></strong><br>
 단, 위 이미지와 같이 부분 그래프가 여러개 있을 경우,<br>
<strong>가장 큰 부분그래프의 비율</strong>로 비교<br><br>
<strong style=" font-size : 105%">• Maximum Common Subgraph(MCS)의 장점</strong><br>
가장 큰 공통 부분그래프로 그래프 구조적 특징을</br>
이용한 <strong>인과성 추론 및 핵심행위</strong> 파악"""
        img2_text_html = f"""
<h6 style='text-align: left;
font-family : times arial; line-height : 200%; 
font-size : 90%; font-weight : 500'>{img2_text}\n\n</h6>"""
        st.markdown(img2_text_html, unsafe_allow_html=True)
        st.text("")

    st.markdown("___")


#   st.markdown("""## <h1 style='text-align: left; font-size:18""")
    st.markdown("""## <h1 style='text-align: left; font-size:180%'>☑ Maximum Common Subgraph(MCS) Similarity</h1>""", 
    unsafe_allow_html=True)
    st.write("""
MCS는 Jaccard 유사도와 비슷하지만, Jaccard 유사도 달리 **최대로 겹치는** 인스턴스(노드)의 수를 비율화 한 것입니다.\n
즉, 다른 겹치는 부분 그래프의 부분적인 행위가 아닌 **핵심 행위**를 파악하여 **유사도를 산출**하는 경향이 있습니다.\n
아래 예시와 함께 살펴보겠습니다.""")
    title2 = "Maximum Common Subgraph(MCS)를 이용한 Scene Graph 구조적 유사도 산출"
    st.markdown(f"#### <h1 style='text-align: left; font-size:150%'>{title2}</h1>",
    unsafe_allow_html=True)
    img_1 = 'image/part2_img2.PNG'
    img1 = Image.open(img_1)
    img1.resize((1000, 700))
        
    st.image(img1, width = 900)
    st.text("")
    st.text("")

    img2_text = """
<strong style=" font-size : 110%">• MCS 유사도 산출 과정</strong><br>
그래프의 <strong>하나의 구성요소(Component)로 되어있는 경우</strong><br>
공통된 노드 및 엣지의 연결관계를 이용한
<strong>최대 공통 부분 그래프(Maximum Common Subgraph) 추출</strong><br>
 두 subgraph 간 공통된 노드 및 엣지의 연결관계 계산 및 비교<br>
그 중 <strong>가장 큰 공통된 부분 그래프</strong> 추출<br>
두 <i>그래프</i> 및 </i>최대 공통 부분그래프</i>의 
전체 노드수 혹은 노드와 엣지수(엣지 유형이 다른경우) 계산<br>
<strong>최대 공통 부분 그래프를 핵심 행위</strong>로써 
<strong>공통된 핵심 행위의 비율</strong>을 <strong>유사도로 계산</strong><br><br>
그래프의 <strong>구성요소(Component)가 나눠져 있는 경우</strong><br>
 <i>위와 동일한 계산식</i><br>
 위의 연산 예시와 같이 구성요소(component)가 나뉘어져 있는 경우,<br>
 동일한 그래프라도 <i>최대 공통 부분그래프</i>로 연산을 하여, 값이 1이 안나올 수 있음"""
    img2_text_html = f"""
    <h6 style='text-align: left;
    font-family : times arial; line-height : 200%; 
    font-size : 90%; font-weight : 500'>{img2_text}\n\n</h6>"""
    st.markdown(img2_text_html, unsafe_allow_html=True)
    st.text("")




def Practice():
    
    ttl_txt1_1 = """ <strong style="font-size : 110%;">유사 이미지</strong> 및 Scene Graph 추출"""
    st.markdown(f""" <h1 class ="center"> {ttl_txt1_1} </h1>""", unsafe_allow_html=True)
    st.text("")
    st.write("원하시는 이미지를 클릭하면, 아래 **유사한 이미지 10개** 및 **Scene Graph**가 출력됩니다.")

    
    
    with open(file='data/sim_dict.pkl', mode='rb') as f:
        sim_dict=pd.read_pickle(f)
    with open(file='data/spo_dict.pkl', mode='rb') as f:
        df_dict=pd.read_pickle(f)


    
    image_lst = ['61539','2370806','2368620','2344853','2343751','285795','2373302','107992','2353558','2348780','2349118']
    img_path = """https://cs.stanford.edu/people/rak248/VG_100K/"""
    imageUrls = [img_path + f"{img_num}.jpg" for img_num in image_lst]
    
    cont_lst = [f"""<a href='#' id={i}><img width='15%' src="{imageUrl}"></a>""" for i, imageUrl in enumerate(imageUrls)]
    content = "".join(cont_lst)
    clicked = click_detector(content)
    
    col01,col02 = st.columns(2)
    st.markdown("___")

    col1, col2, col3, col4, col5= st.columns([3.2, 0.2, 3.2, 0.2, 6.4])


    def showPhoto(photo,df):
        with col3:
            sim_img_num = photo[photo.rfind('/')+1:].split('.')[0]
            st.text(f"• 유사 이미지 번호 : {sim_img_num}")
            st.image(photo)
        with col5:
            graph_visual(df, 'subject','object','predicate')
        
        st.session_state.counter += 1
        if st.session_state.counter >= len(filteredImages):
            st.session_state.counter = 0
            
    with col1:
        
        if clicked is not None:
            imageurl=imageUrls[int(clicked)] if clicked else imageUrls[0]
            min_ttl1 = f"Input Image"
            st.markdown(f"""<h6 style='text-align: center; font-size:30%, font-weight = 600'>{min_ttl1}</h6>""",
            unsafe_allow_html=True)
            img_idx = int(imageurl.split('/')[-1][:-4])
            img_num_lst = sim_dict[img_idx]
            img_path = """https://cs.stanford.edu/people/rak248/VG_100K/"""
            filteredImages = [img_path + f"{img_num}.jpg" for img_num in list(img_num_lst)]
            
            st.text(f"""• 이미지 번호 {img_idx} 선택""")
            st.image(imageurl)

    with col3:
        if clicked is not None:
            if 'counter' not in st.session_state:
                st.session_state.counter = 0
            photo = filteredImages[st.session_state.counter%10]
            df_idx = img_num_lst[st.session_state.counter%10]
            show_btn = col01.button("유사한 이미지 결과 확인하기(계속)",on_click=showPhoto,args=([photo, df_dict[df_idx]]))
            col01.write("Button을 Click하면 유사한 이미지와 SceneGraph가 나옵니다.")
            min_ttl2 = f"Result 1 : Similar Image"
            st.markdown(f"""<h5 style='text-align: center;  font-size:250%, font-weight = 600'>{min_ttl2}</h5>""",
            unsafe_allow_html=True)
    with col5:
        if clicked is not None:
            min_ttl3 = f"Result 2 : Scene Graph of Similar Image"
            st.markdown(f"""<h5 style='text-align: center;  font-size:500%, font-weight = 600'>{min_ttl3}</h5>""",
                        unsafe_allow_html=True)



selected_menu = option_menu(
    None, 
    ["Intro", "Explanation", "Practice"], 
    icons = ['bookmark-check', 'file-play-fill'], 
    menu_icon = "cast", 
    default_index = 0, 
    orientation = "horizontal",
    styles = {"container": {"padding": "5!important", "background-color": "#fafafa"},
    "icon": {"font-size": "21px"},
    "nav-link": {"font-size": "19px", "text-align": "center", "margin":"0px"}
    }
   )



    
if selected_menu == "Intro":
    Intro()
elif selected_menu == 'Explanation':
    Explanation()
elif selected_menu == "Practice":
    Practice()
    
