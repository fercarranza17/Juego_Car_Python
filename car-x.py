import pygame, os, random, json
from datetime import datetime


pygame.init()
clock=pygame.time.Clock()
directory = os.path.dirname(os.path.realpath(__file__))

########## VENTANA DEL JUEGO CAR-X ########## 
pygame.mixer.music.load("sounds/remix.mp3")#cargar musica
pygame.mixer.music.play(-1, 0.0)#la inicia

SCREENWIDTH=800
SCREENHEIGHT=500
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Car-X")
os.environ['SDL_VIDEO_CENTERED'] = '1'
                   
########## COLORES UTILIZADOS  ########## 

RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)

########## FONDOS  ########## 


menuBg = pygame.image.load(directory + "\\sprites\\menuprincipal.png").convert_alpha()

########## FUENTES  ########## 

myfont = pygame.font.SysFont('Lucida Console', 20)

########## VARIABLES GLOBALES  ########## 

userName = str
energy = 100
points = 0
date = str
speed = 5
first = True
fullscreen = False

########## SONIDOS Y AUDIOS ########## 

soundCrash = pygame.mixer.Sound(directory + "\\sounds\\crash.wav")
soundPoints = pygame.mixer.Sound(directory + "\\sounds\\points.wav")
soundGameOver = pygame.mixer.Sound(directory + "\\sounds\\gameOver.wav")

########## CLASES  ########## 

class enemyCar(pygame.sprite.Sprite):

    def __init__(self, kind, lane):
        super().__init__()

        global speed
        
        self.size = (50, 50)

        self.image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(directory + "\\sprites\\lamborgini.png").convert_alpha(),self.size),180)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.kind = kind
        self.lane = lane

        if self.kind == 1:
            self.image = pygame.image.load(directory + "\\sprites\\lamborgini.png").convert_alpha()
        elif self.kind == 2:
            self.image = pygame.image.load(directory + "\\sprites\\formula2.png").convert_alpha()
        elif self.kind == 3:
            self.image = pygame.image.load(directory + "\\sprites\\tanque.png").convert_alpha()
        elif self.kind == 4:
            self.image = pygame.image.load(directory + "\\sprites\\moto.png").convert_alpha()
        elif self.kind == 5:
            self.image = pygame.image.load(directory + "\\sprites\\carro3.png").convert_alpha()
        elif self.kind == 6:
            self.image = pygame.image.load(directory + "\\sprites\\formula5.png").convert_alpha()
            
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.lane
        self.rect.y = -100
        
    def moveForward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
            self.kill()

enemigocarro1 = enemyCar(1, 200)
enemigocargrupo = pygame.sprite.Group()
enemigocargrupo.add(enemigocarro1)

class thing(pygame.sprite.Sprite):

    def __init__(self, lane):
        super().__init__()
          
        self.image = pygame.image.load(directory + "\\sprites\\gasolina.png").convert_alpha()
        self.rect = self.image.get_rect()
        
        self.rect.y = -100
        self.rect.x = lane

    def moveForward(self):
        
        if self.rect.y < 650:
            self.rect.y += speed
        else:
           self.kill()
          
thing1 = thing(-200) 
thingGroup = pygame.sprite.Group()
thingGroup.add(thing1)
            
