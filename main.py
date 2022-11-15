import smtplib
import pandas as pd
import datetime as dt
from random import randint


# add birthdays
def add_birthdays():
    print("Let's add a person to the list")
    name = str(input("Name: ")).title()
    email = str(input("Email: ")).lower()
    birth_year = str(input("Year: "))
    birth_month = str(input("Month # (ie. 1 for January): "))
    birth_day = str(input("Day of month: "))

    data = pd.read_csv("birthdays.csv")
    data.loc[len(data.index)] = [name, email, birth_year, birth_month, birth_day]
    data.to_csv("birthdays.csv", index=False)
    print("\nCurrent List:\n", data)

    add = str(input("\nDo you want to add another? y/n ")).lower()
    if add == "y":
        add_birthdays()
    else:
        pass


# check if today is someone's birthday
def check_and_send():
    data = pd.read_csv("birthdays.csv")
    now = dt.datetime.now()
    month = now.month
    day = now.day
    for index, row in data.iterrows():
        if row.month == month and row.day == day:
            print(row["name"])
            rand_letter = (randint(1, 3))
            print(rand_letter)
            if rand_letter == 1:
                letter_path = "letter_templates/letter_1.txt"
            elif rand_letter == 2:
                letter_path = "letter_templates/letter_2.txt"
            elif rand_letter == 3:
                letter_path = "letter_templates/letter_3.txt"

            with open(file=letter_path, mode="r") as letter_text:
                letter = letter_text.read()
                edit = letter.replace("[NAME]", str(row['name']))
                with open(f"{row['name']}'s_letter.txt", mode="w") as final_letter:
                    final_letter.write(edit)

            with open(f"{row['name']}'s_letter.txt") as file:
                message = file.read()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
                    connection.login("kyrietest1@gmail.com", input("Password: "))
                    connection.sendmail(
                        from_addr="kyrietest1@gmail.com",
                        to_addrs=row["email"],
                        msg=f"Subject:Happy Birthday\n\n{message}"
                    )
                print("Email sent!")
        else:
            pass


# start program - recursive with escape route
def run_program():
    ask_user = int(input("\nChoose you options:\nAdd birthdays to list = 1\nCheck and send cards = 2\n"))
    if ask_user == 1:
        add_birthdays()
        run_program()
    elif ask_user == 2:
        check_and_send()
        run_program()
    elif ask_user == 0:
        return
    else:
        run_program()


run_program()
