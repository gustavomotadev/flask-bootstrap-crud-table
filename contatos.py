from flask import Flask, render_template, request, abort
from http import HTTPStatus
from json import load, dump

def obter_contatos():
    with open('banco.json', 'r', encoding='utf-8') as arquivo_json:
        contatos = load(arquivo_json)
    return contatos

def gravar_contato(novo_contato):
    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:
        contatos = load(arquivo_json)
        contatos.append(novo_contato)
        arquivo_json.seek(0)
        dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
        arquivo_json.truncate()

    return contatos

app = Flask(__name__)

@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(erro):
   return (render_template('erro.jinja', codigo=HTTPStatus.NOT_FOUND, 
        mensagem="Página não encontrada"), HTTPStatus.NOT_FOUND)

@app.errorhandler(HTTPStatus.BAD_REQUEST)
def page_not_found(erro):
   return render_template('erro.jinja', codigo=HTTPStatus.BAD_REQUEST,
        mensagem="Não foi possível realizar operação"), HTTPStatus.BAD_REQUEST

@app.route('/contatos', methods=['GET'])
def mostrar_contatos():

    tipo = request.args.get('tipo')

    contatos = obter_contatos()
    
    if tipo:
        contatos = [c for c in contatos if c.get('tipo') == tipo]

    return render_template('contatos.jinja', contatos=contatos)

@app.route('/contatos', methods=['POST'])
def salvar_contato():

    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    tipo = request.form.get('tipo')

    if not (nome and email and telefone and tipo):
        abort(HTTPStatus.BAD_REQUEST)

    novo_contato = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "tipo": tipo
    }

    contatos = gravar_contato(novo_contato)

    return render_template('contatos.jinja', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)