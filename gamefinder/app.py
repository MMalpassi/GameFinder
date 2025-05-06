from flask import Flask, render_template, request, jsonify
from whoosh.index import open_dir
from whoosh.qparser import QueryParser


# Crear una instancia de Flask
app = Flask(__name__)

# Uso el índice creado
ix = open_dir("indice") 

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/search')
def search():
    query = request.args.get('query')
    sort_by = request.args.get('sort', 'score')
    order = request.args.get('order', 'desc')
    resultados = []
    
    if query:
        with ix.searcher() as searcher:
            parser = QueryParser("texto_lema", ix.schema)
            whoosh_query = parser.parse(query)
            results = searcher.search(whoosh_query)

            for matches in results:
                resultados.append({
                    "name": matches["name"],
                    "platform": matches["platform"],
                    "rdate": matches["rdate"],
                    "developer": matches["developer"],
                    "genre": matches["genre"],
                    "score": matches["score"],
                })
            
            reverse = True if order == 'desc' else False
            try:
                resultados = sorted(resultados, key=lambda x: x[sort_by], reverse=reverse)
            except:
                pass

    return render_template('results.html', results=resultados, query=query, sort=sort_by, order=order)

@app.route('/autocomplete')
def autocomplete():
    partial = request.args.get('q', '')
    suggestions = []

    if partial:
        with ix.searcher() as searcher:
            parser = QueryParser("texto_lema", ix.schema)
            whoosh_query = parser.parse(partial)
            results = searcher.search(whoosh_query, limit=5)
            for hit in results:
                suggestions.append(hit['name'])

    return jsonify(suggestions)


if __name__ == '__main__':
    app.run(debug=True)
