import json
from models.account import TradePlan
from models.trade import TradeResult, AccountOperation, TradeType, AccountOperationType

def load_trades(trade_plan: TradePlan):
    try:
        with open('trades.json', 'r') as file:
            try:
                data = json.load(file)
                trade_plan.current_balance = data['current_balance']
                trade_plan.completed_trades = data['completed_trades']
                trade_plan.max_drawdown = data['max_drawdown']
                trade_plan.max_balance = data['max_balance']
                trade_plan.leverage = data.get('leverage', 2)
                trade_plan.position_size_percent = data.get('position_size_percent', 10)
                trade_plan.trade_history = [
                    TradeResult(
                        type=TradeType(trade['type']),
                        entry=trade['entry'],
                        target=trade['target'],
                        stop=trade['stop'],
                        result=trade['result'],
                        balance_before=trade['balance_before'],
                        balance_after=trade['balance_after'],
                        timestamp=trade['timestamp'],
                        leverage=trade.get('leverage', 2),
                        position_size_percent=trade.get('position_size_percent', 10)
                    )
                    for trade in data['trade_history']
                ]
                trade_plan.account_operations = [
                    AccountOperation(
                        type=AccountOperationType(operation['type']),
                        amount=operation['amount'],
                        timestamp=operation['timestamp']
                    )
                    for operation in data.get('account_operations', [])
                ]
            except json.JSONDecodeError:
                # Arquivo está vazio ou corrompido, começar do zero
                trade_plan.current_balance = trade_plan.initial_balance
                trade_plan.completed_trades = 0
                trade_plan.max_drawdown = 0
                trade_plan.max_balance = trade_plan.initial_balance
                trade_plan.trade_history = []
                trade_plan.account_operations = []
    except FileNotFoundError:
        # Arquivo não existe, começar do zero
        trade_plan.current_balance = trade_plan.initial_balance
        trade_plan.completed_trades = 0
        trade_plan.max_drawdown = 0
        trade_plan.max_balance = trade_plan.initial_balance
        trade_plan.trade_history = []
        trade_plan.account_operations = []

def save_trades(trade_plan: TradePlan):
    data = {
        'current_balance': trade_plan.current_balance,
        'completed_trades': trade_plan.completed_trades,
        'max_drawdown': trade_plan.max_drawdown,
        'max_balance': trade_plan.max_balance,
        'leverage': trade_plan.leverage,
        'position_size_percent': trade_plan.position_size_percent,
        'trade_history': [
            {
                'type': trade.type.value,
                'entry': trade.entry,
                'target': trade.target,
                'stop': trade.stop,
                'result': trade.result,
                'balance_before': trade.balance_before,
                'balance_after': trade.balance_after,
                'timestamp': trade.timestamp,
                'leverage': trade.leverage,
                'position_size_percent': trade.position_size_percent
            }
            for trade in trade_plan.trade_history
        ],
        'account_operations': [
            {
                'type': operation.type.value,
                'amount': operation.amount,
                'timestamp': operation.timestamp
            }
            for operation in trade_plan.account_operations
        ]
    }
    with open('trades.json', 'w') as file:
        json.dump(data, file, indent=2)