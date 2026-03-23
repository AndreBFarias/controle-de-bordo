# Sprint S08: App Mobile Flet

## Resumo Executivo
> Dashboard Flet empacotado como APK para Android, com visualização de metas, finanças e hábitos sincronizados via Syncthing.

## Status: PLANEJADO

## Metas e KPIs

| KPI | Alvo | Atual | Status |
|-----|------|-------|--------|
| APK gerado | 1 | 0 | Pendente |
| Páginas mobile | 3+ | 0 | Pendente |
| Sync via Syncthing | Funcional | Não | Pendente |
| Tamanho do APK | < 50MB | - | Pendente |

## Escopo

### Entregáveis
- [ ] Adaptação do dashboard Flet para layout mobile
- [ ] Navegação por gestos e bottom navigation
- [ ] Registro rápido de transações e hábitos
- [ ] Configuração de Syncthing para SQLite
- [ ] Build APK via `flet build apk`

### Fora do Escopo
- Publicação na Play Store
- Integração direta com Shizuku (via Tasker)

## Dependências
- Sprint S04 (Dashboard Flet)
- Sprint S07 (Ponte Mobile - para sync)

## Estimativa
- Complexidade: Alta
- Duração estimada: 3-4 dias

## Critérios de Aceite
1. APK instala e abre no Android 10+
2. Dashboard mostra dados reais do SQLite
3. Syncthing sincroniza DB entre desktop e mobile
4. App funciona offline (local-first)

*"Mobilidade é liberdade." - Voltaire*
