import re
import time

def preprocessing(content):
    try:
        # Converting all content into lowercase
        content = str(content).lower()

        # Removing Commas
        content = re.sub(r'(?<=\d),(?=\d)', "", content)
        
        # Removing all special characters from the content
        content = re.sub(r'[^\w\d\s.,\-+@#]', " ", content)

        # Removing unwanted whitespaces from the content
        content = re.sub(r'\s{2,}', ' ', content)
        content = content.strip()

        return content
    
    except Exception as e:
        return f"Some error occurred {e}!"