"""Categorização automática de transações por palavras-chave.

Módulo independente que pode ser usado por qualquer adaptador
sem depender de serviços de domínio (respeita arquitetura hexagonal).
"""

from __future__ import annotations

from src.domain.entities.transaction import TransactionCategory

CATEGORY_KEYWORDS: dict[TransactionCategory, list[str]] = {
    TransactionCategory.ALIMENTACAO: [
        "ifood",
        "rappi",
        "uber eats",
        "restaurante",
        "lanchonete",
        "padaria",
        "supermercado",
        "mercado",
        "hortifruti",
        "açougue",
        "feira",
    ],
    TransactionCategory.TRANSPORTE: [
        "uber",
        "99",
        "cabify",
        "combustível",
        "gasolina",
        "estacionamento",
        "pedágio",
        "metro",
        "ônibus",
    ],
    TransactionCategory.MORADIA: [
        "aluguel",
        "condomínio",
        "iptu",
        "energia",
        "água",
        "gás",
        "internet",
    ],
    TransactionCategory.SAUDE: [
        "farmácia",
        "drogaria",
        "consulta",
        "plano de saúde",
        "academia",
        "dentista",
        "hospital",
    ],
    TransactionCategory.EDUCACAO: [
        "alura",
        "coursera",
        "udemy",
        "livro",
        "curso",
        "escola",
        "faculdade",
        "duolingo",
        "open english",
    ],
    TransactionCategory.LAZER: [
        "netflix",
        "spotify",
        "cinema",
        "teatro",
        "bar",
        "balada",
        "show",
        "jogo",
        "game",
        "steam",
        "playstation",
        "xbox",
    ],
    TransactionCategory.ASSINATURAS: [
        "assinatura",
        "mensalidade",
        "plano",
        "premium",
        "pro",
    ],
    TransactionCategory.TECNOLOGIA: [
        "amazon",
        "mercado livre",
        "kabum",
        "pichau",
        "terabyte",
        "aliexpress",
        "shopee",
        "shein",
    ],
    TransactionCategory.BELEZA: [
        "salão",
        "barbearia",
        "cabeleireiro",
        "cosméticos",
        "perfume",
    ],
    TransactionCategory.PET: [
        "pet",
        "veterinário",
        "ração",
        "petshop",
        "petz",
        "cobasi",
    ],
    TransactionCategory.VESTUARIO: [
        "roupa",
        "calçado",
        "tênis",
        "camisa",
        "renner",
        "c&a",
        "riachuelo",
    ],
    TransactionCategory.SALARIO: [
        "salário",
        "salario",
        "pagamento empresa",
        "pro labore",
        "freelance",
        "honorário",
        "bonificação",
    ],
}


def categorize_by_description(description: str) -> TransactionCategory:
    """Categoriza automaticamente uma transação pela descrição.

    Busca case-insensitive por substrings nas palavras-chave de cada categoria.
    Retorna OUTROS se nenhuma correspondência for encontrada.
    """
    desc_lower = description.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return TransactionCategory.OUTROS
