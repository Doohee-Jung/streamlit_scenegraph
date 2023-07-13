# -*- coding: utf8 -*-

import streamlit as st
from st_click_detector import click_detector

from PIL import Image
import pandas as pd
import numpy as np
import networkx as nx
import pickle as pkl
import time
import sys,os

import warnings
warnings.filterwarnings('ignore')
from streamlit_option_menu import option_menu

from utils.vis import graph_visual

st.set_page_config(layout="wide")

st.markdown("""
<style>
.center {
    text-align: center; 
    font-size:250% !important;
}
""", unsafe_allow_html=True)

tbl_scene=pd.read_pickle('data/tbl_scene.pkl')

def get_spo(Subject, Predicate, Object):
    condition = ((tbl_scene.subject == Subject)&(tbl_scene.predicate == Predicate)&(tbl_scene.object == Object))
    img_lst=list(tbl_scene.loc[condition]['image_id'].values[:10])
    groups=tbl_scene.loc[tbl_scene['image_id'].isin(img_lst)].groupby('image_id')            
    return  dict(list(groups))

def load_image(img_path):
    img = Image.open(img_path)
    return img


def Intro():
    st.markdown('<h1 class ="center"> Scene Graph란?</h1>', unsafe_allow_html=True)

    det_exp = """
                Scene Graph(장면 그래프)란 이미지 및 영상 데이터의 <strong>장면(scene)에서 객체(object) 및 관계(relationship)를 추출</strong>하고 이를 
                <strong>주어-술어-목적어' 관계인 SPO(Subject, Predicate, Object) 형태로 그래프를 통해 표현</strong>하는 방법입니다.<br><br>
                &nbsp본 R&D는 기존 장면의 객체들 간의 관계의 SPO를 
                <strong>그래프 데이터 베이스(GDB)</strong>를 이용한 <strong>지식그래프(Knowledge Graph)</strong>로 표현하여, 관계기반 데이터의 조회 및 추출을 편리하게하고
                더 나아가 이미지나 영상의 장면 유사도, 예측 그리고 자동화 시스템을 만드는 것을 목표로 합니다."""
    
    det_exp_font = f"""<h6 style='text-align: left; font-family : times arial; 
    line-height : 165%; font-size : 117%; font-weight : 400'>{det_exp}\n\n</h6>"""


    st.markdown("#### <h1 style='text-align: left;  font-size:230%'>Intro</h1>", unsafe_allow_html=True)
    st.write("")
    
    col1,col2 = st.columns([8.5, 1])

    with col1 :
        st.markdown(det_exp_font, unsafe_allow_html=True)
        st.write("")



def Explanation():

    st.markdown("### <h1 style='text-align: center;font-size:270%'>그래프 데이터베이스(GDB)를 이용한 Scene Graph</h1>", unsafe_allow_html=True)
    
    det_exp = """
                &nbsp이번 챕터에는 <strong>그래프 데이터 베이스(GDB)</strong>를 사용하여 
                Scene Graph를 <strong>지식그래프(Knowledge Graph) 형태</strong>로 표현합니다.<br><br>
                &nbspScene Graph를 GDB의 강점인 <strong>속성(property)</strong>정보를 이용한 
                LPG(Labeled Property Graph) 형태로 모델링하여 단어 간의 SPO의 관계를 유연하게 설명하고, 다양한 그래프 알고리즘 등을 사용할 수 있습니다."""
    
    det_exp_font = f"""<h6 style='text-align: left;  font-family : times arial; 
    line-height : 165%; font-size : 117%; font-weight : 400'>{det_exp}\n\n</h6>"""


    st.markdown("#### <h1 style='text-align: left;  font-size:230%'>Explanation</h1>", unsafe_allow_html=True)
    st.write("")
    
    col1,col2 = st.columns([8.5,1])

    with col1 :
        st.markdown(det_exp_font, unsafe_allow_html=True)
        st.write("")
    st.markdown("___")
