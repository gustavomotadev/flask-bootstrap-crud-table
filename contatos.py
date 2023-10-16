from flask import Flask, render_template, request, abort
from http import HTTPStatus
import banco

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

    contatos = banco.obter_contatos()
    
    if tipo:
        contatos = [c for c in contatos if c.get('tipo') == tipo]

    return render_template('contatos.jinja', contatos=contatos)

@app.route('/salvar_contato', methods=['POST'])
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

    contatos = banco.gravar_contato(novo_contato)

    return render_template('contatos.jinja', contatos=contatos)

@app.route('/remover_contato/<email>', methods=['POST'])
def remover_contato(email: str):

    if not email:
        abort(HTTPStatus.BAD_REQUEST)

    contatos = banco.apagar_contato(email)

    return render_template('contatos.jinja', contatos=contatos)

if __name__ == '__main__':
    app.run(debug=True)