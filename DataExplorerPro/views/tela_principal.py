import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa as classes das outras camadas (Model e Controller)
from models.leitor_csv import LeitorCSV
from controllers.controlador import Controlador

class TelaPrincipal:
    """Classe responsável por criar e gerenciar a interface gráfica (Janela, Botões e Tabelas)."""
    
    def __init__(self):
        # Cria a janela principal da aplicação
        self.root = tk.Tk()
        self.root.title("Data Explorer Pro")
        self.root.geometry("980x700")
        self.root.minsize(900, 600)
        self.root.configure(bg="#0f172a")
        
        # Instancia o Model (Leitor) e o Controller (Regras)
        self.leitor = LeitorCSV()
        self.controlador = Controlador()
        self.df_atual = None  # Variável para armazenar o DataFrame carregado na memória
        
        # Chama o método que desenha os componentes na tela
        self._criar_componentes()
        self.carregar_arquivo_padrao()

    def carregar_arquivo_padrao(self):
        """Carrega automaticamente o CSV de vendas localizado na pasta dados."""
        caminho = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dados", "vendas.csv")
        self.df_atual = self.leitor.carregar(caminho)

        if self.df_atual is not None:
            self.atualizar_interface(self.df_atual)
        else:
            messagebox.showerror("Erro", "Não foi possível carregar o arquivo de vendas.")
        
    def _criar_componentes(self):
        """Método auxiliar interno para desenhar os widgets da tela."""

        # --- 1. CABEÇALHO E BOTÕES ---
        frame_topo = tk.Frame(self.root, bg="#111827", padx=18, pady=14)
        frame_topo.pack(fill=tk.X, padx=10, pady=(10, 0))

        titulo = tk.Label(frame_topo, text="Data Explorer Pro", bg="#111827", fg="#f8fafc", font=("Arial", 18, "bold"))
        titulo.pack(anchor="w")

        frame_acoes = tk.Frame(frame_topo, bg="#111827")
        frame_acoes.pack(fill=tk.X, pady=(10, 0))

        btn_carregar = tk.Button(frame_acoes, text="📂 Carregar CSV", command=self.carregar_csv_acao, bg="#16a34a", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=16, pady=8, cursor="hand2")
        btn_carregar.pack(side=tk.LEFT, padx=(0, 8))

        btn_grafico = tk.Button(frame_acoes, text="📊 Gerar Gráfico", command=self.gerar_grafico_acao, bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=16, pady=8, cursor="hand2")
        btn_grafico.pack(side=tk.LEFT)

        # --- 2. PAINEL DE INDICADORES (KPIs) ---
        self.frame_kpi = tk.Frame(self.root, bg="#0f172a", pady=10)
        self.frame_kpi.pack(fill=tk.X, padx=10)

        card_registros = tk.Frame(self.frame_kpi, bg="#111827", padx=18, pady=12, highlightthickness=1, highlightbackground="#374151")
        card_registros.pack(side=tk.LEFT, padx=(0, 12))
        self.lbl_registros = tk.Label(card_registros, text="Total Registros: 0", bg="#111827", fg="#e2e8f0", font=("Arial", 11, "bold"))
        self.lbl_registros.pack()

        card_total = tk.Frame(self.frame_kpi, bg="#111827", padx=18, pady=12, highlightthickness=1, highlightbackground="#374151")
        card_total.pack(side=tk.LEFT)
        self.lbl_total = tk.Label(card_total, text="Total Vendido: R$ 0,00", bg="#111827", fg="#e2e8f0", font=("Arial", 11, "bold"))
        self.lbl_total.pack()

        # --- 3. PAINEL DE FILTROS ---
        frame_filtro = tk.Frame(self.root, bg="#111827", padx=12, pady=10)
        frame_filtro.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(frame_filtro, text="Filtrar Produto:", bg="#111827", fg="#e2e8f0", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(5, 8))

        self.entry_filtro = tk.Entry(frame_filtro, font=("Arial", 10), width=25, bd=1, relief="solid", bg="#1f2937", fg="#f8fafc", insertbackground="#f8fafc")
        self.entry_filtro.pack(side=tk.LEFT, padx=(0, 8))

        btn_filtrar = tk.Button(frame_filtro, text="Filtrar", command=self.filtrar_acao, bg="#f59e0b", fg="white", font=("Arial", 10, "bold"), relief="flat", padx=16, pady=6, cursor="hand2")
        btn_filtrar.pack(side=tk.LEFT)

        # --- 4. TABELA DE DADOS (TREEVIEW) ---
        frame_tabela = tk.Frame(self.root, bg="#111827", padx=10, pady=10)
        frame_tabela.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        colunas = ("Produto", "Quantidade", "Valor")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#111827", foreground="#f8fafc", fieldbackground="#111827", rowheight=28)
        style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "#ffffff")])
        style.configure("Treeview.Heading", background="#1f2937", foreground="#f8fafc", relief="flat")

        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=22)
        self.tree.tag_configure("oddrow", background="#1f2937")
        self.tree.tag_configure("evenrow", background="#111827")

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def carregar_csv_acao(self):
        """Abre uma janela de diálogo para o usuário escolher o arquivo CSV e processá-lo."""
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos CSV", "*.csv")])
        if caminho:
            # Usa o Model para carregar os dados
            self.df_atual = self.leitor.carregar(caminho)
            if self.df_atual is not None:
                self.atualizar_interface(self.df_atual)
                messagebox.showinfo("Sucesso", "Arquivo CSV carregado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível ler o arquivo CSV.")

    def atualizar_interface(self, df):
        """Atualiza a tabela visual e os indicadores numéricos com base no DataFrame fornecido."""
        # Limpa todos os registros antigos exibidos na tabela
        for row in self.tree.get_children():
            self.tree.delete(row)

        for indice, linha in df.iterrows():
            tag = "evenrow" if indice % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=list(linha), tags=(tag,))

        # Pede para o Controller calcular os indicadores estatísticos
        qtd_registros = self.controlador.calcular_total_registros(df)
        total_vendas = self.controlador.calcular_soma_vendas(df)

        # Atualiza os textos dos rótulos (Labels) na tela
        self.lbl_registros.config(text=f"Total Registros: {qtd_registros}")
        self.lbl_total.config(text=f"Total Vendido: R$ {total_vendas:,.2f}")

    def filtrar_acao(self):
        """Captura o texto digitado no campo de filtro e atualiza a interface."""
        if self.df_atual is not None:
            termo = self.entry_filtro.get()
            # O Controller processa o filtro
            df_filtrado = self.controlador.filtrar_por_produto(self.df_atual, termo)
            self.atualizar_interface(df_filtrado)
        else:
            messagebox.showwarning("Aviso", "Por favor, carregue um arquivo CSV primeiro!")

    def gerar_grafico_acao(self):
        """Gera um gráfico visual de barras utilizando a biblioteca Matplotlib."""
        if self.df_atual is not None:
            # Agrupa os dados por produto somando as quantidades vendidas
            df_agrupado = self.df_atual.groupby('Produto')['Quantidade'].sum()
            
            # Cria uma nova janela pop-up (Toplevel) para exibir o gráfico
            janela_grafico = tk.Toplevel(self.root)
            janela_grafico.title("Gráfico de Vendas por Produto")
            janela_grafico.geometry("600x450")
            
            fig, ax = plt.subplots(figsize=(6, 4))
            df_agrupado.plot(kind='bar', ax=ax, color='#2196F3', edgecolor='black')
            ax.set_title("Quantidade Vendida por Produto")
            ax.set_xlabel("Produto")
            ax.set_ylabel("Quantidade Total")
            plt.xticks(rotation=0)
            
            # Integra a figura do Matplotlib dentro da janela gráfica do Tkinter
            canvas = FigureCanvasTkAgg(fig, master=janela_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            messagebox.showwarning("Aviso", "Carregue um arquivo CSV para gerar o gráfico!")

    def executar(self):
        """Inicia o loop de execução da interface gráfica."""
        self.root.mainloop()
