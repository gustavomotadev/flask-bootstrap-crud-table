from json import load, dump

def obter_contatos():

    with open('banco.json', 'r', encoding='utf-8') as arquivo_json:

        contatos = load(arquivo_json)

    return contatos

def gravar_contato(novo_contato):

    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:

        contatos: list = load(arquivo_json)
        contatos.append(novo_contato)

        arquivo_json.seek(0)
        dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
        arquivo_json.truncate()

    return contatos

def apagar_contato(email):

    with open('banco.json', 'r+', encoding='utf-8') as arquivo_json:

        contatos: list = load(arquivo_json)

        remover = None
        for contato in contatos:
            if contato.get('email') == email:
                remover = contato
                break
        
        if contato:
            contatos.remove(contato)

            arquivo_json.seek(0)
            dump(contatos, arquivo_json, indent=True, ensure_ascii=False)
            arquivo_json.truncate()

    return contatos
