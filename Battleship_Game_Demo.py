import tkinter as tk
from tkinter import messagebox
import random

# Игровое поле и сопоставление букв с индексами
BOARD_SIZE = 10
bot_board = [['empty' for _ in range(10)] for _ in range(10)]
player_board = [['empty' for _ in range(10)] for _ in range(10)]
player_1_board = [['empty' for _ in range(10)] for _ in range(10)]
player_2_board = [['empty' for _ in range(10)] for _ in range(10)]
Letter_to_Index = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}

ships_info = {
    "Carrier": 5,      # Авианосец (5 клеток)
    "Battleship": 4,   # Линкор (4 клетки)
    "Cruiser": 3,      # Крейсер (3 клетки)
    "Submarine": 3,    # Подводная лодка (3 клетки)
    "Destroyer": 2     # Эсминец (2 клетки)
}

# Класс для представления корабля
class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.hits = 0
        self.sunk = False

    def is_sunk(self):
        return self.hits >= self.size

# Флот
fleet_player = []
fleet_player_1 = []
fleet_player_2 = []
fleet_bot = []

# Проверка позиции
def is_position_valid(positions):
    for row, col in positions:
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if 0 <= i < 10 and 0 <= j < 10:
                    if bot_board[i][j] == 'ship':
                        return False
    return True

# Случайное размещение кораблей
def place_ship(ship):
    while True:
        orientation = random.choice(["horizontal", "vertical"])
        
        if orientation == "horizontal":
            row = random.randint(0, 9)
            col = random.randint(0, 10 - ship.size)
            positions = [(row, col + i) for i in range(ship.size)]
        else:
            row = random.randint(0, 10 - ship.size)
            col = random.randint(0, 9)
            positions = [(row + i, col) for i in range(ship.size)]
        
        if all(bot_board[r][c] == 'empty' for r, c in positions) and is_position_valid(positions):
            for r, c in positions:
                bot_board[r][c] = 'ship'  # Поле для бота
            ship.coordinates = positions
            fleet_bot.append(ship)
            break

# Размещаем все корабли для бота
for ship_name, ship_size in ships_info.items():
    ship = Ship(ship_name, ship_size)
    place_ship(ship)

# Создание основного окна
root = tk.Tk()
root.title("Battleship Game")
root.geometry("1200x600")  # Увеличиваем размер окна

frame = tk.Frame(root)
frame.pack(expand=True)

var = tk.IntVar(value=1)

# Font definitions
bold_font = ("Arial", 14, "bold")
normal_font = ("Arial", 14)

# Радиокнопки для выбора режима
tk.Radiobutton(frame, text="Singleplayer", variable=var, value=1, padx=20, pady=20, font=bold_font).grid(row=0, column=0, sticky="w")
tk.Radiobutton(frame, text="Two Players", variable=var, value=2, padx=20, pady=20, font=bold_font).grid(row=0, column=1, sticky="w")

# Функция для старта игры в зависимости от режима
def start_game():
    placement.withdraw()
    if var.get() == 1:
        open_single_player()
    else:
        open_multi_player()
    main_frame.pack_forget()

# Глобальная переменная для списка кораблей бота и игрока
bot_ships = []
player_ships = []
fleet = []
current_ship = None

