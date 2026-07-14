import streamlit as st
import pandas as pd
from src.file_parser import pdf_file_parser
from src.embedder import get_embedding
from src.preprocessing import preprocessing
from src.similarity_score import similarity_score
from src.ranker import rank_files
from src.skill_extractor import missing_skill_keyword

GRADE_STRONG_MATCH = "Strong Match"
GRADE_QUALIFIED = "Qualified"
GRADE_WEAK_MATCH = "Weak Match/Recheck Resume"
GRADE_NO_MATCH = "No Match!"

def get_grade(score):
    if score >= 0.80:
        return GRADE_STRONG_MATCH
    elif score >= 0.60:
        return GRADE_QUALIFIED
    elif score >= 0.40:
        return GRADE_WEAK_MATCH
    else:
        return GRADE_NO_MATCH

# Page SEtup

st.set_page_config(page_title = "Semantic JobFit Analyzer", page_icon="🤖")
st.title(f":blue[**Semantic JobFit Analyzer**]")
st.write("Upload a resume and paste a job description to get the similarity score!")
st.caption("**Note:** :green[Add Job Title for better results!]")

# Header & Sidebar for Job Description
st.header("Upload Resume")
# st.sidebar.header(":rainbow[**Job Title**]")
st.sidebar.header(":blue[**Job Title**  &  **Job Description**]")

# take input of Job description and resume
job_title= st.sidebar.text_input("Enter full form of job title: ", placeholder = "Enter Exact or similar job title")
job_description = st.sidebar.text_area("Enter job descrition here: ", height=500)

uploaded_files = st.file_uploader("Choose a file", type= ['pdf'], accept_multiple_files=True)


if st.button("Calculate Matching Score"):
    if uploaded_files and job_description:
        with st.spinner("Processing"):
            processed_job_desc = preprocessing(job_description)
            embed_job_descr = get_embedding(processed_job_desc)

            results = []
            resume_contents = []
            file_names = []

            for file in uploaded_files:
                try:
                    content = pdf_file_parser(file)
                    processed_content = preprocessing(content)
                    resume_contents.append(processed_content)
                    file_names.append(file.name)
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
            
            if resume_contents:
                embed_resume_files = get_embedding(resume_contents)
                matching_scores = similarity_score(embed_resume_files, embed_job_descr)

                for i, file_name in enumerate(file_names):
                    percentage = round(matching_scores[i][0] * 100, 2)
                    grade = get_grade(matching_scores[i][0])

                    results.append({'File': file_name, 'Scores': percentage, 'Grade': grade})

                    # extracting resume skills and missing skills
                    resume_skills_found, missing_skills = missing_skill_keyword(job_title, processed_job_desc, resume_contents[i])

                    with st.expander(f"Skills details for **{file_name}** (**Score: {percentage}%**, **Grade: {grade}** )"):
                        st.write(f"**Skills found: ** {', '.join(resume_skills_found).title()}")
                        if missing_skills:
                            st.warning(f"**Missing Skills:** {', '.join(missing_skills).title()}")
                        else:
                            st.success("All required skills found.")

        st.success("Analysis complete")
        ranking_pdf = rank_files(results)
        st.dataframe(ranking_pdf, use_container_width = True)
        st.snow()

    else:
        st.warning("Please upload both **Resume** and **Job descriptions**!")
