O Planotrade é um sistema modular para gerenciamento de operações financeiras, com foco na gestão de trades utilizando cálculos automáticos de risco, recompensa e alavancagem. Ele foi projetado para oferecer uma interface interativa de linha de comando (CLI) que auxilia traders a documentar e monitorar suas operações em tempo real.

Este sistema gerencia todas as etapas do ciclo de vida de uma operação financeira, incluindo cálculo de posição, registro de resultados, controle de aportes e saques, além da geração de relatórios detalhados.

Estrutura do Sistema
O Planotrade segue uma abordagem orientada a objetos com os seguintes componentes principais:

Módulo TradePlan:

Responsável pelo gerenciamento da configuração geral do plano de trade, incluindo:
Saldo inicial.
Controle do risco permitido por operação.
Alavancagem.
Histórico de operações.
Gerenciamento de drawdown e saldo máximo.
Módulo TradeService:

Contém a lógica de criação, gerenciamento e encerramento de operações:
Cálculo do tamanho da posição: Com base no risco permitido e no preço de entrada/stop-loss.
Cálculo de risco/recompensa (R/R Ratio).
Registro de operações no histórico.
Atualização do saldo com base nos resultados.
Módulo TradeResult:

Representa uma operação individual:
Tipo de operação (long ou short).
Preço de entrada, alvo e stop-loss.
Resultados finais (lucro ou prejuízo).
Tamanho da posição e alavancagem utilizada.
Timestamp para rastreamento histórico.
Utilitários (file_utils):

Funções auxiliares para salvar e carregar dados em arquivos persistentes, garantindo que o histórico de operações seja mantido entre execuções.
Funcionalidades

1. Nova Operação
   Permite a criação de uma nova operação com os seguintes passos:

Entrada dos parâmetros:
Tipo de operação: long ou short.
Preço de entrada, alvo e stop-loss.
Cálculo automático:
Tamanho da posição, com base no risco permitido.
Relação risco/recompensa (R/R Ratio).
Registro da operação no plano de trade. 2. Gerenciamento de Operações em Aberto
Apresenta uma lista de operações não encerradas, com as seguintes informações:

Tamanho da posição calculado com base no risco e alavancagem.
Ganhos e perdas potenciais.
Relação risco/recompensa.
Data/hora de criação da operação.
Além disso, oferece as opções:

Editar os parâmetros da operação (preço de entrada, alvo, stop).
Fechar a operação com o resultado final (lucro ou prejuízo). 3. Aportes e Saques
Permite ajustar o saldo disponível para operações, registrando aportes ou retiradas na conta.

4. Extrato e Relatórios
   Gera um histórico completo das operações realizadas, incluindo:

Lucros e perdas acumulados.
Tamanho médio das posições.
Drawdown máximo.
Relação de risco/recompensa geral.
Problemas Conhecidos

1. Cálculo de Ganhos/Perdas Potenciais
   O cálculo de ganho e perda potencial para operações abertas não considera corretamente a alavancagem em todos os momentos, levando a valores inconsistentes.

2. Interface CLI Limitada
   A interface atual não suporta navegação mais avançada ou persistência em banco de dados, o que pode dificultar a escalabilidade do sistema.

3. Falta de Validação de Entradas
   Não há verificação robusta de entradas do usuário, o que pode levar a erros como divisão por zero ou valores inválidos nos cálculos.

4. Persistência Simples
   Os dados são armazenados apenas em arquivos locais, sem suporte a sistemas de banco de dados relacionais ou não-relacionais.

PLANOTRADE/
├── models/
│ ├── **pycache**/
│ ├── **init**.py
│ ├── account.py
│ ├── trade.py
├── services/
│ ├── **pycache**/
│ ├── **init**.py
│ ├── account_service.py
│ ├── calculator.py
│ ├── trade_service.py
├── tests/
│ ├── test_calculator.py
├── utils/
│ ├── **pycache**/
│ ├── **init**.py
│ ├── file_utils.py
│ ├── math_utils.py
├── views/
│ ├── **pycache**/
│ ├── **init**.py
│ ├── menu.py
│ ├── reports.py
├── LICENSE
├── main.py
├── Plano de Trade.md
├── README.md
├── trades.json
