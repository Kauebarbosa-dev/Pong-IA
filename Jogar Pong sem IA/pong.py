import pygame
import random
import sys
import time

# Configurações do jogo
WIDTH, HEIGHT = 800, 600
BALL_SPEED_INCREMENT = 0.05  # Incremento mínimo de velocidade
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

# Pontuação e vidas
score = 0
lives = 3

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

    # Movimentar a raquete
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-PADDLE_SPEED, 0)
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.move_ip(PADDLE_SPEED, 0)

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

    # Verificar se a bola caiu
    if ball.bottom >= HEIGHT:
        lives -= 1  # Perde uma vida
        reset_ball()
        if lives <= 0:
            game_over()

    # Renderizar
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Exibir pontuação
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Exibir vidas
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
