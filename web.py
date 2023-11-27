import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(page_title="CUDA Domain Attendance Analysis ", page_icon="🏫", layout="wide")  
st.title("CUDA Attendance Analysis Dashboard")
theme_plotly = None # None or streamlit
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
def color(df):
    colors = []
    for percentage in df['percentage']:
        if percentage < 65:
            colors.append("eod")
        elif 65 <= percentage < 75:
            colors.append("condonation")
        elif 75 <= percentage < 85:
            colors.append("need to increase")
        else:
            colors.append("safe zone")
    return colors

def load_data(sheet_name):
    return pd.read_excel(r"DA Attendance sheet.xlsx", sheet_name=sheet_name)

def donut(filtered):
    if not filtered.empty:
        present_percent = filtered['percentage'].iloc[0]
        absent_percent = 100 - present_percent
        fig = px.pie(names=['Present', 'Absent'], values=[present_percent, absent_percent], hole=0.5)
        fig.update_layout(height=290,width=287,showlegend=False)
        st.plotly_chart(fig)
    else:
        st.write("Registration number not found.")

def display_summary_chart(data, title):
    countlist = [sum(data['percentage'] < 65),
                 sum((65 <= data['percentage']) & (data['percentage'] < 75)),
                 sum((75 <= data['percentage']) & (data['percentage'] < 85)),
                 sum(data['percentage'] >= 85)]

    criteria_data = pd.DataFrame({
        "Attendance criteria": ["eod", "Condonation (65%-75%)", "Need to increase (75%-85%)", "Safe zone (>85%)"],
        "students count": countlist
    })

    hist_chart = px.bar(criteria_data, x='Attendance criteria', y='students count',
                        title=f"Criteria wise student count for {title}",
                color='Attendance criteria',
                color_discrete_sequence=px.colors.qualitative.Set1)

    hist_chart.update_layout(
                    xaxis_title="Attendance criteria",
                    yaxis_title="Students count")
   
    hist_chart.update_layout(height=500,width=747,title_font_size=30,title_x=0.1)

    return hist_chart

def display_individual_chart(data, title):
    
    fig = px.bar(y=data['Stu Name'], x=data['percentage'],
                 title=f'Criteria wise {title} %',
                 color=color(data),
                 labels={'x': 'Percentage', 'y': 'Student Name'})
    fig.update_layout(height=500,width=750,title_font_size=30,title_x=0.25)
    return fig


# load excel file
df_tableau = load_data('Tableau')
df_dadm = load_data('DADM')
df_nlp = load_data('NLP')
df_sql = load_data('SQL')
df_dvsr = load_data('DVSR')

# switcher

st.sidebar.header("Please Filter Here:")
value = st.sidebar.selectbox(label="Select Registration number", options=list(df_tableau["Reg No"]))
selected_student_name = df_tableau.loc[df_tableau['Reg No'] == value, 'Stu Name'].iloc[0]
st.sidebar.warning(f"Student Name: \n {selected_student_name}")
subject = st.sidebar.selectbox('Select Subject', ["Tableau", "Dadm", "NLP", "SQL", "Story Boarding"])

filter_tableau = df_tableau[df_tableau['Reg No'] == value]
filter_dadm = df_dadm[df_dadm['Reg No'] == value]
filter_nlp = df_nlp[df_nlp['Reg No'] == value]
filter_sql = df_sql[df_sql['Reg No'] == value]
filter_dvsr = df_dvsr[df_dvsr['Reg No'] == value]

def HomePage():
   # compute top Analytics
   # columns
   col1, col2, col3, col4, col5 = st.columns(5, gap='small')
   col6, col7 = st.columns(2, gap='small')

   charts = {
       "Tableau": df_tableau,
       "Dadm": df_dadm,
       "Story Boarding": df_dvsr,
       "SQL": df_sql,
       "NLP": df_nlp
   }

   selected_data = charts.get(subject)

   if selected_data is not None:
       with col1:
          st.success('Tableau')
          donut(filter_tableau)

       with col2:
          st.success('DADM')
          donut(filter_dadm)

       with col3:
          st.success('Storytelling')
          donut(filter_dvsr)

       with col4:
          st.success('SQL')
          donut(filter_sql)

       with col5:
          st.success('NLP')
          donut(filter_nlp)

       st.markdown("""---""")

       # graphs
       hist_chart = display_summary_chart(selected_data, subject)
       individual_chart = display_individual_chart(selected_data, subject)

       with col7:
           st.plotly_chart(hist_chart)

       with col6:
          st.plotly_chart(individual_chart)
   else:
       st.error('Please select a valid subject')

HomePage()