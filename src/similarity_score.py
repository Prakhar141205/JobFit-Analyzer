from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(resume_embedding, job_description_embedding):
    # calculate similarity score

    score = cosine_similarity([job_description_embedding], [resume_embedding])

    return score
