import streamlit as st
import requests
import time

# Configuração da página
st.set_page_config(page_title="Envio de WhatsApp (Textos Longos)", page_icon="📱")

st.title("📱 Painel de Envio - CallMeBot")
st.write("Envie mensagens longas para o WhatsApp. O sistema dividirá o texto automaticamente para evitar cortes!")

st.markdown("---")

# Criando os campos da interface
telefone = st.text_input("Número de Telefone (com DDI e DDD)", value="553497660963")
api_key = st.text_input("Sua API Key", value="8977711", type="password")

# Área de texto para a mensagem
mensagem = st.text_area(
    "Digite sua mensagem (não se preocupe com o tamanho):", 
    height=300, 
    placeholder="Cole seu poema ou texto gigante aqui..."
)

def dividir_texto_em_blocos(texto, limite_caracteres=500):
    """
    Divide o texto em blocos menores respeitando as quebras de linha,
    para não cortar as palavras no meio.
    """
    linhas = texto.split('\n')
    blocos = []
    bloco_atual = ""

    for linha in linhas:
        # Se adicionar a próxima linha ultrapassar o limite, salva o bloco atual e começa um novo
        if len(bloco_atual) + len(linha) > limite_caracteres:
            if bloco_atual:
                blocos.append(bloco_atual.strip())
            bloco_atual = linha + "\n"
        else:
            bloco_atual += linha + "\n"
            
    # Adiciona o último bloco que sobrou
    if bloco_atual.strip():
        blocos.append(bloco_atual.strip())
        
    return blocos

# Botão de envio
if st.button("🚀 Enviar Mensagem"):
    if not telefone or not api_key or not mensagem:
        st.warning("⚠️ Por favor, preencha todos os campos antes de enviar.")
    else:
        # Divide a mensagem em partes seguras
        partes_mensagem = dividir_texto_em_blocos(mensagem, limite_caracteres=500)
        total_partes = len(partes_mensagem)
        
        st.info(f"O texto é grande e foi dividido em {total_partes} parte(s). Enviando...")
        
        # Cria uma barra de progresso no Streamlit
        barra_progresso = st.progress(0)
        
        sucesso_total = True
        
        for index, parte in enumerate(partes_mensagem):
            url = "https://api.callmebot.com/whatsapp.php"
            parametros = {
                "phone": telefone,
                "text": parte,
                "apikey": api_key
            }
            
            try:
                resposta = requests.get(url, params=parametros)
                
                if resposta.status_code == 200 and "Message to" in resposta.text:
                    # Atualiza a barra de progresso
                    progresso_atual = int(((index + 1) / total_partes) * 100)
                    barra_progresso.progress(progresso_atual)
                    
                    # Aguarda 2 segundos antes de enviar a próxima parte para a API não bloquear por spam e manter a ordem
                    if index < total_partes - 1:
                        time.sleep(2)
                else:
                    st.error(f"❌ Erro ao enviar a parte {index + 1}. Resposta: {resposta.text}")
                    sucesso_total = False
                    break # Para o envio se der erro em alguma parte
                    
            except Exception as e:
                st.error(f"❌ Ocorreu um erro na conexão na parte {index + 1}: {e}")
                sucesso_total = False
                break
                
        if sucesso_total:
            st.success("✅ Mensagem enviada com sucesso em sua totalidade!")
