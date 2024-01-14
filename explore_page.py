import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)

def clean_education(x):
    if "Bachelor" in x:
        return "Bachelor's degree"
    if "Master" in x:
        return "Master's degree"
    if "Professional degree" in x:
        return "Post Grad"
    return "Less than a Bachelors"

def clean_age(x):
    if "18-24" in x:
        return "18-24 years old"
    if "25-34" in x:
        return "25-34 years old"
    if "35-44" in x:
        return "35-44 years old"
    if "45-54" in x:
        return "45-54 years old"
    if "55-64" in x:
        return "55-64 years old"
    return "Under 18 years old"

@st.cache_data #To Improve the performance of our Application
def load_data():
    df = pd.read_csv('survey_results_public.csv')
    df = df[['Country', 'Age', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df = df.rename({'ConvertedCompYearly' : 'Salary'}, axis = 1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed, full-time']
    df= df.drop("Employment", axis = 1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250000]
    df = df[df['Salary'] >= 10000]
    df = df[df['Country'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] =df['EdLevel'].apply(clean_education)
    df['Age'] = df['Age'].apply(clean_age)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2023""")

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots(figsize = (12, 7))

    ax1.pie(data, labels= data.index, autopct = "%1.1f%%", shadow = True, startangle=90)
    ax1.axis("Equal")

    st.write("""#### Number of Data from Different Countries""")
    st.pyplot(fig1)

    st.write(""" #### Mean Salary based on Countries """)
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(""" #### Mean Salary based on Experience """)
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write(""" #### Mean Salary based on Age """)
    data = df.groupby(["Age"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)