class kar(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.image.load(directory + "\\sprites\\formulaa1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        
    def moveRight(self, pixels):
        if self.rect.x < 550:
            self.rect.x += pixels
 
    def moveLeft(self, pixels):
        if self.rect.x > 200:
            self.rect.x -= pixels

playerKar = kar() 
kar_group = pygame.sprite.Group() 
kar_group.add(playerKar)

class landscape(pygame.sprite.Sprite):
    
    global speed
    
    def __init__(self, y):
        super().__init__()
       
        self.image = pygame.image.load(directory + "\\sprites\\menu11.png").convert_alpha()
        self.rect = self.image.get_rect() 
        self.rect.y = y
        
    def play(self):
        if self.rect.y < 500:
            self.rect.y += speed
        else:
            self.rect.y = -500
            
lands01 = landscape(-500) 
lands02 = landscape(0) 
lands_group = pygame.sprite.Group() 
lands_group.add(lands01) 
lands_group.add(lands02)

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            text = myfont.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

        pos = pygame.mouse.get_pos()
        if self.isOver(pos):
            self.color = WHITE
        else:
            self.color = GREY

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False    

okBtn = button(RED, 250, 300, 200, 25, "ok")

class InputBox:
    
    COLOR_INACTIVE = BLACK
    COLOR_ACTIVE = WHITE

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.COLOR_INACTIVE
        self.text = text
        self.txt_surface = myfont.render(text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]

                else:
                    if len(self.text) < 10:
                        self.text += event.unicode
                self.txt_surface = myfont.render(self.text, True, self.color)
                
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2) 
    
input_box1 = InputBox(300, 300, 140, 32)  

##### FUNCIONES #####
def changescn(scn, text="", btnfnc=""):
    global menu_s, enterName_s, mainLoop_s, instructions_s, msg_s, scores_s
    menu_s = enterName_s = mainLoop_s = instructions_s = msg_s = scores_s = False
    
    if scn == "menu":
        menu_s = True
        menu()
    
    elif scn == "enterName":
        enterName_s = True
        enterName()
        
    elif scn == "mainLoop":
        mainLoop_s = True
        mainLoop()
        
    elif scn == "instructions":
        instructions_s = True
        instructions()
        
    elif scn == "msg":
        msg_s = True
        msg(text,btnfnc)
        
    elif scn == "scores":
        scores_s = True
        scores()
msg_s = True
def msg(text,btnfnc):
    
    global msg_s, first
    
    msgOkBtn = button(RED, SCREENWIDTH/2 - 100, SCREENHEIGHT/2, 200, 25, "ok")
    label = pygame.font.SysFont('Lucida Console', 30).render(text, 1, BLACK)
    
    if text == "PERDISTE!":
        playMusic("stop")
        resetGame()
        first = True
        soundGameOver.play()
        
    while msg_s:
            
        screen.fill(MAGENTA)
        screen.blit(label, (SCREENWIDTH/2 - label.get_width()/2, SCREENHEIGHT/2 - label.get_height()/2 - 50))
        msgOkBtn.draw(screen, BLACK)
        pygame.display.flip()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            
            if event.type==pygame.QUIT:
                msg_s = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if msgOkBtn.isOver(pos):
                    if text == "Game Over!":
                        playMusic("main")
    
                    changescn(btnfnc)
                    
            if event.type == pygame.KEYDOWN:
                                
                if event.key==pygame.K_ESCAPE:
                    changescn(btnfnc)
def playMusic(music):
        pygame.mixer.music.load("sounds/remix.mp3")#cargar musica
        pygame.mixer.music.play(-1, 0.0)#la inicia

def fnc(): 
    
    global fullscreen
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_f] and (all_keys[pygame.K_LSHIFT] or all_keys[pygame.K_RSHIFT]):
        
        fullscreen = not fullscreen
        if fullscreen == True:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(size)
##### SCORE

sortedData = []
data = {}
def saveGame():
    
    global sortedData, data, date, points, userName
    
    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    data.update({date:{"name":userName, "points":points, "energy":energy}} )
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios
    try:
        del data[sortedData[10][0]]

    except IndexError:
        pass
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)
def things():
    
    global points, speed
     
    points += 1
    soundPoints.play()
    thing1.rect.y = 600
    thingGroup.add(thing1)
    speed += 1
def hud():

    global energy, userName, points
    
    label0 = myfont.render("Name: " + str(userName), 1, WHITE, BLACK)
    screen.blit(label0, (610, 20))     
    
    label1 = myfont.render("Energy: " + str(energy), 1, WHITE, BLACK)
    screen.blit(label1, (610, 50))

    label2 = myfont.render("Points: " + str(points), 1, WHITE, BLACK)
    screen.blit(label2, (610, 80))
