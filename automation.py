from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re

def def_inicia_automacao():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def converter_seguidores(texto):
    texto = texto.lower().strip()
    texto = texto.replace("\xa0", " ")
    texto = texto.replace(",", ".")
    
    numero = re.findall(r"\d+\.?\d*", texto)
    
    if not numero:
        return 0
    
    numero = float(numero[0])
    
    if "mil" in texto or "k" in texto:
        return int(numero * 1_000)
    
    if "mi" in texto or "m" in texto:
        return int(numero * 1_000_000)
    
    texto_limpo = re.sub(r"[^\d]", "", texto)
    
    if texto_limpo.isdigit():
        return int(texto_limpo)
    
    return int(numero)


def def_busca_perfil(driver):
    
    if not os.path.exists("perfis.txt"):
        print("Arquivo perfis.txt não encontrado.")
        return
    
    with open("perfis.txt", "r", encoding="utf-8") as file:
        perfis = [linha.strip() for linha in file if linha.strip()]
    
    resultados = []
    
    for perfil in perfis:
        print(f"Acessando: {perfil}")
        driver.get(perfil)
        
        try:
            wait = WebDriverWait(driver, 15)
            
            # Procura texto que contenha "seguidores" ou "followers"
            elemento = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(),'seguidores') or contains(text(),'followers')]")
                )
            )
            
            texto_completo = elemento.text
            print(f"Texto encontrado: {texto_completo}")
            
            seguidores = converter_seguidores(texto_completo)
            
            print(f"Seguidores convertidos: {seguidores}")
        
        except Exception as e:
            seguidores = "Erro ou não encontrado"
            print("Não foi possível capturar seguidores.")
        
        resultados.append(f"{perfil} - {seguidores}")
        time.sleep(3)
    
    with open("resultado_seguidores.txt", "w", encoding="utf-8") as f:
        for linha in resultados:
            f.write(linha + "\n")
    
    print("Arquivo resultado_seguidores.txt criado com sucesso.")


# 🔥 EXECUÇÃO AUTOMÁTICA PARA TESTE NO JUPYTER
navegador = def_inicia_automacao()
def_busca_perfil(navegador)