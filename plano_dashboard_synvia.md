# 📊 Plano de Dashboard - Controle de Qualidade Synvia

**Data:** 01/02/2026  
**Responsável:** Washington Gouvea  
**Status:** Em planejamento

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo
Desenvolver uma dashboard interativa para monitoramento de **estudos de bioequivalência/biodisponibilidade**, permitindo acompanhar em tempo real o status dos lotes, taxas de aprovação e completude das etapas analíticas.

### 1.2 Contexto dos Dados

| Item | Descrição |
|------|-----------|
| **Fonte** | `Z:\ELN-BQV\Dashboard\temp\resumo_powerbi.csv` |
| **Formato** | CSV (separador `;`) |
| **Volume** | ~156 registros, 26 colunas |
| **Atualização** | Periódica (última: 15/01/2026) |
| **Empresas** | 28 clientes farmacêuticos |
| **Estudos** | 133 estudos únicos |
| **Lotes totais** | 2.768 |

---

## 2. Infraestrutura e Acesso

### 2.1 Situação Atual

```
┌─────────────────┐      VPN FortiClient      ┌─────────────────┐
│   Notebook      │ ◄──────────────────────► │  Servidor Rede  │
│   (Washington)  │      (Conexão manual)     │  Z:\ELN-BQV\... │
└─────────────────┘                           └─────────────────┘
```

### 2.2 Restrições Identificadas

| Restrição | Impacto |
|-----------|---------|
| **VPN FortiClient Free** | Desconecta automaticamente após período |
| **Sem servidor dedicado** | Não há máquina 24/7 dentro da rede |
| **Arquivo em rede local** | Acesso apenas via VPN conectada |
| **Atualização manual** | Usuário precisa conectar VPN para atualizar dados |

### 2.3 Fluxo de Atualização Proposto

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Conectar   │ ──► │   Executar  │ ──► │  Arquivo    │ ──► │  Dashboard  │
│  VPN        │     │   Script    │     │  Copiado    │     │  Atualizada │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
    (manual)          (1 clique)         (local ou nuvem)     (automático)
```

**Opções de destino do arquivo:**
- Pasta local no notebook
- SharePoint/OneDrive corporativo (se disponível)
- Google Drive (alternativa)

---

## 3. Métricas e Indicadores

### 3.1 KPIs Principais (Cards)

| KPI | Fórmula | Descrição |
|-----|---------|-----------|
| **Total de Lotes** | `SUM(TOTAL_LOTES)` | Volume total de lotes em análise |
| **Taxa de Aprovação** | `SUM(APROVADOS) / SUM(TOTAL_LOTES) * 100` | % de lotes aprovados |
| **Taxa de Reprovação** | `SUM(REPROVADOS) / SUM(TOTAL_LOTES) * 100` | % de lotes reprovados |
| **Completude Média** | `AVG(%_COMPLETUDE)` | Média de preenchimento dos estudos |
| **Estudos Ativos** | `COUNT(DISTINCT ESTUDO)` | Quantidade de estudos em andamento |
| **Empresas Atendidas** | `COUNT(DISTINCT EMPRESA)` | Quantidade de clientes |

### 3.2 Métricas de Status dos Lotes

| Métrica | Campo | Descrição |
|---------|-------|-----------|
| **Aprovados** | `APROVADOS` / `%_APROVADOS` | Lotes que passaram no controle |
| **Reprovados** | `REPROVADOS` / `%_REPROVADOS` | Lotes que falharam |
| **Rep. em Reanálise** | `REPREAN` / `%_REPREAN` | Reprovados aguardando nova análise |
| **Reprovados (Final)** | `REP` / `%_REP` | Reprovação confirmada |
| **Em Reanálise** | `REAN` / `%_REAN` | Aguardando reanálise |

### 3.3 Métricas do Pipeline Analítico

Cada etapa possui contagem absoluta (`_X`) e percentual (`%_`):

| Etapa | Campos | Descrição |
|-------|--------|-----------|
| **1. Aliquotagem** | `ALIQUOTAGEM_X` / `%_ALIQUOTAGEM` | Divisão das amostras |
| **2. Dopagem** | `DOPAGEM_X` / `%_DOPAGEM` | Preparação das amostras |
| **3. Extração** | `EXTRACAO_X` / `%_EXTRACAO` | Extração do analito |
| **4. Injeção** | `INJECAO_X` / `%_INJECAO` | Injeção cromatográfica |
| **5. Brutos** | `BRUTOS_PREENCHIDOS` / `%_BRUTOS` | Dados brutos preenchidos |

### 3.4 Dimensões para Filtros e Agrupamentos

| Dimensão | Campo | Uso |
|----------|-------|-----|
| **Empresa** | `EMPRESA` | Filtrar por cliente |
| **Estudo** | `ESTUDO` | Filtrar por estudo específico |
| **Ano** | Extraído de `ESTUDO` (ex: `.24` = 2024) | Análise temporal |
| **Arquivo** | `ARQUIVO` | Identificar fonte/analito |
| **Última Atualização** | `ULTIMA_ATUALIZACAO` | Verificar frescor dos dados |

---

## 4. Visualizações Propostas

### 4.1 Layout da Dashboard

```
┌─────────────────────────────────────────────────────────────────────┐
│                    HEADER: Título + Última Atualização              │
├─────────────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │  LOTES  │  │ APROV.  │  │ REPROV. │  │ COMPLET │  │ ESTUDOS │   │
│  │  2.768  │  │  74,8%  │  │  9,9%   │  │  75,5%  │  │   133   │   │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │
├───────────────────────────────┬─────────────────────────────────────┤
│                               │                                     │
│   APROVAÇÃO POR EMPRESA       │      PIPELINE ANALÍTICO (FUNIL)     │
│   (Gráfico de Barras)         │      (Gráfico de Funil/Barras)      │
│                               │                                     │
├───────────────────────────────┼─────────────────────────────────────┤
│                               │                                     │
│   COMPLETUDE POR EMPRESA      │      STATUS DOS LOTES               │
│   (Gráfico de Barras)         │      (Gráfico de Pizza/Donut)       │
│                               │                                     │
├───────────────────────────────┴─────────────────────────────────────┤
│                                                                     │
│              TABELA DETALHADA - ESTUDOS CRÍTICOS                    │
│   (Estudos com baixa aprovação ou completude < 80%)                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Descrição das Visualizações

