import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import pymongo
from pymongo import MongoClient
import altair as alt

#check for connection to db
try:
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
    db = client.SampleTest  # Replace SampelTest with your database name
    collection = db.Test  # Replace Test with your collection name





    # Iterate over the results and print them
#    for document in results:
#        print(document)

except pymongo.errors.ConnectionError as e:
    print(f"Error connecting to MongoDB: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

#df=pd.read_csv('Electric_Vehicle_Population_Data.csv')
#City	State	Postal Code	Model Year	Make	Model	Electric Vehicle Type	Clean Alternative Fuel Vehicle (CAFV) Eligibility	Electric Range	Base MSRP

projection = {"City":1,"State":1,"Postal Code":1,"Model Year":1,"Make":1,"Model":1,"Electric Vehicle Type":1,"Clean Alternative Fuel Vehicle":1,"Electric Range":1,"Base MSRP":1,}

data = collection.find({}, projection)
df1 = pd.DataFrame(list(data))
df1.columns = [col.replace(" ", "_") for col in df1.columns]

#Show a scatter plot of msrp of a car to the range that it gets.
df2=df1.drop(df1[df1['Base_MSRP']== 0].index)
# Create the scatter plot
fig = px.scatter(df2, x="Base_MSRP", y="Electric_Range",hover_data=["Make","Model_Year"])
fig.update_layout(xaxis_range=[0,150000])
fig.update_layout(yaxis_range=[0,400])
# Show the plot
#fig.show()

c=alt.Chart(df2).mark_point().encode(
    x='Base_MSRP',
    y='Electric_Range',

)

st.write(c)


df1.sort_values('City')
df3 = df1['City'].dropna().unique().tolist()



# Create a sidebar selectbox for state selection
option = st.sidebar.selectbox('Which state do you want to display?', df3)

# Filter data based on selected state
select_state = df1[df1['City'] == option]


# Display the filtered data
#st.write(county_data)

d = alt.Chart(select_state).mark_bar().transform_aggregate(
    count='count()',
    groupby=['Make']
).encode(
    y=alt.Y('Make:N', title='Make'),
    x=alt.X('count:Q', title='Count'),
    color='Make:N'
).properties(
    width=1300,
    height=800,
    title='Counts of Cars by Make by city in WA'
)

# Display the bar chart in Streamlit
st.altair_chart(d)