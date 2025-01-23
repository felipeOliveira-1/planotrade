import tkinter as tk
from tkinter import ttk, messagebox
from services.trade_service import TradeService
from models.account import TradePlan
from repositories.file_repository import FileRepository, FileUnitOfWork

class TradeApp:
    def __init__(self, root, trade_plan):
        self.root = root
        repository = FileRepository('trades.json')
        unit_of_work = FileUnitOfWork(repository)
        self.trade_service = TradeService(trade_plan, repository, unit_of_work)
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Plano de Trade")
        self.root.geometry("800x600")
        
        # Criação do notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        # Aba de Nova Operação
        self.new_trade_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.new_trade_frame, text="Nova Operação")
        self.setup_new_trade_tab()
        
        # Aba de Operações Abertas
        self.open_trades_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.open_trades_frame, text="Operações Abertas")
        self.setup_open_trades_tab()
        
        # Aba de Configurações
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Configurações")
        self.setup_settings_tab()
        
    def setup_new_trade_tab(self):
        # Tipo de Operação
        ttk.Label(self.new_trade_frame, text="Tipo de Operação:").grid(row=0, column=0, padx=5, pady=5)
        self.trade_type = tk.StringVar(value="long")
        ttk.Radiobutton(self.new_trade_frame, text="Long", variable=self.trade_type, value="long").grid(row=0, column=1)
        ttk.Radiobutton(self.new_trade_frame, text="Short", variable=self.trade_type, value="short").grid(row=0, column=2)
        
        # Alavancagem
        ttk.Label(self.new_trade_frame, text="Alavancagem:").grid(row=1, column=0, padx=5, pady=5)
        self.leverage = ttk.Combobox(self.new_trade_frame, values=[str(i) for i in range(1, 11)])
        self.leverage.grid(row=1, column=1)
        self.leverage.current(1)  # 2x como padrão
        
        # Tamanho da Posição
        ttk.Label(self.new_trade_frame, text="Tamanho da Posição (%):").grid(row=2, column=0, padx=5, pady=5)
        self.position_size = ttk.Entry(self.new_trade_frame)
        self.position_size.grid(row=2, column=1)
        
        # Preços
        ttk.Label(self.new_trade_frame, text="Preço de Entrada:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_price = ttk.Entry(self.new_trade_frame)
        self.entry_price.grid(row=3, column=1)
        
        ttk.Label(self.new_trade_frame, text="Preço Alvo:").grid(row=4, column=0, padx=5, pady=5)
        self.target_price = ttk.Entry(self.new_trade_frame)
        self.target_price.grid(row=4, column=1)
        
        ttk.Label(self.new_trade_frame, text="Preço Stop-Loss:").grid(row=5, column=0, padx=5, pady=5)
        self.stop_price = ttk.Entry(self.new_trade_frame)
        self.stop_price.grid(row=5, column=1)
        
        # Botão de Confirmação
        ttk.Button(self.new_trade_frame, text="Confirmar Operação", command=self.create_trade).grid(row=6, column=0, columnspan=2, pady=10)
        
    def setup_open_trades_tab(self):
        # Treeview para mostrar operações abertas
        columns = ("#", "Tipo", "Entrada", "Alvo", "Stop", "Ganho Potencial", "Perda Potencial", "Risco/Recompensa")
        self.trades_tree = ttk.Treeview(self.open_trades_frame, columns=columns, show="headings")
        
        for col in columns:
            self.trades_tree.heading(col, text=col)
            self.trades_tree.column(col, width=100)
            
        self.trades_tree.pack(fill='both', expand=True)
        
        # Botões de ação
        button_frame = ttk.Frame(self.open_trades_frame)
        button_frame.pack(fill='x', pady=5)
        
        ttk.Button(button_frame, text="Atualizar", command=self.update_open_trades).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Editar", command=self.edit_trade).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Fechar Operação", command=self.close_trade).pack(side='left', padx=5)
        
    def setup_settings_tab(self):
        # Configurações de conta
        ttk.Label(self.settings_frame, text="Saldo Inicial:").grid(row=0, column=0, padx=5, pady=5)
        self.initial_balance = ttk.Entry(self.settings_frame)
        self.initial_balance.grid(row=0, column=1)
        
        ttk.Label(self.settings_frame, text="Risco por Operação (%):").grid(row=1, column=0, padx=5, pady=5)
        self.risk_per_trade = ttk.Entry(self.settings_frame)
        self.risk_per_trade.grid(row=1, column=1)
        
        ttk.Label(self.settings_frame, text="Alavancagem Padrão:").grid(row=2, column=0, padx=5, pady=5)
        self.default_leverage = ttk.Combobox(self.settings_frame, values=[str(i) for i in range(1, 11)])
        self.default_leverage.grid(row=2, column=1)
        
        # Carrega valores atuais
        self.initial_balance.insert(0, str(self.trade_service.trade_plan.current_balance))
        self.risk_per_trade.insert(0, str(self.trade_service.trade_plan.risk_per_trade))
        self.default_leverage.insert(0, str(self.trade_service.trade_plan.leverage))
        
        ttk.Button(self.settings_frame, text="Salvar Configurações", command=self.save_settings).grid(row=3, column=0, columnspan=2, pady=10)
        
    def create_trade(self):
        try:
            # Coleta os dados do formulário
            trade_data = {
                'type': self.trade_type.get(),
                'leverage': int(self.leverage.get()),
                'position_size': float(self.position_size.get()),
                'entry': float(self.entry_price.get()),
                'target': float(self.target_price.get()),
                'stop': float(self.stop_price.get())
            }
            
            # Mostra detalhes da operação e pede confirmação
            confirm = messagebox.askyesno("Confirmar", "Deseja confirmar a operação?")
            if confirm:
                self.trade_service.create_trade(trade_data)
                messagebox.showinfo("Sucesso", "Operação criada com sucesso!")
            self.update_open_trades()
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Entrada inválida: {str(e)}")
            
    def update_open_trades(self):
        # Atualiza a lista de operações abertas
        self.trades_tree.delete(*self.trades_tree.get_children())
        open_trades = self.trade_service.get_open_trades()
        
        for i, trade in enumerate(open_trades, 1):
            self.trades_tree.insert("", "end", values=(
                i,
                trade.type.value.upper(),
                trade.entry,
                trade.target,
                trade.stop,
                f"${trade.gain:.2f}",
                f"${trade.loss:.2f}",
                f"{trade.risk_reward:.2f}:1"
            ))
            
    def close_trade(self):
        selected = self.trades_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma operação para fechar")
            return
            
        # Obtém o índice da operação selecionada
        item = self.trades_tree.item(selected[0])
        trade_index = int(item['values'][0]) - 1
        
        try:
            # Solicita o resultado da operação
            result = float(messagebox.askstring("Fechar Operação",
                "Digite o resultado da operação (positivo para lucro, negativo para prejuízo):"))
            
            # Fecha a operação no serviço
            self.trade_service.close_trade(trade_index, result)
            
            # Atualiza a lista de operações
            self.update_open_trades()
            messagebox.showinfo("Sucesso", "Operação fechada com sucesso!")
            
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido para o resultado")
        
    def edit_trade(self):
        selected = self.trades_tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma operação para editar")
            return
            
        # Obtém o índice da operação selecionada
        item = self.trades_tree.item(selected[0])
        trade_index = int(item['values'][0]) - 1
        
        # Cria janela de edição
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Editar Operação")
        
        # Campos editáveis
        ttk.Label(edit_window, text="Novo preço de entrada:").grid(row=0, column=0, padx=5, pady=5)
        entry_entry = ttk.Entry(edit_window)
        entry_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Novo preço alvo:").grid(row=1, column=0, padx=5, pady=5)
        target_entry = ttk.Entry(edit_window)
        target_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(edit_window, text="Novo preço stop:").grid(row=2, column=0, padx=5, pady=5)
        stop_entry = ttk.Entry(edit_window)
        stop_entry.grid(row=2, column=1, padx=5, pady=5)
        
        def save_changes():
            try:
                # Atualiza os campos que foram modificados
                if entry_entry.get():
                    self.trade_service.edit_trade(trade_index, 'entry', entry_entry.get())
                if target_entry.get():
                    self.trade_service.edit_trade(trade_index, 'target', target_entry.get())
                if stop_entry.get():
                    self.trade_service.edit_trade(trade_index, 'stop', stop_entry.get())
                    
                self.update_open_trades()
                edit_window.destroy()
                messagebox.showinfo("Sucesso", "Operação atualizada com sucesso!")
                
            except ValueError as e:
                messagebox.showerror("Erro", f"Erro ao editar operação: {str(e)}")
        
        ttk.Button(edit_window, text="Salvar", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def save_settings(self):
        try:
            # Atualiza saldo
            new_balance = float(self.initial_balance.get())
            self.trade_service.trade_plan.current_balance = new_balance
            
            # Atualiza risco por operação
            risk_per_trade = float(self.risk_per_trade.get())
            if not 0 < risk_per_trade <= 100:
                raise ValueError("Risco por operação deve estar entre 0% e 100%")
            self.trade_service.trade_plan.risk_per_trade = risk_per_trade
            
            # Atualiza alavancagem padrão
            leverage = int(self.default_leverage.get())
            if not 1 <= leverage <= 10:
                raise ValueError("Alavancagem deve estar entre 1x e 10x")
            self.trade_service.trade_plan.leverage = leverage
            
            self.trade_service.trade_repository.save_trade_plan(self.trade_service.trade_plan)
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {str(e)}")

def start_gui(trade_plan):
    root = tk.Tk()
    app = TradeApp(root, trade_plan)
    root.mainloop()