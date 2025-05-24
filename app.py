import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import statistics
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Lista de afirmações para avaliação
perguntas = [
    "Missão como participação na Missio Dei",
    "Missão a partir da cruz",
    "Chamados para a missão onde estamos: a missão local",
    "A missão da igreja em tempos de pluralismo religioso",
    "Missão integral: Palavra e ação social",
    "Desafios e oportunidades da missão na era pós-moderna",
    "Missão e discipulado: formando uma igreja viva e atuante",
    "Missão e vocação: todos chamados, todos enviados",
    "A justificação pela fé como centro da mensagem evangelística",
    "Evangelismo pessoal e testemunho cotidiano",
    "Evangelismo em meio à resistência e oposição",
    "A evangelização e o batismo",
    "Evangelismo em tempos de crise e sofrimento",
    "Evangelismo e cultura: evitando sincretismos",
    "Reavivando a paixão evangelística na congregação",
    "Evangelismo e as perguntas do coração humano",
    "Evangelismo como ação do Espírito Santo",
    "Evangelismo em contexto urbano e digital",
    "Evangelismo com integridade: ética e verdade no testemunho",
    "Reavivando a paixão evangelística na comunidade"
]

# Classe para armazenar avaliações
class Avaliacao:
    def __init__(self):
        self.respostas = {}
        self.timestamp = datetime.now()
        self.id = self.timestamp.strftime("%Y%m%d%H%M%S")
    
    def adicionar_resposta(self, pergunta_id, nota):
        """Adiciona ou atualiza uma resposta"""
        try:
            nota_int = int(nota)
            if 0 <= nota_int <= 10:
                self.respostas[pergunta_id] = nota_int
                return True
            return False
        except (ValueError, TypeError):
            return False
    
    def obter_respostas(self):
        """Retorna todas as respostas registradas"""
        return self.respostas
    
    def calcular_media(self):
        """Calcula a média das notas, se houver respostas"""
        if not self.respostas:
            return 0
        return sum(self.respostas.values()) / len(self.respostas)
    
    def esta_completa(self):
        """Verifica se todas as perguntas foram respondidas"""
        return len(self.respostas) == len(perguntas)
    
    def to_dict(self):
        """Converte a avaliação para um dicionário"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "respostas": self.respostas,
            "media": self.calcular_media(),
            "completa": self.esta_completa()
        }

# Armazenar avaliações (em produção seria um banco de dados)
avaliacoes = []

# Função para analisar avaliações
def analisar_avaliacoes(avaliacoes_lista):
    """
    Analisa as avaliações e gera um ranking das perguntas.
    
    Args:
        avaliacoes_lista: Lista de objetos Avaliacao
        
    Returns:
        Um dicionário com análises e ranking
    """
    # Inicializar estruturas de dados para análise
    notas_por_pergunta = {}
    for i in range(len(perguntas)):
        notas_por_pergunta[i] = []
    
    total_avaliacoes = len(avaliacoes_lista)
    avaliacoes_completas = 0
    
    # Coletar todas as notas por pergunta
    for avaliacao in avaliacoes_lista:
        if avaliacao.esta_completa():
            avaliacoes_completas += 1
        
        for pergunta_id, nota in avaliacao.obter_respostas().items():
            notas_por_pergunta[int(pergunta_id)].append(nota)
    
    # Calcular estatísticas para cada pergunta
    estatisticas_perguntas = []
    for i, pergunta in enumerate(perguntas):
        notas = notas_por_pergunta.get(i, [])
        
        # Calcular estatísticas (com tratamento para listas vazias)
        if notas:
            media = sum(notas) / len(notas)
            mediana = statistics.median(notas) if notas else 0
            moda = statistics.mode(notas) if notas else 0
            desvio_padrao = statistics.stdev(notas) if len(notas) > 1 else 0
            total_respostas = len(notas)
            percentual_respostas = (total_respostas / total_avaliacoes) * 100 if total_avaliacoes > 0 else 0
        else:
            media = mediana = moda = desvio_padrao = 0
            total_respostas = 0
            percentual_respostas = 0
        
        estatisticas_perguntas.append({
            'id': i,
            'pergunta': pergunta,
            'media': round(media, 2),
            'mediana': mediana,
            'moda': moda,
            'desvio_padrao': round(desvio_padrao, 2),
            'total_respostas': total_respostas,
            'percentual_respostas': round(percentual_respostas, 2)
        })
    
    # Ordenar perguntas por média (ranking)
    ranking_media = sorted(estatisticas_perguntas, key=lambda x: x['media'], reverse=True)
    
    # Ordenar perguntas por total de respostas (popularidade)
    ranking_popularidade = sorted(estatisticas_perguntas, key=lambda x: x['total_respostas'], reverse=True)
    
    # Gerar relatório final
    relatorio = {
        'total_avaliacoes': total_avaliacoes,
        'avaliacoes_completas': avaliacoes_completas,
        'percentual_completas': round((avaliacoes_completas / total_avaliacoes) * 100, 2) if total_avaliacoes > 0 else 0,
        'estatisticas_perguntas': estatisticas_perguntas,
        'ranking_media': ranking_media,
        'ranking_popularidade': ranking_popularidade,
        'timestamp': datetime.now().isoformat()
    }
    
    return relatorio

# Função para gerar relatório HTML
def gerar_relatorio_html(relatorio):
    """
    Gera um relatório HTML formatado com os resultados da análise.
    
    Args:
        relatorio: Dicionário com os dados da análise
        
    Returns:
        String HTML formatada
    """
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Avaliações</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }
            h1, h2, h3 {
                color: #2c3e50;
            }
            .card {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 20px;
                margin-bottom: 20px;
            }
            .summary {
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                margin-bottom: 30px;
            }
            .summary-item {
                background: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                padding: 15px;
                flex: 1;
                min-width: 200px;
                margin: 10px;
                text-align: center;
            }
            .summary-item h3 {
                margin: 0;
                font-size: 16px;
                color: #7f8c8d;
            }
            .summary-item p {
                margin: 10px 0 0;
                font-size: 24px;
                font-weight: bold;
                color: #2980b9;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            th, td {
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #e0e0e0;
            }
            th {
                background-color: #3498db;
                color: white;
                font-weight: 500;
            }
            tr:hover {
                background-color: #f5f5f5;
            }
            .meter {
                height: 10px;
                background: #e0e0e0;
                border-radius: 5px;
                margin-top: 5px;
            }
            .meter-fill {
                height: 100%;
                background: #3498db;
                border-radius: 5px;
                width: 0%;
            }
            .timestamp {
                text-align: right;
                color: #7f8c8d;
                font-size: 14px;
                margin-top: 30px;
            }
        </style>
    </head>
    <body>
        <h1>Relatório de Avaliações</h1>
        
        <div class="summary">
            <div class="summary-item">
                <h3>Total de Avaliações</h3>
                <p>{total_avaliacoes}</p>
            </div>
            <div class="summary-item">
                <h3>Avaliações Completas</h3>
                <p>{avaliacoes_completas} ({percentual_completas}%)</p>
            </div>
        </div>
        
        <div class="card">
            <h2>Ranking por Média de Notas</h2>
            <table>
                <thead>
                    <tr>
                        <th>Posição</th>
                        <th>Afirmação</th>
                        <th>Média</th>
                        <th>Total de Respostas</th>
                    </tr>
                </thead>
                <tbody>
    """.format(
        total_avaliacoes=relatorio['total_avaliacoes'],
        avaliacoes_completas=relatorio['avaliacoes_completas'],
        percentual_completas=relatorio['percentual_completas']
    )
    
    # Adicionar linhas da tabela de ranking por média
    for i, item in enumerate(relatorio['ranking_media']):
        html += """
                    <tr>
                        <td>{posicao}</td>
                        <td>{pergunta}</td>
                        <td>{media}</td>
                        <td>
                            {total_respostas} ({percentual}%)
                            <div class="meter">
                                <div class="meter-fill" style="width: {percentual}%;"></div>
                            </div>
                        </td>
                    </tr>
        """.format(
            posicao=i+1,
            pergunta=item['pergunta'],
            media=item['media'],
            total_respostas=item['total_respostas'],
            percentual=item['percentual_respostas']
        )
    
    html += """
                </tbody>
            </table>
        </div>
        
        <div class="card">
            <h2>Estatísticas Detalhadas</h2>
            <table>
                <thead>
                    <tr>
                        <th>Afirmação</th>
                        <th>Média</th>
                        <th>Mediana</th>
                        <th>Moda</th>
                        <th>Desvio Padrão</th>
                        <th>Total de Respostas</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Adicionar linhas da tabela de estatísticas
    for item in relatorio['estatisticas_perguntas']:
        html += """
                    <tr>
                        <td>{pergunta}</td>
                        <td>{media}</td>
                        <td>{mediana}</td>
                        <td>{moda}</td>
                        <td>{desvio_padrao}</td>
                        <td>{total_respostas} ({percentual}%)</td>
                    </tr>
        """.format(
            pergunta=item['pergunta'],
            media=item['media'],
            mediana=item['mediana'],
            moda=item['moda'],
            desvio_padrao=item['desvio_padrao'],
            total_respostas=item['total_respostas'],
            percentual=item['percentual_respostas']
        )
    
    html += """
                </tbody>
            </table>
        </div>
        
        <p class="timestamp">Relatório gerado em: {timestamp}</p>
    </body>
    </html>
    """.format(timestamp=relatorio['timestamp'])
    
    return html

# Função para enviar e-mail
def enviar_ranking(avaliacoes_lista):
    """
    Analisa as avaliações e envia o ranking por e-mail.
    
    Args:
        avaliacoes_lista: Lista de objetos Avaliacao
    
    Returns:
        Boolean indicando sucesso ou falha no envio
    """
    # Verificar se há avaliações para analisar
    if not avaliacoes_lista:
        print("Nenhuma avaliação para analisar e enviar.")
        return False
    
    # Gerar relatório de análise
    relatorio = analisar_avaliacoes(avaliacoes_lista)
    html_relatorio = gerar_relatorio_html(relatorio)
    
    # Configurações de e-mail
    destinatario = "fernando@ielb.org.br"
    assunto = f"Ranking de Afirmações - {len(avaliacoes_lista)} avaliações"
    
    # Em um ambiente de produção, usaríamos SMTP real
    # Como estamos em ambiente de desenvolvimento/hospedagem gratuita,
    # vamos simular o envio e salvar o relatório para visualização
    
    # Salvar o relatório em um arquivo para visualização
    try:
        with open('static/ultimo_relatorio.html', 'w') as f:
            f.write(html_relatorio)
        
        print(f"Relatório gerado e salvo. Em produção seria enviado para {destinatario}")
        print(f"Total de avaliações analisadas: {relatorio['total_avaliacoes']}")
        print(f"Avaliações completas: {relatorio['avaliacoes_completas']} ({relatorio['percentual_completas']}%)")
        
        # Em um ambiente real, usaríamos código como este:
        """
        msg = MIMEMultipart('alternative')
        msg['Subject'] = assunto
        msg['From'] = "sistema@avaliacao.com"
        msg['To'] = destinatario
        
        # Anexar versão HTML
        parte_html = MIMEText(html_relatorio, 'html')
        msg.attach(parte_html)
        
        # Enviar e-mail
        with smtplib.SMTP('smtp.servidor.com', 587) as servidor:
            servidor.starttls()
            servidor.login('usuario', 'senha')
            servidor.send_message(msg)
        """
        
        return True
    except Exception as e:
        print(f"Erro ao processar relatório: {str(e)}")
        return False

# Inicializar aplicação Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave para sessões

# Rota principal
@app.route('/')
def index():
    """Rota principal que exibe o formulário de avaliação"""
    # Iniciar uma nova avaliação se não existir na sessão
    if 'avaliacao_id' not in session:
        nova_avaliacao = Avaliacao()
        avaliacoes.append(nova_avaliacao)
        session['avaliacao_id'] = nova_avaliacao.id
    
    # Recuperar a avaliação atual
    avaliacao_atual = None
    for avaliacao in avaliacoes:
        if avaliacao.id == session.get('avaliacao_id'):
            avaliacao_atual = avaliacao
            break
    
    # Se não encontrar (sessão inválida), criar nova
    if avaliacao_atual is None:
        avaliacao_atual = Avaliacao()
        avaliacoes.append(avaliacao_atual)
        session['avaliacao_id'] = avaliacao_atual.id
    
    # Renderizar o template com as perguntas e respostas atuais
    return render_template('index.html', 
                          perguntas=perguntas, 
                          respostas=avaliacao_atual.obter_respostas())

# Rota para processar avaliações
@app.route('/avaliar', methods=['POST'])
def avaliar():
    """Rota para processar as avaliações enviadas"""
    # Recuperar a avaliação atual
    avaliacao_atual = None
    for avaliacao in avaliacoes:
        if avaliacao.id == session.get('avaliacao_id'):
            avaliacao_atual = avaliacao
            break
    
    # Se não encontrar, criar nova
    if avaliacao_atual is None:
        avaliacao_atual = Avaliacao()
        avaliacoes.append(avaliacao_atual)
        session['avaliacao_id'] = avaliacao_atual.id
    
    # Processar as respostas do formulário
    for i, _ in enumerate(perguntas):
        nota = request.form.get(f'pergunta_{i}')
        if nota:
            avaliacao_atual.adicionar_resposta(i, nota)
    
    # Enviar para análise e ranking (mesmo que parcial)
    enviar_ranking(avaliacoes)
    
    # Redirecionar para a página de agradecimento
    return redirect(url_for('agradecimento'))

# Rota para página de agradecimento
@app.route('/agradecimento')
def agradecimento():
    """Página de agradecimento após envio da avaliação"""
    # Limpar a sessão atual
    session.pop('avaliacao_id', None)
    return render_template('agradecimento.html')

# API para salvar nota individual
@app.route('/api/salvar', methods=['POST'])
def salvar_nota():
    """API para salvar uma nota individual via AJAX"""
    data = request.json
    pergunta_id = data.get('pergunta_id')
    nota = data.get('nota')
    
    # Validar os dados
    if pergunta_id is None or nota is None:
        return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
    
    # Recuperar a avaliação atual
    avaliacao_atual = None
    for avaliacao in avaliacoes:
        if avaliacao.id == session.get('avaliacao_id'):
            avaliacao_atual = avaliacao
            break
    
    # Se não encontrar, criar nova
    if avaliacao_atual is None:
        avaliacao_atual = Avaliacao()
        avaliacoes.append(avaliacao_atual)
        session['avaliacao_id'] = avaliacao_atual.id
    
    # Salvar a nota
    sucesso = avaliacao_atual.adicionar_resposta(int(pergunta_id), nota)
    
    return jsonify({
        'success': sucesso, 
        'avaliacao': avaliacao_atual.to_dict()
    })

# Rota para visualizar o último relatório (apenas para teste)
@app.route('/relatorio')
def relatorio():
    """Visualizar o último relatório gerado"""
    try:
        with open('static/ultimo_relatorio.html', 'r') as f:
            return f.read()
    except:
        return "Nenhum relatório gerado ainda."

# Ponto de entrada para execução
if __name__ == '__main__':
    # Criar diretórios necessários
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/img', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Usar porta alternativa se 5000 estiver em uso
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
