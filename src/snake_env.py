import gym
from gym import spaces
import numpy as np
import pygame
import random


class SnakeEnv(gym.Env):
    def __init__(self, width=600, height=400, block_size=20, render_mode=None):
        super(SnakeEnv, self).__init__()

        # Configurações do ambiente
        self.width = width
        self.height = height
        self.block_size = block_size
        self.render_mode = render_mode 

        # Variáveis para renderização
        self.window = None
        self.clock = None

        # Ações: 4 direções (Cima, Baixo, Esquerda, Direita)
        self.action_space = spaces.Discrete(4)

        # Observação: estado representado por vetor (cobra, comida, direção)
        self.observation_space = spaces.Box(
            low=0,
            high=max(width, height),
            shape=(4,),
            dtype=np.int32
        )

        self.reset()

    #inicia ou reinicia o jogo
    def reset(self):
        # Estado inicial
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = (self.block_size, 0)
        self.food = self._random_food()
        self.done = False
        self.score = 0
        return self._get_state()
    
    #Implementa a Lógica do Jogo
    def step(self, action):
        # Atualizar direção com base na ação
        if action == 0:  # Cima
            if self.direction != (0, self.block_size):
                self.direction = (0, -self.block_size)
        elif action == 1:  # Baixo
            if self.direction != (0, -self.block_size):
                self.direction = (0, self.block_size)
        elif action == 2:  # Esquerda
            if self.direction != (self.block_size, 0):
                self.direction = (-self.block_size, 0)
        elif action == 3:  # Direita
            if self.direction != (-self.block_size, 0):
                self.direction = (self.block_size, 0)

        # Movimentar a cobra
        new_head = (self.snake[0][0] + self.direction[0],
                    self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)

        # Comer a comida
        if self.snake[0] == self.food:
            self.food = self._random_food()
            self.score += 1
            reward = 10
        else:
            self.snake.pop()
            reward = 0

        # Colisão com parede ou corpo
        if (self.snake[0][0] < 0 or self.snake[0][0] >= self.width or
            self.snake[0][1] < 0 or self.snake[0][1] >= self.height or
            self.snake[0] in self.snake[1:]):
            self.done = True
            reward = -10

        return self._get_state(), reward, self.done, {}
    
    #Inicia os gráficos do jogo
    def render(self):
        if self.render_mode is None:
            raise ValueError("Render mode is not set. Pass `render_mode` to the environment constructor.")
        
        #Inicializa a janela se não tiver sido criada
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Snake Environment")
            self.clock = pygame.time.Clock()

        #Desenha a Cobra e a Comida
        self.window.fill((255, 255, 255))
        for segment in self.snake: #Lista de BLocos representando a Cobra
            pygame.draw.rect(self.window, (0, 128, 0), (*segment, self.block_size, self.block_size))
        pygame.draw.rect(self.window, (255, 0, 0), (*self.food, self.block_size, self.block_size))
        pygame.display.flip()
        self.clock.tick(10) #atualixa a tela e deixa em 10 FPS

    #Fecha a janela do pygame e libera os recursos
    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
            self.clock = None

    #Retorna o estado atual como um vetor
    def _get_state(self):
        # Estado representado por posição da cobra e comida
        head_x, head_y = self.snake[0]
        food_x, food_y = self.food
        return np.array([head_x, head_y, food_x, food_y], dtype=np.int32)

    #Gera uma posição aleatória para a comida sem que colida com a cobra
    def _random_food(self):
        while True:
            food = (random.randint(0, self.width // self.block_size - 1) * self.block_size,
                    random.randint(0, self.height // self.block_size - 1) * self.block_size)
            if food not in self.snake:
                return food
