import random

# Lista de perguntas do quiz
QUESTIONS = [
    {
        "question": "Quem foi lançado na cova dos leões?",
        "options": ["Daniel", "Davi", "Jonas", "Moisés"],
        "answer": 0,
        "reference": "Daniel 6"
    },
    {
        "question": "Quem construiu uma arca para sobreviver ao dilúvio?",
        "options": ["Noé", "Abraão", "Elias", "Pedro"],
        "answer": 0,
        "reference": "Gênesis 6"
    },
    {
        "question": "Quem derrotou o gigante Golias?",
        "options": ["Sansão", "Saul", "Davi", "Salomão"],
        "answer": 2,
        "reference": "1 Samuel 17"
    },
    {
        "question": "Quem foi engolido por um grande peixe?",
        "options": ["Paulo", "Jonas", "José", "Isaías"],
        "answer": 1,
        "reference": "Jonas 1"
    },
    {
        "question": "Quem recebeu os Dez Mandamentos?",
        "options": ["Moisés", "Arão", "Josué", "Ezequiel"],
        "answer": 0,
        "reference": "Êxodo 20"
    }
]


def run_quiz():
    """Executa o quiz no terminal."""
    print("Bem-vindo ao Quiz das Histórias da Bíblia!")
    questions = QUESTIONS.copy()
    random.shuffle(questions)
    score = 0
    for idx, q in enumerate(questions, start=1):
        print(f"\nPergunta {idx}: {q['question']}")
        for i, option in enumerate(q['options'], start=1):
            print(f"  {i}. {option}")
        try:
            choice = int(input("Sua resposta (1-4): ")) - 1
        except ValueError:
            choice = -1
        if choice == q['answer']:
            print("Correto!")
            score += 1
        else:
            correct = q['options'][q['answer']]
            print(f"Errado! A resposta correta é: {correct}")
            print(f"Referência Bíblica: {q['reference']}")
    print(f"\nPontuação final: {score} de {len(questions)}")


if __name__ == "__main__":
    run_quiz()
