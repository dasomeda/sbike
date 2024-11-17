import streamlit as st
import pandas as pd

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]
with st.sidebar:
    st.caption(f'{ID}님 접속중')
data = pd.read_csv("공공자전거.csv", encoding='cp949',on_bad_lines='skip')

st.title('공공자전거 어디있지?')


data = data.copy().fillna(0)
data.loc[:,'size'] = 10*(data['LCD']+data['QR'])
data


color = {'QR':'#3767eb',
        'LCD':'#eb9d37'}
data.loc[:,'color'] = data.copy().loc[:,'운영방식'].map(color)


st.map(data, latitude="위도",
            longitude="경도",
            size="size",
            color="color")


    
with st.form("input"):
    region = st.multiselect("자치구", data['자치구'].unique())
    gender = st.multiselect("성보관소(대여소)명", data['보관소(대여소)명'].unique())
    school = st.multiselect("운영방식", data['운영방식'].unique())
    submitted = st.form_submit_button("조회")
    
    if submitted:
        name_list = []
        result = data["설치시기"].drop_duplicates().sort_values().reset_index(drop=True)
        for re in region:
            for ge in gender:
                for sc in school:
                    name = f"{re}_{ge}_{sc}"
                    name_list.append(name)
                    selected_df = data[(data['자치구'] == re) & (data['보관소(대여소)명'] == ge)& (data['운영방식'] == sc)]
                    selected_df = selected_df[["설치시기","수"]].rename(columns={"수": name})
                    result = pd.merge(result, selected_df, on='설치시기').sort_values('설치시기')
        
        st.line_chart(data=result, x='설치시기', y=name_list,use_container_width=True)
        