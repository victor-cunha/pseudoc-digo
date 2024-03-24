                            
import pygame
import sys
import random

# Definição das cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definição dos tamanhos da janela e das peças
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 60
BLOCK_GAP = 10

# Lista de formas do Tangram (triângulos e quadrados)
SHAPES = [
    [(0, 0), (1, 0), (0.5, 1)],
    [(0, 0), (1, 0), (0.5, 1), (0.25, 1.25)],
    [(0, 0), (1, 0), (1, 1), (0, 1)],
    [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0.5)],
    [(0, 0), (1, 0), (1, 1), (0, 1), (0.5, 0), (0.5, 1)],
    [(0, 0), (1, 0), (1, 0.5), (0.5, 0.5), (0.5, 1), (0, 1)]
]

# Função para desenhar uma forma na tela
def draw_shape(surface, shape, position, color):
    points = [(int((point[0] + position[0]) * BLOCK_SIZE), int((point[1] + position[1]) * BLOCK_SIZE)) for point in shape]
    pygame.draw.polygon(surface, color, points)

# Função para verificar se um ponto está dentro de uma forma
def is_point_inside_shape(screen, point, shape, position):
    translated_points = [(point[0] - position[0] * BLOCK_SIZE, point[1] - position[1] * BLOCK_SIZE) for point in shape]
    return pygame.Rect(position[0] * BLOCK_SIZE, position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE).collidepoint(point) and pygame.draw.polygon(screen, GREEN, translated_points)

# Função para desenhar texto na tela
def draw_text(surface, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

# Função para criar um botão clicável
def draw_button(surface, text, rect, button_color, text_color, font):
    pygame.draw.rect(surface, button_color, rect)
    pygame.draw.rect(surface, BLACK, rect, 2)
    draw_text(surface, text, font, text_color, rect)

# Função para exibir a tela de início
def show_start_screen(screen, font_large, font):
    screen.fill(WHITE)
    draw_text(screen, "Jogo do Tangram", font_large, BLACK, screen.get_rect().center)
    draw_text(screen, "Clique para começar", font, BLACK, screen.get_rect().center + (0, 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Função para exibir a tela de início
def show_start_screen(screen, font_large, font):
    screen.fill(WHITE)
    text_large = font_large.render("Jogo do Tangram", True, BLACK)
    text_rect_large = text_large.get_rect(center=screen.get_rect().center)
    screen.blit(text_large, text_rect_large)

    text_small = font.render("Clique para começar", True, BLACK)
    text_rect_small = text_small.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text_small, text_rect_small)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


# Função principal do jogo
def main():
    # Inicialização do Pygame
    pygame.init()

    # Configuração da tela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Jogo do Tangram')

    # Fontes
    font_large = pygame.font.Font(None, 64)
    font = pygame.font.Font(None, 36)

    # Loop do jogo
    while True:
        # Mostrar tela de início
        show_start_screen(screen, font_large, font)

        # Variáveis de jogo
        score = 0
        time_remaining = 60  # 60 segundos
        level = 1
        shapes_per_level = 3  # Número de formas a serem colocadas corretamente por nível

        # Posição inicial das peças
        current_shapes = [random.choice(SHAPES) for _ in range(shapes_per_level)]
        current_positions = [(2 + i * 2, 2) for i in range(shapes_per_level)]

        # Retângulo para a área de jogo
        game_area_rect = pygame.Rect(50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)

        # Contador de tempo
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()

        # Loop principal do jogo
        while True:
            # Verificar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if game_area_rect.collidepoint(mouse_pos):
                        # Verifica se o clique do mouse está dentro da área de jogo
                        for i, (shape, position) in enumerate(zip(current_shapes, current_positions)):
                            if is_point_inside_shape(screen, mouse_pos, shape, position):

                                # Se estiver, aumenta a pontuação e verifica se o nível foi concluído
                                score += 1
                                if score % shapes_per_level == 0:
                                    level += 1
                                    current_shapes = [random.choice(SHAPES) for _ in range(shapes_per_level)]
                                    current_positions = [(2 + i * 2, 2) for i in range(shapes_per_level)]

            # Atualizar tempo
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            time_remaining = max(0, 60 - elapsed_time)

            if time_remaining <= 0:
                break  # Encerra o jogo se o tempo acabar

            # Limpar a tela
            screen.fill(WHITE)

            # Desenhar a borda da área de jogo
            pygame.draw.rect(screen, BLACK, game_area_rect, 5)

                        # Desenhar as formas atuais dentro da área de jogo
            for shape, position in zip(current_shapes, current_positions):
                draw_shape(screen, shape, position, RED)

            # Desenhar a pontuação, o tempo restante e o nível na tela
            draw_text(screen, f"Score: {score}", font, BLACK, pygame.Rect(10, 10, 150, 50))
            draw_text(screen, f"Time: {int(time_remaining)}", font, BLACK, pygame.Rect(SCREEN_WIDTH - 160, 10, 150, 50))
            draw_text(screen, f"Level: {level}", font, BLACK, pygame.Rect(10, SCREEN_HEIGHT - 40, 150, 50))

            # Atualizar a tela
            pygame.display.flip()

            # Definir a taxa de atualização da tela
            clock.tick(60)

        # Mostrar tela de fim de jogo
        show_game_over_screen(screen, font_large, font, score)

if __name__ == '__main__':
    main()




           










 

