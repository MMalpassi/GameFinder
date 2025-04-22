import os
import pandas as pd
from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser

csv_lema = pd.read_csv("csv_processing.csv")

# Definir el esquema del índice
schema = Schema(id=ID(stored=True, unique=True),
                name=TEXT(stored=True),
                platform=TEXT(stored=True),
                rdate=TEXT(stored=True),
                score=TEXT(stored=True),
                userscore=TEXT(stored=True),
                developer=TEXT(stored=True),
                genre=TEXT(stored=True),
                players=TEXT(stored=True),
                critics=TEXT(stored=True),
                users=TEXT(stored=True),
                complete_text=TEXT(stored=True),
                texto_lema=TEXT(stored=True),
            )

# Creación del índice
if not os.path.exists("indice"):
    os.mkdir("indice")

ix = create_in("indice", schema)

#Indexación de documentos
writer = ix.writer()
for idx, row in csv_lema.iterrows():
    writer.add_document(
        id=str(idx),
        name=row['name'],
        platform=row['platform'],
        rdate=str(row['r-date']),
        score=str(row['score']),
        userscore=str(row['user score']),
        developer=row['developer'],
        genre=row['genre'],
        players=str(row['players']),
        critics=str(row['critics']),
        users=str(row['users']),
        complete_text=str(row['complete_text']),
        texto_lema=str(row['texto_lema']),
    )

writer.commit()
