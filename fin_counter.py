import tkinter as tk

class Master(tk.Frame):       # создаем класс основного фрейма, принадлежащего главному окну
    def __init__(self, root): # создаем конструктер класса
        super().__init__(root) # переопределяем конструкто родительского класса
        self.init_master()     # инициализируем элементы графического интерфейса

    def init_master(self):     # метод для инициализии элементов графического интерфейса
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) # создаем тулбар для кнопок меню вверху фрейма
        toolbar.pack(side=tk.TOP, fill=tk.X) # отображаем тулбар вверху фрейма и растянут на всю ширину фрейма

        self.add_img = tk.PhotoImage(file='add.gif') # создаем обьект иконки для кнопки
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию',
                                    command=self.open_dialog, bd=0,
                                    bg='#d7d8e0', compound=tk.TOP,
                                    image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

    def open_dialog(self): # функция для вызова дочернего окна путем создания обьекта класса Child()
        Child()

class Child(tk.Toplevel): # класс дочернего окна, которое появляется при нажатии кнопки меню
    def __init__(self):   # Toplevel - класс для создания многооконных программ и дочерних окон
        super().__init__(root)
        self.init_child()  # инициализируем элементы графического интерфейса дочернего окна

    def init_child(self): # инициализируем обьекты и виджеты дочернего окна
        self.title('Добавить доходы/расходы')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        # пока дочернее окно не закрыто - ничего с основным окном сделать нельзя, дочернее окно всегда сверху других окон.
        # для этого применим функции grab_set() и focus_set()
        self.grab_set()  # для перехвата всех событий
        self.focus_set() # для удержания фокуса на окне



if __name__=='__main__':
    root = tk.Tk()
    app = Master(root)
    app.pack()
    root.title('Учет финансов')
    root.geometry('650x450+300+200')
    root.resizable(False, False)

    root.mainloop()