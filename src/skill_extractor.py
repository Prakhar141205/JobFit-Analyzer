import re
import pandas as pd

def preprocessing_text(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s.+#@/-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_all_skills(job_title):

    try:
        data = pd.read_csv("data/job_details/Job_details.csv")

        skills_set = []
        
        if 'IT Skills' in data.columns and 'Soft Skills' in data.columns:
            if job_title is not None:
                if 'IT Skills' in data.columns:
                    for item in data['IT Skills'][data['Job Title'].str.contains(str(job_title).title())]:
                        for items in str(item).lower().split(","):

                            processed_item = preprocessing_text(items)
                            skills_set.append(processed_item)

                
                if 'Soft Skills' in data.columns:
                        for item in data['Soft Skills'][data['Job Title'].str.contains(str(job_title).title())]:
                            for items in str(item).lower().split(","):

                                processed_item = preprocessing_text(items)
                                skills_set.append(processed_item)
            else:
                if 'IT Skills' in data.columns:
                    for item in data['IT Skills']:
                        for items in str(item).lower().split(","):

                            processed_item = preprocessing_text(items)
                            skills_set.append(processed_item)
                if 'Soft Skills' in data.columns:
                    for item in data['Soft Skills']:
                        for items in str(item).lower().split(","):

                            processed_item = preprocessing_text(items)
                            skills_set.append(processed_item)

        else:
            print(f"Skills columns not found in dataset.")
        return set(skills_set)
    
    except:
        print(f"File not found!")
        return set()

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


