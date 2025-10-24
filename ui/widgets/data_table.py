from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QApplication, QInputDialog
)
from PySide6.QtCore import Qt
import csv
from io import StringIO

class DataTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._create_ui()

    def _create_ui(self):
        self.layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.add_row_btn = QPushButton("Добавить строку")
        self.add_col_btn = QPushButton("Добавить столбец")
        self.remove_row_btn = QPushButton("Удалить строку")
        self.remove_col_btn = QPushButton("Удалить столбец")
        self.clear_btn = QPushButton("Очистить")
        self.paste_btn = QPushButton("Вставить CSV")
        btn_layout.addWidget(self.add_row_btn)
        btn_layout.addWidget(self.add_col_btn)
        btn_layout.addWidget(self.remove_row_btn)
        btn_layout.addWidget(self.remove_col_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.paste_btn)
        self.layout.addLayout(btn_layout)

        self.table = QTableWidget(3, 3)
        self._init_headers()
        self.table.setEditTriggers(
            QTableWidget.DoubleClicked |
            QTableWidget.SelectedClicked |
            QTableWidget.EditKeyPressed
        )
        self.layout.addWidget(self.table)

        self.add_row_btn.clicked.connect(self.add_row)
        self.add_col_btn.clicked.connect(self.add_column)
        self.remove_row_btn.clicked.connect(self.remove_row)
        self.remove_col_btn.clicked.connect(self.remove_column)
        self.clear_btn.clicked.connect(self.clear_table)
        self.paste_btn.clicked.connect(self.paste_from_clipboard)

        self.table.horizontalHeader().sectionDoubleClicked.connect(self.edit_column_name)
        self.table.verticalHeader().sectionDoubleClicked.connect(self.edit_row_name)

    def _init_headers(self):
        self.table.setHorizontalHeaderLabels([f"Серия {i+1}" for i in range(self.table.columnCount())])
        self.table.setVerticalHeaderLabels([f"Категория {i+1}" for i in range(self.table.rowCount())])

    def edit_column_name(self, index):
        item = self.table.horizontalHeaderItem(index)
        if not item:
            item = QTableWidgetItem(f"Серия {index+1}")
            self.table.setHorizontalHeaderItem(index, item)
        old = item.text()
        text, ok = QInputDialog.getText(self, "Редактировать название серии", "Новое название:", text=old)
        if ok and text.strip():
            item.setText(text.strip())

    def edit_row_name(self, index):
        item = self.table.verticalHeaderItem(index)
        if not item:
            item = QTableWidgetItem(f"Категория {index+1}")
            self.table.setVerticalHeaderItem(index, item)
        old = item.text()
        text, ok = QInputDialog.getText(self, "Редактировать название категории", "Новое название:", text=old)
        if ok and text.strip():
            item.setText(text.strip())

    def add_row(self):
        current_row = self.table.currentRow()
        if current_row == -1:
            current_row = self.table.rowCount() - 1
        self.table.insertRow(current_row + 1)
        self.table.setVerticalHeaderItem(current_row + 1, QTableWidgetItem(f"Категория {current_row+2}"))

    def add_column(self):
        current_col = self.table.currentColumn()
        if current_col == -1:
            current_col = self.table.columnCount() - 1
        self.table.insertColumn(current_col + 1)
        self.table.setHorizontalHeaderItem(current_col + 1, QTableWidgetItem(f"Серия {current_col+2}"))

    def remove_row(self):
        row = self.table.currentRow()
        if row != -1 and self.table.rowCount() > 1:
            self.table.removeRow(row)

    def remove_column(self):
        col = self.table.currentColumn()
        if col != -1 and self.table.columnCount() > 1:
            self.table.removeColumn(col)

    def clear_table(self):
        self.table.clearContents()
        self.table.setRowCount(3)
        self.table.setColumnCount(3)
        self._init_headers()

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.paste_csv(text)

    def paste_csv(self, data_string):
        if not data_string.strip():
            return

        delimiter = ','
        if ';' in data_string:
            delimiter = ';'
        elif '\t' in data_string:
            delimiter = '\t'

        f = StringIO(data_string)
        reader = list(csv.reader(f, delimiter=delimiter))
        if not reader:
            return

        headers = reader[0][1:] if len(reader[0]) > 1 else [f"Серия {i+1}" for i in range(len(reader[0]))]
        categories = [r[0] if len(r) > 0 else f"Категория {i+1}" for r in reader[1:]]
        data_rows = [r[1:] for r in reader[1:]]

        n_cols = len(headers)
        n_rows = len(data_rows)

        self.table.setColumnCount(n_cols)
        self.table.setRowCount(n_rows)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels(categories)

        for r_idx, row in enumerate(data_rows):
            for c_idx, val in enumerate(row):
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                self.table.setItem(r_idx, c_idx, item)

    def get_table_data(self):
        data = []
        col_count = self.table.columnCount()
        row_count = self.table.rowCount()
        headers = [self.table.horizontalHeaderItem(c).text() for c in range(col_count)]
        for c in range(col_count):
            series = {"name": headers[c], "y": []}
            for r in range(row_count):
                item = self.table.item(r, c)
                try:
                    val = float(item.text()) if item else 0.0
                except:
                    val = 0.0
                series["y"].append(val)
            data.append(series)
        return data

    def get_row_labels(self):
        return [self.table.verticalHeaderItem(r).text() for r in range(self.table.rowCount())]
