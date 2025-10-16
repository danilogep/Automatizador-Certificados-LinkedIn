import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys # Importa a classe Keys

# ==============================================================================
# --- ÁREA DE DADOS ---
# ==============================================================================

# --- IMPORTAÇÃO DA CONSTANTE ---
from DADOS_CERTIFICADOS import DADOS_CERTIFICADOS

MAPA_MESES = {
    'JAN': 'Janeiro', 'FEV': 'Fevereiro', 'MAR': 'Março', 'ABR': 'Abril',
    'MAI': 'Maio', 'JUN': 'Junho', 'JUL': 'Julho', 'AGO': 'Agosto',
    'SET': 'Setembro', 'OUT': 'Outubro', 'NOV': 'Novembro', 'DEZ': 'Dezembro'
}

def parse_certificate_data(raw_data):
    """Processa a string de dados brutos e extrai nome, mês, ano e competência."""
    parsed_list = []
    lines = [line.strip() for line in raw_data.strip().split('\n') if line.strip()]
    for line in lines:
        match = re.search(r'Turma\s+([A-Z]{3})/(\d{4})\s+-\s+(.*)', line, re.IGNORECASE)
        if match:
            mes_abbr, ano_emissao, competencia = match.group(1).upper(), match.group(2), match.group(3).strip()
            mes_emissao = MAPA_MESES.get(mes_abbr, '')
            nome_curso = line[:match.start()].strip().lstrip('·').strip()
            if nome_curso and mes_emissao and ano_emissao and competencia:
                parsed_list.append({"nome": nome_curso, "mes": mes_emissao, "ano": ano_emissao, "competencia": competencia})
        else:
            print(f"AVISO: Não foi possível processar a linha: '{line}'")
    return parsed_list

# ==============================================================================
# --- INÍCIO DO SCRIPT DE AUTOMAÇÃO ---
# ==============================================================================

if __name__ == "__main__":
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(">>> Conectado com sucesso ao navegador já aberto!")
        wait = WebDriverWait(driver, 20)

        certificados = parse_certificate_data(DADOS_CERTIFICADOS)
        total_certificados = len(certificados)
        print(f"Encontrados {total_certificados} certificados para adicionar.")
        
        PROFILE_URL = "https://www.linkedin.com/in/danilo-evangelista-a63570335/"
        ADD_CERTIFICATION_URL = PROFILE_URL + "edit/forms/certification/new/"

        input("Pressione Enter para iniciar o processo de adição no LinkedIn...")

        for i, cert in enumerate(certificados):
            print(f"\n--- Processando certificado ({i+1}/{total_certificados}): {cert['nome']} ---")
            
            try:
                print("  - Navegando diretamente para a página de adição...")
                driver.get(ADD_CERTIFICATION_URL)
                
                print("  - Aguardando o formulário de adição carregar...")
                wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Adicionar licença ou certificado']")))
                print("  - Formulário carregado.")
                time.sleep(2)
                
                print("  - Preenchendo campos básicos...")
                campo_nome = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Ex.: Microsoft Certified Network Associate Security']")))
                campo_nome.send_keys(cert['nome'])
                
                campo_org = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Ex.: Microsoft']")))
                campo_org.send_keys("Enap")
                time.sleep(2.5)
                campo_org.send_keys(Keys.ARROW_DOWN)
                time.sleep(1)
                campo_org.send_keys(Keys.ENTER)
                
                select_mes_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='month']")))
                Select(select_mes_element).select_by_visible_text(cert['mes'])
                
                select_ano_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//select[@name='year']")))
                Select(select_ano_element).select_by_visible_text(cert['ano'])
                
                print("  - Campos básicos preenchidos.")

                # --- LÓGICA FINAL E DEFINITIVA PARA ADICIONAR COMPETÊNCIA ---
                print(f"  - Adicionando competência: {cert['competencia']}...")
                try:
                    botao_add_competencia = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Adicionar competência')]")))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_add_competencia)
                    time.sleep(1)
                    botao_add_competencia.click()

                    # Seletor Definitivo baseado no HTML que você forneceu
                    campo_competencia = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Competência (ex.: Gestão de projetos)']")))
                    campo_competencia.send_keys(cert['competencia'])
                    time.sleep(2.5)

                    # Usa a mesma técnica de teclado que funcionou para a organização
                    campo_competencia.send_keys(Keys.ARROW_DOWN)
                    time.sleep(1)
                    campo_competencia.send_keys(Keys.ENTER)
                    print("  - Competência adicionada com sucesso.")
                except Exception as skill_e:
                    print(f"  - AVISO: Não foi possível adicionar a competência. Erro: {skill_e}")
                # --- FIM DA LÓGICA FINAL ---

                botao_salvar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Salvar']]")))
                botao_salvar.click()
                print("  - Certificado salvo no LinkedIn!")
                
                try:
                    botao_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Pular']] | //button[span[text()='Avançar']]")))
                    botao_final.click()
                    print("  - Popup de compartilhamento fechado.")
                except TimeoutException:
                    print("  - AVISO: Popup de compartilhamento não encontrado, seguindo para o próximo.")

            except Exception as e:
                print(f"  - ERRO ao processar o certificado '{cert['nome']}': {e}")
                driver.get(PROFILE_URL)
                time.sleep(5)
            
            print("Aguardando 10 segundos antes do próximo...")
            time.sleep(10)

    except Exception as e:
        print(f"\nOcorreu um erro geral no script: {e}")
    
    finally:
        print("\n--- Automação finalizada! ---")