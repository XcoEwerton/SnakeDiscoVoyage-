import pygame
import random
import sys
import time
import os

pygame.init()

# ---------------- CONFIGURAÇÕES ----------------
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Disco UFO 🛸")

FONT = pygame.font.SysFont("consolas", 28)
MSG_FONT = pygame.font.SysFont("consolas", 32, bold=True)
GAMEOVER_FONT = pygame.font.SysFont("consolas", 42, bold=True)

clock = pygame.time.Clock()
FPS = 12
base_speed = FPS

# ---------------- ARQUIVO DE RECORD ----------------
record_file = "record.txt"

if os.path.exists(record_file):
    try:
        with open(record_file, "r") as f:
            highscore = int(f.read().strip())
    except:
        highscore = 0
else:
    highscore = 0


def save_record():
    with open(record_file, "w") as f:
        f.write(str(highscore))


# ---------------- CARREGAR IMAGENS ----------------
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

player_img = pygame.image.load("disco.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

food_img = pygame.image.load("disco.png").convert_alpha()
food_img = pygame.transform.scale(food_img, (30, 30))



# ---------------- RESET FUNCTION ----------------
def reset_game():
    global player_pos, direction, snake_body, food_pos, score, FPS, shown_eggs
    player_pos = [WIDTH // 2, HEIGHT // 2]
    direction = "STOP"
    snake_body = [[player_pos[0], player_pos[1]]]
    food_pos = [random.randrange(0, WIDTH // 20) * 20, random.randrange(0, HEIGHT // 20) * 20]
    score = 0
    FPS = base_speed
    shown_eggs.clear()



# ---------------- EASTER EGG CONFIG ----------------
easter_eggs = {
    1000: "XCO: Você está começando a dominar o sistema...",
    5000: "XCO: Isso não é mais sorte. É habilidade alienígena!",
    10000: "XCO: Os terráqueos não estão prontos para você.",
    15000: "XCO: Bem-vindo ao nível dos seres superiores.",
    20000: "XCO: Além disso... você desbloqueou algo? 👀"
}

shown_eggs = {}
current_message = ""
message_timer = 0
msg_x, msg_y = 0, 0



def trigger_message(score):
    global current_message, message_timer, msg_x, msg_y

    if score in easter_eggs and score not in shown_eggs:
        current_message = easter_eggs[score]
        shown_eggs[score] = True
        message_timer = time.time()

        offset = random.choice([(0,-80), (0,80), (-120,0), (120,0)])
        msg_x = player_pos[0] + offset[0]
        msg_y = player_pos[1] + offset[1]

        text_width = MSG_FONT.size(current_message)[0]
        text_height = MSG_FONT.size(current_message)[1]

        if msg_x < 0: msg_x = 20
        if msg_x + text_width > WIDTH: msg_x = WIDTH - text_width - 20
        if msg_y < 0: msg_y = 20
        if msg_y + text_height > HEIGHT: msg_y = HEIGHT - text_height - 20



def draw_message():
    global current_message, message_timer

    if current_message and time.time() - message_timer < 4:
        text = MSG_FONT.render(current_message, True, (0, 255, 120))
        WINDOW.blit(text, (msg_x, msg_y))
    elif current_message and time.time() - message_timer >= 4:
        current_message = ""



# ---------------- TELA GAME OVER ----------------
def show_game_over():
    text = GAMEOVER_FONT.render("💀 GAME OVER 💀", True, (255, 60, 60))
    score_text = FONT.render(f"Score: {score}  |  Recorde: {highscore}", True, (255, 255, 255))
    restart_text = FONT.render("Pressione ENTER para jogar novamente", True, (0, 255, 180))
    exit_text = FONT.render("Pressione ESC para sair", True, (200, 200, 200))

    WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 120))
    WINDOW.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
    WINDOW.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    WINDOW.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 100))



# ---------------- LOOP PRINCIPAL ----------------
reset_game()
game_over = False

running = True
while running:
    WINDOW.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_record()
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    save_record()
                    running = False
            else:
                if event.key == pygame.K_UP and direction != "DOWN": direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP": direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT": direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT": direction = "RIGHT"


    if not game_over:
        # Turbo escalonado
        FPS = base_speed + (score // 5000)

        # Movimentação
        if direction == "UP": player_pos[1] -= 20
        elif direction == "DOWN": player_pos[1] += 20
        elif direction == "LEFT": player_pos[0] -= 20
        elif direction == "RIGHT": player_pos[0] += 20

        snake_body.insert(0, list(player_pos))

        # Come item
        if abs(player_pos[0] - food_pos[0]) < 25 and abs(player_pos[1] - food_pos[1]) < 25:
            score += 100
            if score > highscore:
                highscore = score
                save_record()
            food_pos = [random.randrange(0, WIDTH // 20) * 20, random.randrange(0, HEIGHT // 20) * 20]
            trigger_message(score)
        else:
            snake_body.pop()

        # Colisão com corpo → game over
        if snake_body[0] in snake_body[1:]:
            game_over = True

        # Teleporte nas bordas
        if player_pos[0] < 0: player_pos[0] = WIDTH
        if player_pos[0] > WIDTH: player_pos[0] = 0
        if player_pos[1] < 0: player_pos[1] = HEIGHT
        if player_pos[1] > HEIGHT: player_pos[1] = 0


        # Renderização
        for segment in snake_body:
            WINDOW.blit(player_img, (segment[0], segment[1]))

        WINDOW.blit(food_img, (food_pos[0], food_pos[1]))

        score_text = FONT.render(f"🛸 SCORE: {score}   👑 RECORD: {highscore}", True, (255, 255, 255))
        WINDOW.blit(score_text, (10, 10))

        draw_message()

    else:
        show_game_over()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
