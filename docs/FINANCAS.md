# Módulo Financeiro - Controle de Bordo

## Visão Geral

O módulo financeiro é o pilar central do sistema. Gerencia transações, contas a pagar, orçamentos, categorização automática e prevenção de compras impulsivas, com indicadores macroeconômicos brasileiros.

## Importação de Dados Bancários

### Por que não usamos Open Finance / Belvo / Pluggy

1. **Open Finance Brasil**: Exige autorização do BCB como instituição financeira participante. Um dev independente ou projeto open source não pode acessar diretamente
2. **Belvo**: Contrato mínimo de 12 meses, preço por transação, voltado para fintechs
3. **Pluggy**: Trial de 15 dias, depois plano enterprise

### Estratégia de importação (3 fases)

**V1 - CSV/OFX manual (atual)**
- Usuário exporta extrato do app/internet banking
- Sistema detecta o formato e banco automaticamente
- Categorização automática via palavras-chave

**V2 - Parser de notificações (futuro)**
- Tasker no Android captura notificações bancárias
- Extrai valor, descrição e data via regex
- Envia para o sistema via ntfy.sh ou arquivo local

**V3 - Open Finance via parceiro (futuro longínquo)**
- Se/quando um intermediário oferecer tier gratuito
- Ou se o projeto crescer para ter parceria institucional

### Bancos suportados

| Banco | Formato | Parser | Status |
|-------|---------|--------|--------|
| Nubank | CSV | `nubank_csv.py` | Implementado |
| Genérico | OFX | `ofx_parser.py` | Implementado |
| Genérico | CSV | `generic_csv.py` | Implementado |
| Itaú | OFX | Via OFX genérico | Suportado |
| BB | OFX | Via OFX genérico | Suportado |
| Bradesco | OFX | Via OFX genérico | Suportado |
| Inter | OFX | Via OFX genérico | Suportado |
| Santander | OFX | Via OFX genérico | Suportado |

### Formato do CSV Nubank

```csv
Data,Valor,Identificador,Descrição
2026-03-15,-45.90,abc123,IFOOD *RESTAURANTE
2026-03-14,-89.00,def456,AMAZON.COM.BR
2026-03-01,18000.00,ghi789,SALARIO EMPRESA LTDA
```

## Categorização Automática

O `financial_engine.py` categoriza transações por palavras-chave na descrição:

| Categoria | Palavras-chave |
|-----------|---------------|
| Alimentação | ifood, rappi, supermercado, padaria, açougue |
| Transporte | uber, 99, combustível, estacionamento |
| Moradia | aluguel, condomínio, energia, água, internet |
| Saúde | farmácia, consulta, plano de saúde, academia |
| Educação | alura, coursera, duolingo, livro, curso |
| Lazer | netflix, spotify, cinema, bar, steam |
| Tecnologia | amazon, mercado livre, kabum, shopee |
| Beleza | salão, barbearia, cosméticos |
| Pet | veterinário, ração, petshop, petz |

## Motor Anti-Impulso

Baseado em economia comportamental (Thaler & Sunstein), o `impulse_filter.py` implementa fricção digital contra compras impulsivas.

### Níveis de fricção

| Nível | Condição | Intervenção |
|-------|----------|-------------|
| Nenhuma | Categoria essencial | Nada |
| Suave | Categoria de risco | Lembrete das metas |
| Média | Valor acima do limiar | Esperar 24h + impacto nas metas |
| Forte | Orçamento mensal > 80% | Justificativa em 3 frases |
| Bloqueio | Orçamento estourado | Bloqueio + alerta urgente |

### Vieses combatidos

- **Viés do presente**: Gráfico de impacto futuro da compra
- **Aversão à perda**: Enquadrar economia não feita como "perda"
- **Contabilidade mental**: "Baldes" virtuais para cada meta

## Indicadores Macroeconômicos

O `macro_indicators.py` usa finbr e python-bcb para acessar dados do BCB:

| Indicador | Fonte | Uso |
|-----------|-------|-----|
| Selic | finbr.selic() / SGS 432 | Taxa base para projeções de investimento |
| IPCA | finbr.ipca() / SGS 433 | Inflação para projeção do custo de imóveis |
| CDI | finbr.cdi() / SGS 12 | Rendimento de CDBs e fundos |

### Projeção de economia

```python
# Exemplo: quanto preciso poupar por mês para R$ 100.000 em 24 meses?
indicators = MacroIndicators()
projection = indicators.project_savings(
    monthly_deposit=4000,
    months=24,
    annual_rate=None,  # usa Selic atual automaticamente
)
# {'total_projetado': 108432.50, 'rendimento': 12432.50, ...}
```

## Modelo de Dados

### Transação (transactions)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER PK | Identificador único |
| date | TEXT | Data (ISO 8601) |
| description | TEXT | Descrição da transação |
| amount | REAL | Valor (+ receita, - despesa) |
| type | TEXT | receita, despesa, transferência |
| category | TEXT | Categoria automática |
| bank | TEXT | Banco de origem |
| is_impulse | INTEGER | Marcada como impulso |
| is_recurring | INTEGER | Gasto recorrente |

### Conta a pagar (bills)

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER PK | Identificador único |
| name | TEXT | Nome da conta |
| amount | REAL | Valor |
| due_date | TEXT | Data de vencimento |
| status | TEXT | pendente, paga, atrasada, cancelada |
| recurrence | TEXT | única, mensal, anual, semanal |
| reminder_days | INTEGER | Dias antes para lembrar |

*"A riqueza consiste não em ter grandes posses, mas em ter poucas necessidades." - Epicteto*