#----------------------------------------------------------------------------------------------------------------
    st.markdown("""## <h1 style='text-align: left; font-size:180%'>☑ GDB를 이용한 Scene Graph 모델링</h1>""", unsafe_allow_html=True)
    img_2 = 'image/part1_img2.PNG'
    img2 = load_image(img_2)
    text2 = """
            Scene Graph의 모델링 방법론은 ⑴술어(predicate)를 하나의 노드로 따로 표현하는 방식과 ⑵술어를 엣지로써 표현하는 두 가지 방식이 있습니다.\n
            두 그래프 모델링 방법과 지식그래프화를 하기 위해 어떤 것이 효율적인지에 대해 설명합니다."""
    st.write(text2)

    st.text("")
    st.image(img2, width=1000)
    st.text("")

    img2_text = """
            <strong style=" font-size : 120%">• 술어(predicate)를 <i>노드(node)</i>로 그래프 모델링하는 경우</strong><br>
            &nbsp&nbsp&nbsp&nbsp◦ 일반적으로 Scene Graph 모델링 시 속성(property)정보가 없는 RDF(Resource Description Framework) 
            형태의<br>
            &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp그래프로써 가장 많이 사용하는 기법<br>
            &nbsp&nbsp&nbsp&nbsp◦ 술어를 노드로 표현하여 직관적일 수 있지만, <i>노드의 수가 많아져서 연산량 증가</i><br><br>
            <strong style="font-size : 120%">• 술어(predicate)를 <i>엣지(edge)</i>로 그래프 모델링하는 경우</strong><br>
            &nbsp&nbsp&nbsp&nbsp◦ 객체 간 관계를 나타내는 <strong>술어를 엣지</strong>로 표현하여 기존 SPO의 형태를 유연하게 나타낸 그래프 모델링<br>
            &nbsp&nbsp&nbsp&nbsp◦ GDB의 <i>속성정보를 이용</i>하여 술어에 대한 부가 정보를 엣지의 속성정보로 삽입 가능<br>
            &nbsp&nbsp&nbsp&nbsp◦ 술어를 엣지로 표현하여 노드로 표현했을 때보다 <strong>적은 용량의 DB모델 및 연산속도 감소</strong>"""
    #st.wrtie(img1_text)
    img2_text_html = f"""
    <h6 style='text-align: left;
    font-family : times arial; line-height : 200%; 
    font-size : 100%; font-weight : 500'>{img2_text}\n\n</h6>"""
    st.markdown(img2_text_html, unsafe_allow_html=True)
    st.text("")
#----------------------------------------------------------------------------------------------------------------

def Practice1():

    ttl_txt1_1 = "☑ 이미지를 이용한 및 SPO Scene Graph 추출"
    st.markdown(f""" <h1 class ="center"> {ttl_txt1_1} </h1>""", unsafe_allow_html=True)
   
    st.text("")
    st.write("원하시는 이미지를 클릭하면, 아래 Scene Graph가 출력됩니다.")
    
    image_lst = ['2320618','2335472','2343076','61539','2370806','2368620','2344853','2343751','285795','2348780','2349118','2353558']
    img_path = """https://cs.stanford.edu/people/rak248/VG_100K/"""
    imageUrls = [img_path + f"{img_num}.jpg" for img_num in image_lst]
    cont_lst = [f"""<a href='#' id={i}><img width='15%' src="{imageUrl}"></a>""" for i, imageUrl in enumerate(imageUrls)]
    content = "".join(cont_lst)
    clicked = click_detector(content)


    df=tbl_scene.loc[tbl_scene['image_id'].apply(lambda x : x in image_lst)]
    groups=df.groupby('image_id')
    df_dict = dict(list(groups))

    st.markdown("___")

    if clicked is not None:
        imageurl=imageUrls[int(clicked)] if clicked else imageUrls[0]
        img_idx = imageurl.split('/')[-1][:-4]
        st.text(f"• 이미지 번호 {img_idx}를 선택하셨습니다.")


        col_1, col_2, col_3, col_4 = st.columns([3.5, 0.2, 7.1, 0.2])


        with col_1:
            
            if clicked is not None:

                min_ttl1 = f"Result 1 : selected <i>Image</i>"
                st.markdown(f"""## <h5 style='text-align: center; font-size:250%, font-weight = 600'>{min_ttl1}</h5>""", 
                        unsafe_allow_html=True)
                
                with st.spinner('Loading for Scene Graph...⌛️'):
                    time.sleep(0.5)

                    st.image(imageurl, width = 500)
                   
                    
                
        with col_3:

            min_ttl2 = f"Result 2 : <i>Scene Graph</i> of selected Image"
            st.markdown(f"""## <h5 style='text-align: center; font-size:250%, font-weight = 100'>{min_ttl2}</h5>""", 
                        unsafe_allow_html=True)

            if clicked is not None:

                graph_visual(df_dict[img_idx],'subject','object','predicate',width=900,height=800)

    else:
        pass

        
        # 1) 이미지 번호로 이미지 추출




