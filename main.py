import sqlite3
import sys


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QWidget


class WrongData(Exception):
    pass


class NoData(Exception):
    pass


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.f_show = list()
        self.loadTable()
        self.pushButton.clicked.connect(self.redact)
        self.pushButton_2.clicked.connect(self.add_coffee)

    def loadTable(self):
        self.f_show = self.cur.execute("""SELECT * FROM coffee_table""")
        self.tableWidget.setRowCount(0)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Cорт',
                                                    'Обжарка', 'Молотый/зерна',
                                                    'Вкус', 'Цена',
                                                    'Объем'])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.f_show):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            self.tableWidget.setItem(
                i, 0, QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(
                i, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget.setItem(
                i, 2, QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(
                i, 3, QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(
                i, 4, QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(
                i, 5, QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(
                i, 6, QTableWidgetItem(str(row[6])))
        self.tableWidget.resizeColumnsToContents()
        self.label_2.setText('')

    def redact(self):
        try:
            if self.lineEdit.text() == '' or any(not x.isdigit() for x in self.lineEdit.text()):
                raise WrongData
            else:
                k = self.cur.execute(f"""SELECT id from coffee_table
                            WHERE id = {self.lineEdit.text()}""").fetchone()
                if k is None:
                    raise NoData
                else:
                    f.get_type(False, int(k[0]))
                    f.show()
        except WrongData:
            self.label_2.setText('Неверные данные')
        except NoData:
            self.label_2.setText('Кофе с таким id не существует')

    def add_coffee(self):
        f.get_type(True)
        f.show()


class Form(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.db')
        self.cur = self.con.cursor()
        self.f = False
        self.id = 0
        self.pushButton.clicked.connect(self.complete)
        self.burn_box.addItems([str(x) for x in range(1, 11)])
        self.type_box.addItems(['Молотый', 'В зернах'])

    def update_fields(self):
        self.burn_box.clear()
        self.burn_box.addItems([str(x) for x in range(1, 11)])
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.label_3.setText('')

    def get_type(self, f, id1=''):
        self.update_fields()
        self.f = f
        if id1 != '':
            self.id = id1
        if not self.f:
            s = self.cur.execute(f""" SELECT * from coffee_table
                            WHERE id = {self.id}""").fetchone()
            self.lineEdit.setText(s[1])
            self.lineEdit_2.setText(s[4])
            self.lineEdit_3.setText(s[5][:len(s[5]) - 1])
            self.lineEdit_4.setText(s[6][:len(s[6]) - 1])

    def complete(self):
        try:
            if any(not x.isdigit() for x in (self.lineEdit_3.text() + self.lineEdit_4.text())):
                raise WrongData
            if any(x == '' for x in ([self.lineEdit.text(), self.lineEdit_2.text(),
                                      self.lineEdit_3.text(), self.lineEdit_4.text()])):
                raise WrongData
            a = self.lineEdit.text(), self.burn_box.currentText(),\
                self.type_box.currentText(), self.lineEdit_2.text(),\
                self.lineEdit_3.text() + 'р', self.lineEdit_4.text() + 'г'
            if self.f:
                self.cur.execute(f"""INSERT INTO
                coffee_table(sort_name, burn_power, type, taste, price, volume)
                VALUES('{a[0]}', '{a[1]}', '{a[2]}', '{a[3]}', '{a[4]}', '{a[5]}')""")
            else:
                self.cur.execute(f"""UPDATE coffee_table
                SET sort_name = '{a[0]}'
                WHERE id = {self.id}""")
                self.cur.execute(f"""UPDATE coffee_table
                                SET burn_power = '{a[1]}'
                                WHERE id = {self.id}""")
                self.cur.execute(f"""UPDATE coffee_table
                                SET type = '{a[2]}'
                                WHERE id = {self.id}""")
                self.cur.execute(f"""UPDATE coffee_table
                                SET taste = '{a[3]}'
                                WHERE id = {self.id}""")
                self.cur.execute(f"""UPDATE coffee_table
                                SET price = '{a[4]}'
                                WHERE id = {self.id}""")
                self.cur.execute(f"""UPDATE coffee_table
                                                SET volume = '{a[5]}'
                                                WHERE id = {self.id}""")
            self.con.commit()
            self.close()
            ex.loadTable()
        except WrongData:
            self.label_3.setText('Неверные данные')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    f = Form()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())