carsOut = 0
def launch():
    
    global carsOut
    kind = random.randint(1,6)
    laneRand = random.randint(1,8)
    lane = 0
  
    if laneRand == 1:
        lane = 200
    elif laneRand == 2:
        lane = 250
    elif laneRand == 3:
        lane = 300  
    elif laneRand == 4:
        lane = 350
    elif laneRand == 5:
        lane = 400
    elif laneRand == 6:
        lane = 450
    elif laneRand == 7:
        lane = 500
    elif laneRand == 8:
        lane = 550
        
    if carsOut < 5:

        enemyCar1 = enemyCar(kind, lane)
        enemigocargrupo.add(enemyCar1)
        carsOut += 1
        
    else: 
        
        thing1 = thing(lane)
        thingGroup.add(thing1)
        carsOut = 0
        
##### CHOQUE

aux = False
def crash(value):
    
    global aux
    global energy

    if value == True and aux == False:
        energy -= 20
        soundCrash.play()

        aux = True
        
    if value == False and aux == True:
        aux = False

    if energy < 1:
        saveGame()
        changescn("msg", text="PERDISTE!", btnfnc="menu")
        
##### INICIAR AGAIN

def resetGame():
    global userName, energy, first, points, date, speed
    
    for i in enemigocargrupo:
        i.kill()
        
    for i in thingGroup:
        i.kill()
    
    userName = input_box1.text
    input_box1.text = "" # clear input_box
    input_box1.txt_surface = myfont.render("", True, input_box1.color) # clear input_box 

    input_box1.update
    energy = 100
    points = 0
    speed = 5
   
    now = datetime.now()
    date = now.strftime("%d/%m/%Y %H:%M:%S")
##### MENU

menu_s = bool
def menu():
    
    global data, sortedData, menu_s, firts

    playBtn = button(RED, 300, 270, 200, 25, "JUGAR")
    scoresBtn = button(RED, 300, 300, 200, 25, "PUNTAJES")
    instBtn = button(RED, 300, 330, 200, 25, "INSTRUCCIONES")
    exitBtn = button(RED, 300, 360, 200, 25, "SALIR")
    backBtn = button(RED, 550, 450, 200, 25, "REGRESAR")

    with open(directory + "\\save\\" + "scores.txt", "r") as f:
        data = json.load(f)
    sortedData = sorted(data.items(), key=lambda x: x[1]['points'], reverse=True) # ordenar diccionario de diccionarios

    while menu_s:
        
        fnc()
        screen.blit(menuBg, (0, 0))
        playBtn.draw(screen, (0,0,0))
        scoresBtn.draw(screen, (0,0,0))
        instBtn.draw(screen, (0,0,0))
        exitBtn.draw(screen, (0,0,0))

        if first == False:
        
            backBtn.draw(screen, (0,0,0))

        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() # toma la posicion del mouse
 
            if event.type == pygame.QUIT:
                menu_s = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                ############ Botones 
                
                if playBtn.isOver(pos):         
                    changescn("enterName")
      
                if instBtn.isOver(pos):
                    changescn("instructions")
                
                if exitBtn.isOver(pos):
                    menu_s = False
                    
                if backBtn.isOver(pos):
                    changescn("mainLoop")
                    
                if scoresBtn.isOver(pos):
                    changescn("scores")
                    
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    menu_s = False
        pygame.display.flip()
       
##### scores
   