# Размещаем все корабли для игрока в ручную
def start_placement():
    
    root.destroy()

    # Настройки для интерфейса
    global placement 
    placement = tk.Tk()
    placement.title("Battleship Game")
    global main_frame
    main_frame = tk.Frame(placement)
    main_frame.pack(padx=10, pady=10)

    # Сеточная структура кнопок
    buttons_0_global = []

    # Список для отображения кораблей
    ship_list_label = tk.Label(main_frame, text="Ships:\n", font=("Arial", 14))
    ship_list_label.grid(row=0, column=BOARD_SIZE, rowspan=10, padx=10)

    # Проверка, что позиция корабля не выходит за пределы поля и не пересекается с другими кораблями
    def is_position_valid_manual(positions):
        for row, col in positions:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < 10 and 0 <= j < 10:
                        if player_board[i][j] == 'ship':
                            return False
        return True
    def cell_click(r, c):
        global current_ship
        if current_ship is None:  # Если корабль не выбран
            return False

        # Если корабль уже был размещен
        if current_ship.coordinates:  # Проверяем, что корабль уже был размещен
            old_positions = current_ship.coordinates
            print(f"Перемещаем корабль {current_ship.name} с позиций {old_positions}")

            # Если старая позиция не пустая, удаляем её
            if old_positions:
                for old_r, old_c in old_positions:
                    player_board[old_r][old_c] = 'empty'
                    buttons_0_global[old_r][old_c].config(text=" ", bg="#1591ea")  # Возвращаем исходный цвет
                    print(f"Очищена позиция {old_r}, {old_c}")

            # Очищаем старые координаты
            current_ship.coordinates = []  # Очистим старые координаты

            # Убираем старый корабль из списка
            fleet.remove(current_ship)
            fleet_player.remove(current_ship)
            print(f"Корабль {current_ship.name} удален из списка fleet")

        # Очищаем все красные клетки
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if buttons_0_global[row][col].cget("bg") == "red":
                    if player_board[row][col] == 'ship':
                        buttons_0_global[row][col].config(bg="green")  # Если на клетке есть корабль, делаем её зелёной
                    else:
                        buttons_0_global[row][col].config(bg="#1591ea")  # Если на клетке нет корабля, делаем её синей

        # Размещение нового корабля
        positions = []
        for i in range(current_ship.size):
            if orientation.get() == "horizontal":
                positions.append((r, c + i))

            else:
                positions.append((r + i, c))

        # Проверяем валидность позиции
        valid = all(0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE for r, c in positions) and is_position_valid_manual(positions)

        # Проверка пересечений (клетки остаются красными, если корабль перекрывает другие)
        if not valid:
            for r, c in positions:
                buttons_0_global[r][c].config(bg="red")
            print(f"Невалидная позиция: {positions}")

        # После проверки и размещения
        if valid:
            # Обновляем поле и добавляем корабль в новый список
            for r, c in positions:
                player_board[r][c] = 'ship'
                buttons_0_global[r][c].config(text=current_ship.name[0], bg="green")  # Клетки становятся зелеными

            # Устанавливаем новые координаты
            current_ship.coordinates = positions

            # Добавляем корабль в список, если его нет
            if current_ship not in fleet:
                fleet.append(current_ship)
                fleet_player.append(current_ship)
            update_ships_list()
            check_all_ships_placed()

            return True
        return False

    def reset_colors_after_move():
        # Перебираем все клетки поля и проверяем, стали ли они свободными
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if player_board[row][col] == 'empty':
                    buttons_0_global[row][col].config(bg="#1591ea")  # Если клетка пуста, делаем её зелёной

    def update_ships_list():
        ship_list_label.config(text="Ships:\n")
        for ship in fleet and fleet_player:
            ship_list_label.config(text=ship_list_label.cget("text") + f"{ship.name} ({ship.size} cells)\n")

            # Проверяем и сбрасываем все красные клетки
            reset_colors_after_move()

    def check_intersections_and_reset():
        # Перебираем все клетки и сбрасываем их в зеленый, если они больше не заняты
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Если клетка свободна, сбрасываем цвет в зеленый
                if player_board[row][col] == 'empty':
                    buttons_0_global[row][col].config(bg="#1591ea")  # Если клетка пуста, делаем её зелёной

    def check_all_ships_placed():
        if len(fleet) == len(ships_info):  # Проверяем, все ли корабли размещены
            start_button.grid(row=len(ships_info) + 2, column=BOARD_SIZE + 1, pady=10)  # Появляется кнопка "Начать игру"

    def reset_board():
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                buttons_0_global[row][col].config(text=" ", bg="#1591ea")
                player_board[row][col] = 'empty'

        fleet.clear()
        fleet_player.clear()
        update_ships_list()
        check_all_ships_placed()

        # Проверяем и сбрасываем все красные клетки
        check_intersections_and_reset()

        # Сбрасываем текущий корабль
        global current_ship
        current_ship = None

    # Выбор корабля
    def select_ship(name, size):
        global current_ship
        # Сбрасываем текущий корабль
        current_ship = Ship(name, size)
        print(orientation.get())  # Проверка текущего значения ориентации

    # Настройка игрового поля
    def setup_board():
        buttons_0 = []
        for row in range(BOARD_SIZE):
            button_row = []
            for col in range(BOARD_SIZE):
                btn = tk.Button(main_frame, text=" ", width=9, height=4, bg="#1591ea", 
                                command=lambda r=row, c=col: cell_click(r, c))
                btn.grid(row=row, column=col)
                button_row.append(btn)
            buttons_0.append(button_row)
        return buttons_0

    # Старт игры
    buttons_0_global = setup_board()

    # Радиокнопки для выбора ориентации
    orientation = tk.StringVar(value=None)
    tk.Radiobutton(main_frame, text="Горизонтально", variable=orientation, value="horizontal", font=("Arial", 12)).grid(row=len(ships_info), column=BOARD_SIZE + 1, sticky="w")
    tk.Radiobutton(main_frame, text="Вертикально", variable=orientation, value="vertical", font=("Arial", 12)).grid(row=len(ships_info) + 1, column=BOARD_SIZE + 1, sticky="w")

    # Радиокнопки для выбора корабля
    ship_var = tk.StringVar(value="Carrier")  # Изначально выбран авианосец
    for i, (ship_name, ship_size) in enumerate(ships_info.items()):
        tk.Radiobutton(main_frame, text=ship_name, variable=ship_var, value=ship_name, font=("Arial", 12),
                    command=lambda name=ship_name, size=ship_size: select_ship(name, size)).grid(row=i, column=BOARD_SIZE+2, sticky="w")

    # Кнопка "Начать игру"
    start_button = tk.Button(main_frame, text="Начать игру", font=("Arial", 14), command=start_game)
    start_button.grid(row=len(ships_info) + 2, column=BOARD_SIZE + 1, pady=10)
    start_button.grid_forget()  # Скрыть кнопку в начале

    # Кнопка "Сброс"
    reset_button = tk.Button(main_frame, text="Сброс", font=("Arial", 14), command=reset_board)
    reset_button.grid(row=len(ships_info) + 3, column=BOARD_SIZE + 1, pady=10)

