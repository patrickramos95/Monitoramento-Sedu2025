import requests
from bs4 import BeautifulSoup
from telegram import Bot
import fitz  # PyMuPDF para ler o PDF

# Substitua pelos seus dados reais
TOKEN = '7710474497:AAEHhu5Smk89ac9pWLr4zkb3avjlH14TlJo'  # Token do bot
CHAT_ID = '778502491'  # Seu chat ID

# URL do Diário Oficial do ES
URL = 'https://ioes.dio.es.gov.br/portal/visualizacoes/diario_oficial'

# Palavras-chave para procurar no PDF
KEYWORDS = ['Agente de Suporte Educacional', 'Patrick Feu Ramos']

# Função para enviar mensagem no Telegram
def send_telegram_message(message):
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Função para extrair o texto do PDF
def extract_pdf_text(pdf_url):
    response = requests.get(pdf_url)
    with open("temp.pdf", 'wb') as f:
        f.write(response.content)

    # Abrir o PDF
    doc = fitz.open("temp.pdf")
    text = ""
    
    # Extrair texto de todas as páginas
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    return text

# Função para verificar se as palavras-chave estão no texto do PDF
def check_pdf_for_keywords(text):
    for keyword in KEYWORDS:
        if keyword.lower() in text.lower():
            send_telegram_message(f"Encontrado: '{keyword}' no Diário Oficial!")
            return True
    return False

# Função para buscar o link do PDF mais recente
def get_latest_pdf_link():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Procurar pelo link do PDF mais recente
    # A lógica aqui pode precisar de ajustes dependendo da estrutura da página
    pdf_link = soup.find('a', {'title': 'Visualizar Diário'})['href']
    return 'https://ioes.dio.es.gov.br' + pdf_link  # URL completa do PDF

# Função principal
def check_diario_oficial():
    pdf_url = get_latest_pdf_link()
    print(f"Baixando PDF: {pdf_url}")
    
    # Extrair texto do PDF
    text = extract_pdf_text(pdf_url)
    
    # Verificar se encontrou as palavras-chave
    if not check_pdf_for_keywords(text):
        send_telegram_message("Nenhuma palavra-chave encontrada no Diário Oficial.")
        print("Nenhuma palavra-chave encontrada.")
    else:
        print("Palavra-chave encontrada no PDF!")

# Rodar o script
check_diario_oficial()
