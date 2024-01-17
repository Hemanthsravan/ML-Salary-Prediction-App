import streamlit as st 
import numpy as np 
import pickle


def load_model():
  with open("saved_steps.pk1", "rb") as file:
    data = pickle.load(file)
  return data

data = load_model()

regressor = data["model"]
le_country = data['le_country']
le_age = data['le_age']
le_education = data['le_education']

def show_predict_page():
  st.title("Software Developer Salary Prediction")

  st.write(""" ### We need some information to predict the salary 
           """)
  st.write(""" ##### Insights from Stack Overflow 2023 Survey Data
           """)
  countries = (
  "United States of America",
  "Germany",
  "United Kingdom of Great Britain and Northern Ireland",
  "Canada",
  "India",
  "France",
  "Netherlands",
  "Australia",
  "Brazil",
  "Spain",
  "Sweden",
  "Italy",
  "Poland",
  "Switzerland",
  "Denmark",
  "Norway",
  "Israel",
    )

  ages = (
    '45-54 years old', '25-34 years old', '35-44 years old',
       '55-64 years old', '18-24 years old', 'Under 18 years old',
    )

  education = (
  "Bachelor's degree", 'Less than a Bachelors', "Master's degree",
       'Post Grad',
   )

  country = st.selectbox("Country", countries)
  age = st.selectbox("Age Group", ages)
  education = st.selectbox("Education Level", education)

  experience = st.slider("Years of Experience", 0,50,2)

  ok = st.button("Calculate Salary")

  if ok:
    X = np.array([[country, age, education, experience]])
    X[:, 0] = le_country.transform(X[:, 0])
    X[:, 1] = le_age.transform(X[:, 1])
    X[:, 2] = le_education.transform(X[:, 2])
    X = X.astype(float)

    salary = regressor.predict(X)
    st.subheader(f"The estimated salary is ${salary[0]:.2f}")

