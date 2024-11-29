from stable_baselines3.common.env_checker import check_env
from src.snake_env import SnakeEnv

if __name__ == "__main__":
    env = SnakeEnv()
    check_env(env)
    print("Ambiente SnakeEnv validado com sucesso!")
