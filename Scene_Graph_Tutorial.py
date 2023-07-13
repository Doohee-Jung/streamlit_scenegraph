import os
import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image


# 하기 내용은 표시 텍스트
st.set_page_config(
    page_title="SCENE GRAPH TUTORIAL",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.markdown('![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=https://port-0-streamlit-scenegraph-20zynm2mlk0h48zy.sel4.cloudtype.app/&label=VisitorsCount&labelColor=000000&logo=GitHub&logoColor=FFFFFF&color=1D70B8&style=for-the-badge)')

st.title("R&D 개요") 
st.text("")
st.text("")
st.subheader("""1. 배경""")
text1 = """
◦ 많은 신기술은 이미지나 영상을 활용하고 있으나 해당 object의 속성 연구가 어렵고 미진하므로, 그래프 기술을 활용하여 문제를 해결하고자 Scene Graph 연구 수행\n
◦ Contents 속성 관리 및 활용성에 대해 GDB가 활용 가치가 높음\n
◦ 현재 Scene graph를 DB화 하여 서비스를 하는 Case는 찾기 어려우며 비트나인에서 속성 정보 유지/관리/활용에 대한 방향성을 제시 함으로써 시장 선두 구축"""
st.write(text1)
st.text("")
st.subheader("""2. 목표\n 
본 R&D를 통해 Scene Graph 데이터를 GDB에 활용하여 Scene Graph 분야에서 GDB의 효용성을 확인하고자 한다. 기본적인 검색 과정에서
RDB와 GDB의 검색 방식의 차이점과 그 밖의 활용 방안을 제안하며 상세 내용은 아래와 같다.""")
text2 = """
◦ Scene Graph의 Triplet형태의 이미지 속성 정보 그래프모델링 및 GDB 적재\n
◦ 이미지를 통해 SPO를 검색하거나 SPO를 통해 이미지를 검색하는 기본적인 질의 과정 RDB 와 비교\n
◦ 모델링의 장점을 살릴 수 있는 유사도 측정 방법 제안\n
◦ GDB의 강점을 활용할 수 있는 활용방안 제안"""
st.write(text2)
