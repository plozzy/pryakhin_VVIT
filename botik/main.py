import psycopg2
import sys

from datetime import date

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                         QTableWidgetItem, QPushButton, QMessageBox)

from config import DATABASE, USER, PASSWORD


time = ['9:30', '11:20', '13:10', '15:25', '17:15', '19:00', '20:40', '22:10']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.week_type = 'чет' if get_week_num() % 2 == 0 else 'неч'

        self._connect_to_db()

        self.setWindowTitle("Schedule")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_teachers_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database=DATABASE,
                                        user=USER,
                                        password=PASSWORD,
                                        host="localhost",
                                        port="5432")

        self.cursor = self.conn.cursor()
        self.timetable_table_name = 'qtimetable'
        self.teachers_table_name = 'teachers'


        self.teachers_names, self.teachers_places = self._fetch_teachers()
        # self.teachers_names = []
        self.class_names = self._fetch_classes()

    def _fetch_teachers(self):
        select_teachers = f"SELECT id, name FROM {self.teachers_table_name}"
        self.cursor.execute(select_teachers)
        names = dict(self.cursor.fetchall())
        select_teachers = f"SELECT id, place FROM {self.teachers_table_name}"
        self.cursor.execute(select_teachers)
        places = dict(self.cursor.fetchall())
        return [names, places]

    def _fetch_classes(self):
        select_classes = f"SELECT * FROM {self.timetable_table_name}"
        self.cursor.execute(select_classes)
        return [class_name[1] for class_name in (self.cursor.fetchall())]

    def _create_teachers_table(self, gbox):
        table = QTableWidget()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["ID", "Name", "Place", "Update", "Delete"])

        table.setRowCount(len(self.teachers_names) + 1)
        for i in range(len(self.teachers_names)):
            joinButton = QPushButton("Update")
            joinButton.clicked.connect(lambda ch, tbl=table, id=(i + 1):self._change_teacher_from_table(tbl, id))
            deleteButton = QPushButton("Delete")
            deleteButton.clicked.connect(lambda ch, t_id=(i + 1):self._delete_teacher(t_id))
            table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            try:
                table.setItem(i, 1, QTableWidgetItem(str(self.teachers_names[i + 1])))
                table.setItem(i, 2, QTableWidgetItem(str(self.teachers_places[i + 1])))
            except KeyError:
                table.setItem(i, 1, QTableWidgetItem())
                table.setItem(i, 2, QTableWidgetItem())
            table.setCellWidget(i, 3, joinButton)
            table.setCellWidget(i, 4, deleteButton)

        joinButton = QPushButton("Update")
        joinButton.clicked.connect(lambda ch, tbl=table:self._insert_teacher(tbl.item(i + 1, 1).text(), tbl.item(i + 1, 2).text()))
        table.setItem(i + 1, 0, QTableWidgetItem(''))
        table.setItem(i + 1, 1, QTableWidgetItem(''))
        table.setItem(i + 1, 2, QTableWidgetItem(''))
        table.setCellWidget(i + 1, 3, joinButton)
        table.resizeRowsToContents()

        mvbox = QVBoxLayout()
        mvbox.addWidget(table)
        gbox.setLayout(mvbox)

    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teachers")

        gbox = QGroupBox('Teachers')

        svbox = QVBoxLayout()
        shboxes = [QHBoxLayout() for _ in range(2)]
        [svbox.addLayout(shbox) for shbox in shboxes]
        shboxes[0].addWidget(gbox)

        self._create_teachers_table(gbox)

        self.teachers_tab.setLayout(svbox)
        update_shedule_button = QPushButton("Update")
        shboxes[1].addWidget(update_shedule_button)
        update_shedule_button.clicked.connect(lambda : self._update_shedule())
        self.teachers_tab.setLayout(svbox)

    def _create_table(self, table, gbox, weekday):
        table = QTableWidget()
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["Subject", "Time", "Prepodavatel'", "Location", "Add", "Delete"])

        self._update_table(table, weekday)

        mvbox = QVBoxLayout()
        mvbox.addWidget(table)
        gbox.setLayout(mvbox)

    def _create_shedule_tab(self):
        self.shedule_tab = QWidget()
        self.tabs.addTab(self.shedule_tab, "Schedule")

        self.gboxes = [QGroupBox(day) for day in days]

        self.svbox = QVBoxLayout()
        self.shboxes = [QHBoxLayout() for _ in range(2)]
        [self.svbox.addLayout(shbox) for shbox in self.shboxes]
        [self.shboxes[0].addWidget(day_box) for day_box in self.gboxes]

        self.tables = [QTableWidget() for _ in range(6)]
        for i, table in enumerate(self.tables):
            self._create_table(table, self.gboxes[i], i)

        self.update_shedule_button = QPushButton("Update")
        self.shboxes[1].addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(lambda : self._update_shedule())
        self.shedule_tab.setLayout(self.svbox)

    def _update_table(self, table, weekday):
        global time
        what_we_need = f"WHERE weekday = {weekday} AND week = '{self.week_type}';"
        select_day = f"SELECT * FROM {self.timetable_table_name} {what_we_need}"
        self.cursor.execute(select_day)
        records = sorted(list(self.cursor.fetchall()), key=lambda elem: elem[4])

        table.setRowCount(len(records) + 1)
        empty = ['None', 'удалена', '', 'тут могла быть ваша пара']
        for i, r in enumerate(records):
            if str(r[1]) not in empty:
                joinButton = QPushButton("Join")
                deleteButton = QPushButton("Delete")
                joinButton.clicked.connect(lambda ch, wd=weekday, tbl=table, class_num=i:self._change_day_from_table(tbl, wd, class_num))
                deleteButton.clicked.connect(lambda ch, tbl=table, wd=weekday, num = r[4]:self._delete_class(wd, num))
                table.setItem(i, 0, QTableWidgetItem(str(r[1])))
                table.setItem(i, 1, QTableWidgetItem(str(time[i])))
                try:
                    table.setItem(i, 2, QTableWidgetItem(str(self.teachers_names[r[5]])))
                    table.setItem(i, 3, QTableWidgetItem(str(self.teachers_places[r[5]])))
                except KeyError:
                    table.setItem(i, 2, QTableWidgetItem(str(self.teachers_names[10])))
                    table.setItem(i, 3, QTableWidgetItem((self.teachers_places[10])))
                table.setCellWidget(i, 4, joinButton)
                table.setCellWidget(i, 5, deleteButton)
            else:
                table.setItem(i, 0, QTableWidgetItem(''))
                table.setItem(i, 1, QTableWidgetItem(str(time[i])))
                insert_button = QPushButton("Insert")
                insert_button.clicked.connect(lambda ch, tbl=table, wd=weekday, num=i:self._change_day_from_table(tbl, wd, num))
                table.setCellWidget(i, 4, insert_button)

        insert_button = QPushButton("Insert")
        insert_button.clicked.connect(lambda ch, tbl=table:self._insert_class(tbl.item(i + 1, 0).text(), weekday, i + 1, tbl.item(i + 1, 0).text()))
        table.setItem(i + 1, 0, QTableWidgetItem(''))
        table.setItem(i + 1, 1, QTableWidgetItem(str(time[i + 1])))
        table.setCellWidget(i + 1, 4, insert_button)
        table.resizeRowsToContents()

    def _change_day_from_table(self, table, weekday, class_num):
        try:
            text = table.item(class_num, 0).text()
            try:
                pr_id = int(table.item(class_num, 2).text())
                if pr_id > len(self.teachers_names):
                    return QMessageBox.about(self, "Error", "Такого id не существует")
            except:
               return QMessageBox.about(self, "Error", "Введите ID цифрами")
            update_day = f"UPDATE {self.timetable_table_name} SET class_name = %s, pr_id = %s WHERE weekday = %s AND class_num = %s AND week = '{self.week_type}'"
            self.cursor.execute(update_day, (text, pr_id, weekday, class_num))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "sql error")

    def _change_teacher_from_table(self, table, id):
        try:
            update_teacher = f"UPDATE {self.teachers_table_name} SET name = %s WHERE id = %s"
            self.cursor.execute(update_teacher, (str(table.item(id - 1, 1).text()), str(id), ))
            update_teacher = f"UPDATE {self.teachers_table_name} SET place = %s WHERE id = %s"
            self.cursor.execute(update_teacher, (str(table.item(id - 1, 2).text()), str(id), ))
            self.conn.commit()
        except:
            QMessageBox.about(self, "Error", "Enter all fields")

    def _insert_class(self, class_name, weekday, class_num, pr_id):
        try:
            insert_data = f"""
            INSERT INTO {self.timetable_table_name} (class_name, week, weekday, class_num, pr_id)
            VALUES (%s, %s, %s, %s, %s);
            """
            self.cursor.execute(insert_data, (class_name, self.week_type, str(weekday), str(class_num), str(pr_id), ))
            self.conn.commit()
            self._update_shedule()
        except:
            QMessageBox.about(self, "Error", "sql error")


    def _insert_teacher(self, name, place):
        insert_data = f"""
        INSERT INTO {self.teachers_table_name} (name, place)
        VALUES (%s, %s);
        """
        self.cursor.execute(insert_data, (name, place, ))
        self.conn.commit()
        self._update_shedule()

    def _delete_class(self, weekday, class_num):
        update_day = f"UPDATE {self.timetable_table_name} SET class_name = %s WHERE weekday = %s AND class_num = %s AND week = '{self.week_type}'"
        self.cursor.execute(update_day, ('', weekday, class_num))
        self.conn.commit()
        self._update_shedule()

    def _delete_teacher(self, teacher_id):
        delete_day = f"DELETE FROM {self.teachers_table_name} WHERE id = %s;"
        self.cursor.execute(delete_day, (str(teacher_id), ))
        self.conn.commit()
        self._update_shedule()

    def _update_shedule(self):
        self.teachers_names, self.teachers_places = self._fetch_teachers()
        self.class_names = self._fetch_classes()
        self.tabs.removeTab(1)
        self.tabs.removeTab(0)
        self._create_shedule_tab()
        self._create_teachers_tab()


def get_week_num():
    first_day = date(2021, 8, 30)
    today = date.today()
    delta = (today - first_day).days
    week_number = (delta // 7) + 1
    return week_number


app = QApplication(sys.argv)
win = MainWindow()
win.show()


sys.exit(app.exec_())

