from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
import os
import pickle

app = Flask(__name__)

#########################
# configurando autenticação básica, para que a API só possa ser acessada mediante validação de usuário e senha
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

#########################

colunas = ['tamanho', 'ano', 'garagem']
modelo = pickle.load(open('../../models/modelo.sav', 'rb'))

@app.route('/')
def home():
    return "Minha primeira API."

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')

    polaridade = tb_en.sentiment.polarity

    return 'Polaridade: {}'.format(polaridade)

@app.route('/cotacao/', methods=['POST'])
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]

    preco = modelo.predict([dados_input])

    return jsonify(preco=preco[0])

app.run(debug=True, host='0.0.0.0')