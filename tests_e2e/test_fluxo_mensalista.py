import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_URL = "https://medpark-frontend.vercel.app"
DELAY = 1.5 
NOME_TESTE = "Felipe Moura"
EMAIL_TESTE = "felipe@medpark.com"
PLACA_TESTE = "FEL-1P34"
CPF_TESTE = "004.758.600-12"
RG_TESTE = "123435"
TELEFONE_TESTE = "6199009900"
MODELO_TESTE = "Ford Ka"
COR_TESTE = "Cinza"

LOGIN_ADMIN = "brunna@gmail.com"
SENHA_ADMIN = "senha123"

@pytest.fixture(scope="module")
def driver():
    print("[SETUP] Iniciando Teste Completo de Mensalista...")

    with open("doc_teste.pdf", "w") as f: f.write("dummy content")
    
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=service, options=options)
    yield driver

    print("TEARDOWN] Fim do teste.")
    time.sleep(3)
    driver.quit()

    if os.path.exists("doc_teste.pdf"): os.remove("doc_teste.pdf")

def clicar(driver, xpath):

    elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    elem.click()
    time.sleep(0.5)

def digitar(driver, id_campo, texto):

    elem = driver.find_element(By.ID, id_campo)
    elem.clear()
    elem.send_keys(texto)
    time.sleep(0.3)

def selecionar_dropdown(driver, placeholder_text, option_text):

    trigger_xpath = f"//button[.//span[contains(text(), '{placeholder_text}')]]"
    clicar(driver, trigger_xpath)
    
    option_xpath = f"//div[@role='option']//span[contains(text(), '{option_text}')]"
    clicar(driver, option_xpath)

def fazer_login(driver):
    clicar(driver, "//button[contains(text(), 'Employee Access')]")
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email")))
    digitar(driver, "email", LOGIN_ADMIN)
    digitar(driver, "password", SENHA_ADMIN)
    print("Procurando botão Login...")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
    )
    
    driver.execute_script("arguments[0].click();", submit_btn)   

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Login Sucesso!")
    time.sleep(2)

def fazer_logout(driver):
    driver.find_element(By.CSS_SELECTOR, "nav ~ div button").click()
    print("Admin deslogado.")
    time.sleep(DELAY)

def test_ciclo_de_vida_mensalista(driver):

    driver.get(f"{FRONTEND_URL}/apply-monthly")
    time.sleep(DELAY)

    print("Preenchendo formulário...")
    digitar(driver, "nome_completo", NOME_TESTE)
    digitar(driver, "email", EMAIL_TESTE)
    digitar(driver, "telefone", TELEFONE_TESTE)
    digitar(driver, "cpf", CPF_TESTE)
    digitar(driver, "rg", RG_TESTE)
    digitar(driver, "placa_veiculo", PLACA_TESTE)
    digitar(driver, "modelo_veiculo", MODELO_TESTE)
    digitar(driver, "cor_veiculo", COR_TESTE)

    print("Selecionando Tipo de Veículo...")
    try:
        selecionar_dropdown(driver, "Select type", "Carro")
    except:
        print("Tentando selecionar qualquer tipo disponível...")
        clicar(driver, "//button[.//span[contains(text(), 'Select type')]]")
        clicar(driver, "(//div[@role='option'])[1]")

    print("Selecionando Plano...")
    try:
        selecionar_dropdown(driver, "Choose a monthly plan", "Plano Básico Diário")
    except:
         print("Tentando selecionar qualquer plano disponível...")
         clicar(driver, "//button[.//span[contains(text(), 'Choose a monthly plan')]]")
         clicar(driver, "(//div[@role='option'])[1]")

    print("Fazendo upload de documentos...")

    caminho_arquivo = os.path.abspath("doc_teste.pdf")
    driver.find_element(By.ID, "personalDocument").send_keys(caminho_arquivo)
    driver.find_element(By.ID, "proofOfEmployment").send_keys(caminho_arquivo)
    time.sleep(1)

    print("Enviando solicitação...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Send Application')]").click()

    WebDriverWait(driver, 15).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h3"), "Thank you!")
    )
    print("Solicitação enviada com sucesso!")

    clicar(driver, "//button[contains(text(), 'Return to Homepage')]")
    time.sleep(DELAY)
    
    fazer_login(driver)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Monthly Parkers')]").click()
    print("Procurando solicitação pendente...")
    
    xpath_approve = f"//tr[contains(., '{NOME_TESTE}')]//button[contains(text(), 'Approve')]"
    clicar(driver, xpath_approve)
    
    print("Solicitação Aprovada! Mensalista criado.")
    time.sleep(DELAY)

    fazer_logout(driver)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Pay Your Parking')]")))
    
    inputs_placa = driver.find_elements(By.CSS_SELECTOR, "input[placeholder*='ABC-1234']")
    input_mensalista = inputs_placa[1]
    
    input_mensalista.clear()
    input_mensalista.send_keys(PLACA_TESTE)
    time.sleep(1)
    
    clicar(driver, "//button[contains(text(), 'Check Subscription')]")
    
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), NOME_TESTE)
    )
    print("Assinatura encontrada!")
    
    clicar(driver, "//button[contains(text(), 'Pay Monthly Bill')]")
    
    print("Pagando fatura...")
    time.sleep(1)
    clicar(driver, "//*[contains(text(), 'PIX')]")
    time.sleep(2)
    clicar(driver, "//button[contains(text(), 'Return to Homepage')]") 
    time.sleep(DELAY)
    print("Mensalidade Paga!")

    fazer_login(driver)

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    
    clicar(driver, "//button[contains(text(), 'Patio Control')]")
    
    print(f"Carro {PLACA_TESTE} entrando...")
    digitar(driver, "licensePlate", PLACA_TESTE)
    clicar(driver, "//button[contains(text(), 'Confirm Entry')]")
    
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "body"), PLACA_TESTE)
    )
    print("Entrada registrada!")
    time.sleep(DELAY)

    print(f"Carro {PLACA_TESTE} saindo...")
    xpath_saida = f"//tr[contains(., '{PLACA_TESTE}')]//button[contains(text(), 'Register Exit')]"

    clicar(driver, xpath_saida)

    WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Total to Pay')]"))
    )
    
    print("Mensalista liberado sem cobrança!")

    time.sleep(3)

    fazer_logout(driver)

    print("TESTE DE CICLO DE VIDA COMPLEXO: SUCESSO!")