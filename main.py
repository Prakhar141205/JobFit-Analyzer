import streamlit as st
import pandas as pd
from src.file_parser import pdf_file_parser
from src.embedder import get_embedding
from src.preprocessing import preprocessing
from src.similarity_score import similarity_score
from src.ranker import rank_files
from src.skill_extractor import missing_skill_keyword

import os, time


# Page SEtup

st.set_page_config(page_title = "Resume Screening Engine", page_icon="🤖")
st.title(":rainbow[**AI Powered Resume Screening Engine**]")
st.write("Upload a resume and paste a job description to get the similarity score!")
st.caption("**Note:** :green[Add Job Title for better results!]")

# Header & Sidebar for Job Description
st.header("Upload Resume")
# st.sidebar.header(":rainbow[**Job Title**]")
st.sidebar.header(":rainbow[**Job Title**  &  **Job Description**]")

# take input of Job description and resume
job_title= st.sidebar.text_input("**Enter full form of job title: **", placeholder = "Enter Exact or similar job title")
job_description = st.sidebar.text_area("Enter job descrition here: ", height=500)

uploaded_files = st.file_uploader("Choose a file", type= ['pdf'], accept_multiple_files=True)


if st.button("Calculate Matching Score"):
    if uploaded_files and job_description:

        file_scores = {'File': [], 'Scores': [], 'Grade': []}
        with st.spinner("Processing"):
            processed_job_desc = preprocessing(job_description)

            # file parsing

            for file in uploaded_files:
                # parsing the input file
                content = pdf_file_parser(file)

                # processing the file content

                file_content_processed = preprocessing(content)

                # get embedding

                embed_resume_file = get_embedding(file_content_processed)
                embed_job_descr = get_embedding(processed_job_desc)

                matching_score = similarity_score(embed_resume_file, embed_job_descr)
                percentage = round(matching_score[0][0] * 100 , 3)

                # ranking file according to score
                file_scores['File'].append(file.name)
                file_scores['Scores'].append(percentage)

                if matching_score[0][0] >= 0.80:
                    file_scores["Grade"].append("Strong Match")
                elif (matching_score[0][0] >= 0.60) and (matching_score[0][0] < 0.80):
                    file_scores["Grade"].append("Qualified")
                elif (matching_score[0][0] >= 0.40) and (matching_score[0][0] < 0.60):
                    file_scores["Grade"].append("Weak Match/Recheck Resume")
                else:
                    file_scores["Grade"].append("No Match!")


                # extracting resume skills and missing skills

                resume_skills_found, missing_skills = missing_skill_keyword(job_title, processed_job_desc, file_content_processed)

                with st.expander(f"Skills details for **{file.name}** (**Score: {percentage}%**)"):
                    st.write(f"**Skills found: ** {', '.join(resume_skills_found).title()}")
                    if missing_skills:
                        st.warning(f"**Missing Skills:** {', '.join(missing_skills).title()}")
                    else:
                        st.success("All required skills found.")
        st.success("Analysis complete")
        ranking_pdf = rank_files(file_scores)
        st.dataframe(ranking_pdf, use_container_width = True)
        st.snow()

    else:
        st.warning("Please upload both **Resume** and **Job descriptions**!")



