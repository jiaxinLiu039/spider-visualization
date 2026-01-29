from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.utils
import plotly.graph_objects as go
import json
import os
import re
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta

app = Flask(__name__)

def extract_temperatures(temp_str):
    # 处理换行符并提取最高温度和最低温度
    temp_str = temp_str.replace('\n', '').replace(' ', '')
    matches = re.findall(r'(-?\d+)', temp_str)
    if len(matches) >= 2:
        return float(matches[0]), float(matches[1])
    return None, None

def create_weather_plots():
    try:
        data_path = os.path.join('data', 'jinan_weather_2015_2024.csv')
        df = pd.read_csv(data_path, encoding='utf-8')
        print(f"数据列名: {df.columns.tolist()}")
        print(f"数据形状: {df.shape}")
        
        # 转换日期列
        df['日期'] = pd.to_datetime(df['日期'])
        
        # 提取最高和最低温度
        df[['最高温度', '最低温度']] = df['温度'].apply(extract_temperatures).apply(pd.Series)
        df = df.dropna(subset=['最高温度', '最低温度'])
        
        # 筛选2024年的数据
        df_2024 = df[df['日期'].dt.year == 2024].copy()
        
        # 处理天气数据
        df_2024['天气'] = df_2024['天气'].fillna('未知')
        # 清理天气数据中的换行符和多余空格
        df_2024['天气'] = df_2024['天气'].str.replace('\n', '').str.replace(' ', '')
        
        # 分离白天和夜间天气
        weather_split = df_2024['天气'].str.split('/', expand=True)
        if len(weather_split.columns) >= 2:
            df_2024['白天天气'] = weather_split[0]
            df_2024['夜间天气'] = weather_split[1]
        else:
            df_2024['白天天气'] = df_2024['天气']
            df_2024['夜间天气'] = df_2024['天气']
        
        # 统计白天天气
        day_weather_counts = df_2024['白天天气'].value_counts()
        fig4 = px.pie(
            values=day_weather_counts.values,
            names=day_weather_counts.index,
            title='2024年济南市白天天气分布',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        # 统计夜间天气
        night_weather_counts = df_2024['夜间天气'].value_counts()
        fig5 = px.pie(
            values=night_weather_counts.values,
            names=night_weather_counts.index,
            title='2024年济南市夜间天气分布',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        # 更新扇形图布局（四，五）
        for fig in [fig4, fig5]:
            fig.update_layout(
                title_x=0.5,
                title_font_size=24,
                template='plotly_white',
                height=600,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5
                )
            )
        
        # 创建全年温度变化趋势图
        fig1 = px.line(df, 
                      x='日期',
                      y=['最高温度', '最低温度'],
                      title='济南市2015-2024年温度变化趋势',
                      labels={
                          '日期': '日期',
                          'value': '温度 (°C)',
                          'variable': '温度类型'
                      },
                      color_discrete_sequence=['red', 'blue'])
        
        # 更新第一个图表布局
        fig1.update_layout(
            title_x=0.5,
            title_font_size=24,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            hovermode='x unified',
            template='plotly_white',
            legend_title_text='',
            height=600
        )
        
        # 筛选10月31日的数据
        oct31_data = df[df['日期'].dt.month.eq(10) & df['日期'].dt.day.eq(31)]
        
        # 创建10月31日温度变化趋势图
        fig2 = px.line(oct31_data, 
                      x='日期',
                      y=['最高温度', '最低温度'],
                      title='济南市2015-2024年10月31日温度变化趋势',
                      labels={
                          '日期': '日期',
                          'value': '温度 (°C)',
                          'variable': '温度类型'
                      },
                      color_discrete_sequence=['red', 'blue'])
        
        # 更新第二个图表布局
        fig2.update_layout(
            title_x=0.5,
            title_font_size=24,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            hovermode='x unified',
            template='plotly_white',
            legend_title_text='',
            xaxis=dict(
                tickformat='%Y年'
            ),
            height=600
        )
        
        # 计算每年的最高和最低温度
        df['年份'] = df['日期'].dt.year
        yearly_stats = df.groupby('年份').agg({
            '最高温度': 'max',
            '最低温度': 'min'
        }).reset_index()
        
        # 创建年度温度对比图
        fig3 = px.bar(yearly_stats,
                     x='年份',
                     y=['最高温度', '最低温度'],
                     title='济南市2015-2024年年度温度对比',
                     labels={
                         '年份': '年份',
                         'value': '温度 (°C)',
                         'variable': '温度类型'
                     },
                     color_discrete_sequence=['red', 'blue'],
                     barmode='group')
        
        # 更新第三个图表布局
        fig3.update_layout(
            title_x=0.5,
            title_font_size=24,
            xaxis_title_font_size=16,
            yaxis_title_font_size=16,
            hovermode='x unified',
            template='plotly_white',
            legend_title_text='',
            height=600,
            xaxis=dict(
                tickmode='array',
                tickvals=yearly_stats['年份'],
                ticktext=[f'{year}年' for year in yearly_stats['年份']]
            )
        )
        
        # 更新所有图表的图例名称
        for fig in [fig1, fig2, fig3]:
            fig.for_each_trace(lambda t: t.update(name='最高温度' if t.name == '最高温度' else '最低温度'))
        
        # 将图表转换为JSON
        graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON5 = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)
        print("图表生成成功")
        return graphJSON1, graphJSON2, graphJSON3, graphJSON4, graphJSON5
    except Exception as e:
        print(f"生成图表时出错: {str(e)}")
        return None, None, None, None, None

@app.route('/')
def index():
    # 生成所有图表数据
    graphJSON1, graphJSON2, graphJSON3, graphJSON4, graphJSON5 = create_weather_plots()
    
    if graphJSON1 is None or graphJSON2 is None or graphJSON3 is None or graphJSON4 is None or graphJSON5 is None:
        return "生成图表时出错，请检查控制台输出"
    
    # 打印图表数据的前100个字符用于调试程序
    print("graphJSON1:", graphJSON1[:100])
    print("graphJSON2:", graphJSON2[:100])
    print("graphJSON3:", graphJSON3[:100])
    print("graphJSON4:", graphJSON4[:100])
    print("graphJSON5:", graphJSON5[:100])
    
    return render_template('index.html', 
                         graphJSON1=graphJSON1,
                         graphJSON2=graphJSON2,
                         graphJSON3=graphJSON3,
                         graphJSON4=graphJSON4,
                         graphJSON5=graphJSON5)

if __name__ == '__main__':
    app.run(debug=True) 
    
    #运行：python app.py
    