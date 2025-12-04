from flask import Flask,render_template,request,jsonify,url_for,send_from_directory
import os
import uuid
from utils import preprocess_Exemplo_1,preprocess_Exemplo_2,preprocess
from database import corpus
from Read_files import getPdfContent,readImage

from rank_bm25 import BM25Okapi

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/search',methods=['POST','GET'])
def search():
    query = request.form['query']
    # print(query)
    # buscar dentre os documentos
    query_tokens = preprocess_Exemplo_1(query)
    docs_tokens = corpus.tokens()
    if docs_tokens:
            
        
        # BM25
        bm25 = BM25Okapi(docs_tokens)
        bm25_scores = bm25.get_scores(query_tokens)

        return render_template('search.html',query = query,results = corpus.results(bm25_scores))
    else:
        return render_template('search.html',query = query,results = [])
@app.route('/corpus',methods=['POST','GET'])
def corpus_page():
    match request.method:
        case 'POST':
            files = request.files.getlist('files')
            suportados = 0
            nao_suportados = 0
            for file in files:
                id = uuid.uuid4().hex
                filename = file.filename
                name = f'id_{id}_name_{filename}'
                file_path = f'corpus/{name}'
                file.save(file_path)
                file.stream.seek(0)
                # salvar otimizado
                tipo = file.content_type
                match tipo:
                    case 'application/pdf':
                        content = getPdfContent(file.read())
                        corpus.addItem(id,filename,content)

                    # case cs if cs.startswith('image'):
                    #     content = readImage(file.read())
                    #     corpus.addItem(id,filename,content)

                    case cs if cs.startswith('text/'):
                        content = file.read().decode("utf-8")
                        corpus.addItem(id,filename,content)
                    case _:
                        os.remove(file_path)
                        nao_suportados += 1
                        # return jsonify({
                        #     'erro':'tipo nao suportado '
                        # }),405
            qtd_arquivos = len(files)
            suportados = qtd_arquivos - nao_suportados

            return jsonify({
                'len':suportados,
                'qtd_arquivos':qtd_arquivos,
                'nao_suportados':nao_suportados
            }),200

        case 'GET':
            return jsonify({
                'len':len(os.listdir('corpus'))
            }),200
        case _:
            return jsonify({
                'erro':'methodo nao suportado'
            }),405

@app.route('/corpus/<path:filename>')
def corpus_files(filename):
    return send_from_directory('corpus',filename)

@app.route('/acess/<string:id>')
def acess(id):
    name = corpus.getName(id)
    content = {
        'title':name,
        'file':url_for('corpus_files',filename=f'id_{id}_name_{name}')
    }
    return render_template('return.html',content = content)


if __name__ == '__main__':
    app.run(port='8000',debug=True)