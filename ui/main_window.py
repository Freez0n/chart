from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QSplitter, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ui.widgets.data_table import DataTableWidget
from ui.widgets.settings_panel import SettingsPanel
from plotting.plot_manager import PlotManager
from data.models import ChartConfig, DataSeries

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("диаграммы")
        self.resize(1100, 700)

        self._create_ui()
        self.plot_manager = PlotManager()

    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        hbox = QHBoxLayout(central)

        splitter = QSplitter(Qt.Horizontal)
        hbox.addWidget(splitter)

        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(8, 8, 8, 8)

        self.data_table = DataTableWidget()
        left_layout.addWidget(self.data_table, 3)

        row = QWidget()
        row_l = QHBoxLayout(row)
        row_l.setContentsMargins(0, 0, 0, 0)
        row_l.addWidget(QLabel("Тип:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems([
            "Линейный график",
            "Столбчатая диаграмма",
            "Точечная диаграмма",
            "Круговая диаграмма"
        ])
        row_l.addWidget(self.type_combo)
        self.build_btn = QPushButton("Построить / Обновить")
        row_l.addWidget(self.build_btn)
        left_layout.addWidget(row)

        self.settings = SettingsPanel()
        left_layout.addWidget(self.settings, 2)
        left_layout.addStretch()
        splitter.addWidget(left_frame)

        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(8, 8, 8, 8)

        self.fig = Figure(figsize=(6, 5))
        self.canvas = FigureCanvas(self.fig)
        right_layout.addWidget(self.canvas, 1)

        self.info_label = QLabel("Информация: пусто")
        right_layout.addWidget(self.info_label)
        splitter.addWidget(right_frame)
        splitter.setSizes([420, 660])

        self.build_btn.clicked.connect(self.on_build)
        self.type_combo.currentTextChanged.connect(self.on_type_change)
        self.on_type_change(self.type_combo.currentText())

    def on_type_change(self, t):
        mapping = {
            "Линейный график": "line",
            "Столбчатая диаграмма": "bar",
            "Точечная диаграмма": "scatter",
            "Круговая диаграмма": "pie"
        }
        chart_type = mapping.get(t, "line")
        self.settings.set_chart_type(chart_type)

    def _show_error(self, title, text):
        QMessageBox.critical(self, title, text)

    def on_build(self):
        raw_table = self.data_table.get_table_data()
        row_labels = self.data_table.get_row_labels()

        if not raw_table:
            self._show_error("Ошибка данных", "Нет данных для построения.")
            return

        chart_type = self.settings.chart_type
        config = ChartConfig.from_dict(self.settings.get_config_dict())
        config.chart_type = chart_type

        series_list = []
        if chart_type == "pie":
            if len(raw_table) == 0 or len(raw_table[0]['y']) == 0:
                self._show_error("Ошибка данных", "Нет данных для круговой диаграммы.")
                return
            y = [v for v in raw_table[0]['y']]
            series_list.append(DataSeries(name="", y=y, x=row_labels))
        else:
            for s in raw_table:
                series_list.append(DataSeries(name=s['name'], y=s['y'], x=list(range(len(s['y'])))))

        try:
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            self.plot_manager.render(ax, series_list, config)
            self.canvas.draw_idle()

            names = ", ".join(s.name for s in series_list if s.name)
            self.info_label.setText(
                f"Тип: {chart_type} | Серии: {names} | N={len(series_list[0].y) if series_list else 0}"
            )
        except Exception as e:
            self._show_error("Ошибка построения", str(e))
