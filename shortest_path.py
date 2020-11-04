import collections

grid = ["..........",
        "..*#...##.",
        "..##...#*.",
        ".....###..",
        "......*..."]
def bfs(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return [path, directions(path)]
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and (x2, y2) not in seen:
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
    

width, height = 6, 7
grid = ["#$##@#",
        "abcdef",
        "ghijkl",
        "mnopqr",
        "stuvwx",
        "yz1234",
        "567890"]

word = "aviao tu"

words = word.split(" ")

index = 0

last_c = (0,1)
for w in words:
    if(index != 0):
        goal = "$"
        res = bfs(grid, last_c)
        if(res[1][-1] != "selecionar"):
            res[1].append("selecionar")
        print(' '.join(res[1]))
        last_c = res[0][-1]
    for l in w:
        goal = l
        res = bfs(grid, last_c)
        if(res[1][-1] != "selecionar"):
            res[1].append("selecionar")
        print(' '.join(res[1]))
        last_c = res[0][-1]
    index += 1
