import sqlite3
import sys


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.f_show = []
        self.loadTable()

    def loadTable(self):
        self.f_show = self.cur.execute("""SELECT * FROM coffee_table""")
        self.tableWidget.setRowCount(0)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['Cорт',
                                                    'Обжарка', 'Молотый/зерна',
                                                    'Вкус', 'Цена',
                                                    'Объем'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.f_show):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(
                i, 2, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(
                i, 3, QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(
                i, 4, QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(
                i, 5, QTableWidgetItem(str(row[6])))
        self.tableWidget.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())