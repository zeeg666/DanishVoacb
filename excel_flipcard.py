import pandas as pd

# Load the Excel file and read into a DataFrame
excel_path = "Master Data.xlsx"
df = pd.read_excel(excel_path)

# Create a dictionary for quick lookup of translation and sentence
word_data = {row['Word']: (row['Translation'], row['Sentence'] if pd.notna(row['Sentence']) else None) for _, row in df.iterrows()}

# Function to get translation and sentence for a given word
def get_translation_and_sentence(word):
    return word_data.get(word, (None, None))
