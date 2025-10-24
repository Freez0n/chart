from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QCheckBox,
    QSpinBox, QComboBox, QDoubleSpinBox
)

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.chart_type = "line"
        self._create_ui()

    def _create_ui(self):
        self.layout = QVBoxLayout(self)
        self.form = QFormLayout()
        self.layout.addLayout(self.form)

        self.title_edit = QLineEdit("Заголовок графика")
        self.xlabel_edit = QLineEdit("Ось X")
        self.ylabel_edit = QLineEdit("Ось Y")
        self.legend_cb = QCheckBox()
        self.legend_cb.setChecked(True)
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(6, 32)
        self.fontsize_spin.setValue(10)

        self.form.addRow(QLabel("<b>Общие настройки</b>"))
        self.form.addRow("Заголовок:", self.title_edit)
        self.form.addRow("Подпись X:", self.xlabel_edit)
        self.form.addRow("Подпись Y:", self.ylabel_edit)
        self.form.addRow("Показывать легенду:", self.legend_cb)
        self.form.addRow("Размер шрифта:", self.fontsize_spin)
        self.form.addRow(QLabel("<b>Параметры типа графика</b>"))

        self.line_style_cb = QComboBox(); self.line_style_cb.addItems(["Сплошная", "Пунктирная", "Точечная"])
        self.line_width_spin = QDoubleSpinBox(); self.line_width_spin.setRange(0.5,5.0); self.line_width_spin.setValue(1.5)
        self.marker_cb = QComboBox(); self.marker_cb.addItems(["нет","o","s","^","*"])
        self.bar_width_spin = QDoubleSpinBox(); self.bar_width_spin.setRange(0.1,1.0); self.bar_width_spin.setSingleStep(0.1); self.bar_width_spin.setValue(0.8)
        self.pie_autopct_cb = QCheckBox("Показывать проценты"); self.pie_autopct_cb.setChecked(True)

        self.form.addRow("Стиль линии:", self.line_style_cb)
        self.form.addRow("Ширина линии:", self.line_width_spin)
        self.form.addRow("Маркер:", self.marker_cb)
        self.form.addRow("Ширина столбца:", self.bar_width_spin)
        self.form.addRow(self.pie_autopct_cb)

        self.type_widgets = {
            "line": [self.line_style_cb, self.line_width_spin, self.marker_cb],
            "bar": [self.bar_width_spin],
            "scatter": [self.marker_cb, self.line_width_spin],
            "pie": [self.pie_autopct_cb],
        }

        self.set_chart_type("line")

    def set_chart_type(self, t):
        self.chart_type = t
        for widgets in self.type_widgets.values():
            for w in widgets:
                w.setVisible(False)
        for w in self.type_widgets.get(t, []):
            w.setVisible(True)

    def get_config_dict(self):
        return {
            "title": self.title_edit.text(),
            "xlabel": self.xlabel_edit.text(),
            "ylabel": self.ylabel_edit.text(),
            "legend": self.legend_cb.isChecked(),
            "fontsize": self.fontsize_spin.value(),
            "line_style": self.line_style_cb.currentText(),
            "line_width": self.line_width_spin.value(),
            "marker": self.marker_cb.currentText(),
            "bar_width": self.bar_width_spin.value(),
            "pie_autopct": self.pie_autopct_cb.isChecked()
        }
