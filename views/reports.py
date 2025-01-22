from models.account import TradePlan

def show_final_report(trade_plan: TradePlan):
    print("\n--- Relatório Final ---")
    print(f"Saldo inicial: ${trade_plan.initial_balance:.2f}")
    print(f"Saldo final: ${trade_plan.current_balance:.2f}")
    print(f"Total de operações realizadas: {trade_plan.completed_trades}")
    print(f"Drawdown máximo: {trade_plan.max_drawdown:.2f}%")
    print("-----------------------\n")