scores_s = bool
def scores():

    global data

    tag = "NAME".ljust(10) + "POINTS".center(10) + "DATE".rjust(10)

    if len(sortedData) > 0:
        place0 = str(data[(sortedData[0][0])]["name"].ljust(10) + str(data[(sortedData[0][0])]["points"]).center(10) + str(sortedData[0][0]).rjust(25))
    else:
        place0 = "Empty"
        
    if len(sortedData) > 1:
        place1 = str(data[(sortedData[1][0])]["name"].ljust(10) + str(data[(sortedData[1][0])]["points"]).center(10) + str(sortedData[1][0]).rjust(25))
    else:
        place1 = "Empty"
        
    if len(sortedData) > 2:
        place2 = str(data[(sortedData[2][0])]["name"].ljust(10) + str(data[(sortedData[2][0])]["points"]).center(10) + str(sortedData[2][0]).rjust(25))
    else:
        place2 = "Empty"
        
    if len(sortedData) > 3:
        place3 = str(data[(sortedData[3][0])]["name"].ljust(10) + str(data[(sortedData[3][0])]["points"]).center(10) + str(sortedData[3][0]).rjust(25))
    else:
        place3 = "Empty"
        
    if len(sortedData) > 4:
        place4 = str(data[(sortedData[4][0])]["name"].ljust(10) + str(data[(sortedData[4][0])]["points"]).center(10) + str(sortedData[4][0]).rjust(25))
    else:
        place4 = "Empty"
        
    if len(sortedData) > 5:
        place5 = str(data[(sortedData[5][0])]["name"].ljust(10) + str(data[(sortedData[5][0])]["points"]).center(10) + str(sortedData[5][0]).rjust(25))
    else:
        place5 = "Empty"
        
    if len(sortedData) > 6:
        place6 = str(data[(sortedData[6][0])]["name"].ljust(10) + str(data[(sortedData[6][0])]["points"]).center(10) + str(sortedData[6][0]).rjust(25))
    else:
        place6 = "Empty"  

    if len(sortedData) > 7:
        place7 = str(data[(sortedData[7][0])]["name"].ljust(10) + str(data[(sortedData[7][0])]["points"]).center(10) + str(sortedData[7][0]).rjust(25))
    else:
        place7 = "Empty"
        
    if len(sortedData) > 8:
        place8 = str(data[(sortedData[8][0])]["name"].ljust(10) + str(data[(sortedData[8][0])]["points"]).center(10) + str(sortedData[8][0]).rjust(25))
    else:
        place8 = "Empty"
        
    if len(sortedData) > 9:
        place9 = str(data[(sortedData[9][0])]["name"].ljust(10) + str(data[(sortedData[9][0])]["points"]).center(10) + str(sortedData[9][0]).rjust(25))
    else:
        place9 = "Empty"

    scoresOk = button(RED, 150, 450, 200, 25, "Back")
    scoresClear = button(RED, 450, 450, 200, 25, "Clear Score")
    scoresTitle = myfont.render("SCORES - TOP10", 1, WHITE, BLUE)
    tag2 = myfont.render(tag, 1, WHITE, BLUE)
    score0 = myfont.render(place0, 1, WHITE)
    score1 = myfont.render(place1, 1, WHITE)
    score2 = myfont.render(place2, 1, WHITE)
    score3 = myfont.render(place3, 1, WHITE)
    score4 = myfont.render(place4, 1, WHITE)
    score5 = myfont.render(place5, 1, WHITE)
    score6 = myfont.render(place6, 1, WHITE)
    score7 = myfont.render(place7, 1, WHITE)
    score8 = myfont.render(place8, 1, WHITE)
    score9 = myfont.render(place9, 1, WHITE)

    global scores_s
    while scores_s:
        fnc()
        screen.fill(MAGENTA)
        pygame.draw.rect(screen,BLACK,(90,20,600,400))
        screen.blit(scoresTitle, (100, 30))
        screen.blit(tag2, (100, 80))
        screen.blit(score0, (100, 120))
        screen.blit(score1, (100, 150))
        screen.blit(score2, (100, 180))
        screen.blit(score3, (100, 210))
        screen.blit(score4, (100, 240))
        screen.blit(score5, (100, 270))
        screen.blit(score6, (100, 300))
        screen.blit(score7, (100, 330))
        screen.blit(score8, (100, 360))
        screen.blit(score9, (100, 390))
        scoresOk.draw(screen, (0,0,0))
        scoresClear.draw(screen, (0,0,0))
        ##### EVENTS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
 
            if event.type == pygame.QUIT:
                scores_s = False
                
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: 
                    changescn("menu")

            if event.type == pygame.mousebotonabajo:          
                if scoresOk.isOver(pos):
                    changescn("menu")
                    
                elif scoresClear.isOver(pos):
                    clearScores()

        # Refresh Screen
        pygame.display.flip()
        
def clearScores():
    
    global data, sortedData
    data.clear()
    sortedData.clear()
    
    with open(directory + "\\save\\" + "scores.txt", "w") as f:
        json.dump(data, f)
    changescn("scores")
##### instructions

