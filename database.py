import json
from utils import preprocess


class Corpus:
    def __init__(self,path = 'persist.json'):
        self.path = path
        with open(path,'r',encoding='utf-8') as f:
            self.itens = json.load(f)

    def results(self,score):
        results = [(result,iten) for result,iten in zip(score,self.itens)]
        results.sort(key=lambda r: r[0],reverse=True)
        return [
            {   
                'id':r[1]['id'],
                'title':r[1]['name'],
                'description':r[1]['content'][:200],
                'BM25':r[0]
            }
            for r in results]

    def tokens(self):
        return [iten['token'] for iten in self.itens]

    def addItem(self,id,name,content):
        self.itens.append({
            'id':id,
            'name':name,
            'content':content,
            'token':preprocess(content)
        })
        with open(self.path,'w',encoding='utf-8') as f:
            json.dump(self.itens,f,ensure_ascii=False,indent=4)
    def getName(self,id):
        for item in self.itens:
            if item['id'] == id:
                return item['name']
            
corpus = Corpus()