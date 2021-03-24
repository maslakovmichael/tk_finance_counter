import tkinter as tk
from tkinter import ttk
import sqlite3

class Master(tk.Frame):       # создаем класс основного фрейма, принадлежащего главному окну
    def __init__(self, root): # создаем конструктер класса
        super().__init__(root) # переопределяем конструкто родительского класса
        self.init_master()     # инициализируем элементы графического интерфейса
        self.db = db # создаем в конструкторе переменную self.db, которой присвоем переменную db, созданную в if __name__=='__main__'
        self.view_records() # чтоб при первом запуске отображалось содержимое виджетов в виджетах


    def init_master(self):     # метод для инициализии элементов графического интерфейса
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) # создаем тулбар для кнопок меню вверху фрейма
        toolbar.pack(side=tk.TOP, fill=tk.X) # отображаем тулбар вверху фрейма и растянут на всю ширину фрейма

        self.add_img = tk.PhotoImage(file='add.gif') # создаем обьект иконки для кнопки
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию',
                                    command=self.open_dialog, bd=0,
                                    bg='#d7d8e0', compound=tk.TOP,  # чтоб иконка отображалась над названием кнопки
                                    image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.edit_image = tk.PhotoImage(file='update.gif') # создаем обьект иконки для кнопки
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', image=self.edit_image, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, # чтоб иконка отображалась над названием кнопки
                                    command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT) # создаем кнопку редактирования записи, которая вызывает функцию self.open_records()

        self.delete_image = tk.PhotoImage(file='delete.gif') # создаем обьект иконки для кнопки
        btn_delete_dialog = tk.Button(toolbar, text='Удалить позицию',
                                      bg='#d7d8e0', bd=0,
                                      image=self.delete_image, compound=tk.TOP, # чтоб иконка отображалась над названием кнопки
                                      command = self.delete_records)
        btn_delete_dialog.pack(side=tk.LEFT) # создаем кнопку удаления записи, которая вызывает функцию self.delete_records()

        self.search_image = tk.PhotoImage(file='search.gif')  # создаем обьект иконки для кнопки
        btn_search_dialog = tk.Button(toolbar, text='Поиск',
                                      bg='#d7d8e0', bd=0,
                                      image=self.search_image, compound=tk.TOP,
                                      # чтоб иконка отображалась над названием кнопки
                                      command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)  # создаем кнопку поиска записи, которая вызывает функцию self.open_search_dialog()

        self.refresh_image = tk.PhotoImage(file='refresh.gif')  # создаем обьект иконки для кнопки
        btn_refresh_dialog = tk.Button(toolbar, text='Обновить',
                                      bg='#d7d8e0', bd=0,
                                      image=self.refresh_image, compound=tk.TOP,
                                      # чтоб иконка отображалась над названием кнопки
                                      command=self.view_records)
        btn_refresh_dialog.pack(side=tk.LEFT)  # создаем кнопку обновления записей, которая вызывает функцию self.veiw_records()

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

    def update_records(self, description, costs, total):# создаем функцию изменения записи, вызываем метод execute(), передаем SQL-запрос на запись с новыми данными, с условием определенного id
        self.db.curs.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE ID=?''',
                             (description, costs, total, self.tree.set(self.tree.selection()[0], '#1')))
        # ID получаем из обьекта self.tree через метод set() - получим id выделенной строки обьекта self.tree,
        # еще в методе set() нужно указать два аргумента - self.tree.selection()[0] - из списка всех ID в обьекте self.tree берем первый элемент - это будет обьект выбраной строки
        # '#1' - второй аргумент метода self.tree.set() - говорит - какой именно столбец нам необходим из обьекта строки self.tree.selection()[0]
        self.db.conn.commit() # сохраняем данные в бд
        self.view_records() # отображаем данные в полях виджета

    def delete_records(self): # функция удалениф записей
        for select_item in self.tree.selection(): # чтоб можно было удалять сразу несколько выделенных строк - перебираем в цикле обьект self.tree.selection()
            self.db.curs.execute('''DELETE FROM finance WHERE id=?''', (self.tree.set(select_item, '#1'),)) # для каждай строки из выделенного мышью обьема self.tree.select() - производим удаление из бд
            # значение id строки берем из self.tree.set(select_item, '#1')
            self.db.conn.commit() # записываем изменения
            self.view_records() # отображаем обновленную информацию в виджетах


    def search_records(self, description):
        description = ('%'+description+'%',) # составляем кортеж из слова запроса для использования с оператором WHERE a LIKE b
        self.db.curs.execute('''SELECT * FROM finance WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()] # очищаем поля в self.tree
        [self.tree.insert('', 'end', values=row) for row in self.db.curs.fetchall()] # заполняем поля в self.tree данными, полученными из self.db.curs.fetchall()

    # WHERE name LIKE 'text%' - находит любые значения, начинающиеся с text
    # WHERE name LIKE '%text' - находит любые значения, заканчивающиеся на text
    # WHERE name LIKE '%text%' - находит любые значения, которые имеют text в любой позиции
    # WHERE name LIKE '_text%' - находит любые значения, которые имеют text во второй позиции
    # WHERE name LIKE 'text_%_%' - находит любые значения, которые начинаются с text и имеют не менее трех символов
    # WHERE name LIKE 'text%data' - находит любые значения, которые начинаются с text и заканчиваются data

    def open_dialog(self): # функция для вызова дочернего окна путем создания обьекта класса Child()
        Child()

    def open_update_dialog(self): # функция для вызова дочернего окна редактирования через создание обьекта класса Update()
        Update()

    def open_search_dialog(self): # функция для вызова окна поиска
        Search()

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

class Update(Child): # создаем класс Update - наследуем его от класса Child - чтоб использовать форму ввода для updating
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app # для доступа к функции update_records - обьявляем обьект self.view как app


    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать',
                                command=lambda: self.view.update_records(self.entry_description.get(),
                                                                        self.combobox.get(),
                                                                        self.entry_money.get()))
        btn_edit.place(x=190, y=170)
        # btn_edit.bind('<Button-1>', lambda event: self.view.update_records(self.entry_description.get(),
        #                                                                    self.combobox.get(),
        #                                                                    self.entry_money.get()))
        self.btn_ok.destroy() # удаляем кнопку 'Добавить'


class Search(tk.Toplevel): # создаем класс для поиска по бд, наследуемся от класса tk.Toplevel
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск') # изменяем название
        self.geometry('300x100+400+300') # установим размеры окна поиска
        self.resizable(False, False) # запрещаем менять размеры окна

        label_search = tk.Label(self, text='Поиск') # лейбл с назваением
        label_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self) # поле для ввода поискового запроса
        self.entry_search.place(x=105, y=20, width=165)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+') # чтоб окно автоматически закрывалось после нажатия на кнопку
        # add='+' - параметр для добавления на одно нажатие кнопки второй доп функции

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