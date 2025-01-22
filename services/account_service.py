from models.account import TradePlan
from models.trade import AccountOperation, AccountOperationType
from utils.file_utils import save_trades
from datetime import datetime

class AccountService:
    def __init__(self, trade_plan: TradePlan):
        self.trade_plan = trade_plan

    def deposit(self, amount: float):
        if amount <= 0:
            print("Erro: O valor do aporte deve ser positivo")
            return
        
        self.trade_plan.current_balance += amount
        operation = AccountOperation(
            type=AccountOperationType.DEPOSIT,
            amount=amount,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.trade_plan.account_operations.append(operation)
        save_trades(self.trade_plan)
        print(f"\nAporte de ${amount:.2f} realizado com sucesso!")
        print(f"Novo saldo: ${self.trade_plan.current_balance:.2f}")

    def withdraw(self, amount: float):
        if amount <= 0:
            print("Erro: O valor do saque deve ser positivo")
            return
        
        if amount > self.trade_plan.current_balance:
            print("Erro: Saldo insuficiente para o saque")
            return
            
        self.trade_plan.current_balance -= amount
        operation = AccountOperation(
            type=AccountOperationType.WITHDRAW,
            amount=amount,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        self.trade_plan.account_operations.append(operation)
        save_trades(self.trade_plan)
        print(f"\nSaque de ${amount:.2f} realizado com sucesso!")
        print(f"Novo saldo: ${self.trade_plan.current_balance:.2f}")

    def show_statement(self):
        print("\n--- Extrato da Conta ---")
        for operation in self.trade_plan.account_operations:
            if operation.type == AccountOperationType.DEPOSIT:
                print(f"[{operation.timestamp}] Aporte: +${operation.amount:.2f}")
            else:
                print(f"[{operation.timestamp}] Saque: -${operation.amount:.2f}")
        print("-----------------------")
        print(f"Saldo atual: ${self.trade_plan.current_balance:.2f}")
        print("-----------------------\n")