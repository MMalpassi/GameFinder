import spacy
import pandas as pd

nlp = spacy.load("en_core_web_sm")

#Procesamiento de documento .csv:
csv_processing = pd.read_csv("docs\games-data.csv")

columnas = ['name', 'platform', 'r-date', 'score', 'user score',
            'developer', 'genre', 'players', 'critics', 'users']

csv_processing['complete_text'] = csv_processing[columnas].astype(str).agg(' '.join, axis=1)

#Procesamiento con Spacy:
lemmatized_texts = []
for doc in nlp.pipe(csv_processing['complete_text'], batch_size=20):
    lemas = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    lemmatized_texts.append(" ".join(lemas))

csv_processing['texto_lema'] = lemmatized_texts

# Guardar el nuevo archivo CSV
csv_processing.to_csv("csv_processing.csv", index=False)
