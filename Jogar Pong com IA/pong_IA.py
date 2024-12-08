import pygame
import random
import numpy as np
import pickle

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
PADDLE_SPEED = 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
BALL_SPEED_INCREMENT = 0.1

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong com IA")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Raquete e bola
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]

# Pontuação
score = 0

# Q-Learning
state_space = 30
action_space = 3  # 0: esquerda, 1: parado, 2: direita
q_table_file = "q_table.pkl"

# Inicializar a tabela Q
try:
    with open(q_table_file, "rb") as file:
        q_table = pickle.load(file)
except FileNotFoundError:
    q_table = {}

alpha = 0.3  # Taxa de aprendizado
gamma = 0.9  # Fator de desconto
epsilon = 0.3  # Probabilidade inicial de explorar
epsilon_decay = 0.995

# Função para obter o estado
def get_state():
    delta_x = int((ball.centerx - paddle.centerx) // (WIDTH / state_space))
    ball_direction_x = 1 if ball_speed[0] > 0 else -1
    ball_direction_y = 1 if ball_speed[1] > 0 else -1
    return (delta_x, ball_direction_x, ball_direction_y)

# Escolher ação baseada na política epsilon-greedy
def choose_action(state):
    if np.random.rand() < epsilon:  # Exploração
        return np.random.choice(range(action_space))
    if state not in q_table:
        q_table[state] = np.zeros(action_space)
    return np.argmax(q_table[state])  # Exploração

# Atualizar a tabela Q
def update_q_table(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = np.zeros(action_space)
    if next_state not in q_table:
        q_table[next_state] = np.zeros(action_space)
    q_table[state][action] += alpha * (
        reward + gamma * np.max(q_table[next_state]) - q_table[state][action]
    )

# Função para salvar a tabela Q
def save_q_table():
    with open(q_table_file, "wb") as file:
        pickle.dump(q_table, file)

# Loop principal
running = True
while running:
    state = get_state()  # Obter estado atual
    action = choose_action(state)  # Escolher ação baseada na política

    # Aplicar ação
    if action == 0 and paddle.left > 0:  # Esquerda
        paddle.x -= PADDLE_SPEED
    elif action == 2 and paddle.right < WIDTH:  # Direita
        paddle.x += PADDLE_SPEED

    # Movimentar a bola
    ball.move_ip(ball_speed)

    # Rebater nas paredes
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Verificar colisão com a raquete
    if ball.colliderect(paddle) and ball_speed[1] > 0:
        ball_speed[1] = -ball_speed[1]
        score += 20  # Incrementar pontuação ao acertar a bola
        reward = 20
        ball_speed[0] += BALL_SPEED_INCREMENT if ball_speed[0] > 0 else -BALL_SPEED_INCREMENT
        ball_speed[1] += BALL_SPEED_INCREMENT if ball_speed[1] > 0 else -BALL_SPEED_INCREMENT
    elif ball.bottom >= HEIGHT:
        score -= 10  # Penalidade ao errar a bola
        reward = -10
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]
    else:
        reward = 1  # Recompensa leve por manter a bola em jogo

    # Atualizar a tabela Q
    next_state = get_state()
    update_q_table(state, action, reward, next_state)

    # Decaimento do epsilon
    epsilon = max(0.1, epsilon * epsilon_decay)

    # Renderizar o jogo
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_q_table()
            running = False

pygame.quit()
