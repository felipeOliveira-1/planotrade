from models.account import TradePlan
from services.trade_service import TradeService
from services.account_service import AccountService
from views.reports import show_final_report

def adjust_leverage(trade_plan: TradePlan):
    while True:
        try:
            leverage = int(input(f"\nDigite a alavancagem desejada (1-10, atual: {trade_plan.leverage}x): "))
            if 1 <= leverage <= 10:
                trade_plan.leverage = leverage
                print(f"Alavancagem ajustada para {leverage}x")
                return
            else:
                print("A alavancagem deve estar entre 1x e 10x")
        except ValueError:
            print("Digite um número válido")

def adjust_position_size(trade_plan: TradePlan):
    while True:
        try:
            size = float(input(f"\nDigite o tamanho da posição em % (1-100, atual: {trade_plan.position_size_percent}%): "))
            if 1 <= size <= 100:
                trade_plan.position_size_percent = size
                print(f"Tamanho da posição ajustado para {size}%")
                return
            else:
                print("O tamanho da posição deve estar entre 1% e 100%")
        except ValueError:
            print("Digite um número válido")

def main_menu(trade_plan: TradePlan):
    trade_service = TradeService(trade_plan)
    account_service = AccountService(trade_plan)
    
    while True:
        print("\n--- Menu Principal ---")
        print("\n--- Menu Principal ---")
        print(f"Alavancagem atual: {trade_plan.leverage}x")
        print(f"Tamanho da posição: {trade_plan.position_size_percent}%")
        print("1 - Nova operação")
        print("2 - Ajustar alavancagem")
        print("3 - Ajustar tamanho da posição")
        print("4 - Acessar operações em aberto")
        print("5 - Realizar aporte")
        print("6 - Realizar saque")
        print("7 - Ver extrato")
        print("8 - Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            try:
                trade_service.create_trade()
            except ValueError as e:
                print(f"Erro: {str(e)}")
        elif choice == '2':
            adjust_leverage(trade_plan)
        elif choice == '3':
            adjust_position_size(trade_plan)
        elif choice == '4':
            trade_service.manage_open_trades()
        elif choice == '5':
            try:
                amount = float(input("Digite o valor do aporte: "))
                account_service.deposit(amount)
            except ValueError:
                print("Digite um valor numérico válido")
        elif choice == '6':
            try:
                amount = float(input("Digite o valor do saque: "))
                account_service.withdraw(amount)
            except ValueError:
                print("Digite um valor numérico válido")
        elif choice == '7':
            account_service.show_statement()
        elif choice == '8':
            show_final_report(trade_plan)
            print("\nAté logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")