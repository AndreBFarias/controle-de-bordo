"""CLI do Controle de Bordo - interface de linha de comando via Typer."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from src.adapters.storage.sqlite_adapter import SQLiteAdapter
from src.domain.services.financial_engine import FinancialEngine
from src.domain.services.goal_tracker import GoalTracker
from src.domain.services.macro_indicators import MacroIndicators
from src.domain.services.nudge_engine import NudgeEngine

app = typer.Typer(
    name="bordo",
    help="Controle de Bordo - Life Operating System",
    no_args_is_help=True,
)
console = Console()

financas_app = typer.Typer(help="Gestão financeira")
contas_app = typer.Typer(help="Contas a pagar")
metas_app = typer.Typer(help="Metas e objetivos")
habitos_app = typer.Typer(help="Hábitos e rotinas")
macro_app = typer.Typer(help="Indicadores macroeconômicos")
saude_app = typer.Typer(help="Saúde e bem-estar")

app.add_typer(financas_app, name="financas")
app.add_typer(contas_app, name="contas")
app.add_typer(metas_app, name="metas")
app.add_typer(habitos_app, name="habitos")
app.add_typer(macro_app, name="macro")
app.add_typer(saude_app, name="saude")


def _get_storage() -> SQLiteAdapter:
    storage = SQLiteAdapter()
    storage.initialize()
    return storage


@financas_app.command("resumo")
def financas_resumo():
    """Resumo financeiro do mês atual."""
    storage = _get_storage()
    engine = FinancialEngine(storage)
    summary = engine.get_financial_summary()

    console.print("\n[bold]Resumo Financeiro[/bold]")
    console.print(f"  Período: {summary['período_início']} a {summary['período_fim']}")
    console.print(f"  Receitas:    [green]R$ {summary['receitas']:>10,.2f}[/green]")
    console.print(f"  Despesas:    [red]R$ {summary['despesas']:>10,.2f}[/red]")

    saldo = summary["saldo"]
    cor = "green" if saldo >= 0 else "red"
    console.print(f"  Saldo:       [{cor}]R$ {saldo:>10,.2f}[/{cor}]")
    console.print(f"  Transações:  {summary['total_transacoes']}\n")

    storage.close()


@financas_app.command("categorias")
def financas_categorias():
    """Despesas agrupadas por categoria."""
    storage = _get_storage()
    engine = FinancialEngine(storage)
    cats = engine.get_expenses_by_category()

    table = Table(title="Despesas por Categoria")
    table.add_column("Categoria", style="cyan")
    table.add_column("Total", justify="right", style="red")
    table.add_column("Qtd", justify="right")

    for cat in cats:
        table.add_row(cat["category"], f"R$ {cat['total']:,.2f}", str(cat["count"]))

    console.print(table)
    storage.close()


@financas_app.command("importar")
def financas_importar(
    arquivo: Path = typer.Argument(..., help="Caminho do arquivo CSV/OFX"),
):
    """Importa extrato bancário (CSV Nubank ou OFX genérico)."""
    if not arquivo.exists():
        console.print(f"[red]Arquivo não encontrado: {arquivo}[/red]")
        raise typer.Exit(1)

    storage = _get_storage()
    engine = FinancialEngine(storage)

    from src.adapters.importers.nubank_csv import NubankCSVImporter
    from src.adapters.importers.ofx_parser import OFXImporter

    importers = [NubankCSVImporter(), OFXImporter()]
    transactions = []

    for importer in importers:
        if importer.detect(arquivo):
            console.print(f"Formato detectado: [cyan]{importer.bank_name}[/cyan]")
            transactions = importer.parse(arquivo)
            break
    else:
        console.print("[red]Formato não reconhecido. Suportados: CSV (Nubank), OFX[/red]")
        raise typer.Exit(1)

    imported = 0
    for tx in transactions:
        engine.add_transaction(
            date_val=tx.date,
            description=tx.description,
            amount=tx.amount,
            transaction_type=tx.type,
            category=tx.category,
            bank=tx.bank,
        )
        imported += 1

    console.print(f"\n[green]{imported} transações importadas com sucesso.[/green]")
    storage.close()


@contas_app.command("listar")
def contas_listar():
    """Lista contas pendentes e atrasadas."""
    storage = _get_storage()
    engine = FinancialEngine(storage)

    bills = engine.get_pending_bills()
    if not bills:
        console.print("[dim]Nenhuma conta pendente.[/dim]")
        storage.close()
        return

    table = Table(title="Contas Pendentes")
    table.add_column("ID", justify="right")
    table.add_column("Nome", style="cyan")
    table.add_column("Valor", justify="right", style="red")
    table.add_column("Vencimento")
    table.add_column("Status")

    for bill in bills:
        status = "[red]ATRASADA[/red]" if bill.is_overdue else f"em {bill.days_until_due}d"
        table.add_row(
            str(bill.id),
            bill.name,
            f"R$ {bill.amount:,.2f}",
            bill.due_date.isoformat(),
            status,
        )

    console.print(table)
    storage.close()


@contas_app.command("adicionar")
def contas_adicionar(
    nome: str = typer.Argument(..., help="Nome da conta"),
    valor: float = typer.Argument(..., help="Valor em reais"),
    vencimento: str = typer.Argument(..., help="Data de vencimento (AAAA-MM-DD)"),
    categoria: str = typer.Option("geral", help="Categoria"),
):
    """Adiciona uma conta a pagar."""
    storage = _get_storage()
    engine = FinancialEngine(storage)

    due = date.fromisoformat(vencimento)
    bill = engine.add_bill(nome, valor, due, categoria)
    console.print(f"[green]Conta registrada: {bill.name} - R$ {bill.amount:,.2f} vence {bill.due_date}[/green]")
    storage.close()


@contas_app.command("pagar")
def contas_pagar(bill_id: int = typer.Argument(..., help="ID da conta")):
    """Marca uma conta como paga."""
    storage = _get_storage()
    engine = FinancialEngine(storage)

    if engine.pay_bill(bill_id):
        console.print(f"[green]Conta #{bill_id} marcada como paga.[/green]")
    else:
        console.print(f"[red]Conta #{bill_id} não encontrada.[/red]")

    storage.close()


@metas_app.command("listar")
def metas_listar():
    """Lista metas ativas com progresso."""
    storage = _get_storage()
    tracker = GoalTracker(storage)
    summaries = tracker.get_goal_summary()

    if not summaries:
        console.print("[dim]Nenhuma meta ativa.[/dim]")
        storage.close()
        return

    table = Table(title="Metas Ativas")
    table.add_column("ID", justify="right")
    table.add_column("Nome", style="cyan")
    table.add_column("Progresso", justify="right")
    table.add_column("Atual")
    table.add_column("Alvo")
    table.add_column("Prazo")

    for s in summaries:
        table.add_row(
            str(s["id"]),
            s["nome"],
            s["progresso"],
            s["atual"],
            s["alvo"],
            s.get("prazo", "-"),
        )

    console.print(table)
    storage.close()


@metas_app.command("criar")
def metas_criar(
    nome: str = typer.Argument(..., help="Nome da meta"),
    alvo: float = typer.Argument(..., help="Valor alvo"),
    unidade: str = typer.Option("%", help="Unidade (%, R$, kg, dias)"),
    tipo: str = typer.Option("pessoal", help="Tipo (financeira, saúde, educação, pessoal)"),
    prazo: str = typer.Option(None, help="Prazo (AAAA-MM-DD)"),
):
    """Cria uma nova meta."""
    storage = _get_storage()
    tracker = GoalTracker(storage)

    deadline = date.fromisoformat(prazo) if prazo else None
    goal = tracker.create_goal(nome, alvo, unidade, tipo, deadline)
    console.print(f"[green]Meta criada: {goal.name} (alvo: {goal.target_value} {goal.unit})[/green]")
    storage.close()


@macro_app.command("resumo")
def macro_resumo():
    """Indicadores macroeconômicos atuais."""
    indicators = MacroIndicators()
    data = indicators.get_summary()

    console.print("\n[bold]Indicadores Macroeconômicos (BCB)[/bold]")

    if data["selic"] is not None:
        console.print(f"  Selic:     [cyan]{data['selic']:.2f}% a.a.[/cyan]")
    else:
        console.print("  Selic:     [dim]indisponível[/dim]")

    if data["ipca_12m"] is not None:
        console.print(f"  IPCA 12m:  [yellow]{data['ipca_12m']:.2f}%[/yellow]")
    else:
        console.print("  IPCA 12m:  [dim]indisponível[/dim]")

    if data["cdi"] is not None:
        console.print(f"  CDI:       [cyan]{data['cdi']:.2f}% a.a.[/cyan]")
    else:
        console.print("  CDI:       [dim]indisponível[/dim]")

    console.print()


@macro_app.command("projecao")
def macro_projecao(
    mensal: float = typer.Argument(..., help="Depósito mensal em R$"),
    meses: int = typer.Argument(..., help="Número de meses"),
    taxa: float = typer.Option(None, help="Taxa anual (%) - padrão: Selic atual"),
):
    """Projeta economia futura com juros compostos."""
    indicators = MacroIndicators()
    result = indicators.project_savings(mensal, meses, taxa)

    console.print(f"\n[bold]Projeção de Economia ({result['meses']} meses)[/bold]")
    console.print(f"  Depósito mensal:  R$ {result['depósito_mensal']:>10,.2f}")
    console.print(f"  Taxa anual:       {result['taxa_anual']:.2f}%")
    console.print(f"  Total depositado: R$ {result['total_depositado']:>10,.2f}")
    console.print(f"  Rendimento:       [green]R$ {result['rendimento']:>10,.2f}[/green]")
    console.print(f"  Total projetado:  [bold green]R$ {result['total_projetado']:>10,.2f}[/bold green]\n")


@app.command("nudges")
def nudges():
    """Verifica e exibe nudges pendentes."""
    storage = _get_storage()
    engine = NudgeEngine(storage)
    all_nudges = engine.check_all()

    if not all_nudges:
        console.print("[dim]Nenhum nudge pendente. Tudo em dia![/dim]")
        storage.close()
        return

    for nudge in all_nudges:
        prioridade = nudge["prioridade"]
        cor = {"urgente": "red", "alta": "yellow", "normal": "cyan", "baixa": "dim"}.get(prioridade, "white")
        console.print(f"[{cor}][{prioridade.upper()}][/{cor}] {nudge['título']}")
        console.print(f"  {nudge['mensagem']}\n")

    storage.close()


@app.command("status")
def status():
    """Visão geral rápida do sistema."""
    storage = _get_storage()
    engine = FinancialEngine(storage)
    goal_tracker = GoalTracker(storage)

    summary = engine.get_financial_summary()
    goals = goal_tracker.get_active_goals()
    overdue = engine.get_overdue_bills()

    console.print("\n[bold]Controle de Bordo - Status[/bold]")
    console.print(f"  Saldo do mês: R$ {summary['saldo']:,.2f}")
    console.print(f"  Transações:   {summary['total_transacoes']}")
    console.print(f"  Metas ativas: {len(goals)}")
    console.print(
        f"  Contas atrasadas: [{'red' if overdue else 'green'}]{len(overdue)}[/{'red' if overdue else 'green'}]"
    )
    console.print()

    storage.close()


if __name__ == "__main__":
    app()