| # | Visualização | Tipo | Dados |
|---|--------------|------|-------|
| 1 | **KPIs** | Cards | Totalizadores principais |
| 2 | **Aprovação por Empresa** | Barras Horizontais | `%_APROVADOS` agrupado por `EMPRESA` |
| 3 | **Pipeline Analítico** | Funil ou Barras | Médias de `%_ALIQUOTAGEM` até `%_BRUTOS` |
| 4 | **Completude por Empresa** | Barras + Meta | `%_COMPLETUDE` com linha de meta (80%) |
| 5 | **Status dos Lotes** | Donut | Distribuição Aprovados/Reprovados/Reanálise |
| 6 | **Tabela Crítica** | Tabela | Estudos com `%_APROVADOS < 70%` ou `%_COMPLETUDE < 80%` |

### 4.3 Filtros Interativos

- **Empresa** (multi-seleção)
- **Ano do Estudo** (2022, 2023, 2024, 2025)
- **Faixa de Completude** (slider: 0% - 100%)
- **Apenas estudos críticos** (checkbox)

---

## 5. Opções de Tecnologia

### 5.1 Comparativo

| Critério | Power BI | Streamlit (Python) | React + Vercel |
|----------|----------|-------------------|----------------|
| **Tempo de desenvolvimento** | 2-4h | 3-5h | 8-16h |
| **Custo** | Pro: ~R$50/mês | Grátis | Grátis |
| **Curva de aprendizado** | Baixa | Média | Alta |
| **Visual** | ★★★★★ | ★★★★☆ | ★★★★★ |
| **Flexibilidade** | Média | Alta | Muito Alta |
| **Compartilhamento** | Licença Pro | Link local/nuvem | Link público |
| **Atualização automática** | Gateway | Script manual | Script manual |
| **Manutenção** | Baixa | Média | Alta |

### 5.2 Recomendação

**A definir** com base em:
- Disponibilidade de licença Power BI Pro
- Necessidade de compartilhamento externo
- Familiaridade da equipe com Python

---

## 6. Próximos Passos

| # | Ação | Responsável | Prazo |
|---|------|-------------|-------|
| 1 | Definir tecnologia (Power BI vs Streamlit) | Washington | - |
| 2 | Verificar disponibilidade de SharePoint/OneDrive | Washington | - |
| 3 | Desenvolver dashboard | Claude + Washington | - |
| 4 | Criar script de cópia de arquivo (se necessário) | Claude | - |
| 5 | Testar fluxo completo (VPN → Atualização) | Washington | - |
| 6 | Documentar processo para equipe | Washington | - |

---

## 7. Observações Técnicas

### 7.1 Estrutura do Arquivo CSV

```
Separador: ;
Encoding: UTF-8 (com BOM)
Campos numéricos: Ponto como decimal
Data: DD/MM/YYYY HH:MM
```

### 7.2 Tratamentos Necessários

- Extrair ano do código do estudo (ex: `001.001.24` → 2024)
- Extrair nome da empresa do código (ex: `001_EMS` → EMS)
- Tratar registros com `TOTAL_LOTES = 0` (estudos não iniciados)
- Converter `ULTIMA_ATUALIZACAO` para datetime

---

*Documento gerado em 01/02/2026*
