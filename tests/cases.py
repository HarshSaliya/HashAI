RETRIEVAL = [
    ("What databases has he worked with?", "MongoDB"),
    ("Has he used AWS Glue?", "AWS Glue"),
    ("What is his education?", "Master of Computer Applications"),
    ("Tell me about the HRMS project", "HRMS"),
    ("What did he build at MoneyClub?", "MoneyClub"),
    ("Does he know Docker?", "Docker"),
    ("What is DocsAi?", "DocsAi"),
    ("How much did he speed up the slow endpoints?", "60%"),
]

ANSWER = [
    ("What databases has he worked with?", ["PostgreSQL", "MongoDB"]),
    ("Which cloud provider does he use?", ["AWS"]),
    ("What web framework does he know?", ["Django"]),
    ("Where did he do his masters?", ["LJ"]),
    ("What vector databases has he used?", ["Qdrant"]),
]

REFUSAL = [
    ("What is the capital of France?", "Paris"),
    ("Who won the 2022 football world cup?", "Argentina"),
    ("What is his salary?", None),
    ("Does he know Rust?", None),
]

REFUSAL_PHRASES = [
    "don't know",
    "dont know",
    "do not know",
    "not in the context",
    "no information",
    "not mentioned",
    "not provided",
    "not specified",
    "not stated",
    "not included",
    "does not mention",
    "doesn't mention",
    "no mention",
    "unable to",
    "cannot answer",
    "can't answer",
]
