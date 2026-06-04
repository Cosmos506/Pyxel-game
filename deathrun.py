import pyxel

def update():
    global x,y, scroll_x, scroll_y, vy, on_ground, is_died, pers_x, pers_y, is_begin
    
    vy += 0.4 # gravity
    if ( pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y)) and on_ground and not is_died and not is_begin and not is_finish:
        vy = -5 # jump_force
        
    print(vy, on_ground)
    
    next_y = y + vy
    if angle_move(x, next_y, scroll_x) :
        y = next_y
        if vy < 0 : 
            on_ground = False
    else :
        if vy > 0 : 
            on_ground = True
        for i in range(int(y), int(next_y)) : 
            if died(x, y+1, scroll_x):
                is_died = True
                break
            if angle_move(x, i +1 , scroll_x) :
                continue
            else : 
                y = i
                break
        vy = 0        
    
    if x < 0 or died(x, y+1, scroll_x) or died(x+1, y, scroll_x) or died(x-1, y, scroll_x):
        if not is_finish:
            is_died = True
            x = -5
            y = -5
    
    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
        if x < 1024 and angle_move(x + 1, y, scroll_x) and not is_died and not is_begin and not is_finish:
            x = x + 1
            pers_x, pers_y = 0,0
    if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
        if x > 0 and angle_move(x - 1, y, scroll_x) and not is_died and not is_begin and not is_finish:
            x = x - 1
            pers_x, pers_y = 8,0
            
    if pyxel.frame_count % 3 == 0 and not is_begin and not is_finish:
        scroll_x += 1
        x-= 1
        
    if y - scroll_y >80 :
        scroll_y += 1
    if scroll_y > 0 and y - scroll_y < 30 :
        scroll_y -= 1
        
    if x > 100 :
        scroll_x += 1
        x = 100

        
def angle_move(x, y, scroll_x) :
    reponse = False
    
    if can_move(x, y, scroll_x) and can_move(x + 7, y, scroll_x) and can_move(x, y + 7, scroll_x) and can_move(x + 7, y + 7, scroll_x) :
        reponse = True
    
    return reponse
    
def can_move(x, y, scroll_x) :
    tile_x = (x + scroll_x) //8
    tile_y = y//8
    
    
    return pyxel.tilemaps[0].pget(tile_x, tile_y) == (0,31)

def died(x, y, scroll_x) :
    reponse = False
    
    if can_died(x, y, scroll_x) or can_died(x + 7, y, scroll_x) or can_died(x, y + 7, scroll_x) or can_died(x + 7, y + 7, scroll_x) :
        reponse = True
    
    return reponse

def can_died(x, y, scroll_x) :
    tile_x = (x + scroll_x) //8
    tile_y = y//8
        
    return pyxel.tilemaps[0].pget(tile_x, tile_y) == (3,2) or pyxel.tilemaps[0].pget(tile_x, tile_y) == (4,2) or pyxel.tilemaps[0].pget(tile_x, tile_y) == (0,9) or pyxel.tilemaps[0].pget(tile_x, tile_y) == (1,9)

def finish(x, y, scroll_x) :
    reponse = False
    
    if can_finish(x, y, scroll_x) or can_finish(x + 7, y, scroll_x) or can_finish(x, y + 7, scroll_x) or can_finish(x + 7, y + 7, scroll_x) :
        reponse = True
    
    return reponse

def can_finish(x, y, scroll_x) :
    tile_x = (x + scroll_x) //8
    tile_y = y//8
        
    return pyxel.tilemaps[0].pget(tile_x, tile_y) == (3,9) or pyxel.tilemaps[0].pget(tile_x, tile_y) == (3,10)
        
        

def draw():
    global x,y, scroll_x, scroll_y, is_died, pers_x, pers_y, is_begin, is_finish, timer, tempory_timer
    
    if is_begin :
        pyxel.text(128//6, 128//8, "Tu as perdu tes parents.", 7)
        pyxel.text(128//6, 128//8 * 2, "Retrouve les !", 7)
        
        if pyxel.frame_count > 120 :
            is_begin = False
            scroll_x = 0
    else :
        if not is_finish and not is_died: 
            tempory_timer += 1
        
        
        second = tempory_timer//30
        milieme = (tempory_timer % 30) * 1000 // 30
        timer_str = f"{second}.{milieme:03d}"
        
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, scroll_x, scroll_y, 128, 128) # Le fond 
        pyxel.blt(x, y - scroll_y, 0,pers_x,pers_y, 8, 8, 0) # le personnage
        pyxel.text(0,0, "Timer : " + timer_str, 7)
        
        if is_died:
            pyxel.cls(0)
            pyxel.text(128//3, 128//2, "Game over", 7)
            
        if finish(x, y+1, scroll_x) or finish(x+1, y, scroll_x) or finish(x-1, y , scroll_x):
            pyxel.cls(0)
            pyxel.text(128//6, 128//8, "Tu as retrouvé tes parents.", 7)
            pyxel.text(128//6, 128//8 * 2, "Bravo ! ", 7)
            pyxel.text(128//6, 128//8 * 4, "Temps : " + timer_str, 7)
            is_finish = True
        

            
    

########################
#  PROGRAMME PRINCIPAL #
########################

pyxel.init(128, 128, title = "Super deathrun")

x = 65
y= 25
vy = 0
scroll_x = 0
scroll_y = 0
timer = 0
tempory_timer = 0

on_ground = False
is_died = False
is_begin = True
is_finish = False

pers_x = 0
pers_y = 0


pyxel.load("1.pyxres")

# Lancement du jeu
pyxel.run(update, draw)