# Одиночный режим
def open_single_player():
    global bot_ships  # Делаем bot_ships глобальной переменной
    global player_ships  # Делаем player_ships глобальной переменной
    global root_0
    root_0 = tk.Tk()
    root_0.title("Singleplayer")
    root_0.geometry("1200x600")  # Увеличиваем размер окна

    # Создаем фрейм для центра
    center_frame = tk.Frame(root_0)
    center_frame.pack(expand=True)

    # Фрейм для списка кораблей игрока
    ship_list_frame_player = tk.Frame(center_frame)
    ship_list_frame_player.grid(row=1, column=0, padx=20)

    # Создаем метки для каждого корабля игрока и добавляем их в player_ships
    player_ships = [tk.Label(ship_list_frame_player, text=ship.name, font=("Arial", 14)) for ship in fleet_player]
    for idx, ship_label in enumerate(player_ships):
        ship_label.grid(row=idx, column=0, sticky="w")

    # Фрейм для поля игрока
    frame_0 = tk.Frame(center_frame)
    frame_0.grid(row=1, column=1, padx=20)

    # Добавляем кнопки для поля игрока
    buttons_player_board = []
    for row in range(10):
        button_row = []
        for col_letter in Letter_to_Index.keys():
            btn = tk.Button(frame_0, text=" ", width=5, height=2, bg="#1591ea",
                            command=lambda r=row, c=col_letter: click_on_player_board(r, c))
            btn.grid(row=row, column=Letter_to_Index[col_letter])
            button_row.append(btn)
        buttons_player_board.append(button_row)

    global buttons_0_global
    buttons_0_global = buttons_player_board

    # Фрейм для списка кораблей бота
    ship_list_frame_bot = tk.Frame(center_frame)
    ship_list_frame_bot.grid(row=1, column=4, padx=20)

    # Создаем метки для каждого корабля бота и добавляем их в bot_ships
    bot_ships = [tk.Label(ship_list_frame_bot, text=ship.name, font=("Arial", 14)) for ship in fleet_bot]
    for idx, ship_label in enumerate(bot_ships):
        ship_label.grid(row=idx, column=0, sticky="w")

    # Фрейм для поля бота
    frame_bot = tk.Frame(center_frame)
    frame_bot.grid(row=1, column=3, padx=20)

    buttons_bot = []
    for row in range(10):
        button_row = []
        for col_letter in Letter_to_Index.keys():
            btn = tk.Button(frame_bot, text=" ", width=5, height=2, bg="#1591ea",
                            command=lambda r=row, c=col_letter: click_on_bot_board(r, c))
            btn.grid(row=row, column=Letter_to_Index[col_letter])
            button_row.append(btn)
        buttons_bot.append(button_row)

    global buttons_bot_global
    buttons_bot_global = buttons_bot

    # Названия полей и "VS"
    label_1 = tk.Label(center_frame, text="Игрок 1", font=("Arial", 14, "bold"))
    label_1.grid(row=0, column=1)

    vs_label = tk.Label(center_frame, text="VS", font=("Arial", 14, "bold"), fg="red")
    vs_label.grid(row=1, column=2)

    label_2 = tk.Label(center_frame, text="Бот", font=("Arial", 14, "bold"))
    label_2.grid(row=0, column=3)

    root_0.mainloop()

