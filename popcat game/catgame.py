import pgzrun # imports pygame (game coding for python)
import os # imports os (BE CAREFUL)
import random # imports random (randomizer)

# Window
WIDTH = 1200
HEIGHT = 700
# Centers window
os.environ["SDL_VIDEO_CENTERED"] = "1"

# Menu
menu_y = 0
menu_x = 0
start = False
instructions = False

## Popcat on menu
MENU_POPCAT = Actor("closed cat")
MENU_POPCAT_X = WIDTH/5 # X coordinate variable
MENU_POPCAT_Y = HEIGHT-150 # Y coordinate variable
MENU_POPCAT.pos = MENU_POPCAT_X, MENU_POPCAT_Y 

# Colors
white = 255, 255, 255 # RGB for white
dark_brown = 107, 30, 18 # RGB for dark brown
brown = 230, 206, 151 # RGB for brown

# Popcat sprite and attributes
POPCAT = Actor("closed cat") # makes the cat + the picture of the cat
POPCAT_X = WIDTH/2 # X coordinate variable
POPCAT_Y = HEIGHT-80 # Y coordinate variable
POPCAT.pos = (POPCAT_X, POPCAT_Y) # position
POPCAT.health = 3 # health of cat

# Food and attributes
food_options = ["musubi","salmon bowl","salmon sashimi","salmon sushi","temaki roll","tuna sashimi", "wasabi"] # LIST of food png names
FOOD = Actor(food_options[random.randint(0,len(food_options)-2)]) # makes the food + randomizes the food
FOOD.pos = (random.randint(50, WIDTH-50),-200) # randomizes X position, y is above the window
FOOD_SPEED = 3 # speed of falling food

# Text and buttons
points = 0 # point counter
header_pos = WIDTH/2 , 100 # position of points
subheader_pos = WIDTH/2 , 175
clickme_pos = WIDTH/3.25 , 600

shadow_color = dark_brown

clickme_angle = 10
clickme_size = 20

start_LABEL_POS = WIDTH/1.4, HEIGHT/2.08
start_button = Actor("chopsticks1")
start_button.pos = WIDTH , HEIGHT/2

instructions_LABEL_POS = WIDTH/1.4, HEIGHT/1.21
instructions_button = Actor("chopsticks1")
instructions_button.pos = WIDTH , HEIGHT/1.18

instructions_POS =  WIDTH/1.5, HEIGHT/1.65

def draw():
    if start == False: # Checks if on menu
        menu_draw()
    elif start == True: # if not on menu
        game_draw()

def update():
    global POPCAT_X, points, instructions, start

    if start == False: 
        move_background() # hover over function for meaning
        if keyboard.B and instructions == True: # Press B key to return to main menu
            instructions = False

    elif start == True: 
        if POPCAT.health > 0: # if POPCAT is alive
            if keyboard.A or keyboard.left and POPCAT_X > 10: # if player presses A and the POPCAT X coor. is > than 10 (barrier from window)
                POPCAT_X -= 10 # speed, moves left
                POPCAT.pos = POPCAT_X,POPCAT_Y # updates the position
            elif keyboard.D or keyboard.right and POPCAT_X < WIDTH-90: # if player presses D and POPCAT X coor is < the width of the window - 90
                POPCAT_X += 10 # speed, moves right
                POPCAT.pos = POPCAT_X,POPCAT_Y # updates position
            # food movement
            FOOD.y += FOOD_SPEED # makes the food fall / move
            eat()
        else:
            if keyboard.R:
                game_reset()

        # debug and checking (not important for functionality)
        # print(f"popcat x: {POPCAT_X} | food: {FOOD.pos}, {FOOD_SPEED}")
        # print(header_pos[1])
        print(food_options)

def menu_draw():
    if start == False and instructions == False:
        screen.clear() # clears screen of previous "draws"
        screen.blit("sushi tray", (menu_x,menu_y)) # creates bg
        MENU_POPCAT.draw() # menu popcat

        # Title for menu drawn on screen
        screen.draw.text("Welcome to Cat Game!", center=header_pos,fontname = "pixel",fontsize = 75, shadow=(-1,1), scolor = shadow_color, color = brown, gcolor = white)
        
        # Subheader for menu drawn on screen
        screen.draw.text("Press start to begin", center=subheader_pos,fontname = "pixel",fontsize = 50, shadow=(-1,1), scolor = shadow_color)
        
        # click me text drawn on screen
        screen.draw.text("Click me for\nsurprise :3", center=clickme_pos,fontname = "pixel",fontsize = clickme_size, shadow=(-1,1), scolor = shadow_color, angle = clickme_angle)
        
        # START button drawn on screen
        start_button.draw()
        screen.draw.text("START", center= start_LABEL_POS,fontname = "pixel",fontsize = 75, shadow=(-1,1), scolor = shadow_color, gcolor = white)

        # INSTRUCTIONS button drawn on screen
        instructions_button.draw()
        screen.draw.text("GUIDE", center= instructions_LABEL_POS,fontname = "pixel",fontsize = 75, shadow=(-1,1), scolor = shadow_color, gcolor = white)

    # Instructions page
    elif start == False and instructions == True: # if not start and the instructions r on
        screen.clear() # clears screen
        screen.blit("sushi tray", (menu_x,menu_y)) # bg

        MENU_POPCAT.draw() # menu popcat
        MENU_POPCAT.pos = MENU_POPCAT_X, MENU_POPCAT_Y

        # TITLE and SUBHEADER
        screen.draw.text("INSTRUCTIONS", center=header_pos,fontname = "pixel",fontsize = 75, shadow=(-1,1), scolor = shadow_color, color = brown, gcolor = white)
        screen.draw.text("Press B to go back", center=subheader_pos,fontname = "pixel",fontsize = 50, shadow=(-1,1), scolor = shadow_color)
        
        # Actual instructions
        screen.draw.text("Move left with the A key or \nleft arrow key and move right\nwith the D key or right arrow key\n\n Move around to collect sushi\nbut avoid the wasabi!\n(POPCAT finds it too spicy :[ )", center=instructions_POS,fontname = "pixel",fontsize = 35, shadow=(-1,1), scolor = shadow_color)

