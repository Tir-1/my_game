import pygame
import sqlite3
import random
from draw import draw_info, draw_score, draw_score2, BackFon

# Создание переменных которые нам пригодятся потом.
decks1 = []  # колода игрока
decks2_choose = ["dark_knight1", "frost1", "frost2", "poison_steel2", ["flock5", "flock6"], ["flock7", "flock8"],
                 "tower3", "tower4", "redania_solder3", "redania_solder4", "rider1", "rider2",
                 "temple_of_winter1", "vampire3", "vampire4", "poison_steel1", "hunter3", "hunter4"]
decks2 = []  # колода противника
replays = []
# Возможные карты игрока
deck_king = ["redania_solder1", "redania_solder2", "tower1", "tower2", "kaedwin_solder1", "kaedwin_solder2", "healer1",
             "knight1", "crossbow1", "crossbow2"]
deck_monsters = ["vampire1", "vampire2", ["flock1", "flock3"], ["flock2", "flock4"]]
deck_hunter = ["hunter1", "hunter2", "poison_steel1", "poison_steel2", ]
all_sprites = pygame.sprite.Group()
back_sprites = pygame.sprite.Group()
deck_sprites = pygame.sprite.Group()
card_sprites = pygame.sprite.Group()
enemy_objects = {"attack": [], "vampire": [], "flock": [], "hunter": [], "basic": [], "gain": [], "frost": [],
                 "frosty": []}
his_cards = {"attack": [], "vampire": [], "hunter": [], "flock": [], "basic": [], "gain": [], "frost": [], "frosty": []}
vampires = {"vampire": [], "flock": []}
enemy_cards = {}
my_cards = {"target_attack": [], "target_hunter": [], "target_basic": []}
doubles = []
old_names = []


# Этот класс хранит важные для игры переменные, а также отвечает за глобальные события
class Game:
    def __init__(self):
        self.player_move = True
        self.can_move = False
        self.target = False
        self.target_num = 0
        self.first = ""
        self.second = ""
        self.move = 1
        self.waits = {}
        self.name = ""
        self.played = True
        self.score1 = 0
        self.score2 = 0
        self.text = "Ничего нет, Нажмите лкм по карточке"
        self.pas = False
        self.temple = False
        self.n = True
        self.n2 = True
        self.choose = True
        self.effect = ""
        self.end_text = ""

    # Исполнение способности "приказ"
    def do(self, objects):
        for i in objects:
            obj1 = i
            if self.effect == "poison":
                obj1.regeneration = False
            elif self.effect == "hunter" and obj1.description[:19] == "Категория: Чудовище":
                self.target_num = -6
            self.effect = ""
            print("do", self.player_move)
            self.can_move = True
            print(self.target_num)
            obj1.set_hp(self.target_num)
            obj1.die()
            if self.player_move:
                pass
            else:
                self.set()
            self.target = False

    # завершение хода
    def set(self):
        if self.pas:
            if self.score1 > self.score2:
                self.end_text = "Победа!!!"
            elif self.score1 < self.score2:
                self.end_text = "Ты проиграл..."
            else:
                self.end_text = "Победила дружба!"
        if self.player_move:
            # Применение способности Регенерация
            for i in vampires["vampire"]:
                if i.regeneration:
                    game.score1 += i.old_health - i.health
                    i.health = i.old_health
            for i in vampires["flock"]:
                if i.regeneration:
                    game.score1 += i.old_health - i.health
                    i.health = i.old_health
            self.n = True
            for i in replays:
                i.replay()
            self.player_move = False
        else:
            for i in his_cards["vampire"]:
                if i.regeneration:
                    game.score2 += i.old_health - i.health
                    i.health = i.old_health
            for i in his_cards["flock"]:
                if i.regeneration:
                    game.score2 += i.old_health - i.health
                    i.health = i.old_health
            # Эффект мороза
            frost_damage = -1
            if self.temple:
                frost_damage = -2
            if row1.effect == "frost":
                print(row1.len_effects)
                number = -4
                number2 = 1
                for i in range(2):
                    for j in row1.names:
                        if row1.names[str(number)] != "":
                            print(number)
                            card = row1.obj[row1.names[str(number)][1]]
                            card.set_hp(frost_damage)
                            card.die()
                            break
                        number += number2
                    number = 4
                    number2 = -1
                row1.len_effects -= 1
            if row2.effect == "frost":
                number = -4
                number2 = 1
                for i in range(2):
                    for j in row2.names:
                        if row2.names[str(number)] != "":
                            card = row2.obj[row2.names[str(number)][1]]
                            card.set_hp(frost_damage)
                            card.die()
                            break
                        number += number2
                    number = 4
                    number2 = -1
                row2.len_effects -= 1
            self.player_move = True
        # После смены хода можно будет активировать способность приказ
        for i in self.waits:
            if self.waits[i] == 0:
                self.waits[i] = 1
        game.played = True
        game.n = True
        self.n2 = True

    # Вывод результатов матча
    def end(self):
        pygame.font.init()
        font2 = pygame.font.Font(None, 100)
        end_text = font2.render(str(self.end_text), True, (100, 255, 100))
        cords_x = 600
        cords_y = 400
        screen.blit(end_text, (cords_x, cords_y))