def check_win_condition():
    player_all_sunk = all(ship.is_sunk() for ship in fleet_player)
    bot_all_sunk = all(ship.is_sunk() for ship in fleet_bot)
    
    if player_all_sunk:
        print("Победа бота!")
        # Дополнительные действия, такие как блокировка кнопок, сообщение об окончании игры и т.д.
        messagebox.showinfo(" Бот выиграл!", "Лошара!")
        root_0.destroy()


    elif bot_all_sunk:
        print("Победа игрока!")
        # Дополнительные действия, такие как блокировка кнопок, сообщение об окончании игры и т.д.
        messagebox.showinfo("Игрок выиграл!","Чё сильно умный?")
        root_0.destroy()

current_turn = "player"  # Начинает игрок

# Функция для смены хода
def switch_turn():
    global current_turn
    if current_turn == "player":
        current_turn = "bot"
    else:
    #    bot_attack()  # После хода игрока бот сразу атакует
        current_turn = "player"


# Функция для обновления цвета кнопок при потоплении корабля
def update_ship_color(ship, buttons):
    for (r, c) in ship.coordinates:
        buttons[r][c].config(bg="black")  # меняем цвет на черный

# Функция для атаки бота
"""def bot_attack():
    row = random.randint(0, 9)
    col_letter = random.choice(list(Letter_to_Index.keys()))
    
    # Проверяем, не было ли атаковано это место раньше
   # if buttons_0_global[row][Letter_to_Index[col_letter]]['text'] in ["X", "O"]:
    #    return bot_attack()  # Если уже атаковано, бот пробует снова

    click_on_player_board(row, col_letter)  # Имитация нажатия
    print(f"Бот атакует клетку {row}, {col_letter}")
"""
# Функция клика по полю игрока
def click_on_player_board(row, col_letter):
    global current_turn
    if current_turn != "bot":  # Проверяем, что сейчас ход бота
        return  # Если нет, то выходим из функции

    col = Letter_to_Index[col_letter]
    hit = False
    for ship in fleet_player:
        if (row, col) in ship.coordinates:
            hit = True
            ship.hits += 1
            buttons_0_global[row][col].config(bg="red", text="X")  # меняем цвет на красный при попадании
            
            if ship.is_sunk():  # если корабль потоплен
                for r, c in ship.coordinates:
                    button = buttons_0_global[r][c]
                    button.config(bg="black", text="X")
                print(f"{ship.name} потоплен!")
                update_ship_list(ship, player_ships)
                check_win_condition()
            break

    if not hit:
        buttons_0_global[row][col].config(bg="cyan", text="O")  # цвет при промахе
    
    # Переключаем ход
        switch_turn()  # После атаки бота ход переключается на игрока


# Функция обновления статуса кораблей в списке
def update_ship_list(ship, ship_list_labels):
    # Находим нужный Label для потопленного корабля
    for label in ship_list_labels:
        if label.cget("text") == ship.name:
            label.config(fg="red")  # Меняем цвет на красный для потопленного корабля
            break

# Функция клика по полю бота (обновление статуса списка после потопления)
def click_on_bot_board(row, col_letter):
    global current_turn
    if current_turn == "bot":  # Проверяем, что сейчас ход игрока
        return  # Если нет, то выходим из функции

    col = Letter_to_Index[col_letter]
    hit = False
    for ship in fleet_bot:
        if (row, col) in ship.coordinates:
            hit = True
            ship.hits += 1
            if ship.is_sunk():
                for r, c in ship.coordinates:
                    button = buttons_bot_global[r][c]
                    button.config(bg="black", text="X")
                print(f"{ship.name} потоплен!")
                update_ship_list(ship, bot_ships)  # Обновляем список потопленных кораблей
                check_win_condition()
            break
    
    button = buttons_bot_global[row][col]
    if hit and not ship.is_sunk():
        button.config(bg="red", text="X")
        print(f"Игрок попал в клетку {row}, {col_letter}")
    elif not hit:
        button.config(bg="cyan", text="O")
        print(f"Игрок промахнулся на клетке {row}, {col_letter}")

        switch_turn()

