import tkinter as tk
from tkinter import ttk
import sqlite3

class Master(tk.Frame):       # создаем класс основного фрейма, принадлежащего главному окну
    def __init__(self, root): # создаем конструктер класса
        super().__init__(root) # переопределяем конструкто родительского класса
        self.init_master()     # инициализируем элементы графического интерфейса
        self.db = db # создаем в конструкторе переменную self.db, которой присвоем переменную db, созданную в if __name__=='__main__'
        self.view_records() # чтою при первом запуске отображалось содержимое виджетов в виджетах


    def init_master(self):     # метод для инициализии элементов графического интерфейса
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) # создаем тулбар для кнопок меню вверху фрейма
        toolbar.pack(side=tk.TOP, fill=tk.X) # отображаем тулбар вверху фрейма и растянут на всю ширину фрейма

        self.add_img = tk.PhotoImage(file='add.gif') # создаем обьект иконки для кнопки
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию',
                                    command=self.open_dialog, bd=0,
                                    bg='#d7d8e0', compound=tk.TOP,
                                    image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'description', 'costs', 'total'), height=15, show='headings') # создаем таблицу для записей
        # свойство show='headings' --- чтоб непоказывать нулевую колонку (primary key)
        self.tree.column('ID', width=30, anchor=tk.CENTER) # задаем параметры колонкам, имена которых мы передали кортежем выше
        self.tree.column('description', width=335, anchor=tk.CENTER)
        self.tree.column('costs', width=190, anchor=tk.CENTER)
        self.tree.column('total', width=90, anchor=tk.CENTER) # anchor - привязка текста внутри ячейки

        self.tree.heading('ID', text='ID') # задаем название для колонки, которое будет видеть пользователь
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')

        self.tree.pack()

    def records(self, description, costs, total): # создаем функцию для добавления записи в базу данных
        self.db.insert_data(description, costs, total) # у обьекта self.db вызываем функцию добавления данных в поля
        self.view_records() # чтоб при кождом добавлении поля в виджетах отобразилось содержимое бд

    def view_records(self): # функция для отображения содержимого базы данных в окне нашего приложения
        self.db.curs.execute('''SELECT * FROM finance''') # извлекаем все поля из таблицы finance
        [self.tree.delete(i) for i in self.tree.get_children()] # очишаем виджет перед отображением данных бд
        [self.tree.insert('', 'end', values=row) for row in self.db.curs.fetchall()] # извлекаем содержимое бд и построчно помещаем его в виджеты

    def open_dialog(self): # функция для вызова дочернего окна путем создания обьекта класса Child()
        Child()

class Child(tk.Toplevel): # класс дочернего окна, которое появляется при нажатии кнопки меню
    def __init__(self):   # Toplevel - класс для создания многооконных программ и дочерних окон
        super().__init__(root)
        self.init_child()  # инициализируем элементы графического интерфейса дочернего окна
        self.view = app # создаем переменную self.view - присваеваем ей обьект app (обьект нашего приложения) - для того, чтоб обратится к функции record из класса Master

    def init_child(self): # инициализируем обьекты и виджеты дочернего окна
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        # создаем надписи к полям ввода
        label_description = tk.Label(self, text='Наименование: ')
        label_description.place(x=30, y=50)
        label_select = ttk.Label(self, text='Статья дохода/расхода: ')
        label_select.place(x=30, y=80)
        label_sum = ttk.Label(self, text='Сумма: ')
        label_sum.place(x=30, y=110)

        self.entry_description = ttk.Entry(self) # создаем в дочернем окне поле ввода для описания
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self) # создаем в дочернем окне поле ввода для суммы денег
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'], width=10) # создадим комбобокс с вариантами выбора
        self.combobox.current(0) # установим по умолчанию первый элемени списка values
        self.combobox.place(x=200, y=80)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)
        # создаем кнопку закрытия дочернего окна

        self.btn_ok = ttk.Button(self, text='Добавить',
                                 command=lambda: self.view.records(self.entry_description.get(),
                                                                        self.combobox.get(),
                                                                        self.entry_money.get())) # добавляем данные при нажатии кнопки
        self.btn_ok.place(x=220, y=170)
       # self.btn_ok.bind('<Button-1>') #, lambda event: self.view.record(self.entry_description.get(),
                                        #                              self.entry_money.get(),
                                         #                             self.combobox.get()))
        # кнопка будет срабатывать при нажатии левай кнопки мыши и выполнять lambda-функцию
        #


        # пока дочернее окно не закрыто - ничего с основным окном сделать нельзя, дочернее окно всегда сверху других окон.
        # для этого применим функции grab_set() и focus_set()
        self.grab_set()  # для перехвата всех событий
        self.focus_set() # для удержания фокуса на окне

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db') # соеденение с базой данных. если бд еще нет - то она будет создана
        self.curs = self.conn.cursor() # создание обьекта cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS finance(id INTEGER PRIMARY KEY, description TEXT, costs TEXT, total REAL)''') # создание таблици с именем finance и полями в ней
        # NULL - пустое; INTEGER - целочисленное; REAL - числовое; TEXT - текстовое; BLOB - бинарное (типа фото и так далее)
        self.conn.commit() # сохранить изменения

    def insert_data(self, description, costs, total): # запись значений в таблицу в столбцы
        self.curs.execute('''INSERT INTO finance(description, costs, total) VALUES(?, ?, ?)''', (description, costs, total))
        self.conn.commit()


if __name__=='__main__':
    root = tk.Tk()
    db = DB()  # создаем обьект класса базы данных
    app = Master(root)
    app.pack()
    root.title('Учет финансов')
    root.geometry('650x450+300+200')
    root.resizable(False, False)

    root.mainloop()