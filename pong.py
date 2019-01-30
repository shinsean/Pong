#Created By Sean Shin
#Pong in Python Pygame

#Importing the libraries for later.
import pygame, random, time, math

#Initializing Pygame so we can use the pygame library.
pygame.init()

#Window size. The resolution 750 x 570 is closer to the original but this is more balanced.
DISPLAY_WIDTH = 950
DISPLAY_HEIGHT = 570

#The frames per second.
FPS = 60

#The clock.
CLOCK = pygame.time.Clock()

#Color pallettes for the game. Only need black and white for pong.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Creating the display to display the sprites.
GAME_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

#Don't really know how or why pygame.sprite.Sprite works but its useful.
#This is the mold to make the player's paddles.
class Player(pygame.sprite.Sprite):
    #The Constructor. This creates the object with the passed arguments and assigned values.
    def __init__(self, x_position):
        super().__init__()

        #The dimensions of the paddle.
        #Original 11
        self.width = 15
        #Original 50
        self.height = 90

        #This is how much the y_position of the paddle is going to be changed.
        self.y_velocity = 0

        #Color of the paddle.
        self.color = WHITE

        #Don't know what this is for but probably useful.
        self.image = pygame.Surface([self.width, self.height])

        #Fills the image with white.
        self.image.fill(WHITE)

        #Gets the rectangle that has the dimensions of this object.
        self.rect = self.image.get_rect()

        #Changing the position of the paddle.
        self.rect.x = x_position
        self.rect.y = self.y_position = ((DISPLAY_HEIGHT//2)-10)

    #Changes the rect.y by adding y_velocity to it.
    def update(self):
        #This adds the y_velocity(which would be changed by the key controls) to the current y position.
        self.rect.y += self.y_velocity

        #This checks if the paddle has gone off the screen.
        #If it has, it sets to y position to the edge value it went off of.
        if self.rect.y < 0:
            self.rect.y = 0
        #The reason why we do (DISPLAY_HEIGHT - self.height) is so that the game checks if the bottom edge went
        #off the screen. Normally, the x positions and y positions are calculated in the top left.
        #(DISPLAY_HEIGHT - self.height) makes it so that the game factors that in.
        elif self.rect.y > (DISPLAY_HEIGHT - self.height):
            self.rect.y = (DISPLAY_HEIGHT - self.height)

    #This displays the paddle(s) onto the screen using pygame.
    def display_self(self):
        pygame.draw.rect(GAME_DISPLAY, self.color, [self.rect.x, self.rect.y, self.width, self.height])

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #This is for the length and width of the ball.
        #Since the ball is a square, only one dimension has to be given.
        #Original 10
        self.side = 10

        #Defining some basic things for the ball such as its color, its rectangle.
        self.color = WHITE
        self.image = pygame.Surface([self.side, self.side])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        #The x and y positions of the ball.
        self.rect.x = DISPLAY_WIDTH * (1/4)
        self.rect.y = random.randint(200, 300)

        #The velocity of the x and y of the moving ball.
        self.x_velocity = 8.0
        self.y_velocity = 8.0

        #TThis flips a "coin" and if its 1, it reverses the ball.
        if random.randint(0, 1) == 1:
            self.rect.x = DISPLAY_WIDTH * (3/4)
            self.x_velocity = -8.0

        #This is the maximum anlge the ball can go.
        self.max_bounce_angle = (5 * math.pi)/12

    #Updates the coordinates of the ball.
    def update(self):
        #Adds the x_velocity and y_velocity to the x and y positions.
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

    #Changes the y_velocity variable to its opposite if it hits the wall.
    #The collision detection will be added later.
    def wall_bounce(self):
        #Checks if the ball has hit the bottom.
        if self.rect.y >= (DISPLAY_HEIGHT - self.side):
            #If so, it changes the y_velocity.
            self.y_velocity *= -1

        #Checks if the ball hit the top.
        if self.rect.y <= 0:
            #If so, it changes the y_velocity.
            self.y_velocity *= -1
            
    #This function will change both the x_velocity and the y_velocity when the ball hits a paddle.
    def player_bounce(self, paddle_y_mid, paddle_height, player_designation):
        #If this is gone, it doesn't work so leave it here.
        ball_speed = 11

        #This chunk gets the bounce_angle of the ball's current angle.
        #The bounce_angle is used to calculate the new y_velocity.
        intersect_y = paddle_y_mid - self.rect.y
        normalized_intersect_y = math.fabs((intersect_y/(paddle_height/2)))
        bounce_angle = normalized_intersect_y * self.max_bounce_angle

        if player_designation == "P1":  
            # This is some trigonometry that I can partially explain.
            self.y_velocity = ball_speed * math.sin(bounce_angle)
            #This reverses the x_velocity. The x_velocity is not dynamic.
            self.x_velocity = ball_speed * math.fabs(math.cos(bounce_angle)) * -1

        elif player_designation == "P2":
            self.y_velocity = ball_speed * math.sin(bounce_angle)
            self.x_velocity = ball_speed * math.fabs(math.cos(bounce_angle))

    def display_self(self):
        pygame.draw.rect(GAME_DISPLAY, self.color, [self.rect.x, self.rect.y, self.side, self.side])

    #Resets the ball after a round ends.
    def reset_self(self):
        self.x_velocity = 8.0
        self.y_velocity = 8.0

        self.rect.x = DISPLAY_WIDTH * (1/4)
        self.rect.y = random.randrange(200, 300)

        if random.randint(0, 1) == 1:
            self.x_velocity = self.x_velocity * -1
            self.rect.x = DISPLAY_WIDTH * (3/4)

#A function that kills the program.
def quit_game():
    pygame.quit()
    quit()

#Checks to see if a person has won.
def check_win(ball_x, ball_side_length):
    if ball_x > (DISPLAY_WIDTH - ball_side_length):
        return("P2V")
    if ball_x < 0:
        return("P1V") 

#Create the ball to be used.
ball = Ball()

#Create a group of 1 ball (used in checking collisions) and add the ball to it.
pong_balls = pygame.sprite.Group()
pong_balls.add(ball)

#Create the player's paddles
player_one = Player(DISPLAY_WIDTH * 0.9)
player_two = Player(DISPLAY_WIDTH * 0.1)

#Creating a group of two paddles and adding the paddles to it.
pong_paddles = pygame.sprite.Group()
pong_paddles.add(player_one)
pong_paddles.add(player_two)

def game_loop():
    #game_exit is set to False right now to stop the while loop from breaking.
    game_exit = False
    #The player's scores.
    player_one_score = 0
    player_two_score = 0

    while not game_exit:

        for event in pygame.event.get():
            
            #Checking if the player pressed the exit button.
            if event.type == pygame.QUIT:
                quit_game()

            #This entire chunk of code does the following:
            #1.Check if someone has pressed down on a key. 
            #If so, add the corresponding amount to the y_velocity.
            #2. Check if someone has let go of a key.
            #If so, subtract the corresponding amount from the y_velocity.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: 
                    player_one.y_velocity += -15
                elif event.key == pygame.K_DOWN:
                    player_one.y_velocity += 15

                if event.key == pygame.K_w:
                    player_two.y_velocity += -15
                elif event.key == pygame.K_s:
                    player_two.y_velocity += 15

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_one.y_velocity += 15
                elif event.key == pygame.K_DOWN:
                    player_one.y_velocity += -15

                if event.key == pygame.K_w:
                    player_two.y_velocity += 15
                elif event.key == pygame.K_s:
                    player_two.y_velocity += -15

        #Update the y of the player.
        player_one.update()
        player_two.update()

        #Updates the ball.
        ball.update()

        #Checks if the ball has hit Player One's paddle.
        if pygame.sprite.spritecollide(player_one, pong_balls, False):
            ball.rect.x = player_one.rect.x - ball.side
            ball.player_bounce((player_one.rect.y + (player_one.height / 2)), player_one.height, "P1")

        #Checks if the ball has hit Player Two's paddle.
        if pygame.sprite.spritecollide(player_two, pong_balls, False):
            ball.rect.x = player_two.rect.x + player_two.width
            ball.player_bounce((player_two.rect.y + (player_two.height / 2)), player_two.height, "P2")

        #Checks if a player has won.
        if check_win(ball.rect.x, ball.side) == "P1V":
            print("Player One Victory")
            player_one_score += 1
            ball.reset_self()
            time.sleep(1)
        elif check_win(ball.rect.x, ball.side) == "P2V":
            print("Player Two Victory")
            player_two_score += 1
            ball.reset_self()
            time.sleep(1)

        if player_one_score == 10:
            print("Player One Has Won The Game")
            quit_game()
        elif player_two_score == 10:
            print("Player Two Has Won The Game")
            quit_game()

        #Checks if it has hit a wall and carries out some instructions if yes (see line:105).
        ball.wall_bounce()

        #Fill the screen with black. Kinda redundant.
        GAME_DISPLAY.fill(BLACK)
        
        #Display the sprites onto the GAME_DISPLAY.
        player_one.display_self()
        player_two.display_self()
        ball.display_self()

        pygame.display.update()
        CLOCK.tick(FPS)

game_loop()