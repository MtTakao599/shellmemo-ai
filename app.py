import sys, os
from PySide6.QtWidgets import *
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt

from db import init_db, add_entry, get_entries, update_entry, delete_entry, update_order_bulk

os.environ["QT_IM_MODULE"] = "fcitx"
os.environ["XMODIFIERS"] = "@im=fcitx"

init_db()


class ShellMemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ShellMemo")
        self.resize(900, 600)

        layout = QVBoxLayout(self)

        # ===== 上ボタン =====
        top = QHBoxLayout()
        self.btn_input = QPushButton("追加　Ctrl+N")
        self.btn_manage = QPushButton("管理　Ctrl+M")
        top.addWidget(self.btn_input)
        top.addWidget(self.btn_manage)
        layout.addLayout(top)

        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        # =============================
        # 入力画面
        # =============================
        self.input_widget = QWidget()
        input_layout = QVBoxLayout(self.input_widget)

        self.cmd = QLineEdit()
        self.cmd.setPlaceholderText("コマンド")

        self.desc = QTextEdit()
        self.desc.setPlaceholderText("説明")

        self.tag = QLineEdit()
        self.tag.setPlaceholderText("タグ")

        self.save_btn = QPushButton("保存　Ctrl+Enter")

        input_layout.addWidget(self.cmd)
        input_layout.addWidget(self.desc)
        input_layout.addWidget(self.tag)
        input_layout.addWidget(self.save_btn)

        # =============================
        # 管理画面
        # =============================
        self.manage_widget = QWidget()
        manage_layout = QVBoxLayout(self.manage_widget)

        self.listbox = QListWidget()
        manage_layout.addWidget(self.listbox)

        # 🔥 ドラッグ並び替え
        self.listbox.setDragDropMode(QAbstractItemView.InternalMove)
        self.listbox.setDefaultDropAction(Qt.MoveAction)
        self.listbox.setSelectionMode(QAbstractItemView.SingleSelection)

        self.listbox.model().rowsMoved.connect(self.save_order)

        # 編集欄
        self.cmd_edit = QLineEdit()
        self.desc_edit = QTextEdit()
        self.tag_edit = QLineEdit()

        manage_layout.addWidget(QLabel("コマンド"))
        manage_layout.addWidget(self.cmd_edit)
        manage_layout.addWidget(QLabel("説明"))
        manage_layout.addWidget(self.desc_edit)
        manage_layout.addWidget(QLabel("タグ"))
        manage_layout.addWidget(self.tag_edit)

        # ボタン
        btns = QHBoxLayout()
        self.update_btn = QPushButton("更新")
        self.delete_btn = QPushButton("削除")

        btns.addWidget(self.update_btn)
        btns.addWidget(self.delete_btn)
        manage_layout.addLayout(btns)

        self.stack.addWidget(self.input_widget)
        self.stack.addWidget(self.manage_widget)

        # ===== イベント =====
        self.btn_input.clicked.connect(self.show_input)
        self.btn_manage.clicked.connect(self.show_manage)

        self.save_btn.clicked.connect(self.add_data)
        self.update_btn.clicked.connect(self.update_data)
        self.delete_btn.clicked.connect(self.delete_data)

        self.listbox.currentRowChanged.connect(self.load_selected)

        # ===== ショートカット =====
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.show_input)
        QShortcut(QKeySequence("Ctrl+M"), self).activated.connect(self.show_manage)
        QShortcut(QKeySequence("Ctrl+Return"), self).activated.connect(self.add_data)

        self.refresh()

    # ===== 画面 =====
    def show_input(self):
        self.stack.setCurrentIndex(0)

    def show_manage(self):
        self.stack.setCurrentIndex(1)

    # ===== DB =====
    def refresh(self):
        self.entries = get_entries()
        self.listbox.clear()

        for e in self.entries:
            item = QListWidgetItem(f"{e[1]} [{e[3]}]")
            item.setData(Qt.UserRole, e[0])  # 🔥 ID保持
            self.listbox.addItem(item)

    def add_data(self):
        add_entry(
            self.cmd.text(),
            self.desc.toPlainText(),
            self.tag.text()
        )
        self.cmd.clear()
        self.desc.clear()
        self.tag.clear()
        self.refresh()

    def load_selected(self, row):
        if row < 0:
            return

        e = self.entries[row]
        self.cmd_edit.setText(e[1])
        self.desc_edit.setText(e[2])
        self.tag_edit.setText(e[3])

    def update_data(self):
        row = self.listbox.currentRow()
        if row < 0:
            return

        entry_id = self.listbox.item(row).data(Qt.UserRole)

        update_entry(
            entry_id,
            self.cmd_edit.text(),
            self.desc_edit.toPlainText(),
            self.tag_edit.text()
        )
        self.refresh()

    def delete_data(self):
        row = self.listbox.currentRow()
        if row < 0:
            return

        entry_id = self.listbox.item(row).data(Qt.UserRole)
        delete_entry(entry_id)
        self.refresh()

    # ===== 並び替え保存 =====
    def save_order(self, *args):
        id_list = []

        for i in range(self.listbox.count()):
            item = self.listbox.item(i)
            entry_id = item.data(Qt.UserRole)
            id_list.append(entry_id)

        update_order_bulk(id_list)
        self.refresh()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ShellMemo()
    w.show()
    sys.exit(app.exec())