# Функция реализующая ИИ противника
def ai():
    try:
        check = True
        number = 0
        effect = 0
        row = 1
        card = 0
        if len(enemy_objects["flock"]) != 0:
            card = enemy_cards[enemy_objects["flock"][0]]
            check = False
        if len(enemy_objects["vampire"]) != 0 and check:
            card = enemy_cards[enemy_objects["vampire"][0]]
            check = False
        if len(my_cards["target_hunter"]) != 0 and check and len(enemy_objects["hunter"]) != 0:
            card = enemy_cards[enemy_objects["hunter"][0]]
            check = False
        if row2.total != 0 and check or row1.total != 0 and check:
            if len(enemy_objects["frost"]) != 0:
                card = enemy_cards[enemy_objects["frost"][0]]
                if row1.total > row2.total:
                    effect = 1
                else:
                    effect = 2
                check = False
        if row1.effect == "frost" and check or row2.effect == "frost" and check:
            if len(enemy_objects["frosty"]) != 0:
                card = enemy_cards[enemy_objects["frosty"][0]]
                check = False
                row = 2
        if len(my_cards["target_attack"]) != 0 and check:
            if len(enemy_objects["attack"]) != 0:
                card = enemy_cards[enemy_objects["attack"][0]]
                check = False
        if check:
            for i in enemy_objects:
                if len(enemy_objects[i]) != 0:
                    card = enemy_cards[enemy_objects[i][0]]
            row = 2
        # Определение его ряда и позиции
        if row == 1 and row3.total == 8:
            row = 2
        if row == 2 and row4.total == 8:
            row = 1
        if row == 1:
            names = row3.give()
        else:
            names = row4.give()
        if names["0"] == "":
            number = 0
        else:
            for i in range(4):
                if names[str(i + 1)] == "":
                    number = i + 1
                    break
                elif names[str(-(i + 1))] == "":
                    number = -(i + 1)
                    break
        card.play(row, number, effect)
    except:
        game.pas = True


