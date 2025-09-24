from . import start, random_fact, gpt, talk, quiz, translator, recs

routers = [
    start.router,
    random_fact.router,
    gpt.router,
    talk.router,
    quiz.router,
    translator.router,
    recs.router,
]
