import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

#Color of the circle
BG_COLOR = (0, 25, 40)
#Set LIVES to 5, we have maximum 5 LIVES to target the circles
LIVES = 5
#Height of top bar
TOP_BAR_HEIGHT = 50

#Fonts
LABEL_FONT = pygame.font.SysFont("comicsans", 24)


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    #Size of circle
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    #For distance from each and evry circle
    def collide(self, x, y):
        dis = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        return dis <= self.size


def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


#Time
def format_time(secs):
    milli = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


#Top bar of the window
#There will the number of lives perest at top bar, The game will end based on that count
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    #Rectangular top bar
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    #Time
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "black")

    #Speed
    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "black")

    #Hits
    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "black")

    #Lives
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    #Displaying Time, Speed, Hits, Lives at top bar
    #blit - how we display the another surface 
    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (650, 5))


#Ending the screen or window
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, "white")

    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    #When user is playing!
    run = True
    while run:
        for event in pygame.event.get():
            #Press any key down
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


#When our game will end, Time, Speed, Hits & Accuracy will display. This is the formula to set Time, Speed, Hits & Accuracy
def get_middle(surface):
    return WIDTH / 2 - surface.get_width()/2


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    #Collision with target
    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        # Runs 60 frames per second
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            #Window
            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            #Updating the target size
            target.update()

            #Remove the target when the size of circle will be 0
            if target.size <= 0:
                targets.remove(target)
                misses += 1

            #Collision with target, * Splat operator: equal to most position 0 to most position 1
            #After Click, and target will remove 
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        #I have set LIVES = 5, if we misses more than 5 target then the game will end
        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()