# Общий класс карты от которого наследуются более узконаправленные классы
class Card(pygame.sprite.Sprite):
    def __init__(self, group, cords_x, cords_y, name, screen, team):
        super().__init__(group)
        connection = sqlite3.connect("cards.db")
        cursor = connection.cursor()
        if len(name) > 2:
            self.name = name
        else:
            self.name = name[0]
        data = cursor.execute("SELECT * FROM allcards WHERE name = ?", (self.name[:-1],)).fetchall()
        connection.close()
        self.health = data[0][2]
        self.old_health = data[0][2]
        self.armor = data[0][3]
        self.status = data[0][4]
        self.description = data[0][5]
        self.type1 = data[0][6].split(", ")[0]
        self.type2 = data[0][6].split(", ")[1]
        self.whatDo = data[0][8].split(", ")
        self.image = pygame.image.load("data/" + data[0][7] + ".png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.team = team
        self.regeneration = False
        if "regeneration" in self.whatDo:
            self.regeneration = True

    # Функция помогающая функции play  в других классах
    def play2(self):
        if "regeneration" in self.whatDo:
            names = vampires["flock"]
            if self.team == 2:
                names = his_cards["flock"]
            for i in names:
                if i.name != self.name:
                    i.old_health += 1
                    i.set_hp(1)
        if "damage" in self.whatDo:
            if "iffrost" == self.whatDo[0]:
                if self.check_frost():
                    if "me" in self.whatDo:
                        self.set_hp(self.whatDo[-1])

    # Возвращает есть ли эффект мороза на другой стороне
    def check_frost(self):
        if self.team == 2:
            if row1.effect == "frost" or row2.effect == "frost":
                return True
        else:
            if row3.effect == "frost" or row4.effect == "frost":
                return True
        return False

    # Устанавливает описание карты
    def give_description(self):
        game.text = self.description

    # отвечает за изменения ОЗ карты
    def set_hp(self, hp):
        difference = 0
        if int(hp) > 0:
            self.health += int(hp)
            difference = int(hp)
        else:
            self.armor += int(hp)
            if self.armor < 0:
                if self.health + self.armor <= 0:
                    difference = -self.health
                else:
                    difference = self.armor
                self.health += self.armor
                self.armor = 0
        if self.team == 1:
            print("k")
            game.score1 += difference
        else:
            game.score2 += difference
        print(self.name, self.health, game.target)

    # Отрисовывает карту и элементы на ней(ОЗ, готовность приказа, эффекты)
    def draw_picture(self, health, sc):
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        color = pygame.Color("White")
        if self.health > self.old_health:
            color = pygame.Color("Green")
        elif self.health < self.old_health:
            color = pygame.Color("Red")
        text_hp = font.render(str(health), True, color)
        cords_x = 10
        cords_y = 10
        sc.fill(pygame.Color("black"))
        self.image = pygame.image.load("data/" + self.name[:-1] + ".png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        sc = self.image
        if self.name in game.waits:
            if game.waits[self.name] == 1:
                pygame.draw.circle(sc, pygame.Color("Green"), (90, 90), 10)
            if game.waits[self.name] == 0:
                pygame.draw.circle(sc, pygame.Color("Grey"), (90, 90), 10)
        sc.blit(text_hp, (cords_x, cords_y))


# Класс отвечающий за карты противника
class EnemyCard(Card):
    def __init__(self, group, cords_x, cords_y, name, screen, team):
        super().__init__(group, cords_x, cords_y, name, screen, team)
        self.rect = self.image.get_rect()
        self.rect.x = cords_x
        self.rect.y = cords_y
        enemy_objects[self.type2] = enemy_objects[self.type2] + [name]
        self.index = len(enemy_objects[self.type2])
        self.row = 1

    # Функция получения описания карты/действий с нею
    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if event.button == 3:
                self.give_description()
            if event.button == 1 and game.target:
                game.waits[game.name] = -1
                game.name = ""
                return "t", self
        return False, False

    # функция отвечающая за размещение карты
    def play(self, row, number, effect=0):
        game.score2 += self.health
        his_cards[self.type2] = his_cards[self.type2] + [self]
        self.play2()
        if row == 1:
            row3.add_name2((3, self.name), self, number)
        else:
            self.row = 2
            row4.add_name2((3, self.name), self, number)
        if "effect" in self.whatDo:
            if effect == 1:
                row1.effect = "frost"
                row1.len_effects = int(self.whatDo[-1])
            else:
                row2.effect = "frost"
                row2.len_effects = int(self.whatDo[-1])
        if "temple" in self.whatDo:
            game.temple = True
        if "damage" in self.whatDo and not "me" in self.whatDo:
            check = False
            target_card = ""
            if len(my_cards["target_hunter"]) != 0 and self.description[:18] == "Категория: Охотник":
                target_card = my_cards["target_hunter"][0]
                check = True
            elif len(my_cards["target_attack"]) != 0:
                target_card = my_cards["target_attack"][0]
                check = True
            elif len(my_cards["target_basic"]) != 0:
                target_card = my_cards["target_basic"][0]
                check = True
            if check:
                if self.name[:-1] == "poison_steel":
                    target_card.regeneration = False
                if self.name[:-1] == "hunter" and target_card.description[:19] == "Категория: Чудовище":
                    self.whatDo[-1] = -6
                target_card.set_hp(int(self.whatDo[-1]))
                target_card.die()
        enemy_objects[self.type2].__delitem__(0)
        if "flock" in self.whatDo and game.n:
            game.n = False
            ai()

    # Функция отвечающая за смерть карты
    def die(self):
        if self.health <= 0:
            if game.temple:
                game.temple = False
            if "regeneration" in self.whatDo:
                n = his_cards["flock"]
                for i in range(len(n)):
                    if n[i].name == self.name:
                        n.__delitem__(i)
                        his_cards["flock"] = n
                        break
            self.kill()

    # Перемещение карты
    def move(self, cords_x, cords_y):
        self.rect.x = cords_x
        self.rect.y = cords_y


# Класс карты игрока, пока та находится у него в руке
class CardInHand(Card):
    def __init__(self, group, cords_x, cords_y, name, screen, team):
        super().__init__(group, cords_x, cords_y, name, screen, team)
        self.rect = self.image.get_rect()
        self.rect.x = cords_x
        self.rect.y = cords_y
        self.old_x = cords_x
        self.old_y = cords_y
        self.loot = False
        self.x_touch = 0
        self.y_touch = 0
        if len(name) > 2:
            self.name = name
        else:
            self.name = name[0]

    # Возможность перетаскивать карту мышкой, чтобы разместить её
    def update(self, *args):
        if game.n or self in doubles:
            if args and args[0].type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                    self.rect.collidepoint(args[0].pos):
                x1, y1 = event.pos
                if self.rect.x <= x1 <= self.rect.x + 100 and self.rect.y <= y1 <= self.rect.y + 100:
                    self.x_touch, self.y_touch = x1 - self.rect.x, y1 - self.rect.y
                    self.loot = True
            if args and args[0].type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.loot:
                    self.loot = False
                    x_rect, y_rect = event.pos
                    if 400 <= y_rect < 600:
                        return 1, self.name, x_rect
                    if 600 <= y_rect <= 800:
                        return 2, self.name, x_rect
                    if 200 <= y_rect < 400 and "row" in self.whatDo:
                        game.target_num = self.whatDo[-1]
                        return 3, self.name, x_rect

                    else:
                        self.rect.x = self.old_x
                        self.rect.y = self.old_y
            if self.loot and args[0].type == pygame.MOUSEMOTION:
                cords_x, cords_y = event.pos
                self.rect.x = cords_x
                self.rect.y = cords_y
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and event.button == 3 and \
                self.rect.collidepoint(args[0].pos):
            self.give_description()
            print(self.name)
        return False, False

    def die(self):
        self.kill()

    def move(self, cords_x, cords_y):
        self.rect.x = cords_x
        self.rect.y = cords_y


# Класс игрового ряда
class Row1:
    def __init__(self):
        self.len_effects = 0
        self.names = {"-4": "", "-3": "", "-2": "", "-1": "", "0": "", "1": "", "2": "", "3": "", "4": ""}
        self.names_c = []
        self.names_r = []
        self.names_l = []
        self.obj = {}
        self.total = 0
        self.effect = ""
        self.update()

    # Отрисовка всех карт в ряду
    def update(self):
        self.fix()
        if self.effect == "frost":
            draw_effect()
        cords_x = 10
        self.total = 0
        if self.len_effects <= 0:
            self.effect = ""
        for i in self.names:
            if self.names[i] != "":
                self.total += 1
                card = self.obj[self.names[i][1]]
                card.move(cords_x, card.rect.y)
                hp = card.health
                card.draw_picture(hp, card.image)
            cords_x += 110
        card_sprites.draw(screen)

    # Добавление карты в ряд
    def add_name(self, info, card):
        index = 0
        if self.names["0"] == "":
            self.names["0"] = (1, info[1])
            self.obj[info[1]] = card
        else:
            if 400 <= info[2]:
                self.names_r.append((info[2], info[1]))
                self.obj[info[1]] = card
                a = dict(self.names_r)
                a = sorted(a.items(), key=lambda x: x[0])
                self.names_r = a
                number = 1
                for i in range(len(self.names_r)):
                    if self.names["0"] != self.names_r[i]:
                        self.names[str(number)] = self.names_r[i]
                    number += 1
            else:
                self.names_l.append((info[2], info[1]))
                self.obj[info[1]] = card
                a = dict(self.names_l)
                a = sorted(a.items(), key=lambda x: x[0])
                a.reverse()
                self.names_l = a
                number = -1
                for i in range(len(self.names_l)):
                    self.names[str(number)] = self.names_l[i]
                    number -= 1
            index = number
        card.set_pos(index)

    # Делает так, чтобы карты в ряду стояли упорядночно(на равном расстоянии друг от друга)
    def fix(self):
        number = -4
        for i in range(8):
            if number != 0:
                if number < 0:

                    if self.names[str(number)] != "" and self.names[str(number + 1)] == "":
                        self.names[str(number + 1)] = self.names[str(number)]
                        self.names[str(number)] = ""
                if number > 0:
                    if self.names[str(number)] != "" and self.names[str(number - 1)] == "":
                        self.names[str(number - 1)] = self.names[str(number)]
                        self.names[str(number)] = ""
            number += 1


def draw_effect():
    if row1.effect == "frost":
        pygame.font.init()
        font = pygame.font.Font(None, 50)
        frost_len = font.render(str(row1.len_effects), True, pygame.Color("White"))
        cords_x = 1020
        cords_y = 500
        screen.blit(frost_len, (cords_x, cords_y))
    elif row2.effect == "frost":
        pygame.font.init()
        font2 = pygame.font.Font(None, 50)
        frost_len = font2.render(str(row2.len_effects), True, pygame.Color("White"))
        cords_x = 1020
        cords_y = 700
        screen.blit(frost_len, (cords_x, cords_y))


# Тоже класс ряда, но для противника(функции те же самые с небольшими изменениями)
class EnemyRow(Row1):
    def __init__(self):
        super().__init__()

    def add_name2(self, info, card_e, number):
        self.names[str(number)] = info[1]
        self.obj[info[1]] = card_e

    def give(self):
        return self.names

    def update(self):
        self.fix()
        cords_x = 10
        for i in self.names:
            if self.names[i] != "":
                card_e = self.obj[self.names[i]]
                if card_e.row == 1:
                    card_e.move(cords_x, 250)
                else:
                    card_e.move(cords_x, 50)
                number = card_e.health
                card_e.draw_picture(number, card_e.image)
            cords_x += 110
        card_sprites.draw(screen)


# Класс разыгранной карты игрока
class CardOnRow(Card):
    def __init__(self, group, cords_x, cords_y, name, screen, team):
        super().__init__(group, cords_x, cords_y, name, screen, team)
        self.rect = self.image.get_rect()
        self.rect.x = cords_x
        self.rect.y = cords_y
        my_cards[self.type1] = my_cards[self.type1] + [self]
        check = True
        if "regeneration" in self.whatDo:
            if "flock" in self.whatDo:
                vampires["flock"] = vampires["flock"] + [self]
                if game.n:
                    game.n = False
                    check = False
                    doubles[0].move(1000, 800)
                    doubles[0].old_y, doubles[0].old_x = 800, 1000
                else:
                    doubles.__delitem__(0)
            else:
                vampires["vampire"] = vampires["vampire"] + [self]
        self.index = len(my_cards[self.type1])
        self.pos = 0
        game.score1 += self.health
        self.play2()
        if self.whatDo[0] == "damage":
            if game.score2 > 0:
                game.target = True
                game.target_num = self.whatDo[-1]
                if self.name[:-1] == "hunter":
                    game.effect = "hunter"
                elif self.name[:-1] == "poison_steel":
                    game.effect = "poison"
            else:
                game.can_move = True
                game.played = False
        elif "wait" in self.whatDo:
            print(self.name)
            if "zeal" in self.whatDo:
                game.waits[self.name] = 1
            else:
                game.waits[self.name] = 0
            if "preparation" in self.whatDo:
                print(self.rect.y)
                if self.rect.y == 450:
                    game.waits[self.name] = 1
                else:
                    self.set_hp(1)
            game.can_move = True
            if "replay" in self.whatDo:
                replays.append(self)
        if check and game.target == False:
            game.n = False
            game.can_move = True
            game.played = False

    # Устанавливает описание карты/задействует способность приказ/возвращает данные карты
    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and event.button == 3 and \
                self.rect.collidepoint(args[0].pos):
            self.give_description()
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                self.rect.collidepoint(args[0].pos):
            if self.whatDo[0] == "wait" and game.target == False:
                if game.waits[self.name] == 1:
                    game.target = True
                    game.target_num = self.whatDo[-1]
                    if "inspiration" in self.whatDo:
                        if self.health > self.old_health:
                            game.target_num = self.whatDo[-1]
                        else:
                            game.target_num = self.whatDo[-2]

                    game.name = self.name
            print("k")
            if game.target:
                print(game.name)
                game.waits[game.name] = -1
                game.name = ""

                return "t", self
        return False, False

    # Перемещение карты
    def move(self, cords_x, cords_y):
        self.rect.x = cords_x
        self.rect.y = cords_y

    def die(self):
        if self.health <= 0:
            print("die")
            types = []
            for i in range(len(my_cards[self.type1])):
                if i != self.index - 1:
                    types.append(my_cards[self.type1][i])
            my_cards[self.type1] = types
            if "regeneration" in self.whatDo:
                number = vampires["flock"]
                for i in range(len(number)):
                    if number[i].name == self.name:
                        number.__delitem__(i)
                        vampires["flock"] = number
            row1.names[str(self.pos)] = ""
            self.kill()

    # Смена позиции карты в ряду
    def set_pos(self, index):
        self.pos = index

    # Есть карты у которых способность приказ востанавливается, это функция отвечает за это
    def replay(self):
        if "knight" in self.whatDo:
            if self.armor > 0:
                print("knight")
                game.waits[self.name] = 1
        if "healer" in self.whatDo:
            game.waits[self.name] = 1


# Класс отвечающий за создание спрайтов колод и набор карт в руку игрока
class Deck(pygame.sprite.Sprite):
    def __init__(self, group, name, scale, x, y, deck):
        super().__init__(group)
        self.deck = deck
        self.image = pygame.image.load("data/" + name)
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs):
        if args and self.rect.collidepoint(args[0].pos):
            card = self.random_card()
            if card != False:
                decks1.append(card)
                give_cards()
            print(decks1)
            print(deck_king)

    def random_card(self):
        if len(self.deck) > 1:
            number = random.randrange(0, len(self.deck) - 1, 1)
            card = self.deck[number]
            self.deck.__delitem__(number)
            return card
        elif len(self.deck) != 0:
            card = self.deck[0]
            self.deck.__delitem__(0)
            return card
        else:
            return False


# Выдача карт игроку
def give_cards():
    cords_x = 10
    cords_y = 820
    for i in decks1:
        if not i in old_names:
            old_names.append(i)
            if len(i) <= 2:
                card_h = CardInHand(all_sprites, 1, -120, i[1], screen, 1)
                doubles.append(card_h)
                CardInHand(all_sprites, cords_x, cords_y, i[0], screen, 1)
            else:
                CardInHand(all_sprites, cords_x, cords_y, i, screen, 1)
        cords_x += 100


# Выдача карт противнику
def give_cards2():
    card = 0
    for i in range(8):
        if len(decks2_choose) > 1:
            number = random.randrange(0, len(decks2_choose) - 1, 1)
            card = decks2_choose[number]
            decks2_choose.__delitem__(number)
        elif len(decks2_choose) != 0:
            card = decks2_choose[0]
            decks2_choose.__delitem__(0)
        if len(card) == 2:
            decks2.append(card[0])
            decks2.append(card[1])
        else:
            decks2.append(card)
        if len(decks2) == 8:
            break


if __name__ == '__main__':
    target = False
    game = Game()
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption("Поле")
    running = True
    x, y = 1500, 1000
    num = 0
    size = width, height = x, y
    screen = pygame.display.set_mode(size)
    row1 = Row1()
    row2 = Row1()
    row3 = EnemyRow()
    row4 = EnemyRow()
    BackFon(back_sprites, "info.png", (500, 300), 1000, 700)
    BackFon(back_sprites, "hand.png", (1000, 400), 0, 800)
    BackFon(back_sprites, "table2.png", (1500, 800), 0, 0)
    BackFon(back_sprites, "wait.png", (200, 200), 1200, 200)
    Deck(deck_sprites, "deck_king.png", (200, 200), 200, 600, deck_king)
    Deck(deck_sprites, "monsters.png", (200, 200), 500, 600, deck_monsters)
    Deck(deck_sprites, "deck_hunters.png", (200, 200), 800, 600, deck_hunter)
    give_cards2()
    y = -100
    x = 10
    for i0 in decks2:
        ob = EnemyCard(card_sprites, x, y, i0, screen, 2)
        enemy_cards[i0] = ob
        x += 100
    while running:
        draw_info(game.text, screen)
        if game.choose:  # Отрисовка спрайтов на этапе набора карт
            pygame.font.init()
            font7 = pygame.font.Font(None, 50)
            text = font7.render("ГВИНТ2.0", True, (100, 255, 100))
            text_x = 600
            text_y = 150
            screen.blit(text, (text_x, text_y))
            deck_sprites.draw(screen)
        else:  # Отрисовка карт на эатпе самой игры
            back_sprites.draw(screen)
            draw_score(game.score1, screen)
            draw_score2(game.score2, screen)
            draw_info(game.text, screen)
            row1.update()
            row2.update()
            row3.update()
            row4.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for i1 in all_sprites:
                    i1.update(event)
            if game.choose:
                # Взятие карты в руку
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i2 in deck_sprites:
                        i2.update(event)
                        if len(decks1) == 8:
                            give_cards()
                            game.choose = False
            elif game.player_move:  # Если сейчас ход игрока
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP \
                        or event.type == pygame.MOUSEMOTION:
                    # Размещение карты
                    for i3 in all_sprites:
                        information = i3.update(event)
                        if 1 in information and game.played:
                            i3.kill()
                            n = information[2]
                            ob = CardOnRow(card_sprites, information[2], 450, information[1], screen, 1)
                            row1.add_name(information, ob)
                            row1.update()
                        if 2 in information and game.played:
                            i3.kill()
                            ob = CardOnRow(card_sprites, information[2], 650, information[1], screen, 1)
                            row2.add_name(information, ob)
                            row2.update()
                        if 3 in information and game.played:
                            i3.kill()
                            x = []
                            for i4 in row3.names:
                                if row3.names[i4] != "":
                                    obj = row3.obj[row3.names[i4]]
                                    x.append(obj)
                            game.do(x)
                            game.played = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # Завершение хода или задействование способности приказ
                    if 1200 < x <= 1400 and 200 < y <= 400:
                        if game.can_move:
                            game.can_move = False
                            game.set()
                    if event.button == 1 and game.target:
                        for i5 in card_sprites:
                            information = i5.update(event)
                            if information[0] == "t":
                                game.do([information[1]])
                    else:
                        for i6 in card_sprites:
                            information = i6.update(event)
            else:
                # Если ход противника
                ai()
                game.set()
        all_sprites.draw(screen)
        game.end()
        pygame.display.update()
        screen.fill((0, 0, 0))
        clock.tick(60)
pygame.quit()
