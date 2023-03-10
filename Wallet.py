import csv
import os
import datetime
import logging
import matplotlib.pyplot as plt

file_name=""


#Ostavljam klase kako biste videli ideju, koja nije realizovana, nazalost.

class Novcanik:
    def __init__(self,  username: str, kolicina_novca: int): 
        self.username = username
        self.kolicina_novca = kolicina_novca
    def get_username_novcanika(self):
        return self.username
    def get_kolicina_novca(self):
        return self.kolicina_novca
    def __str__(self):
        return f'{self.username}: {self.kolicina_novca}'
    def menjanje_novca(self, broj: int):
        self.kolicina_novca += broj      

def novcanici_niz(file_path):
    novcanici = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            username = row[0]
            kolicina_novca = int(row[1])
            novcanik = Novcanik(username, kolicina_novca)
            novcanici.append(novcanik)
    return novcanici

def pronadji_novcanik(ime_novcanika, novcanici):
    for i in range(len(novcanici)):
        if novcanici[i].get_username_novcanika() == ime_novcanika:
            return i
    return None

def trazenje_iznosa_u_novcaniku(username):
    put_za_novcanike = os.path.join(os.path.dirname(__file__), 'novcanici.csv')
    novcanici = novcanici_niz(put_za_novcanike)
    broj = pronadji_novcanik(username, novcanici)
    string_novca_i_imena = str(novcanici[broj])
    iznos_string = string_novca_i_imena.split(":")[1]
    iznos = int(iznos_string.strip())
    return iznos

def promeni_novcanu_vrednost(username, new_amount):
    file_path = os.path.join(os.path.dirname(__file__), 'novcanici.csv')
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith(username):
            parts = line.split(',')
            parts[1] = ' ' + str(new_amount) + '\n'
            lines[i] = ','.join(parts)
            break
    with open(file_path, 'w') as f:
        f.writelines(lines)
"""
class Korisnik:
    def __init__(self, ime, sifra, novcanik: Novcanik):
        self.ime = ime
        self.sifra = sifra
        self.novcanik = novcanik
    def prikaz_novcanika(self):
        print(self.novcanik.provera_stanja_novcanika())
    def potrosi_novac(self, iznos: int):
        if self.novcanik.kolicina_novca >= iznos:
            self.novcanik.kolicina_novca -= iznos
            print(f"Potroseno {iznos} dinara.")
        else:
            print("Nemate dovoljno novca.")
 
    def uvrsti(self):
        global novcanici
        if self.ime in novcanici:
            self.novcanik = novcanici[self.ime]
        else:
            self.novcanik = Novcanik(0)
            novcanici[self.ime] = self.novcanik
"""   
def ispisivanje_fajla(file_name):
    with open(file_name, 'r') as f:
        print(f.read())

def login_ili_registracija():
    global file_name
    choice = input("Da li biste hteli da se u(L)ogujete ili (R)egistrujete? ").lower()
    while choice not in ["l", "r"]:
        choice = input("Nemoguc pokusaj. Molim vas unesite 'L' za login ili 'R' za registraciju: ").lower()
    if choice == "l":
        uloguj()
    elif choice == "r":
        registracija()

def registracija():
    global file_name
    file_name = os.path.join(os.path.dirname(__file__), 'korisnici.csv')
    username = input("Unesite ime: ")
    password = input("Unesite password: ")
    try:
        with open(file_name, 'a', newline='\n') as f:
            writer = csv.writer(f)
            writer.writerow([username, password])
        print("Registracija uspesna!")
    except Exception as e:
        logging.error(f"Dogodila se greska prilikom registracije: {e}")
    uloguj()

