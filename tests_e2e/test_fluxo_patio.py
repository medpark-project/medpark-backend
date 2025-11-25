import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FRONTEND_URL = "https://medpark-frontend.vercel.app" 
LOGIN_ADMIN = "brunna@gmail.com"
SENHA_ADMIN = "senha123"
PLACA_TESTE1 = "TES-2T34"
PLACA_TESTE2 = "TES-9999"
PLACA_TESTE3 = "TES-9090"

@pytest.fixture(scope="module")
def driver():
    print("\nIniciando Chrome...")
    
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    
    print("\nTeste finalizado. Fechando em 5 segundos...")
    time.sleep(5)
    driver.quit()

def test_fluxo_visual(driver):
    
    driver.get(FRONTEND_URL)
    time.sleep(2)
    
    print("Clicando no Login...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Employee Access')]").click()
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "email")))
    
    print("Digitando credenciais...")
    driver.find_element(By.ID, "email").send_keys(LOGIN_ADMIN)
    time.sleep(1)
    driver.find_element(By.ID, "password").send_keys(SENHA_ADMIN)
    time.sleep(1)
    
    print("Procurando botão Login...")
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Login')]"))
    )
    
    driver.execute_script("arguments[0].click();", submit_btn)   

    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("Login Sucesso!")
    time.sleep(2)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Patio Control')]").click()
    WebDriverWait(driver, 10).until(EC.url_contains("/patio-control"))
    print("Entrou no Pátio!")
    time.sleep(2)

    driver.find_element(By.ID, "licensePlate").send_keys(PLACA_TESTE1)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Entry')]").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{PLACA_TESTE1}')]"))
    )
    print("Entrada 1 Registrada!")
    time.sleep(2)

    driver.find_element(By.ID, "licensePlate").send_keys(PLACA_TESTE2)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Entry')]").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{PLACA_TESTE2}')]"))
    )
    print("Entrada 2 Registrada!")
    time.sleep(2)

    driver.find_element(By.ID, "licensePlate").send_keys(PLACA_TESTE3)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Entry')]").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{PLACA_TESTE3}')]"))
    )
    print("Entrada 3 Registrada!")
    time.sleep(2)

    print("Tentando registrar saída da PLACA_TESTE1...")

    xpath_btn = f"//tr[contains(., '{PLACA_TESTE1}')]//button[contains(text(), 'Register Exit')]"
    
    btn_saida = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath_btn))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", btn_saida)
    time.sleep(1)
    btn_saida.click()
    
    driver.find_element(By.XPATH, "//*[contains(text(), 'Cash')]").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//*[contains(text(), 'Payment Received - Open Gate')]").click()
    
    print(f"{PLACA_TESTE1} pago via dinheiro com sucesso.")
    time.sleep(3)
    
    driver.find_element(By.CSS_SELECTOR, "nav ~ div button").click()

    print("Admin deslogado.")
    time.sleep(2)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Pay Your Parking')]")))
    
    input_home = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Enter license plate']")
    input_home.clear()
    input_home.send_keys(PLACA_TESTE2)
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Check Ticket')]").click()
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'Payment Details')]")))
    print("Detalhes do ticket carregados.")

    driver.find_element(By.XPATH, "//button[contains(text(), 'Pay Now')]").click()

    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Select Your Payment Method')]")))
    
    print("Selecionando PIX...")
    driver.find_element(By.XPATH, "//*[contains(text(), 'PIX')]").click()

    print("Aguardando validação bancária simulada...")
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Payment Successful')]")))

    driver.find_element(By.XPATH, "//button[contains(text(), 'Return to Homepage')]").click()
    print(f"{PLACA_TESTE2} pago via PIX com sucesso.")
    time.sleep(1)

    input_home = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='Enter license plate']")
    input_home.clear()
    input_home.send_keys(PLACA_TESTE3)
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Check Ticket')]").click()
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), 'Payment Details')]")))
    driver.find_element(By.XPATH, "//button[contains(text(), 'Pay Now')]").click()
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Select Your Payment Method')]")))
    
    print("Selecionando Cartão de Crédito...")
    driver.find_element(By.XPATH, "//*[contains(text(), 'Credit / Debit Card')]").click()

    print("Preenchendo dados do cartão...")
    time.sleep(1)
    driver.find_element(By.ID, "cardNumber").send_keys("4111111111111111")
    driver.find_element(By.ID, "nameOnCard").send_keys("SELENIUM TESTER")
    driver.find_element(By.ID, "expiryDate").send_keys("12/30")
    driver.find_element(By.ID, "cvc").send_keys("123")
    
    time.sleep(1)

    btn_pagar_cartao = driver.find_element(By.XPATH, "//button[contains(text(), 'Pay R$')]")
    btn_pagar_cartao.click()

    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Payment Successful')]")))
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Return to Homepage')]").click()
    print(f"{PLACA_TESTE3} pago via Cartão com sucesso.")

    print("TODOS OS CENÁRIOS CONCLUÍDOS COM SUCESSO!")