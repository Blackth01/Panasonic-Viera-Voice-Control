#coding: utf-8
from time import sleep
from flask import render_template, request, jsonify
from app import app
import panasonic_viera
import unidecode
import collections

def arrow_keys(command):
    global rc
    print(command)
    if(command[0:9] == "seleciona"):
        rc.send_key(panasonic_viera.Keys.enter)
        sleep(0.5)
    elif(command[0:4] == "cima"):
        rc.send_key(panasonic_viera.Keys.up)
        sleep(0.5)
    elif(command[0:5] == "baixo"):
        rc.send_key(panasonic_viera.Keys.down)
        sleep(0.5)
    elif(command[0:7] == "esquerd"):
        rc.send_key(panasonic_viera.Keys.left)
        sleep(0.5)
    elif(command[0:6] == "direit"):
        rc.send_key(panasonic_viera.Keys.right)
        sleep(0.5)

def bfs(grid, start, goal, wall):
    global width, height
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return [path, directions(path)]
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != wall and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def directions(path):
    result = []
    index = 1
    max_index = len(path)
    if(max_index == 1):
       result.append("selecionar")
       return result
    while(index < max_index):
        before = path[index-1]
        after = path[index]
        if(before[0] == after[0]):
            if(before[1] > after[1]):
                result.append("cima")
            else:
                result.append("baixo")
        else:
            if(before[0] > after[0]):
                result.append("esquerda")
            else:
                result.append("direita")
        index+=1
    return result

def escrever(word):
    global width, height
    width, height = 6, 7
    grid = ["#$####",
            "abcdef",
            "ghijkl",
            "mnopqr",
            "stuvwx",
            "yz1234",
            "567890"]
    wall = "#"
    words = word.split(" ")

    index = 0

    last_c = (0,1)
    for w in words:
        if(index != 0):
            goal = "$"
            res = bfs(grid, last_c, goal, wall)
            if(res[1][-1] != "selecionar"):
                res[1].append("selecionar")
            print(' '.join(res[1]))
            for c in res[1]:
                arrow_keys(c)
            last_c = res[0][-1]
        for l in w:
            goal = l
            res = bfs(grid, last_c, goal, wall)
            if(res[1][-1] != "selecionar"):
                res[1].append("selecionar")
            print(' '.join(res[1]))
            for c in res[1]:
                arrow_keys(c)
            last_c = res[0][-1]
        index += 1

@app.before_first_request
def connect_tv():
    global rc
    rc = panasonic_viera.RemoteControl("TV_IP", app_id="APP_ID", encryption_key="ENC_KEY")
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form.get('command')
    print(command)
    if(command == "aplicativos" or command == "aplicativo"):
        rc.send_key(panasonic_viera.Keys.apps)
    elif(command[0:8] == "escrever"):
        command = unidecode.unidecode(command)
        command = command.split(" ")
        command.pop(0)
        command = " ".join(command)
        print("vai escrever: %s" % command)
        escrever(command)
    elif(command == "voltar"):
        rc.send_key(panasonic_viera.Keys.return_key)
    elif(command == "pausar"):
        rc.send_key(panasonic_viera.Keys.pause)
    elif(command[0:9] == "seleciona"):
        #rc.send_key(panasonic_viera.Keys.enter)
        commands = command.split(" ")
        for c in commands:
            arrow_keys(c)
    elif(command[0:4] == "cima"):
        #rc.send_key(panasonic_viera.Keys.up)
        commands = command.split(" ")
        for c in commands:
            arrow_keys(c)
    elif(command[0:5] == "baixo"):
        #rc.send_key(panasonic_viera.Keys.down)
        commands = command.split(" ")
        for c in commands:
            arrow_keys(c)
    elif(command[0:7] == "esquerd"):
        #rc.send_key(panasonic_viera.Keys.left)
        commands = command.split(" ")
        for c in commands:
            arrow_keys(c)
    elif(command[0:6] == "direit"):
        #rc.send_key(panasonic_viera.Keys.right)
        commands = command.split(" ")
        for c in commands:
            arrow_keys(c)
    elif(command == "sair"):
        rc.send_key(panasonic_viera.Keys.exit)
    elif(command == "netflix"):
        rc.launch_app("0010000200180011")
    elif(command == "prime"):
        rc.launch_app("0010000100180011")
    elif(command == "youtube"):
        rc.launch_app("0070000200180011")
    elif(command == "aumentar volume"):
        volume = rc.get_volume()
        rc.set_volume(volume + 10)
    elif(command == "diminuir volume" or command == "baixar volume"):
        volume = rc.get_volume()
        rc.set_volume(volume - 10)
    elif(command[0:6] == "volume"):
        value = command.split(" ")[1]
        try:
            value = int(value)
            rc.set_volume(value)
        except:
            print('Erro ao setar volume!')
    return jsonify({'msg':'Sucesso!'})