def uloguj():
    global file_name
    global novcanik
    file_name = os.path.join(os.path.dirname(__file__), 'korisnici.csv')
    with open(file_name, 'r') as csvfile:
        user_reader = csv.reader(csvfile)
        user_data = {rows[0]:rows[1] for rows in user_reader}
    global username 
    username = input("Upisi svoj username: ")
    password = input("Upisi password: ")
    if username in user_data.keys():
        if password == user_data[username]:
            print("Dobrodosao, ",username)
            headers = ["datum", "kolicina", "kategorija", "opis"]
            file_name = f"{username}_transakcije.csv"
            if not os.path.exists(file_name):
               with open(file_name, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
            main()
        else:
            print("Netacan password!")
    else:
        print("Korisnik nije pronadjen :(")

def transakcija():
    #trenutni_novcanik = Novcanik(username, trazenje_iznosa_u_novcaniku(username))
    while True:
        try:
            date = input("Unesite datum u formatu: dan-mesec-godina")
            date = datetime.datetime.strptime(date, "%d-%m-%Y")
            print()
            break
        except ValueError:
            print("Pogresno ste uneli datum, pokusajte ponovo: ")
    while True:
        try:
            quantity = int(input("Unesite kolicinu novca: "))
            nova_kolicina=trazenje_iznosa_u_novcaniku(username)+quantity
            #trenutni_novcanik(username, nova_kolicina)
            promeni_novcanu_vrednost(username, nova_kolicina)
            print()
            if quantity == 0:
                raise ValueError
            break
        except ValueError:
            print("Kolicina ne moze biti nula, pokusajte ponovo!")

    category = input("Unesite jednu od sledecih kategorija: hrana, slobodno vreme, prevoz, pokloni, ucenje")
    while category not in ["hrana", "slobodno vreme", "prevoz", "pokloni", "ucenje"]:
        print("Nemoguca kategorija, pokusajte ponovo!")
        category = input("Unesite kategoriju: ")
    description = input("Unesite opis: ")
    with open(file_name, 'a', newline='') as csvfile:
        transaction_writer = csv.writer(csvfile)
        transaction_writer.writerow([date.strftime("%d:%m:%Y"), quantity, category, description]) 

def ucitaj_transakcijske_podatke(file_path):
    transaction_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  
        for row in reader:
            date = row[0]
            amount = int(row[1])
            category = row[2]
            description = row[3]
            transaction = (date, amount, category, description)
            transaction_data.append(transaction)
    return transaction_data

def napravi_novcanik_graf():
    user_balances = {}
    with open('novcanici.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            username = row[0]
            balance = int(row[1])
            user_balances[username] = balance

    plt.bar(user_balances.keys(), user_balances.values())
    plt.xlabel('Korisnik')
    plt.ylabel('Stanje')
    plt.title('Stanja novcanika')
    plt.show()

def izracunaj_ustedu_i_potrosnju():
    file_name = os.path.join(os.path.dirname(__file__), f"{username}_transakcije.csv")
    transaction_data=ucitaj_transakcijske_podatke(file_name)

    while True:
        try:
            start_date_str = input("Unesite pocetni datum: (dd:mm:yyyy): ")
            end_date_str = input("unesite zavrsni datum: (dd:mm:yyyy): ")

            start_date = datetime.datetime.strptime(start_date_str, "%d:%m:%Y")
            end_date = datetime.datetime.strptime(end_date_str, "%d:%m:%Y")
            break
        except ValueError:
            print("Pogresno ste uneli datum, pokusajte ponovo: ")
    if start_date > end_date:
        print("Pocetni datum ne moze biti posle zavrsnog datuma.")
        return

    savings = 0
    expenses = 0

    for transaction in transaction_data:
        transaction_date = datetime.datetime.strptime(transaction[0], "%d:%m:%Y")
        if start_date <= transaction_date <= end_date:
            if transaction[1] > 0:
                savings += transaction[1]
            else:
                expenses += abs(transaction[1])    
    
    if savings == 0 and expenses == 0:
        print("Nista nije ustedjeno/potroseno")
    else:
        print(f"Ustedjeno: {savings} Potroseno: {expenses}")

def main():
    #trenutni_novcanik = Novcanik(username, trazenje_iznosa_u_novcaniku(username))
    print("Izaberite jednu od sledecih opcija: ")
    print("1, za unosenje novih transakcija")
    print("2, za racunanje ustedjevine")
    print("3, za pregled stanja u novcaniku")
    print("4, za ispisivanje svih transakcija")
    print("5, za pregled prosecne potrosnje u odnosu na kategoriju")
    print("6, za dodavanje ili izbacivanje novca iz novcanika")
    print("7, za pregled stanja u svim novcanicima")
    while True:
        try: 
            user_input = int(input("Unesite broj od 1 do 7: "))
            print()
            if not 1 <= user_input <= 7:
                raise ValueError
        except ValueError:
            print("Morate da unesete broj od 1 do 7!")
        else:
            if user_input == 1:              
                # unosenje novih transakcija
                print("Transakcije se ispisuju prema sablonu: datum, kolicina, kategorija, opis")
                print()
                transakcija()
                print("Uneli ste transakcije")
                print()
                
            elif user_input == 2:
                # za racunanje ustedjevine
                izracunaj_ustedu_i_potrosnju()
                print()

            elif user_input == 3:
                # za pregled stanja nu novcaniku
                put_za_novcanike = os.path.join(os.path.dirname(__file__), 'novcanici.csv')
                novcanici = novcanici_niz(put_za_novcanike)
                index_novcanika = pronadji_novcanik(username, novcanici)
                print(novcanici[index_novcanika])
                novcanici[index_novcanika]
                print()

            elif user_input == 4:
                # Ispisi transakcija(ispis fajla)
                ispisivanje_fajla(file_name)
                print()

            elif user_input == 5:
                # za pregled potrosnje u odnosu na kategoriju
                # inicijalizovanje recnika
                category_totals = {"hrana": 0, "slobodno vreme": 0, "prevoz": 0, "pokloni": 0, "ucenje": 0}
                category_counts = {"hrana": 0, "slobodno vreme": 0, "prevoz": 0, "pokloni": 0, "ucenje": 0}

                with open(file_name, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader) 
                    for row in reader:
                        category = row[2]
                        amount = int(row[1])
                        category_totals[category] += amount
                        category_counts[category] += 1

                for category in category_totals:
                    if(category_counts[category] == 0):
                        print(f"Ni jednom nije izvrsena uplata za kategoriju: {category}!")
                    else:
                        average = abs(category_totals[category]) / category_counts[category]
                        print(f"Prosecna potrosnja u kategoriji {category} je {average}")
                print()
            elif user_input == 6:
                # menjanje novca u novcaniku
                dodatna_kolicina = input("Unesite broj koji ubacujete/izbacujete (u odnosu na to da li je negativan ili pozitivan): ")
                nova_kolicina = trazenje_iznosa_u_novcaniku(username) + int(dodatna_kolicina) 
                promeni_novcanu_vrednost(username, nova_kolicina)    
                print()
            elif user_input == 7:
                #graf za stanje u novcanicima
                napravi_novcanik_graf()
                print()

            continue_program = input("Da li zelite da nastavite? (da/ne) ")
            if continue_program.lower() == 'ne':
                break
  

login_ili_registracija()