def game_draw():
    if POPCAT.health > 0: # if POPCAT is alive
        screen.clear() # clears screen to not leave copies of drawings
        screen.blit("background", (0,0)) # background draw
        POPCAT.draw() # puts POPCAT into scene
        FOOD.draw() # puts FOOD into scene
        screen.draw.text(f"{points}", center=header_pos, fontname = "pixel",fontsize = 100, shadow=(-1,1), scolor = shadow_color)
        # this ^ draws the points into the scene
    else:
        screen.clear() # removes everything on screen
        # points text
        screen.draw.text(f"You got {points}!", center=header_pos, fontname = "pixel",fontsize = 100)
        screen.draw.text(f"Press R to Restart", center=subheader_pos, fontname = "pixel",fontsize = 50)
    
def eat():
    global points, FOOD_SPEED # GLOBAL = to use and edit variables within function
    if POPCAT.colliderect(FOOD): # if POPCAT collides with FOOD
        if FOOD.image != food_options[-1]: # if the photo of the food isn't (!=) the LAST item in the list (wasabi)
            open_cat() # opens cat's mouth
            clock.schedule_unique(close_cat, 0.25) # closes mouth after 0.25 sec
            FOOD.pos = (random.randint(50, WIDTH-50),-200) # resets pos of food to above the window and random x pos/coor
            increase_wasabi() # may increase wasabi chances
            FOOD.image = food_options[random.randint(0,len(food_options)-1)] # randomizes the food image
            FOOD_SPEED += 0.5 # increases the falling speed by 0.5
            points += 1 # adds a point
        else: # otherwise / if it's the LAST item in the list (wasabi)
            cry_cat() # makes the cat cry
            FOOD.pos = (random.randint(50, WIDTH-50),-200) # resets pos of food to above the window and random x pos/coor
            FOOD.image = food_options[random.randint(0,len(food_options)-1)] # randomizes the food image
            POPCAT.health -= 1 # lessens POPCAT health
            clock.schedule_unique(close_cat,1.5) # returns to normal closed mouth cat after 1.5 secs

    if FOOD.y > HEIGHT + 20: # if the food y coor. is past the height + 20 (fallen past the screen)
        FOOD.pos = (random.randint(50, WIDTH-50),-200) # resets pos of food to above the window and random x pos/coor
        FOOD.image = food_options[random.randint(0,len(food_options)-1)] # randomizes the food image

def on_mouse_down(pos):
    global start, instructions
    if start == False: # while it's on the menu page
        if MENU_POPCAT.collidepoint(pos):
            background_cat() # makes menu cat clickable
        if start_button.collidepoint(pos): # if u click start button
            start = True # starts game
            POPCAT.health = 3
            music.play("bg music.wav")
        if instructions_button.collidepoint(pos): # if u click instructions button
            instructions = True # turns on instructions

def open_cat(): # function for opening cat's mouth
    """Opens POPCAT's mouth"""
    POPCAT.image = "open cat" # changes the image to a opened mouth cat
    sounds.pop.play() # plays the pop sound

def close_cat(): # function for closing cat's mouth / resets to normal cat
    POPCAT.image = "closed cat" # changes the image to closed mouth cat

def cry_cat(): # function for making the cat cry
    POPCAT.image = "cat cry2" # changes image to hurt crying cat
    sounds.bleh.play() # plays the blegh noise

def background_cat():
    open_menu_cat() # opens mouth
    clock.schedule_unique(close_menu_cat, 0.50) # closes mouth after 0.25 sec

def close_menu_cat():
    MENU_POPCAT.image = "closed cat"
def open_menu_cat():
    MENU_POPCAT.image = "open cat"
    sounds.pop.play() # plays the pop sound

def increase_wasabi():
    if random.randint(2,1000) %5 == 0: # if the random number from 2 - 1000 is divisible by 3
        food_options.append("wasabi") # add another wasabi to the list

def move_background():
    """
    Moves background around.
    """
    global menu_y, menu_x

    # background
    # if it hits any wall move opposite direction
    if menu_x >= -WIDTH/4 and menu_y==0 and menu_x != 0:
        menu_y+=0
        menu_x+=1
    elif menu_y <= -HEIGHT/2.5 and menu_x>-WIDTH/4:
        menu_y-=0
        menu_x-=1
    elif menu_x == -WIDTH/4 and menu_y<0:
        menu_x-=0
        menu_y+=0.75
    elif menu_y >= -HEIGHT/2.5 and menu_x>-WIDTH/4:
        menu_y-=0.75
        menu_x-=0
    
    # debugging
    # print(menu_x , menu_y, WIDTH , HEIGHT)

def game_reset():
    global start, points, food_options, FOOD_SPEED
    start = False
    points = 0
    while len(food_options) != 7:
        food_options.remove("wasabi")
    FOOD_SPEED = 3
    FOOD.Y = 3


pgzrun.go() # runs game