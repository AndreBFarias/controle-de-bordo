# Integração com Luna - Controle de Bordo

## Contexto

A Luna (v5.4.0) é uma assistente de IA multimodal com interface TUI, voz, visão e personalidade própria. O módulo `life_manager` da Luna já implementa funcionalidades básicas de finanças, saúde e metas.

O Controle de Bordo nasce como projeto separado para:
1. Desenvolver o motor de regras sem acoplamento à Luna
2. Oferecer UI visual (Flet) que a Luna TUI não comporta
3. Permitir uso standalone para quem não tem Luna instalada
4. Ser publicado como projeto open source independente

## Plano de Integração

### Fase 1: Motor compartilhável (atual)

A estrutura `src/domain/` é projetada como biblioteca importável:

```python
# Instalável via pip
pip install controle-de-bordo

# Importável como módulo
from controle_de_bordo.domain.services import FinancialEngine
from controle_de_bordo.domain.entities import Transaction
```

### Fase 2: Adapter Luna (futuro)

Um adapter `LunaModuleAdapter` traduz a interface `IModule` da Luna para os serviços do Controle de Bordo:

```python
# src/modules/controle_de_bordo/adapter.py (no repo Luna)
class ControleDeBordoModule:
    """Adapter que expõe o motor do Controle de Bordo como módulo Luna."""

    def on_load(self, ctx: ModuleContext) -> None:
        from controle_de_bordo.adapters.storage import SQLiteAdapter
        self.storage = SQLiteAdapter(ctx.data_dir / "bordo.db")
        self.storage.initialize()
        self.engine = FinancialEngine(self.storage)

    def on_enable(self, ctx: ModuleContext) -> None:
        ctx.event_bus.on("life:expense_recorded", self._on_expense)
```

### Fase 3: module.yaml (futuro)

```yaml
id: "controle_de_bordo"
name: "Controle de Bordo"
version: "1.0.0"
description: "Life OS integrado - finanças, hábitos, saúde, estudos"
luna_version: ">=5.5.0"

dependencies:
  - life_manager  # Herda dados existentes

pip_dependencies:
  - "controle-de-bordo>=0.1.0"
  - "finbr>=0.3.0"

provides:
  skills:
    - path: "skills/bordo_financial"
      class: "BordoFinancialSkill"
    - path: "skills/bordo_impulse"
      class: "BordoImpulseSkill"
    - path: "skills/bordo_macro"
      class: "BordoMacroSkill"

  commands:
    - name: "bordo"
      aliases: ["controle"]
      description: "Painel do Controle de Bordo"
      handler: "commands.cmd_bordo"
    - name: "selic"
      description: "Taxa Selic atual e projeções"
      handler: "commands.cmd_selic"

  events:
    listens:
      - "life:bill_due"
      - "life:expense_recorded"
    emits:
      - "bordo:impulse_detected"
      - "bordo:goal_milestone"
      - "bordo:nudge_triggered"
```

## Mapeamento de Funcionalidades

| Luna life_manager | Controle de Bordo | Ação na integração |
|-------------------|-------------------|-------------------|
| `FinancialSkill` | `FinancialEngine` | Substituir por motor mais robusto |
| `HealthSkill` | `HealthRecord` + serviços | Evoluir com Health Connect |
| `PlanningSkill` | `GoalTracker` + `Habit` | Substituir por tracker com KPIs |
| `LifeStorage` (JSON) | `SQLiteAdapter` (SQLite) | Migrar dados JSON para SQLite |
| `EventBus` simples | `EventBus` tipado | Compatível - apenas conectar |
| `LifeDashboardWidget` | Flet dashboard | Manter ambas interfaces |

## Migração de Dados

O `life_manager` usa JSON files em `~/.luna/modules/life_manager/data/`. A migração para SQLite será feita por um script dedicado:

```python
# Lê JSON existente da Luna
# Converte para entidades Pydantic
# Insere no SQLite do Controle de Bordo
```

## Coexistência

O `life_manager` original da Luna pode coexistir com o Controle de Bordo. Ambos acessam dados diferentes até a migração completa. Após a migração, o `life_manager` é desativado e o Controle de Bordo assume.

*"O todo é maior que a soma das partes." - Aristóteles*
