import random

POSITIVE_FEEDBACK = [
    "Muito bem! Você é um explorador da Bíblia!",
    "Acertou! Você está indo super bem!",
    "Excelente! Continue assim!",
    "Uau! Resposta certa!",
]

ENCOURAGING_FEEDBACK = [
    "Quase! Você está aprendendo!",
    "Tudo bem errar, vamos tentar a próxima!",
    "Boa tentativa! Você consegue!",
    "Não foi dessa vez, mas você está indo bem!",
]

# Perguntas baseadas em João 1.35–51
QUESTIONS = [
    {
        "level": "4-7",
        "question": "Quem João Batista disse ser o Cordeiro de Deus?",
        "options": ["Jesus", "Pedro", "André", "João"],
        "answer": 0,
        "reference": "João 1.36",
    },
    {
        "level": "4-7",
        "question": "Dois discípulos seguiram Jesus. Um deles se chamava?",
        "options": ["André", "Filipe", "Tomé", "Tiago"],
        "answer": 0,
        "reference": "João 1.40",
    },
    {
        "level": "4-7",
        "question": "André foi contar a boa notícia para quem?",
        "options": ["Seu irmão Simão", "Seu pai", "Sua mãe", "Seu primo"],
        "answer": 0,
        "reference": "João 1.41-42",
    },
    {
        "level": "4-7",
        "question": "Qual novo nome Jesus deu a Simão?",
        "options": ["Pedro", "Mateus", "Paulo", "Elias"],
        "answer": 0,
        "reference": "João 1.42",
    },
    {
        "level": "4-7",
        "question": "Quem Jesus chamou dizendo: \"Siga-me\"?",
        "options": ["Filipe", "Judas", "Bartolomeu", "Lucas"],
        "answer": 0,
        "reference": "João 1.43",
    },
    {
        "level": "4-7",
        "question": "Filipe contou a Natanael sobre quem?",
        "options": ["Jesus", "Moisés", "Davi", "Noé"],
        "answer": 0,
        "reference": "João 1.45",
    },
    {
        "level": "8-12",
        "question": "O que os dois discípulos perguntaram a Jesus ao segui-lo?",
        "options": [
            "Mestre, onde moras?",
            "Mestre, quem és tu?",
            "Mestre, por que vieste?",
            "Mestre, o que farás?",
        ],
        "answer": 0,
        "reference": "João 1.38",
    },
    {
        "level": "8-12",
        "question": "O que Jesus respondeu quando perguntaram onde ele morava?",
        "options": ["Vinde e vede", "Esperem aqui", "Voltem amanhã", "Sigam João"],
        "answer": 0,
        "reference": "João 1.39",
    },
    {
        "level": "8-12",
        "question": "Qual era a cidade de Filipe?",
        "options": ["Betsaida", "Belém", "Nazareno", "Cafarnaum"],
        "answer": 0,
        "reference": "João 1.44",
    },
    {
        "level": "8-12",
        "question": "Quando Natanael duvidou, ele disse que algo bom poderia vir de qual lugar?",
        "options": ["Nazaré", "Jerusalém", "Belém", "Samaria"],
        "answer": 0,
        "reference": "João 1.46",
    },
    {
        "level": "8-12",
        "question": "Jesus viu Natanael debaixo de quê?",
        "options": ["Uma figueira", "Uma oliveira", "Uma palmeira", "Uma videira"],
        "answer": 0,
        "reference": "João 1.48",
    },
    {
        "level": "8-12",
        "question": "Que título Natanael disse sobre Jesus?",
        "options": [
            "Filho de Deus e Rei de Israel",
            "Profeta e líder",
            "Rei dos reis e sacerdote",
            "Mestre e escriba",
        ],
        "answer": 0,
        "reference": "João 1.49",
    },
]


def choose_level():
    print("Escolha o nível do quiz:")
    print("  1. 4-7 anos")
    print("  2. 8-12 anos")
    choice = input("Digite 1 ou 2: ").strip()
    if choice == "2":
        return "8-12"
    return "4-7"


def run_quiz():
    """Executa o quiz no terminal."""
    print("Bem-vindo ao Quiz das Histórias da Bíblia! 🎉")
    level = choose_level()
    print(f"Vamos jogar no nível {level}! Você consegue! 💪")

    questions = [q for q in QUESTIONS if q["level"] == level]
    random.shuffle(questions)
    score = 0

    for idx, q in enumerate(questions, start=1):
        print(f"\nPergunta {idx}: {q['question']}")
        for i, option in enumerate(q["options"], start=1):
            print(f"  {i}. {option}")
        try:
            choice = int(input("Sua resposta (1-4): ")) - 1
        except ValueError:
            choice = -1

        if choice == q["answer"]:
            print(random.choice(POSITIVE_FEEDBACK))
            score += 1
        else:
            correct = q["options"][q["answer"]]
            print(random.choice(ENCOURAGING_FEEDBACK))
            print(f"A resposta correta é: {correct} 🌟")
            print(f"Referência Bíblica: {q['reference']}")

    print(f"\nVocê terminou! Sua pontuação foi {score} de {len(questions)}. Parabéns! 🥳")


if __name__ == "__main__":
    run_quiz()