instructions_s = bool
def instructions():
    
    global instructions_s
    
    backBtn = button(RED, 550, 450, 200, 25, "Back")

    label0 = myfont.render("Instrucciones:", 1, WHITE, BLUE)
    label1 = myfont.render("* Drive through the higway and dont crash", 1, WHITE, BLUE)
    label2 = myfont.render("* Use las teclas A y D para mover su carro", 1, WHITE, BLUE)
    label3 = myfont.render("* Use la tecla F para mazimizar su pantalla", 1, WHITE, BLUE)
    label4 = myfont.render("* Atrapa todos los diamantes que puedas para ganar puntos", 1, WHITE, BLUE)
    while instructions_s:
        fnc()
        
        ##### RENDER #####
            
        screen.fill(MAGENTA)
        
        pygame.draw.rect(screen,BLACK,(25,20,750,400))
        
        screen.blit(label0, (30, 30))
        screen.blit(label1, (100, 100))
        screen.blit(label2, (100, 150))
        screen.blit(label3, (100, 200))
        screen.blit(label4, (100, 250))
  
        backBtn.draw(screen, (0,0,0))
        
        ##### ACTUALIZACION #####
        
        pygame.display.flip()
        
        ##### EVENTOS #####
        
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            
            if event.type == pygame.mousebotonabajo:
                
                if backBtn.isOver(pos):
                    changescn("menu")
                    
            if event.type == pygame.QUIT:
                instructions_s = False
                
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: #Pressing the esc Key will quit the game
                    changescn("menu")
##### Digitar su nombre 
enterName_s = False
def enterName():
    global enterName_s, user_text, first
    enterOkBtn = button(RED, 300, 350, 200, 25, "READY")
    enterBackBtn = button(RED, 550, 450, 200, 25, "REGRESAR")
    labelEnterName = myfont.render("DIGITE SU NOMBRE:", 1, BLACK)
    while enterName_s:
        fnc()
        screen.blit(menuBg, (0, 0)) 
        enterOkBtn.draw(screen, (0,0,0)) 
        enterBackBtn.draw(screen, (0,0,0))
        screen.blit(labelEnterName, (300, 270))  
        input_box1.update()
        input_box1.draw(screen) 
        ##### EVENTOS #####
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos() 
            input_box1.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN: 
                ############ botones
                if enterOkBtn.isOver(pos):
                    if input_box1.text == "":
                        changescn("msg", text="Tienes que ingresar tu nombre", btnfnc="enterName")
                    else:
                        first = False
                        resetGame()
                        changescn("mainLoop")
         
                if enterBackBtn.isOver(pos):
                    changescn("menu")
            
            if event.type==pygame.QUIT:
                enterName_s = False
                
            if event.type == pygame.KEYDOWN:                
                if event.key==pygame.K_ESCAPE:
                    changescn("menu")
        pygame.display.flip()
##### Bucle 
count = 0
mainLoop_s = bool
def mainLoop():
    global mainLoop_s, first, count, fullscreen, size, speed
    playMusic("engine")
    while mainLoop_s:
        fnc()
        count += 1
        if count > 10:
            count = 0
            launch()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainLoop_s = False
        ##### CLAVES 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            playerKar.moveLeft(5)
        if keys[pygame.K_d]:
            playerKar.moveRight(5)  

        if keys[pygame.K_t]:
            pass
        if keys[pygame.K_ESCAPE]:
            saveGame()
            playMusic("main")
            changescn("menu")
        ##### render
        lands_group.draw(screen)
        enemigocargrupo.draw(screen)
        kar_group.draw(screen)        
        thingGroup.draw(screen)
        hud()
        lands01.play()
        lands02.play()
        ##### LOGICA
        for car in enemigocargrupo:
            car.moveForward()
        for thing in thingGroup:
           thing.moveForward()
        ##### COLISIONES #####
        car_collision_list = pygame.sprite.spritecollide(playerKar,enemigocargrupo,False,pygame.sprite.collide_mask)
        if car_collision_list:
            crash(True)
        else:
            crash(False)
        # GASOLINA
        thing_collision = pygame.sprite.spritecollide(playerKar,thingGroup,True,pygame.sprite.collide_mask)
        if thing_collision:
            things()
        #Refresh Screen
        pygame.display.flip()
        clock.tick(60) # This method should be called once per frame // aprox 16 - 17 fps
playMusic("main")
menu()