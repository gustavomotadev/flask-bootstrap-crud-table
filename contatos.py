from flask import Flask, render_template, request
from http import HTTPStatus
from json import load

def obter_contatos():
    with open('banco.json', 'r', encoding='utf-8') as arquivo_json:
        contatos = load(arquivo_json)
    return contatos

app = Flask(__name__)

@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(erro):
   return render_template('404.jinja'), HTTPStatus.NOT_FOUND

@app.route('/contatos')
def mostrar_contatos():

    tipo = request.args.get('tipo')

    contatos = obter_contatos()
    
    if tipo:
        contatos = [c for c in contatos if c.get('tipo') == tipo]

    return render_template('contatos.jinja', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)