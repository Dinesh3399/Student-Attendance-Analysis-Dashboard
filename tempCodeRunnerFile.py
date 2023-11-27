   data = pd.DataFrame({
               "Attendance criteria": ["eod", "Condonation (65%-75%)", "Need to increase (75%-85%)", "Safe zone (>85%)"],
               "students count": countlist_nlp
            })

            fig = px.bar(data, x='Attendance criteria', y='students count',
                        color='Attendance criteria',
                        color_discrete_sequence=px.colors.qualitative.Set1)

            fig.update_layout(title="Student Distribution based on Criteria",
                           xaxis_title="Attendance criteria",
                           yaxis_title="Students count")
