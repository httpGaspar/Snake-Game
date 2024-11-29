import pygame
import random

#inicializa o pygame
pygame.init()

#Dimensões da tela
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

#Cores
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255) 

#Configurando a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snack Game")

#Função principal
def main():
    #Posição inicial da cobra
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = (BLOCK_SIZE, 0)

    #Posição inicial da comida
    food = (random.randint(0, WIDTH // BLOCK_SIZE - 1)* BLOCK_SIZE,
            random.randint(0, HEIGHT // BLOCK_SIZE - 1)* BLOCK_SIZE)
    
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Controles da Cobra
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, BLOCK_SIZE):
            direction = (0, -BLOCK_SIZE)
        if keys[pygame.K_DOWN] and direction != (0, -BLOCK_SIZE):
            direction = (0, BLOCK_SIZE)
        if keys[pygame.K_LEFT] and direction != (BLOCK_SIZE, 0):
            direction = (-BLOCK_SIZE, 0)
        if keys[pygame.K_RIGHT] and direction != (-BLOCK_SIZE, 0):
            direction = (BLOCK_SIZE, 0)

        #Mover a cobra
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0,new_head)

        #Verificar colisão com a comida
        if snake[0] == food:
            food = (random.randint(0, WIDTH // BLOCK_SIZE - 1)* BLOCK_SIZE,
                     random.randint(0, HEIGHT// BLOCK_SIZE - 1)* BLOCK_SIZE)
            
        else:
            snake.pop()

        #Verificar colisões com paredes ou corpo
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:]):
            running = False

        #Renderizar a tela
        screen.fill(LIGHT_GREEN)
        pygame.draw.rect(screen, RED, (*food, BLOCK_SIZE, BLOCK_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, BLUE, (*segment, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()

        #Controlar a velocidade do jogo
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main() 