def cell_click_1(row, col_letter):
    col = Letter_to_Index[col_letter]
    hit = False
    for ship in fleet_player_1:
        if (row, col) in ship.coordinates:
            hit = True
            ship.hits += 1
            if ship.is_sunk():
                for r, c in ship.coordinates:
                    button = buttons_1_global[r][c]
                    button.config(bg="black", text="X")
                print(f"{ship.name} потоплен!")
            break
    
    button = buttons_1_global[row][col]
    if hit and not ship.is_sunk():
        button.config(bg="red", text="X")
        print(f"Игрок 1 попал в клетку {row}, {col_letter}")
    elif not hit:
        button.config(bg="cyan", text="O")
        print(f"Игрок 1 промахнулся на клетке {row}, {col_letter}")

def cell_click_2(row, col_letter):
    col = Letter_to_Index[col_letter]
    hit = False
    for ship in fleet_player_2:
        if (row, col) in ship.coordinates:
            hit = True
            ship.hits += 1
            if ship.is_sunk():
                for r, c in ship.coordinates:
                    button = buttons_2_global[r][c]
                    button.config(bg="black", text="X")
                print(f"{ship.name} потоплен!")
            break
    
    button = buttons_2_global[row][col]
    if hit and not ship.is_sunk():
        button.config(bg="red", text="X")
        print(f"Игрок 2 попал в клетку {row}, {col_letter}")
    elif not hit:
        button.config(bg="cyan", text="O")
        print(f"Игрок 2 промахнулся на клетке {row}, {col_letter}")

# Многопользовательский режим
def open_multi_player():
    root_1 = tk.Tk()
    root_1.title("Multiplayer (In Progress)")
    root_1.geometry("1200x600")  # Увеличиваем размер окна

    # Создаем фрейм для центра
    center_frame = tk.Frame(root_1)
    center_frame.pack(expand=True)

    # Фрейм для списка вражеских кораблей игрока 1
    ship_list_frame_player1 = tk.Frame(center_frame)
    ship_list_frame_player1.grid(row=1, column=0, padx=20)

    # Добавляем список вражеских кораблей
    enemy_ships_1 = [tk.Label(ship_list_frame_player1, text=ship.name, font=normal_font) for ship in fleet_player_2]
    for idx, ship_label in enumerate(enemy_ships_1):
        ship_label.grid(row=idx, column=0, sticky="w")

    # Фрейм для поля игрока 1
    frame_1 = tk.Frame(center_frame)
    frame_1.grid(row=1, column=1, padx=20)

    buttons_1 = []
    for row in range(10):
        button_row = []
        for col_letter in Letter_to_Index.keys():
            btn = tk.Button(frame_1, text=" ", width=5, height=2, bg="#1591ea",
                            command=lambda r=row, c=col_letter: cell_click_1(r, c))
            btn.grid(row=row, column=Letter_to_Index[col_letter])
            button_row.append(btn)
        buttons_1.append(button_row)

    global buttons_1_global
    buttons_1_global = buttons_1

    # Фрейм для списка вражеских кораблей игрока 2
    ship_list_frame_player2 = tk.Frame(center_frame)
    ship_list_frame_player2.grid(row=1, column=4, padx=20)

    # Добавляем список кораблей игрока 2
    enemy_ships_2 = [tk.Label(ship_list_frame_player2, text=ship.name, font=normal_font) for ship in fleet_player_1]
    for idx, ship_label in enumerate(enemy_ships_2):
        ship_label.grid(row=idx, column=0, sticky="w")

    # Фрейм для поля игрока 2
    frame_2 = tk.Frame(center_frame)
    frame_2.grid(row=1, column=3, padx=20)

    buttons_2 = []
    for row in range(10):
        button_row = []
        for col_letter in Letter_to_Index.keys():
            btn = tk.Button(frame_2, text=" ", width=5, height=2, bg="#1591ea",
                            command=lambda r=row, c=col_letter: cell_click_2(r, c))
            btn.grid(row=row, column=Letter_to_Index[col_letter])
            button_row.append(btn)
        buttons_2.append(button_row)

    global buttons_2_global
    buttons_2_global = buttons_2

    # Названия полей для двух игроков и "VS"
    label_1 = tk.Label(center_frame, text="Игрок 1", font=bold_font)
    label_1.grid(row=0, column=1)

    vs_label = tk.Label(center_frame, text="VS", font=bold_font, fg="red")
    vs_label.grid(row=1, column=2)

    label_2 = tk.Label(center_frame, text="Игрок 2", font=bold_font)
    label_2.grid(row=0, column=3)

    root_1.mainloop()

# Запуск программы
start_game_button = tk.Button(frame, text="Start Game", command=start_placement, font=bold_font)
start_game_button.grid(row=1, column=0, columnspan=2, pady=40)

root.mainloop()