def Practice2():


    ttl_txt1_1 = "☑ SPO를 이용한 이미지 및 해당 이미지에 대한 Scene Graph 추출"
    st.markdown(f"""## <h1 class ="center">{ttl_txt1_1}</h1>""", unsafe_allow_html=True)
    st.text("")

    col_a, col_b = st.columns([2, 1])
    
    with col_a:
        st.write("이미지에 검색할 **주어, 술어, 목적어**(**SPO**)를 입력해주세요.")
    with col_b:
        q_btn = st.radio(label = '질의 종류', options = ['단일 질의', '복합 질의'], label_visibility = 'collapsed')
        st.write('<style>div.row-widget.stRadio > div{flex-direction : row;}</style>', unsafe_allow_html=True)

    st.write("")

    sub2img_msg1 = "이미지를 검색할 **주어**(**Subject**)를 입력해주세요."
    pred2img_msg1 = "이미지를 검색할 **술어**(**Predicate**)를 입력해주세요."
    obj2img_msg1 = "이미지를 검색할 **목적어**(**Object**)를 입력해주세요."

# -------------------------------------------------------- 단일 질의 (下)--------------------------------------------------------
    try:
        if q_btn == "단일 질의":
        
            # 기본적으로 전체 selectbox가 빈값이 될수는 없어서 첫번째 selectbox만 'man'으로 지정해주기
            ## 추후 다른 값들은 디폴트가 아니라 selectbox list의 첫번째 요소로 넣어서 바로 나오게하기
            ### n번째 selectbox에 따라 가능한 항목 list들만 나오게함
            sub_list1 = sorted(list(set(list(tbl_scene['subject'].values))), reverse = False) 
            default_ix1 = sub_list1.index('man')
            pred_input1 = ""
            obj_input1 = ""

            col1 , col2, col3 = st.columns(3)
            with col1:
                sub_input1 = st.selectbox(label = sub2img_msg1, options = sub_list1,
                                    key = 1, disabled = False, index = default_ix1)
                sub_input1.lower() # 소문자로 전부 통일


            with col2:
                if sub_input1 != "":
                    pred_list1 = sorted(list(set(list(tbl_scene.loc[tbl_scene.subject == sub_input1]['predicate'].values))),
                                        reverse = False)
                    pred_list1.insert(0, 'playing')
                    pred_input1 = st.selectbox(label = pred2img_msg1, options = pred_list1,
                                    key = 2, disabled = False)
                    pred_input1.lower() # 소문자로 전부 통일
                #st.write(pred_list)


            with col3:
                if sub_input1 != "" and pred_input1 != "" :
                    obj_list1 = sorted(list(set(list(tbl_scene.loc[(tbl_scene.subject == sub_input1)&
                                                                (tbl_scene.predicate == pred_input1)]['object'].values))),
                                                                reverse = False)
                    obj_list1.insert(0, 'soccer')
                    
                    obj_input1 = st.selectbox(label = obj2img_msg1, options = obj_list1,
                                        key = 3, disabled = False)#, index = default_ix3)
                    obj_input1.lower() # 소문자로 전부 통일
            col01,col02,col03=st.columns(3)
        

            if sub_input1 != "" and pred_input1 != "" and obj_input1 != "":

                img_dic = get_spo(sub_input1, pred_input1, obj_input1) #이미지와 해당 SPO테이블이 dictionary 형태로 저장되는 함수
                img_number = len(img_dic.keys())
                with col02:
                    img_number_txt1 = f"<strong><i>{img_number}</i></strong> - Image is detected ❗"
                    st.markdown(f"""<span style='text-align: left; font-size:120%'>{img_number_txt1}</span>""", unsafe_allow_html=True)
                st.markdown("___")
                            
                if img_number > 0:
            
                    col1, col2, col3, col4 = st.columns([4.8, 0.2, 4.8, 0.2])

                    if 'counter' not in st.session_state: 
                        st.session_state.counter = 0

                    # Get list of images in folder
                    img_num_lst =  list(img_dic.keys())
                    img_path =  """https://cs.stanford.edu/people/rak248/VG_100K/"""
                    filteredImages = [img_path + f"{img_num}.jpg" for img_num in img_num_lst]
                    
                    #filteredImages = [image_resize(image) for image in filteredImages]
                    def showPhoto(photo, df):
                        ## Increments the counter to get next photo
                        st.session_state.counter += 1
                        if st.session_state.counter >= len(filteredImages):
                            st.session_state.counter = 0

                        with col03:
                            img_number_txt2 = f"<strong style='font-size:150%'><i>{st.session_state.counter + 1}</i></strong>(th) out of {img_number}"
                            st.markdown(f"""###### {img_number_txt2}""", unsafe_allow_html=True)

                        with col1:
                            res_ttl1 = f"Result 1 : <strong style = 'font-size : 120%'><i>Image</i></strong> matched by SPO"
                            st.markdown(f"""##### {res_ttl1}""",
                                        unsafe_allow_html=True)
                            st.image(photo)
                        with col3: 
                            res_ttl2 = f"Result 2 : <strong style = 'font-size : 120%'><i>Scene Graph</i></strong> of Image matched by SPO"
                            st.markdown(f"""##### {res_ttl2}""",
                                        unsafe_allow_html=True)
                            graph_visual(df, 'subject','object','predicate')


                    

                    # Select photo a send it to button
                    photo = filteredImages[st.session_state.counter%img_number]
                    df_idx = img_num_lst[st.session_state.counter%img_number]
                    show_btn = col01.button("이미지 검색 결과 확인하기(계속)⏭️",on_click = showPhoto, args = ([photo, img_dic[df_idx]]))

            
            if sub_input1 == "":
                st.write("❗ 주어를 입력(선택)해주세요")
            if pred_input1 == "":
                st.write("❗ 술어를 입력(선택)해주세요")
            if obj_input1 == "":
                st.write("❗ 목적어를 입력(선택)해주세요")
            if sub_input1 == "" and pred_input1 == "" and obj_input1 == "":
                st.write("❗ **주어** 혹은 **술어** 혹은 **목적어**를 ***전부*** 입력해주세요.")
    except:
        st.write("Not Matched Image ❗")
