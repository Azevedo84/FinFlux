import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class FinanceDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💰 Dashboard Financeiro Familiar")
        self.setGeometry(100, 100, 1400, 850)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # 🔹 Linha de cards (saldo, entradas, despesas, etc.)
        resumo_layout = QHBoxLayout()
        self.cards = {}
        for titulo, cor in [
            ("Saldo Conta", "#4CAF50"),
            ("Entradas Mês", "#2196F3"),
            ("Despesas Mês", "#F44336"),
            ("Resultado", "#9C27B0"),
            ("Investimentos", "#FF9800"),
            ("Meta Poupança", "#3F51B5")
        ]:
            card = self.create_card(titulo, "R$ 0,00", cor)
            resumo_layout.addWidget(card)
            self.cards[titulo] = card.findChild(QLabel, "valor")

        main_layout.addLayout(resumo_layout)

        # 🔹 Tabela de cartões
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Cartão", "Vencimento", "Fatura", "Recebimento", "Saldo na Data", "Status"
        ])
        self.table.setStyleSheet("QTableWidget {font-size:14px; border-radius:8px;}")
        main_layout.addWidget(self.table)

        # 🔹 Linha de gráficos
        graficos_layout = QHBoxLayout()

        # Gráfico 1 - Top 10 categorias
        self.canvas1 = self.create_chart_canvas()
        graficos_layout.addWidget(self.canvas1)

        # Gráfico 2 - Orçamento categorias
        self.canvas2 = self.create_chart_canvas()
        graficos_layout.addWidget(self.canvas2)

        # Gráfico 3 - Investimentos
        self.canvas3 = self.create_chart_canvas()
        graficos_layout.addWidget(self.canvas3)

        main_layout.addLayout(graficos_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Carregar dados fake
        self.load_fake_data()

    def create_card(self, titulo, valor, cor):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {cor};
                border-radius: 20px;
                padding: 15px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        layout = QVBoxLayout()
        label_titulo = QLabel(titulo)
        label_titulo.setFont(QFont("Arial", 11, QFont.Bold))
        label_valor = QLabel(valor)
        label_valor.setObjectName("valor")
        label_valor.setFont(QFont("Arial", 16, QFont.Bold))
        label_valor.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)
        frame.setLayout(layout)
        return frame

    def create_chart_canvas(self):
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        canvas = FigureCanvas(fig)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas.updateGeometry()
        return canvas

    def load_fake_data(self):
        # Atualiza cards
        self.cards["Saldo Conta"].setText("R$ 5.200,00")
        self.cards["Entradas Mês"].setText("R$ 8.000,00")
        self.cards["Despesas Mês"].setText("R$ 6.300,00")
        self.cards["Resultado"].setText("R$ 1.700,00")
        self.cards["Investimentos"].setText("R$ 2.500,00")
        self.cards["Meta Poupança"].setText("75%")

        # Preenche tabela
        dados = [
            ("Nubank", "10/09", "R$ 1.200,00", "05/09", "R$ 5.000,00", "✅"),
            ("Inter", "23/09", "R$ 2.100,00", "21/09", "R$ 3.000,00", "❌")
        ]
        self.table.setRowCount(len(dados))
        for row, d in enumerate(dados):
            for col, value in enumerate(d):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

        # Atualiza gráficos
        self.update_charts()

    def update_charts(self):
        # Gráfico 1 - Top 10 categorias
        categorias = ["Mercado", "Aluguel", "Energia", "Água", "Lazer", "Transporte", "Internet", "Restaurante", "Educação", "Saúde"]
        valores = [random.randint(200, 1500) for _ in categorias]

        fig1 = self.canvas1.figure
        fig1.clear()
        ax1 = fig1.add_subplot(111)
        ax1.pie(valores, labels=categorias, autopct='%1.1f%%', startangle=90)
        ax1.set_title("Top 10 Despesas")
        self.canvas1.draw()

        # Gráfico 2 - Orçamento (5 piores/5 melhores)
        categorias = [f"Cat{i}" for i in range(1, 11)]
        orcamento = [1000 for _ in categorias]
        gasto = [random.randint(500, 1500) for _ in categorias]

        fig2 = self.canvas2.figure
        fig2.clear()
        ax2 = fig2.add_subplot(111)
        ax2.bar(categorias, gasto, label="Gasto")
        ax2.plot(categorias, orcamento, color="red", marker="o", label="Orçamento")
        ax2.legend()
        ax2.set_title("Comparativo Orçamento x Gasto")
        self.canvas2.draw()

        # Gráfico 3 - Investimentos
        meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"]
        valores = [random.randint(500, 3000) for _ in meses]

        fig3 = self.canvas3.figure
        fig3.clear()
        ax3 = fig3.add_subplot(111)
        ax3.plot(meses, valores, marker="o", color="green", linewidth=2)
        ax3.set_title("Evolução Investimentos")
        self.canvas3.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = FinanceDashboard()
    win.show()
    sys.exit(app.exec_())
