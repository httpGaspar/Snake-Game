import os
import sys
from stable_baselines3 import PPO #Algoritmo de aprendizado por reforço
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from src.snake_env import SnakeEnv  # Substitua pelo caminho correto, se necessário.

# Definir constantes
MODEL_DIR = "models" #Diretorio onde os modelos serão salvos
TIMESTEPS = 1000000 #Número total de passos que o modelo executara durante o treinamento

# Criar o ambiente
env = SnakeEnv(render_mode='human')

# Verificar se o modelo deve ser treinado ou carregado
if len(sys.argv) > 1 and sys.argv[1] == "train":
    # Treinamento do modelo
    print("Iniciando treinamento...")
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
    
    # Salvar o modelo final
    final_model_path = os.path.join(MODEL_DIR, "final_model.zip")
    model.save(final_model_path)

    # Salvar também como latest_model.zip
    latest_model_path = os.path.join(MODEL_DIR, "latest_model.zip")
    model.save(latest_model_path)

    print(f"Treinamento concluído. Modelo salvo em: {final_model_path}")

else:
    # Carregar modelo existente
    model_path = os.path.join(MODEL_DIR, "latest_model.zip")
    if os.path.exists(model_path):
        print("Carregando modelo existente...")
        model = PPO.load(model_path, env=env)
    else:
        print("Modelo não encontrado. Treinamento necessário.")
        sys.exit(1)  # Sai do programa se não houver modelo

# Testar o modelo após o treinamento ou carregamento
print("Testando o modelo...")
obs = env.reset()
done = False
while not done:
    action, _ = model.predict(obs)
    obs, reward, done, info = env.step(action)
    env.render()  # Exibe a renderização do jogo

# Encerrar o ambiente
env.close()