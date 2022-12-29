import requests

utenti = []
nomi = []
nomi2 = []

class Info:
    def __init__(self, username):
        self.username = username
        line = users.readline()
        self.tasks = {}

        while line!= "end\n" and line!="\n":
            key = ""
            sec = ""
            i =0
            while (line[i]!="@"):
                key += line[i]
                i+=1
            i+=2
            while i<len(line)-1:
                sec += line[i]
                i+=1

            self.tasks[key] = sec
            line = users.readline()

def rawdata():
    url = 'https://training.olinfo.it/api/user'
    global res
    res = requests.post(url, json ={"action":"get", "username":user})
    res = res.json()
    if(res["success"]==0):
        print("utente non trovato")

def cleandata():
    users.write(f'{user}\n')

    for task in res["scores"]:
        users.write(f'{task["title"]}@ {task["score"]} \n')

    users.write("end\n")

def checknew():
    print("l'utente è gia presente, ecco i nuovi problemi che ha risolto:")
    for item in utenti:
        if item.username == (user+"\n"):
            for task in res["scores"]:
              #  print(item.tasks)
                if not(task["title"] in item.tasks):
                    print(f'{task["title"]} points: {task["score"]}')
                elif int(item.tasks[task["title"]]) != task["score"]:
                    print(f'new score in task {task["title"]}, {task["score"]} points!')
            break
    print("vuoi vedere altro? (tutti, parziali, no)")
    risposta = input()
    if risposta == "tutti":
        for task in res["scores"]:
            print(f'{task["title"]}, {task["score"]} points!')
    elif risposta == "parziali":
        for task in res["scores"]:
            if task["score"] != 100:
                print(f'{task["title"]}, {task["score"]} points!')

def printdata():
    print("utente nuovo, vuoi vedere i task risolti per ora? (si, parziali, no)")
    risposta = input()
    if risposta=="si":
        for task in res["scores"]:
            print(f'{task["title"]}, {task["score"]} points!')
    elif risposta=="parziali":
        for task in res["scores"]:
            if task["score"]!=100:
                print(f'{task["title"]}, {task["score"]} points')
    return

def ispresent():
    if (user+"\n") in nomi:
        checknew()
    else:
        printdata()
    cleandata()

def main():
    global users
    users = open("utenti.txt", "r")

    nome = users.readline()
    while nome:
        utenti.append(Info(nome))
        nomi.append(nome)
        nome = users.readline()

    users = open("utenti.txt", "w")

    global user
    while 1:
        user = input("inserisci il nome utente oppure fine\n")
        if(user == "fine"):
            break

        nomi2.append(user)
        rawdata()
        if res["success"] != 0:
            ispresent()

    for item in utenti:
        if not(item.username[:-1] in nomi2):
            users.write(f'{item.username}')
            for task in item.tasks:
                users.write(f'{task}@ {item.tasks[task]} \n')
            users.write("end\n")

main()
