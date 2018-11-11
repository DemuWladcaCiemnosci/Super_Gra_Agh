﻿# -*- coding: utf-8 -*-
import os
import random
import time
import Addons
import Code
from Items import Weapon
from Items import Armor
import pickle


class Player:
    def __init__(self):
        self.exp = 0
        self.lvl = 1
        self.max_hp = 100
        self.hp = self.max_hp
        self.weapon = []
        self.armor = []
        self.available_weapons = []
        self.available_attack_names = []
        self.available_armors = []

    def attack(self, enemy_name, senemy_hp):
        enemy_hp = senemy_hp

        while True:
            time.sleep(0.05)
            p = -1
            while not (0 <= p < len(self.weapon)):
                os.system('cls')
                print("-" * 20)
                Addons.slow_print("Hp Gracza: " + str(self.hp) + "\nHp przeciwnika: " + str(enemy_hp), 0.005)

                for x in range(0, len(self.weapon)):
                    print("%s. %s   (dmg %s-%s, chance %s%%, crit %s%%)" % (
                        x + 1, self.weapon[x].attack_name, self.weapon[x].dmg - 10, self.weapon[x].dmg + 10, self.weapon[x].chance,
                        self.weapon[x].crit))

                print("\nPodaj numer ataku")
                p = input(">>>")

                try:
                    p = int(p)
                    p -= 1
                except ValueError:
                    p = -1

            print("...")
            if random.randint(0, 100) < self.weapon[p].chance:
                if random.randint(1, 100) > self.weapon[p].crit:
                    tmp = self.weapon[p].dmg + random.randint(-10, 10)
                else:
                    print("Obrażenia krytyczne!")
                    tmp = (self.weapon[p].dmg + random.randint(-10, 10))*2
                enemy_hp -= tmp
                Addons.slow_print("Trafiłeś za " + str(tmp), 0.01)

            else:
                print("\nChybiłeś :(")

            if enemy_hp <= 0:
                tmp = random.randint(int(senemy_hp * (self.lvl / 10 + 1)) - 20, int(senemy_hp * (self.lvl / 10 + 1)))
                Addons.slow_print("Wygrałeś!", 0.01)
                self.update_lvl(tmp)
                break

            tmp = int(random.randint(10, 25) * ((self.lvl / 6) + 1))
            Addons.slow_print(enemy_name + " atakuje Cię!", 0.01)
            self.update_hp(tmp)

            input("\n\nWciśnij ENTER, aby kontynuować...")

    def update_lvl(self, value):
        time.sleep(0.05)
        levelup = False
        old_max_hp = self.max_hp

        self.exp += value
        Addons.slow_print("Dostałeś " + str(value) + " exp", 0.005)

        while self.exp >= self.lvl * 100:
            self.exp -= self.lvl * 100
            self.lvl += 1
            self.max_hp += 10
            levelup = True

        if levelup:
            print("*" * 20)
            Addons.slow_print("Nowy poziom!\nTwój poziom: " + str(self.lvl) + "\nJesteś w pełni wyleczony."
                            "\nTwój maksymalny poziom hp został zwiększony o " +
                            str(self.max_hp - old_max_hp) + "\n", 0.005)
            self.hp = self.max_hp
        else:
            Addons.slow_print("Brakuje Ci " + str(self.lvl * 100 - self.exp) + " exp do nowego poziomu", 0.005)

    def update_hp(self, value):
        time.sleep(0.05)

        # redukcja obrazen
        dmg_reduction = 0
        for x in self.armor:
            dmg_reduction += x.armor
        value = int(value * (100 - dmg_reduction) / 100)

        self.hp -= value
        if self.hp <= 0:
            Addons.slow_print("Tracisz " + str(value) + " hp", 0.005)
            print("[*] RIP [*]")
            Addons.print_gameover()
            self.save_score()
            input("\nWciśnij ENTER, aby kontunuować...")
            exit(0)

        elif value > 0:
            Addons.slow_print("Tracisz %s hp, pozostało Ci %s/%s hp." % (value, self.hp, self.max_hp), 0.005)
        else:
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            Addons.slow_print("Zostajesz uleczony o %s hp, masz %s/%s hp." % (abs(value), self.hp, self.max_hp), 0.005)

    def add_armor(self, name, armor):
        self.armor.append(Armor(name, armor))

    def add_weapon(self, name, dmg, chance, crit, attack_name):
        self.weapon.append(Weapon(name, dmg, chance, crit, attack_name))

    def add_random_weapon(self):
        if len(self.available_weapons) > 0:
            index = random.randint(0, len(self.available_weapons) - 1)
            name = self.available_weapons.pop(index)
            dmg = random.randint(self.lvl + 2, self.lvl + 6) * 10
            chance = random.randint(40, 90)
            crit = random.randint(self.lvl + 1, self.lvl + 10)
            attack_name = self.available_attack_names.pop(index)
            self.add_weapon(name, dmg, chance, crit, attack_name)
            Addons.slow_print("Otrzymujesz przedmiot: %s (dmg %s-%s, chance %s%%, crit %s%%)" % (name, dmg - 10, dmg + 10, chance, crit), 0.005)

    def add_random_armor(self):
        if len(self.available_weapons) > 0:
            name = self.available_armors.pop(random.randint(0, len(self.available_armors) - 1))
            armor = random.randint(1, 2) * 5
            self.add_armor(name, armor)
            Addons.slow_print("Otrzymujesz przedmiot: %s (redukcja obrażeń %s%%)" % (name, armor), 0.005)

    def load_names(self, count):
        with open("weapon.txt", encoding='utf-8') as f:
            lines = []
            tmp = 1
            for i, line in enumerate(f):
                if "..." in line:
                    tmp += 1
                if tmp > count:
                    break

                if tmp > count - 1 and "..." not in line:
                    lines.append(line.replace("\n", ""))

            for i in range(0, len(lines) - 1, 3):
                self.available_weapons.append(lines[i])
                self.available_attack_names.append(lines[i + 1])
                self.available_armors.append(lines[i + 2])
        f.close()

    def show_equipment(self):
        os.system('cls')
        print("-" * 20)
        for x in range(1, len(self.weapon)):
            print("%s. %s   (dmg %s-%s, chance %s%%, crit %s%%)" % (
                x, self.weapon[x].name, self.weapon[x].dmg - 10, self.weapon[x].dmg + 10, self.weapon[x].chance, self.weapon[x].crit))

        for x in range(0, len(self.armor)):
            print("%s. %s   (redukcja obrażeń %s%%)" % (len(self.weapon) + x, self.armor[x].name, self.armor[x].armor))

        print("\n" + str(len(self.weapon) + len(self.armor)) + ". Kartka z zapisanym kodem: " + Code.return_known_code())
        input("\n\nWciśnij ENTER, aby kontunuować...")

    def save_score(self):
        score = self.exp
        for i in range(self.lvl + 1):
            score += i * 100
        score -= 100

        score += (len(self.weapon) - 2) * 50 + (len(self.armor) - 1) * 50
        print("\nZdobyłeś %s punktów!\n" % score)
