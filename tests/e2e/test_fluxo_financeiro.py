"""Teste E2E: fluxo financeiro completo.

Importação CSV -> categorização -> resumo -> contas -> impulso -> nudges.
Exercita o caminho real de ponta a ponta com SQLite real.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from src.adapters.importers.nubank_csv import NubankCSVImporter
from src.adapters.storage.sqlite_adapter import SQLiteAdapter
from src.domain.entities.transaction import TransactionCategory
from src.domain.services.financial_engine import FinancialEngine
from src.domain.services.goal_tracker import GoalTracker
from src.domain.services.impulse_filter import FrictionLevel, ImpulseFilter
from src.domain.services.nudge_engine import NudgeEngine, NudgeType
from src.events.bus import EventBus
from src.events.events import TransactionCreated


class TestFluxoFinanceiro:
    """Fluxo completo: importar extrato -> analisar -> nudges."""

    def test_importar_csv_nubank_e_gerar_resumo(self, storage: SQLiteAdapter, sample_csv):
        """CSV do Nubank é importado, categorizado e resumido corretamente."""
        importer = NubankCSVImporter()
        engine = FinancialEngine(storage)

        assert importer.detect(sample_csv)

        transactions = importer.parse(sample_csv)
        assert len(transactions) == 6

        for tx in transactions:
            engine.add_transaction(
                date_val=tx.date,
                description=tx.description,
                amount=tx.amount,
                transaction_type=tx.type,
                category=tx.category,
                bank=tx.bank,
            )

        summary = engine.get_financial_summary(
            start_date=date(2026, 3, 1),
            end_date=date(2026, 3, 31),
        )

        assert summary["receitas"] == 18000.00
        assert summary["despesas"] == pytest.approx(520.40, abs=0.01)
        assert summary["saldo"] == pytest.approx(17479.60, abs=0.01)
        assert summary["total_transacoes"] == 6

    def test_categorizacao_automatica(self, storage: SQLiteAdapter, sample_csv):
        """Transações são categorizadas por palavras-chave."""
        importer = NubankCSVImporter()
        transactions = importer.parse(sample_csv)

        categories = {tx.description: tx.category for tx in transactions}

        assert categories["IFOOD *RESTAURANTE TESTE"] == TransactionCategory.ALIMENTACAO
        assert categories["AMAZON.COM.BR"] == TransactionCategory.TECNOLOGIA
        assert categories["ACADEMIA SMARTFIT"] == TransactionCategory.SAUDE
        assert categories["PADARIA BOM PÃO"] == TransactionCategory.ALIMENTACAO
        assert categories["SALARIO EMPRESA LTDA"] == TransactionCategory.SALARIO

    def test_contas_a_pagar_com_vencimento(self, storage: SQLiteAdapter):
        """Contas são registradas, monitoradas e marcadas como pagas."""
        engine = FinancialEngine(storage)

        ontem = date.today() - timedelta(days=1)
        amanha = date.today() + timedelta(days=1)
        semana = date.today() + timedelta(days=5)

        engine.add_bill("Internet", 120.00, ontem)
        engine.add_bill("Energia", 180.00, amanha)
        engine.add_bill("Aluguel", 2500.00, semana)

        atrasadas = engine.get_overdue_bills()
        assert len(atrasadas) == 1
        assert atrasadas[0].name == "Internet"

        proximas = engine.get_upcoming_bills(days=7)
        assert len(proximas) == 2

        assert engine.pay_bill(atrasadas[0].id)
        assert len(engine.get_overdue_bills()) == 0

    def test_filtro_anti_impulso(self, storage: SQLiteAdapter):
        """Motor anti-impulso classifica compras por nível de fricção."""
        engine = FinancialEngine(storage)
        impulse = ImpulseFilter(storage, monthly_budget=5000, impulse_threshold=50)

        tx_essencial = engine.add_transaction(
            date.today(),
            "Supermercado Extra",
            -120.00,
            category=TransactionCategory.ALIMENTACAO,
        )
        result = impulse.analyze(tx_essencial)
        assert result.friction_level == FrictionLevel.NONE
        assert not result.is_impulse

        tx_risco = engine.add_transaction(
            date.today(),
            "Steam compra jogo",
            -89.00,
            category=TransactionCategory.LAZER,
        )
        result = impulse.analyze(tx_risco)
        assert result.friction_level in (FrictionLevel.MEDIUM, FrictionLevel.HARD)
        assert result.is_impulse
        assert result.delay_hours >= 24

    def test_nudges_contas_atrasadas(self, storage: SQLiteAdapter):
        """Nudge engine detecta contas atrasadas e gera alertas."""
        engine = FinancialEngine(storage)
        nudge = NudgeEngine(storage)

        ontem = date.today() - timedelta(days=3)
        engine.add_bill("Cartão Nubank", 450.00, ontem)

        nudges = nudge.check_all()
        bill_nudges = [n for n in nudges if n["tipo"] == NudgeType.BILL_REMINDER]

        assert len(bill_nudges) >= 1
        assert bill_nudges[0]["prioridade"] == "urgente"
        assert "Cartão Nubank" in bill_nudges[0]["título"]

    def test_event_bus_emite_transacao(self, event_bus: EventBus):
        """Event bus publica e recebe eventos tipados."""
        received = []

        def on_transaction(event: TransactionCreated):
            received.append(event)

        event_bus.on("TransactionCreated", on_transaction)

        event = TransactionCreated(
            transaction_id=1,
            amount=-89.00,
            category="lazer",
            is_impulse=True,
        )
        event_bus.emit(event, source="financial_engine")

        assert len(received) == 1
        assert received[0].amount == -89.00
        assert received[0].is_impulse


class TestIndicadoresMacro:
    """Testes para indicadores macroeconômicos (podem falhar offline)."""

    def test_projecao_economia(self):
        """Projeção de economia funciona com taxa manual."""
        from src.domain.services.macro_indicators import MacroIndicators

        indicators = MacroIndicators()
        result = indicators.project_savings(
            monthly_deposit=4000,
            months=24,
            annual_rate=12.25,
        )

        assert result["total_projetado"] > 96000
        assert result["rendimento"] > 0
        assert result["total_depositado"] == 96000
        assert result["meses"] == 24


class TestGoalTracker:
    """Testes para tracking de metas."""

    def test_criar_e_atualizar_meta(self, storage: SQLiteAdapter):
        """Meta é criada, atualizada e detecta conclusão."""
        tracker = GoalTracker(storage=storage)

        goal = tracker.create_goal(
            name="Apartamento",
            target_value=100000,
            unit="R$",
            goal_type="financeira",
            deadline=date(2028, 12, 31),
        )
        assert goal.id is not None
        assert goal.progress_percent == 0.0

        updated = tracker.update_progress(goal.id, 50000)
        assert updated.progress_percent == 50.0
        assert updated.remaining == 50000

        updated = tracker.increment_progress(goal.id, 50000)
        assert updated.is_completed
        assert updated.status.value == "concluída"

    def test_resumo_de_metas(self, storage: SQLiteAdapter):
        """Resumo lista todas as metas ativas com projeções."""
        tracker = GoalTracker(storage=storage)

        tracker.create_goal("Inglês fluente", 100, "%", "educação")
        tracker.create_goal("Viagem Europa", 30000, "R$", "financeira")

        summaries = tracker.get_goal_summary()
        assert len(summaries) == 2
        assert all("nome" in s for s in summaries)


class TestStorageSQLite:
    """Testes para o adaptador SQLite."""

    def test_crud_basico(self, storage: SQLiteAdapter):
        """Insert, query, update, delete funcionam corretamente."""
        row_id = storage.insert(
            "transactions",
            {
                "date": "2026-03-22",
                "description": "Teste CRUD",
                "amount": -50.0,
                "type": "despesa",
            },
        )
        assert row_id > 0

        row = storage.get_by_id("transactions", row_id)
        assert row["description"] == "Teste CRUD"

        storage.update("transactions", row_id, {"description": "Teste atualizado"})
        row = storage.get_by_id("transactions", row_id)
        assert row["description"] == "Teste atualizado"

        storage.delete("transactions", row_id)
        assert storage.get_by_id("transactions", row_id) is None

    def test_query_com_filtros(self, storage: SQLiteAdapter):
        """Query com filtros retorna resultados corretos."""
        storage.insert(
            "transactions",
            {
                "date": "2026-03-22",
                "description": "Receita",
                "amount": 1000.0,
                "type": "receita",
            },
        )
        storage.insert(
            "transactions",
            {
                "date": "2026-03-22",
                "description": "Despesa",
                "amount": -500.0,
                "type": "despesa",
            },
        )

        receitas = storage.query("transactions", filters={"type": "receita"})
        assert len(receitas) == 1
        assert receitas[0]["description"] == "Receita"

        total = storage.count("transactions")
        assert total == 2
