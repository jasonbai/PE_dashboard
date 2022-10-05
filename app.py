# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image


st.title('指数PE看板')
image = Image.open('gzh.jpeg')
st.image(image, caption='扫码关注-理性派的旅行')
st.markdown('#### 本站基于-微信公众号文章[**指数估值看板**](https://mp.weixin.qq.com/s/M4sdSfsnwm98rf7Y0eohsg) 制作而成，功能驱动由[streamlit](https://streamlit.io/) 支持，实现交互操作及数据展示。')
st.markdown('> **数据说明：**')
st.markdown('数据开始时间：2012-07-01')
st.markdown('数据最新时间：2022-10-5')


## 逻辑计算部分
df_data = pd.read_csv('pe.csv')
df_data['Unnamed: 0'] = pd.to_datetime(df_data['Unnamed: 0'])
df_data = df_data.set_index('Unnamed: 0')
df_data = df_data.rename(columns={'000001.XSHG':'上证指数','000016.XSHG':'上证50','000300.XSHG':'沪深300','399673.XSHE':'创业板50','000905.XSHG':'中证500','000036.XSHG':'上证消费','000808.XSHG':'医药生物','399359.XSHE':'国证基建'})

new = df_data.describe(percentiles=[0.25,0.5,0.8])
new = new.T
new['当前PE'] = df_data.iloc[-1]

st.markdown('---')
## 观察指数部分
st.markdown('### 通过下拉框可以选择自己感兴趣的指数，观察指数PE情况')

pclass = st.selectbox("选择指数", ['上证指数', '上证50', '沪深300', '创业板50', '中证500', '上证消费', '医药生物', '国证基建'])


data_plot=pd.DataFrame(df_data[pclass])

data_plot['25%分位数']=new.loc[pclass,'25%']
data_plot['50%分位数']=new.loc[pclass,'50%']
data_plot['80%分位数']=new.loc[pclass,'80%']

st.line_chart(data_plot)


#策略
new['操作建议'] = ['千载难逢，加3倍买' if i<= j else '加1倍买' if i>j and i<=m else '不买了，可以卖' if i>m and i<=h else '卖空，躺平' for i,j,m,h in zip(new['当前PE'],new['25%'],new['50%'],new['80%'])]

df_1 = new[['当前PE','25%','50%','80%','操作建议']]

st.markdown('### 操作建议：')
st.write(pclass)
st.write(df_1.loc[pclass,'操作建议'])


st.write("### -----策略逻辑----")
st.write("个人主观理解,仅供参考")
st.markdown("依照25%、50%、80%的分位数做区隔，分四段。四段建议是这样的：\
1. 千载难逢，加 3 倍买 2. 加 1 倍买 3. 不买了，可以卖 4. 卖空，躺平")


st.dataframe(df_1)



