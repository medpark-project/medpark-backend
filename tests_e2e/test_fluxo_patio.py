import pytest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do URL do Frontend
FRONTEND_URL = "https://medpark-frontend.vercel.app"

# Tempo (em segundos) para o professor ler o que está acontecendo
DELAY = 2

@pytest.fixture(scope="module")
def driver():
    print("\n🍿 [SETUP] Abrindo o Firefox na sua tela...")
    
    service = FirefoxService(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()

    options.add_argument("--headless") 
    options.add_argument("--window-size=1920,1080")
    
    # --- MODO VISUAL ATIVADO ---
    # NÃO estamos usando --headless porque seu Firefox funciona!
    
    driver = webdriver.Firefox(service=service, options=options)
    driver.maximize_window()
    yield driver
    
    print("\n🏁 [TEARDOWN] Teste acabou. Fechando em 5 segundos...")
    time.sleep(5)
    driver.quit()

def test_fluxo_completo_patio(driver):
    # 1. LOGIN
    print("\n▶️ Passo 1: Acessando Sistema...")
    driver.get(FRONTEND_URL)
    time.sleep(DELAY)
    
    print("   Clicando em Login...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Employee Access')]"))
    ).click()
    time.sleep(1)
    
    print("   Digitando credenciais...")
    email = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "email")))
    email.send_keys("brunna@gmail.com")
    time.sleep(0.5)
    driver.find_element(By.ID, "password").send_keys("senha123")
    time.sleep(DELAY)
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    WebDriverWait(driver, 10).until(EC.url_contains("/dashboard"))
    print("✅ Login realizado!")
    time.sleep(DELAY)

    # 2. NAVEGAÇÃO
    print("\n▶️ Passo 2: Indo para o Pátio...")
    driver.get(f"{FRONTEND_URL}/patio-control")
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Patio Control")
    )
    print("✅ Página carregada!")
    time.sleep(DELAY)

    # 3. ENTRADA
    print("\n▶️ Passo 3: Registrando Entrada...")
    placa = "DEMO-FINAL"
    driver.find_element(By.ID, "licensePlate").send_keys(placa)
    time.sleep(1)
    
    print("   Clicando em Confirmar...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm Entry')]").click()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{placa}')]"))
    )
    print("✅ Veículo apareceu na tabela!")
    time.sleep(DELAY)

    # 4. SAÍDA
    print("\n▶️ Passo 4: Registrando Saída...")
    xpath_btn = f"//div[contains(text(), '{placa}')]/ancestor::tr//button[contains(text(), 'Register Exit')]"
    btn_saida = driver.find_element(By.XPATH, xpath_btn)
    
    # Scroll até o botão para garantir que ele está visível
    driver.execute_script("arguments[0].scrollIntoView(true);", btn_saida)
    time.sleep(1)
    
    btn_saida.click()
    
    # Espera Modal
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Total to Pay')]"))
    )
    print("✅ Modal aberto!")
    time.sleep(DELAY)
    
    # Pagar
    print("   Pagando...")
    # Tenta clicar no texto Cash ou no botão
    try:
        driver.find_element(By.XPATH, "//*[contains(text(), 'Cash')]").click()
    except:
        driver.execute_script("document.evaluate(\"//*[contains(text(), 'Cash')]\", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")
    
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Payment Received')]").click()
    
    # Sucesso
    time.sleep(DELAY)
    print("✅ Fluxo concluído com sucesso! 🚀")