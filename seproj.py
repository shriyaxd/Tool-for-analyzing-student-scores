#!/usr/bin/env python
# coding: utf-8

# In[3]:


pip install streamlit pandas matplotlib seaborn


# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Define subject weightages and their splits
subject_weightages = {
    "BD": {"M1": 15, "M2": 15, "EndSem": 30, "Others": 40},
    "HPC": {"M1": 20, "M2": 20, "EndSem": 40, "Others": 20},
    "SE": {"M1": 10, "M2": 20, "EndSem": 50, "Others": 20},
    "CN": {"M1": 25, "M2": 25, "EndSem": 30, "Others": 20},
    "ITPD": {"M1": 20, "M2": 20, "EndSem": 30, "Others": 30}
}

max_marks = {
    "M1": 30,
    "M2": 30,
    "EndSem": 100,
    "Others": 100
}

# Initialize Streamlit app
st.title("Student Score Analysis and Prediction Tool")

# Input target SGPA
target_sgpa = st.number_input("Enter your target SGPA for the semester:", min_value=0.0, max_value=10.0, step=0.1)

# Function to calculate required marks
def calculate_required_marks(current_marks, target_sgpa):
    total_weighted_score = 0
    total_weight = 0
    required_scores = {}
    
    for subject, components in current_marks.items():
        subject_score = 0
        for component, score in components.items():
            if score is not None:
                subject_score += score * subject_weightages[subject][component] / max_marks[component]
        total_weighted_score += subject_score
        total_weight += sum(subject_weightages[subject].values())
    
    required_sgpa = target_sgpa * 10  # Assuming SGPA out of 10
    remaining_weight = 100 - total_weight
    required_remaining_score = (required_sgpa * remaining_weight) / 100

    for subject, components in current_marks.items():
        required_scores[subject] = {}
        for component in subject_weightages[subject].keys():
            if components[component] is None:
                required_scores[subject][component] = (required_remaining_score * max_marks[component]) / (subject_weightages[subject][component] * remaining_weight / 100)
            else:
                required_scores[subject][component] = components[component]

    return required_scores

# Input marks achieved so far
current_marks = {}
for subject in subject_weightages.keys():
    st.subheader(f"Enter marks for {subject}")
    current_marks[subject] = {}
    for component in subject_weightages[subject].keys():
        current_marks[subject][component] = st.number_input(f"{component} marks:", min_value=0, max_value=max_marks[component], step=1, key=f"{subject}_{component}")

# Calculate required marks
required_marks = calculate_required_marks(current_marks, target_sgpa)

# Display required marks
st.subheader("Required Marks to Achieve Target SGPA")
for subject, components in required_marks.items():
    st.write(f"{subject}:")
    for component, marks in components.items():
        st.write(f"{component}: {marks:.2f}")

# Visualize the marks
fig, ax = plt.subplots(figsize=(10, 6))
for subject, components in current_marks.items():
    marks = [components[comp] if components[comp] is not None else 0 for comp in subject_weightages[subject].keys()]
    sns.barplot(x=list(subject_weightages[subject].keys()), y=marks, ax=ax, label=subject)

ax.set_ylabel("Marks")
ax.set_title("Current Marks Distribution")
ax.legend()
st.pyplot(fig)


# In[ ]:




