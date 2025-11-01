# 📘 Dicionário de Dados — Projeto Pretoleira Gamarra

Este documento descreve as colunas e unidades dos principais arquivos gerados.

---

## Arquivo: `producao_mensal.xlsx`
| Coluna | Descrição | Unidade |
|--------|------------|---------|
| data | Data de referência (mensal) | YYYY-MM-DD |
| campo | Nome do campo de petróleo | texto |
| producao_barris | Produção mensal de petróleo | barris |
| receita | Receita mensal do campo | BRL |
| custo_operacional | Custo operacional total do campo | BRL |
| custo_geral_brl | Custo geral alocado proporcionalmente | BRL |
| lucro_liquido_brl | Lucro líquido do campo | BRL |
| margem_liquida_pct | Margem líquida (lucro/receita) | % |

---

## Arquivo: `financials_consolidated.xlsx`
| Coluna | Descrição | Unidade |
|--------|------------|---------|
| data | Data de referência (mensal) | YYYY-MM-DD |
| producao_total_barris | Produção total consolidada | barris |
| receita_total_brl | Receita total consolidada | BRL |
| custo_operacional_total_brl | Custos operacionais totais | BRL |
| custo_geral_total_brl | Custos gerais totais | BRL |
| lucro_total_brl | Lucro líquido consolidado | BRL |

---

## Arquivo: `custos_gerais.xlsx`
| Coluna | Descrição | Unidade |
|--------|------------|---------|
| data | Data mensal | YYYY-MM-DD |
| admin_brl | Custo administrativo | BRL |
| manutencao_brl | Custo de manutenção | BRL |
| logistica_brl | Custo logístico | BRL |

---

## Observações
- Todas as séries são mensais de **2005-01** até **2025-12**.
- Moeda padrão: **Real (BRL)**.
- Datas sempre no formato ISO `YYYY-MM-DD`.
