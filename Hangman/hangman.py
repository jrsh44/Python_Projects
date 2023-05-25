import sys
import json
import time
import random

##########################################################

def show_menu():
    print("---------------------")
    print("1. New Game")
    print("2. Continue")
    print("3. Change difficulty level. Now: "+diff)
    print("4. Score")
    print("5. Quit")
    print("----------------------")


def start_new_game():
    global points, password_num, password, user_life
    points=0
    user_life=life
    password_num.clear()
    used_nums.clear()
    for i in range(0,len(password)):
        password_num.append(i)
    continue_game()


def continue_game():
    global points, password_num, password, life, user_life
    if user_life == 0:
        print("YOU LOST")
        print("Check your score or start the new game")
    else:
        if len(used_nums) == len(password):
            print("Solved all words!!\nCheck your score or start the new game!") 
        else:
            if len(password_num) ==0:
                print("You haven't started yet")
            else:
                user_life = life
                user_word=[]
                used_letters=set()
                num_choosen = random.choice(password_num)
                password_num.remove(num_choosen)
                used_nums.append(num_choosen)
                word = password[num_choosen]["password"]
                start_time=time.time()

                for _ in word:
                    user_word.append("_")
                
                while True:
                    condition=0
                    letter=input("Enter a letter: ")
                    if not(letter.isalpha()):
                        print("Enter a letter from the English alphabet.")
                        continue
                    else: pass
                    if len(letter) >1:
                        print("Please enter up to one letter")
                        continue
                    for i in used_letters:
                        if i == letter:
                            print("This letter has already been given")
                            condition=1
                        else: pass
                    used_letters.add(letter)
                    if condition ==0:
                        found_index = find_indexes(word, letter)
                        if len(found_index) == 0:
                            print("There is no such letter!")
                            user_life-=1
                            if user_life==0:
                                show_state_of_the_game(user_word, used_letters, user_life)
                                print("-YOU LOST-")
                                print("Check your score or start the new game")
                                break
                            else:pass
                        else:
                            for index in found_index:
                                user_word[index] = letter
                            if "".join(user_word) == word:
                                points+=len(word)*multiplier*8-round(time.time()-start_time)
                                print("Congrats, you guessed the password!!")
                                print("Letters used:",used_letters)
                                print("For the password:",word,"you get",str(len(word)*multiplier*8-round(time.time()-start_time)),"points!")
                                print("Took", round(time.time()-start_time), "seconds.")
                                break
                            else: pass
                    show_state_of_the_game(user_word, used_letters, user_life)
                        
def show_state_of_the_game(user_word, used_letters, user_life):
    print()
    print(user_word)
    print("Number of remaining attempts: ", user_life)
    print("Letters used:",used_letters)
    print()
    

def find_indexes(word, letter):
    indexes = []
    for index, letter_in_word in enumerate(word):
        if letter == letter_in_word:
            indexes.append(index)
    return indexes


def change_difficulty():
    global diff, life, multiplier
    while True:
        print()
        print("Choose a difficulty level:")
        print("1. Easy - 15 zyc")
        print("2. Medium - 10 zyc")
        print("3. Hard - 5 zycia")
        user_num = input("Choice [1, 2, 3]: ")
        if user_num == "1":
            print("You have chosen a level - Easy")
            diff="Easy"
            multiplier = 1
            life = 15
            break
        elif user_num == "2":
            print("You have chosen a level - Medium")
            diff="Medium"
            multiplier = 2
            life = 10
            break
        elif user_num == "3":
            print("You have chosen a level - Hard")
            diff="Hard"
            multiplier = 4
            life = 5
            break
        else:
            print("Select a number from the range [1-3]\n---------")


def show_score():
    global points,password_num,used_nums
    print()
    print("===================")
    if len(password_num) ==0 and len(used_nums) == 0:
        print("You haven't guessed any password yet.")
    else:
        print("During this game, they scored",points,"points!")
    print("===================")


def exit():
    global time0
    print()
    print("Thank you for playing!")
    print("Total time spent in the app is",round(time.time()-time0),"seconds.")
    sys.exit(0)


################################################################

with open("Hangman\\passwords.json") as json_file:
    password=json.load(json_file)

time0=time.time()
multiplier = 2
diff="Medium"
user_life = life = 10
points = 0
password_num=[]
used_nums=[]

print("\n=====================================")
print("=========== H A N G M A N ===========")
print("=====================================\n")

while True:
    show_menu()
    menu_number = input("Choose action [1, 2, 3, 4, 5]: ")
    if menu_number == "1":
        start_new_game()
    elif menu_number == "2":
        continue_game()
    elif menu_number == "3":
        change_difficulty()
    elif menu_number == "4":
        show_score()
    elif menu_number == "5":
        exit()
    else:
        print("Select a number from the range [1-5].")
    print()
