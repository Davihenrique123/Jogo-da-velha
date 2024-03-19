from flask import Flask, render_template, redirect, url_for, request
from flask_cors import CORS
import json
import Jogo_da_velha_flask
app = Flask(__name__)
CORS(app)
diclogin = {}
arquivo = 'info.txt'
X_ou_O = ''

def ler_info_user(nome):
    with open('info.txt', 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split('/')
            if partes[0] == nome:
                vitorias = int(partes[2])
                derrotas = int(partes[3])
                partidas = int(partes[4])
                velhas = partidas - (vitorias + derrotas)
                return {'vitorias': vitorias, 'derrotas': derrotas, 'velhas':velhas, 'partidas': partidas}

    return {'vitorias': 0, 'derrotas': 0, 'partidas': 0}

def adicionar_resultado(nome_arquivo, nome_player, resultado):
    with open(nome_arquivo, 'r+') as arquivo:
        linhas = arquivo.readlines()
        for i, linha in enumerate(linhas):
            partes = linha.strip().split('/')
            if partes[0] == nome_player:
                if resultado == 'vitoria':
                    partes[2] = str(int(partes[2]) + 1)
                elif resultado == 'derrota':
                    partes[3] = str(int(partes[3]) + 1)
                partes[4] = str(int(partes[4]) + 1)
                linhas[i] = '/'.join(partes) + '\n'
                break
        arquivo.seek(0)
        arquivo.writelines(linhas)

@app.route('/')
def home():
    return render_template('Login.html')

@app.route('/fail')
def fail():
    return render_template('Login.html', teste = True)

@app.route('/menu/<name>')
def menu(name):
    return render_template('Menu.html', nome_usuario = True, name = name)

@app.route('/menu_volta')
def menu_volta():
    return render_template('Menu.html',nome_usuario = False )

@app.route('/instrucao', methods=['POST', 'GET'])
def instrucao():
    return render_template('Instrucoes.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        for linha in open('info.txt'):
            linha_list = linha.strip().split('/')
            diclogin[linha_list[0]]=linha_list[1]
        user = request.form['nm']
        senha = request.form['pass']

        if user in diclogin and senha ==  diclogin[user]:
            global nome
            nome = user
            return redirect(url_for('menu',  name = user))
        else:
            return redirect(url_for('fail'))
    else:
        return render_template('Login.html')

@app.route('/cadastro', methods = ['POST', 'GET'])
def cadastro():
    if request.method == 'POST':
        user = request.form['nm']
        senha = request.form['pass']
        with open('info.txt', 'r+') as arquivo:
            linhas = arquivo.readlines()
            for i, linha in enumerate(linhas):
                partes = linha.strip().split('/')
                if partes[0] != user:
                    infoUser = "\n" + user + "/" + senha + "/" + "0" "/" + "0" + "/" + "0"
                    arquivo.write(infoUser)
                    arquivo.close()
                    return redirect(url_for('menu', name = user))  
                else:
                    return render_template('Cadastro.html', nome = True)
    else:
        return render_template('Cadastro.html')

@app.route('/escolha')
def escolha():
    return render_template('Escolha.html')

@app.route('/Jogo')
def Jogo():
    return render_template('Jogo.html')

@app.route('/historico', methods=['GET'])
def historico():
     if request.method == 'GET':
        nome_usuario = request.args.get('nome')
        if nome_usuario:
            info_user = ler_info_user(nome_usuario)
            return render_template('resultado.html', nome = nome_usuario, informacoes = info_user)

@app.route('/informacoes',methods = ['GET'])
def info():
    return render_template('informacoes.html')

@app.route('/resultado_final/<vitoria_ou_derrota>')
def resultado_final(vitoria_ou_derrota):
    global X_ou_O
    if (vitoria_ou_derrota == "1" and X_ou_O == "X") or (vitoria_ou_derrota == "2" and X_ou_O == "O"):
        resultado = 'vitoria'
        result_partida = 'Você Venceu'
        emoji_resul = True

    elif vitoria_ou_derrota == 'true':
        resultado = ''
        result_partida = 'Deu Velha'
        emoji_resul = False

    else:
        resultado = 'derrota'
        result_partida = 'Você Perdeu'
        emoji_resul = False

    print(nome)
    adicionar_resultado(arquivo, nome, resultado)
    Jogo_da_velha_flask.zerar_tudo()
    return render_template('Vitoria_Derrota.html', resultado_game = result_partida, emoji = emoji_resul)

@app.route('/jogada_A/<coordenada>/<P1>')
def jogada_A(coordenada, P1):
    global X_ou_O
    X_ou_O = P1
    resultados = {}
    Verifica_velha = False
    if X_ou_O == "X":
        Jogada_X = Jogo_da_velha_flask.jogadaPL(Jogo_da_velha_flask.player1, coordenada)
        Verifica_vitoria = Jogo_da_velha_flask.verificação()

        if Verifica_vitoria != "1" and Verifica_vitoria != "2":
            if Jogo_da_velha_flask.jogadas_possiveis != []:
                Jogada_O = Jogo_da_velha_flask.jogadaCPU(Jogo_da_velha_flask.player2)
                Verifica_vitoria = Jogo_da_velha_flask.verificação()
                resultados['Bola'] = Jogada_O
        if Jogo_da_velha_flask.jogadas_possiveis == []:
            if Verifica_vitoria != "1" and Verifica_vitoria != "2":
                Verifica_velha = True
    
    else:
        Jogada_X = Jogo_da_velha_flask.jogadaPL(Jogo_da_velha_flask.player2, coordenada)
        Verifica_vitoria = Jogo_da_velha_flask.verificação()

        if Verifica_vitoria != "1" and Verifica_vitoria != "2":
            if Jogo_da_velha_flask.jogadas_possiveis != []:
                Jogada_O = Jogo_da_velha_flask.jogadaCPU(Jogo_da_velha_flask.player1)
                Verifica_vitoria = Jogo_da_velha_flask.verificação()
                resultados['Bola'] = Jogada_O
        if Jogo_da_velha_flask.jogadas_possiveis == []:
            if Verifica_vitoria != "1" and Verifica_vitoria != "2":
                Verifica_velha = True

    resultados['X'] = Jogada_X
    resultados['Verifica_vitoria'] = Verifica_vitoria
    resultados['Verifica_velha'] = Verifica_velha
    return json.dumps(resultados)
    
@app.route('/jogada_B/<jogador>/<coordenada>/<P1>')
def jogada_B(jogador, coordenada, P1):
    global X_ou_O
    X_ou_O = P1
    resultados = {}
    Verifica_velha = False
   
    Jogada = Jogo_da_velha_flask.jogadaPL(jogador, coordenada)
    Verifica_vitoria = Jogo_da_velha_flask.verificação()
    resultados['Jogada'] = Jogada
    resultados['Verifica_vitoria'] = Verifica_vitoria

    if Jogo_da_velha_flask.jogadas_possiveis == []:
        if Verifica_vitoria != "1" and Verifica_vitoria != "2":
            Verifica_velha = True

    resultados['Verifica_vitoria'] = Verifica_vitoria
    resultados['Verifica_velha'] = Verifica_velha
    return json.dumps(resultados)

@app.route('/jogada_C/<P1>')
def jogada_C(P1):
    global X_ou_O
    X_ou_O = P1
    resultados = {}
    Verifica_velha = False
    Jogada_X = Jogo_da_velha_flask.jogadaCPU(Jogo_da_velha_flask.player1)
    Verifica_vitoria = Jogo_da_velha_flask.verificação()
    resultados['X'] = Jogada_X

    if Verifica_vitoria != "1" and Verifica_vitoria != "2":
        if Jogo_da_velha_flask.jogadas_possiveis != []:
            Jogada_O = Jogo_da_velha_flask.jogadaCPU(Jogo_da_velha_flask.player2)
            Verifica_vitoria = Jogo_da_velha_flask.verificação()
            resultados['Bola'] = Jogada_O
    if Jogo_da_velha_flask.jogadas_possiveis == []:
        if Verifica_vitoria != "1" and Verifica_vitoria != "2":
            Verifica_velha = True

    resultados['Verifica_vitoria'] = Verifica_vitoria
    resultados['Verifica_velha'] = Verifica_velha
    return json.dumps(resultados)

app.run(debug=True)
# app.run(host='0.0.0.0', port=5000)