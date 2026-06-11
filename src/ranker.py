import pandas as pd

def rank_files(file_scores):
    try:
        pdf_score_df = pd.DataFrame(file_scores).sort_values(by='Scores', ignore_index= True, ascending=False)
        return pdf_score_df
    except Exception as e:
        return f"Error Occured {e}"
