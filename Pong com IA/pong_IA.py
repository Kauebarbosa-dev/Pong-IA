import pygame
import random
import sys
import time
import numpy as np

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
BALL_SPEED_INCREMENT = 0.1  # Incremento maior de velocidade
PADDLE_SPEED = 8
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong com IA")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Raquete
paddle = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 20, 100, 10)
# Bola
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]

# Pontuação
score = 0

# Q-Learning: Tabela Q
state_space = 20  # Aumento no número de estados
action_space = 3  # 3 ações: esquerda, direita, parado
q_table = np.zeros((state_space, action_space))  # Tabela Q inicializada com 0
alpha = 0.3  # Aumento na taxa de aprendizado
gamma = 0.95  # Aumento no fator de desconto
epsilon = 0.5  # Alta exploração no começo

# Função para obter o estado (simplificação)
def get_state():
    """Retorna um estado baseado na posição da bola e da raquete."""
    ball_x, ball_y = ball.center
    paddle_x = paddle.centerx
    
    # Vamos simplificar o estado mapeando a posição da bola e da raquete em um intervalo
    state = int(ball_x // (WIDTH / state_space))  # Divide o campo em mais "faixas" de X
    return state

# Função para escolher a ação da IA (baseada na política epsilon-greedy)
def choose_action(state):
    """Escolhe uma ação baseada na tabela Q usando a política epsilon-greedy."""
    if random.uniform(0, 1) < epsilon:
        return random.choice([0, 1, 2])  # Exploração: escolha aleatória
    else:
        return np.argmax(q_table[state])  # Exploração: escolha com maior Q-valor

# Função para atualizar a tabela Q
def update_q_table(state, action, reward, next_state):
    """Atualiza a tabela Q com base na fórmula do Q-Learning."""
    best_next_action = np.argmax(q_table[next_state])
    q_table[state, action] = q_table[state, action] + alpha * (reward + gamma * q_table[next_state, best_next_action] - q_table[state, action])

def reset_ball():
    """Reinicia a posição da bola e define uma nova direção."""
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed[0] = random.choice([-4, 4])
    ball_speed[1] = random.choice([-4, 4])

def game_over():
    """Exibe mensagem de 'Game Over' e o score final, depois encerra o jogo."""
    screen.fill(BLACK)
    
    # Mensagem de Game Over
    game_over_text = font.render("GAME OVER", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Exibir o score final
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(final_score_text, final_score_rect)

    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    sys.exit()

# Loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # IA decide o movimento
    state = get_state()
    action = choose_action(state)

    # Mover a raquete com base na ação escolhida
    if action == 0 and paddle.left > 0:
        paddle.move_ip(-PADDLE_SPEED, 0)  # Mover para a esquerda
    elif action == 1 and paddle.right < WIDTH:
        paddle.move_ip(PADDLE_SPEED, 0)  # Mover para a direita
    # Ação 2: Ficar parado (sem movimento)

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
        score += 10  # Ganha pontos por rebater a bola
        
        # Aumentar velocidade da bola minimamente
        ball_speed[0] += BALL_SPEED_INCREMENT if ball_speed[0] > 0 else -BALL_SPEED_INCREMENT
        ball_speed[1] += BALL_SPEED_INCREMENT if ball_speed[1] > 0 else -BALL_SPEED_INCREMENT

        reward = 20  # Recompensa positiva por acerto
    else:
        reward = -5  # Penalização por erro (bola caindo), perde 5 pontos

    # Atualizar a tabela Q
    next_state = get_state()
    update_q_table(state, action, reward, next_state)

    # Verificar se a bola caiu e reiniciar
    if ball.bottom >= HEIGHT:
        reset_ball()

    # Renderizar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Exibir pontuação
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
