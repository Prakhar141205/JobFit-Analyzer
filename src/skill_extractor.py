import re
import pandas as pd
import streamlit as st

def preprocessing_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s.+#@/-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

@st.cache_data
def load_skills_data(path="data/job_details/Job_details.csv"):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"Error: The file was not found at {path}")
        return None

def get_all_skills(job_title):
    data = load_skills_data()
    if data is None:
        return set()

    skills_set = []
    skill_columns = ['IT Skills', 'Soft Skills']

    if not all(col in data.columns for col in skill_columns):
        print("Skills columns not found in dataset.")
        return set()

    if job_title:
        data = data[data['Job Title'].str.contains(str(job_title).title(), na=False)]

    for col in skill_columns:
        skills = data[col].dropna().str.lower().str.split(',').explode()
        processed_skills = skills.apply(preprocessing_text)
        skills_set.extend(processed_skills)
    return set(skills_set)

def matching_skill_keyword_finder(job_title, text):
    """Find all matching skill keyword from load_skills and given test"""

    skills = get_all_skills(job_title)

    skill_found  = []
    for item in skills:
        if str(item) in str(text):
            skill_found.append(item)

    return set(skill_found)


def missing_skill_keyword(job_title, job_description, resume):

    skills_for_job_descr = matching_skill_keyword_finder(job_title, job_description)
    skills_from_resume = matching_skill_keyword_finder(job_title, resume)

    missing_skills = skills_for_job_descr - skills_from_resume

    return skills_from_resume, missing_skills