# -------------------------------------------------------- 단일 질의 (上)--------------------------------------------------------

# -------------------------------------------------------- 복합 질의 (下)--------------------------------------------------------

    if q_btn == "복합 질의":

        # -------------------------------------- 복합질의 내 조건1(단일 질의 조건) (下)--------------------------------------------

        # 기본적으로 전체 selectbox가 빈값이 될수는 없어서 첫번째 selectbox만 'man'으로 지정해주기
        ## 추후 다른 값들은 디폴트가 아니라 selectbox list의 첫번째 요소로 넣어서 바로 나오게하기
        ### n번째 selectbox에 따라 가능한 항목 list들만 나오게함
        sub_list1 = sorted(list(set(list(tbl_scene['subject'].values))), reverse = False)  
        default_ix1 = sub_list1.index('man')
        pred_input1 = ""
        obj_input1 = ""

        col1 , col2, col3 = st.columns(3)
        with col1:
            sub_input1 = st.selectbox(label = sub2img_msg1, options = sub_list1,
                                key = 1, disabled = False, index = default_ix1)
            sub_input1.lower() # 소문자로 전부 통일


        with col2:
            if sub_input1 != "":
                pred_list1 = sorted(list(set(list(tbl_scene.loc[tbl_scene.subject == sub_input1]['predicate'].values))), reverse = False)
                pred_list1.insert(0, 'playing')
                pred_input1 = st.selectbox(label = pred2img_msg1, options = pred_list1,
                                key = 2, disabled = False)
                pred_input1.lower() # 소문자로 전부 통일
            #st.write(pred_list)


        with col3:
            if sub_input1 != "" and pred_input1 != "" :
                obj_list1 = sorted(
                    list(set(list(tbl_scene.loc[(tbl_scene.subject == sub_input1)&(tbl_scene.predicate == pred_input1)]['object'].values))),
                    reverse = False)
                obj_list1.insert(0, 'tennis')
                
                obj_input1 = st.selectbox(label = obj2img_msg1, options = obj_list1,
                                    key = 3, disabled = False)#, index = default_ix3)
                obj_input1.lower() # 소문자로 전부 통일
        col01,col02,col03=st.columns(3)

        
        if sub_input1 == "":
            st.write("❗ 주어를 입력(선택)해주세요")
        if pred_input1 == "":
            st.write("❗ 술어를 입력(선택)해주세요")
        if obj_input1 == "":
            st.write("❗ 목적어를 입력(선택)해주세요")
        if sub_input1 == "" and pred_input1 == "" and obj_input1 == "":
            st.write("❗ **주어** 혹은 **술어** 혹은 **목적어**를 ***전부*** 입력해주세요.")

    # -------------------------------------- 복합질의 내 조건1(단일 질의 조건) (上)--------------------------------------------

    # -------------------------------------- 복합질의 내 조건2(복합 질의 조건) (下)--------------------------------------------

        sub2img_msg2 = "이미지를 검색할 **두 번째 주어**(**Subject**)를 입력해주세요."
        pred2img_msg2 = "이미지를 검색할 **두 번째 술어**(**Predicate**)를 입력해주세요."
        obj2img_msg2 = "이미지를 검색할 **두 번째 목적어**(**Object**)를 입력해주세요."
        
        cond1_img_list = list(tbl_scene.loc[(tbl_scene['subject'] == sub_input1) & 
                                    (tbl_scene['predicate'] == pred_input1) &(tbl_scene['object'] == obj_input1), 'image_id'])
        cond1_tbl_scene = tbl_scene[tbl_scene['image_id'].isin(cond1_img_list) & 
                                    ((tbl_scene['subject'] != sub_input1) | (tbl_scene['predicate'] != pred_input1) | 
                                    (tbl_scene['object'] != obj_input1))].reset_index(drop = True)
        
        sub_list2 = sorted(list(set(list(cond1_tbl_scene['subject'].values))), reverse = False)
        default_idx1 = sub_list2.index('man')
        
        pred_input2 = ""
        obj_input2 = ""
        
        col1 , col2, col3 = st.columns(3)
        with col1:
            sub_input2 = st.selectbox(label = sub2img_msg2, options = sub_list2,
                                    key = 4, disabled = False, index = default_idx1) 
            #전부 빈값으로 놔둘 수 없어서 일단 두 번째 subject 값만 제일 첫번째 값으로 채우기
            sub_input2.lower() # 소문자로 전부 통일
            
        with col2:
            if sub_input2 != "":
                pred_list2 = sorted(list(set(list(cond1_tbl_scene.loc[cond1_tbl_scene.subject == sub_input2]['predicate'].values))),
                                    reverse = False)
                pred_list2.insert(0, 'wearing')
                pred_input2 = st.selectbox(label = pred2img_msg2, options = pred_list2,
                                        key = 5, disabled = False)
                pred_input2.lower() # 소문자로 전부 통일
                #st.write(pred_list)
                
        with col3:
            if sub_input2 != "" and pred_input2 != "" :
                obj_list2 = sorted(list(set(list(
                    cond1_tbl_scene.loc[(cond1_tbl_scene.subject == sub_input2)&(cond1_tbl_scene.predicate == pred_input2)]['object'].values))),
                    reverse = False)
                obj_list2.insert(0, 'white shirt')
                obj_input2 = st.selectbox(label = obj2img_msg2, options = obj_list2,
                                        key = 6, disabled = False)
                obj_input2.lower() # 소문자로 전부 통일
        
        col01,col02,col03=st.columns(3)


        if (sub_input1 != "" and pred_input1 != "" and obj_input1 != "") and (sub_input2 != "" and pred_input2 != "" and obj_input2 != ""):
        # 복합질의가 전부 다 찼을 때

            cond2_img_list = list(cond1_tbl_scene.loc[(cond1_tbl_scene['subject'] == sub_input2) & 
                                    (cond1_tbl_scene['predicate'] == pred_input2) & (cond1_tbl_scene['object'] == obj_input2),
                                    'image_id'])
            grps = tbl_scene[tbl_scene['image_id'].isin(cond2_img_list)].groupby('image_id')

            img_dic = dict(list(grps)) #이미지와 해당 SPO테이블이 dictionary 형태로 저장
            img_number = len(img_dic.keys())
            
            with col02:
                img_number_txt1 = f"<strong><i>{img_number}</i></strong> - Image is detected ❗"
                st.markdown(f"""<span style='text-align: left; font-size:120%'>{img_number_txt1}</span>""", unsafe_allow_html=True)
            st.markdown("___")
                        
            if img_number > 0:
        
                col1, col2, col3, col4 = st.columns([4.8, 0.2, 4.8, 0.2])

                if 'counter' not in st.session_state: 
                    st.session_state.counter = 0

                # Get list of images in folder
                img_num_lst =  list(img_dic.keys())
                img_path =  """https://cs.stanford.edu/people/rak248/VG_100K/"""
                filteredImages = [img_path + f"{img_num}.jpg" for img_num in img_num_lst]
                
                #filteredImages = [image_resize(image) for image in filteredImages]
                def showPhoto(photo, df):
                    ## Increments the counter to get next photo
                    st.session_state.counter += 1
                    if st.session_state.counter >= len(filteredImages):
                        st.session_state.counter = 0

                    with col03:
                        img_number_txt2 = f"<strong style='font-size:150%'><i>{st.session_state.counter + 1}</i></strong>(th) out of {img_number}"
                        st.markdown(f"""###### {img_number_txt2}""", unsafe_allow_html=True)

                    with col1:
                        res_ttl1 = f"Result 1 : <strong style = 'font-size : 120%'><i>Image</i></strong> matched by SPO"
                        st.markdown(f"""##### {res_ttl1}""",
                                    unsafe_allow_html=True)
                        st.image(photo)
                    with col3: 
                        res_ttl2 = f"Result 2 : <strong style = 'font-size : 120%'><i>Scene Graph</i></strong> of Image matched by SPO"
                        st.markdown(f"""##### {res_ttl2}""",
                                    unsafe_allow_html=True)
                        graph_visual(df, 'subject','object','predicate')


                

                # Select photo a send it to button
                photo = filteredImages[st.session_state.counter%img_number]
                df_idx = img_num_lst[st.session_state.counter%img_number]
                show_btn = col01.button("이미지 검색 결과 확인하기(계속)⏭️",on_click = showPhoto, args = ([photo, img_dic[df_idx]]))

    
    if sub_input1 == "":
        st.write("❗ 주어를 입력(선택)해주세요")
    if pred_input1 == "":
        st.write("❗ 술어를 입력(선택)해주세요")
    if obj_input1 == "":
        st.write("❗ 목적어를 입력(선택)해주세요")
    if sub_input1 == "" and pred_input1 == "" and obj_input1 == "":
        st.write("❗ **주어** 혹은 **술어** 혹은 **목적어**를 ***전부*** 입력해주세요.")
 
    # -------------------------------------- 복합질의 내 조건2(복합 질의 조건) (上)--------------------------------------------

        
selected_menu = option_menu(
    None, 
    ["Intro", "Explanation", "Practice1 (IMG to SPO)", "Practice2 (SPO to IMG)"], 
    icons = ['bookmark-check', 'file-play-fill'], 
    menu_icon = "cast", 
    default_index = 0, 
    orientation = "horizontal",
    styles = {"container": {"padding": "5!important", "background-color": "#fafafa"},
    "icon": {"font-size": "21px"},
    "nav-link": {"font-size": "13.0px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#007AFF",}})


    
if selected_menu == "Intro":
    Intro()
elif selected_menu == 'Explanation':
    Explanation()
elif selected_menu == "Practice1 (IMG to SPO)":
    Practice1()
elif selected_menu == "Practice2 (SPO to IMG)":
    Practice2()
    
