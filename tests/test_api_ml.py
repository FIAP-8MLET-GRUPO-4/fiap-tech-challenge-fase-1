import requests
import random
import time
import json

# URL da sua API (conforme você passou)
URL = "http://172.24.0.1:8000/api/v1/ml/predictions"

# Configuração
QTD_REQUISICOES = 30  # Quantas vezes vamos chamar a API
INTERVALO_SEGUNDOS = 1 # Tempo entre cada chamada para não travar o log

def gerar_flor_aleatoria():
    """
    Gera dados aleatórios, mas baseados nos perfis reais da Iris
    para não enviar dados sem sentido (como pétala negativa).
    """
    tipo = random.choice(['pequena', 'grande', 'media'])
    
    if tipo == 'pequena': # Perfil Setosa (baseado no seu Exemplo 1)
        return {
            "sepal_length": round(random.uniform(4.3, 5.8), 1),
            "sepal_width":  round(random.uniform(2.3, 4.4), 1),
            "petal_length": round(random.uniform(1.0, 1.9), 1),
            "petal_width":  round(random.uniform(0.1, 0.6), 1)
        }
    elif tipo == 'grande': # Perfil Virginica (baseado no seu Exemplo 2)
        return {
            "sepal_length": round(random.uniform(6.0, 7.9), 1),
            "sepal_width":  round(random.uniform(2.2, 3.8), 1),
            "petal_length": round(random.uniform(4.5, 6.9), 1),
            "petal_width":  round(random.uniform(1.4, 2.5), 1)
        }
    else: # Um perfil misto/aleatório
        return {
            "sepal_length": round(random.uniform(4.5, 8.0), 1),
            "sepal_width":  round(random.uniform(2.0, 4.5), 1),
            "petal_length": round(random.uniform(1.0, 7.0), 1),
            "petal_width":  round(random.uniform(0.1, 2.5), 1)
        }

print(f"--- Iniciando Teste de Carga na API: {URL} ---")

for i in range(1, QTD_REQUISICOES + 1):
    # 1. Gera os dados
    payload = gerar_flor_aleatoria()
    
    print(f"\n[Requisicao {i}] Enviando dados da flor:")
    print(json.dumps(payload, indent=2))

    try:
        # 2. Faz o POST para a API
        response = requests.post(URL, json=payload, timeout=5)
        
        # 3. Exibe o resultado
        if response.status_code == 200:
            print(f"✅ Sucesso! Resposta da API:")
            print(response.json()) # Aqui deve vir a predição da espécie
        else:
            print(f"❌ Erro {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Erro de Conexão: Verifique se o IP está correto e o container está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

    # Pausa para respirar
    time.sleep(INTERVALO_SEGUNDOS)

print("\n--- Teste Finalizado ---")