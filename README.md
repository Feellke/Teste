# Sistema de Avaliação - Missão e Evangelismo

Este é um sistema web para avaliação de afirmações sobre missão e evangelismo, desenvolvido com Flask.

## Características

- Interface moderna e responsiva
- Avaliação de afirmações com notas de 0 a 10
- Análise e ranking das afirmações
- Envio automático de relatórios por e-mail
- Funciona com respostas parciais

## Tecnologias

- Backend: Flask (Python)
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Hospedagem: Compatível com Render, Heroku, PythonAnywhere

## Configuração para Desenvolvimento

1. Clone o repositório
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Execute o aplicativo:
   ```
   python app.py
   ```

## Configuração para Produção

O aplicativo está configurado para ser facilmente implantado em serviços de hospedagem como Render:

- Procfile incluído para serviços compatíveis com Gunicorn
- Variáveis de ambiente para configuração de e-mail e banco de dados
- Porta configurável via variável de ambiente PORT

## Estrutura do Projeto

```
avaliacao_web/
├── app.py                # Aplicativo Flask principal
├── Procfile              # Configuração para hospedagem
├── requirements.txt      # Dependências
├── static/               # Arquivos estáticos
│   ├── css/              # Estilos CSS
│   ├── js/               # JavaScript
│   └── img/              # Imagens
└── templates/            # Templates HTML
```

## Licença

Este projeto é para uso exclusivo conforme solicitado.

## Jogo de Quiz Bíblico

Um pequeno jogo em linha de comando foi adicionado para ajudar jovens a estudarem histórias da Bíblia. Para jogar, execute:

```
python bible_quiz.py
```

O jogo apresenta perguntas de múltipla escolha e mostra a referência bíblica correspondente após cada resposta.
