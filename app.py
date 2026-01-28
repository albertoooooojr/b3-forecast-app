import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt
import concurrent.futures
from datetime import datetime

st.set_page_config(page_title="B3 Stock Forecast", layout="wide")

# ============================
# Title
# ============================
st.markdown("## 📈 B3 (Brazil) Stock Forecast & RSI Scanner")
st.markdown("<sub>📈 Previsão de Ações da B3 (Brasil) com Scanner RSI Avançado</sub>", unsafe_allow_html=True)

# ============================
# Top Stocks & Small Caps
# ============================
blue_chips = {
    "ABEV3 - Ambev": "ABEV3",
    "ASAI3 - Assaí": "ASAI3",
    "AXIA3 - Axia Energia (ON)": "AXIA3",
    "AXIA6 - Axia Energia (PN B)": "AXIA6",
    "B3SA3 - B3": "B3SA3",
    "BBAS3 - Banco do Brasil": "BBAS3",
    "BBDC3 - Bradesco ON": "BBDC3",
    "BBDC4 - Bradesco PN": "BBDC4",
    "BBSE3 - BB Seguridade": "BBSE3",
    "BEEF3 - Minerva": "BEEF3",
    "BPAC11 - BTG Pactual": "BPAC11",
    "BRAP4 - Bradespar": "BRAP4",
    "CMIG4 - Cemig": "CMIG4",
    "CPFE3 - CPFL Energia": "CPFE3",
    "CPLE6 - Copel": "CPLE6",
    "CSAN3 - Cosan": "CSAN3",
    "CSNA3 - CSN": "CSNA3",
    "CYRE3 - Cyrela": "CYRE3",
    "DXCO3 - Dexco": "DXCO3",
    "EGIE3 - Engie Brasil": "EGIE3",
    "EMBR3 - Embraer": "EMBR3",
    "ENGI11 - Energisa": "ENGI11",
    "EQTL3 - Equatorial": "EQTL3",
    "EVEN3 - Even Construtora": "EVEN3",
    "GGBR4 - Gerdau": "GGBR4",
    "GOAU4 - Metalúrgica Gerdau": "GOAU4",
    "HAPV3 - Hapvida": "HAPV3",
    "HYPE3 - Hypera Pharma": "HYPE3",
    "IGTI11 - Iguatemi": "IGTI11",
    "ITSA4 - Itaúsa": "ITSA4",
    "ITUB4 - Itaú Unibanco": "ITUB4",
    "KLBN11 - Klabin": "KLBN11",
    "LREN3 - Lojas Renner": "LREN3",
    "MDIA3 - M. Dias Branco": "MDIA3",
    "MGLU3 - Magazine Luiza": "MGLU3",
    "MRVE3 - MRV": "MRVE3",
    "MULT3 - Multiplan": "MULT3",
    "PETR3 - Petrobras ON": "PETR3",
    "PETR4 - Petrobras PN": "PETR4",
    "PRIO3 - PetroRio": "PRIO3",
    "RADL3 - Raia Drogasil": "RADL3",
    "RAIL3 - Rumo": "RAIL3",
    "RAIZ4 - Raízen": "RAIZ4",
    "RENT3 - Localiza": "RENT3",
    "SANB11 - Santander": "SANB11",
    "SBSP3 - Sabesp": "SBSP3",
    "SLCE3 - SLC Agrícola": "SLCE3",
    "SMTO3 - São Martinho": "SMTO3",
    "SOMA3 - Grupo Soma": "SOMA3",
    "SUZB3 - Suzano": "SUZB3",
    "TAEE11 - Taesa": "TAEE11",
    "TGMA3 - Tegma": "TGMA3",
    "TIMS3 - TIM": "TIMS3",
    "TOTS3 - Totvs": "TOTS3",
    "UGPA3 - Ultrapar": "UGPA3",
    "USIM5 - Usiminas": "USIM5",
    "VALE3 - Vale": "VALE3",
    "VIVT3 - Telefônica": "VIVT3",
    "WEGE3 - WEG": "WEGE3",
    "YDUQ3 - YDUQS": "YDUQ3",
}

small_caps = {
    "Small Cap - 3TENTOS - TTEN3": "TTEN3",
    "Small Cap - ABC BRASIL - ABCB4": "ABCB4",
    "Small Cap - ALLOS - ALOS3": "ALOS3",
    "Small Cap - ALPARGATAS - ALPA4": "ALPA4",
    "Small Cap - ALUPAR - ALUP11": "ALUP11",
    "Small Cap - ANIMA - ANIM3": "ANIM3",
    "Small Cap - ARMAC - ARML3": "ARML3",
    "Small Cap - AUREN - AURE3": "AURE3",
    "Small Cap - AUTOMOB - AMOB3": "AMOB3",
    "Small Cap - AZZAS 2154 - AZZA3": "AZZA3",
    "Small Cap - BANCO PAN - BPAN4": "BPAN4",
    "Small Cap - BANRISUL - BRSR6": "BRSR6",
    "Small Cap - BEMOBI TECH - BMOB3": "BMOB3",
    "Small Cap - BLAU - BLAU3": "BLAU3",
    "Small Cap - BOA SAFRA - SOJA3": "SOJA3",
    "Small Cap - BR PARTNERS - BRBI11": "BRBI11",
    "Small Cap - BRASILAGRO - AGRO3": "AGRO3",
    "Small Cap - BRASKEM - BRKM5": "BRKM5",
    "Small Cap - BRAVA - BRAV3": "BRAV3",
    "Small Cap - CAMIL - CAML3": "CAML3",
    "Small Cap - CASAS BAHIA - BHIA3": "BHIA3",
    "Small Cap - CBA - CBAV3": "CBAV3",
    "Small Cap - CEA MODAS - CEAB3": "CEAB3",
    "Small Cap - COGNA ON - COGN3": "COGN3",
    "Small Cap - COPASA - CSMG3": "CSMG3",
    "Small Cap - CURY S/A - CURY3": "CURY3",
    "Small Cap - CVC BRASIL - CVCB3": "CVCB3",
    "Small Cap - CYRELA REALT - CYRE4": "CYRE4",
    "Small Cap - DESKTOP - DESK3": "DESK3",
    "Small Cap - DIMED - PNVL3": "PNVL3",
    "Small Cap - DIRECIONAL - DIRR3": "DIRR3",
    "Small Cap - ECORODOVIAS - ECOR3": "ECOR3",
    "Small Cap - EZTEC - EZTC3": "EZTC3",
    "Small Cap - FERBASA - FESA4": "FESA4",
    "Small Cap - FLEURY - FLRY3": "FLRY3",
    "Small Cap - FRAS-LE - FRAS3": "FRAS3",
    "Small Cap - GAFISA - GFSA3": "GFSA3",
    "Small Cap - GPS - GGPS3": "GGPS3",
    "Small Cap - GRENDENE - GRND3": "GRND3",
    "Small Cap - GRUPO MATEUS - GMAT3": "GMAT3",
    "Small Cap - GRUPO SBF - SBFG3": "SBFG3",
    "Small Cap - GUARARAPES - GUAR3": "GUAR3",
    "Small Cap - HELBOR - HBOR3": "HBOR3",
    "Small Cap - HIDROVIAS - HBSA3": "HBSA3",
    "Small Cap - IGUATEMI S.A - IGTI11": "IGTI11",
    "Small Cap - INTELBRAS - INTB3": "INTB3",
    "Small Cap - IOCHP-MAXION - MYPK3": "MYPK3",
    "Small Cap - IRANI - RANI3": "RANI3",
    "Small Cap - IRBBRASIL RE - IRBR3": "IRBR3",
    "Small Cap - JHSF PART - JHSF3": "JHSF3",
    "Small Cap - JSL - JSLG3": "JSLG3",
    "Small Cap - KEPLER WEBER - KEPL3": "KEPL3",
    "Small Cap - LAVVI - LAVV3": "LAVV3",
    "Small Cap - LOG COM PROP - LOGG3": "LOGG3",
    "Small Cap - LWSA - LWSA3": "LWSA3",
    "Small Cap - M.DIASBRANCO - MDIA3": "MDIA3",
    "Small Cap - MAGAZ LUIZA - MGLU3": "MGLU3",
    "Small Cap - MARCOPOLO - POMO4": "POMO4",
    "Small Cap - MELIUZ - CASH3": "CASH3",
    "Small Cap - METAL LEVE - LEVE3": "LEVE3",
    "Small Cap - MILLS - MILS3": "MILS3",
    "Small Cap - MOURA DUBEUX - MDNE3": "MDNE3",
    "Small Cap - MOVIDA - MOVI3": "MOVI3",
    "Small Cap - NATURA - NATU3": "NATU3",
    "Small Cap - ODONTOPREV - ODPV3": "ODPV3",
    "Small Cap - ONCOCLINICAS - ONCO3": "ONCO3",
    "Small Cap - ORIZON - ORVR3": "ORVR3",
    "Small Cap - P.ACUCAR-CBD - PCAR3": "PCAR3",
    "Small Cap - PAGUE MENOS - PGMN3": "PGMN3",
    "Small Cap - PETRORECSA - RECV3": "RECV3",
    "Small Cap - PETZCOBASI - AUAU3": "AUAU3",
    "Small Cap - PLANOEPLANO - PLPL3": "PLPL3",
    "Small Cap - POSITIVO TEC - POSI3": "POSI3",
    "Small Cap - PRINER - PRNR3": "PRNR3",
    "Small Cap - QUALICORP - QUAL3": "QUAL3",
    "Small Cap - QUERO-QUERO - LJQQ3": "LJQQ3",
    "Small Cap - RANDON PART - RAPT4": "RAPT4",
    "Small Cap - RECRUSUL - RCSL3": "RCSL3",
    "Small Cap - RECRUSUL - RCSL4": "RCSL4",
    "Small Cap - SANEPAR - SAPR11": "SAPR11",
    "Small Cap - SAO MARTINHO - SMTO3": "SMTO3",
    "Small Cap - SER EDUCA - SEER3": "SEER3",
    "Small Cap - SID NACIONAL - CSNA3": "CSNA3",
    "Small Cap - SIMPAR - SIMH3": "SIMH3",
    "Small Cap - SMART FIT - SMFT3": "SMFT3",
    "Small Cap - SYN PROP TEC - SYNE3": "SYNE3",
    "Small Cap - TEGMA - TGMA3": "TGMA3",
    "Small Cap - TENDA - TEND3": "TEND3",
    "Small Cap - TRACK FIELD - TFCO4": "TFCO4",
    "Small Cap - TUPY - TUPY3": "TUPY3",
    "Small Cap - UNIPAR - UNIP6": "UNIP6",
    "Small Cap - VALID - VLID3": "VLID3",
    "Small Cap - VAMOS - VAMO3": "VAMO3",
    "Small Cap - VIVARA S.A. - VIVA3": "VIVA3",
    "Small Cap - VULCABRAS - VULC3": "VULC3",
}

# Combinar todos os ativos
all_stocks = {**blue_chips, **small_caps}


# ============================
# RSI Function
# ============================
def calculate_rsi(series, window=14):
    """Calcula o Índice de Força Relativa (RSI)"""
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ============================
# Function to fetch and calculate RSI
# ============================
def fetch_rsi_data(name, code):
    """Busca dados e calcula RSI para um ativo"""
    try:
        df = yf.download(code + ".SA", period="6mo", interval="1d", progress=False)
        if df.empty or len(df) < 14:
            return None
        
        df["RSI"] = calculate_rsi(df["Close"])
        last_rsi = df["RSI"].iloc[-1]
        last_price = df["Close"].iloc[-1]
        
        status = ""
        if last_rsi >= 70:
            status = "🔴 Sobrecomprado"
        elif last_rsi <= 30:
            status = "🟢 Sobrevendido"
        
        if status:
            return {
                "Ativo": name,
                "Código": code,
                "RSI": round(last_rsi, 2),
                "Preço": round(last_price, 2),
                "Status": status
            }
    except Exception as e:
        pass
    
    return None


# ============================
# RSI Scanner - Parallel Processing
# ============================
st.subheader("🔎 RSI Scanner - Ações Sobrecompradas/Sobrevendidas")
st.markdown("<sub>🔎 Scanner RSI - Análise de Todos os Ativos (Blue Chips + Small Caps)</sub>", unsafe_allow_html=True)

# Filtro por tipo de ativo
col1, col2, col3 = st.columns(3)
with col1:
    show_blue_chips = st.checkbox("Blue Chips", value=True)
with col2:
    show_small_caps = st.checkbox("Small Caps", value=True)
with col3:
    scan_button = st.button("🔄 Atualizar Scanner RSI", use_container_width=True)

# Selecionar ativos a processar
stocks_to_scan = {}
if show_blue_chips:
    stocks_to_scan.update(blue_chips)
if show_small_caps:
    stocks_to_scan.update(small_caps)

if scan_button or len(stocks_to_scan) > 0:
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    # Usar processamento paralelo para melhor performance
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            executor.submit(fetch_rsi_data, name, code): (name, code)
            for name, code in stocks_to_scan.items()
        }
        
        completed = 0
        total = len(futures)
        
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            progress_bar.progress(completed / total)
            status_text.text(f"Processando: {completed}/{total} ativos...")
            
            result = future.result()
            if result:
                results.append(result)
    
    progress_bar.empty()
    status_text.empty()
    
    if results:
        # Ordenar por RSI (mais extremos primeiro)
        df_rsi = pd.DataFrame(results)
        df_rsi["Distância do Extremo"] = df_rsi["RSI"].apply(
            lambda x: min(abs(x - 70), abs(x - 30))
        )
        df_rsi = df_rsi.sort_values("Distância do Extremo").drop("Distância do Extremo", axis=1)
        
        # Exibir estatísticas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Ativos Analisados", len(stocks_to_scan))
        with col2:
            sobrecomprados = len(df_rsi[df_rsi["Status"] == "🔴 Sobrecomprado"])
            st.metric("Sobrecomprados (RSI ≥ 70)", sobrecomprados)
        with col3:
            sobrevendidos = len(df_rsi[df_rsi["Status"] == "🟢 Sobrevendido"])
            st.metric("Sobrevendidos (RSI ≤ 30)", sobrevendidos)
        with col4:
            st.metric("Oportunidades Encontradas", len(df_rsi))
        
        st.divider()
        
        # Exibir tabela com formatação
        st.dataframe(
            df_rsi.reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
            column_config={
                "RSI": st.column_config.NumberColumn(format="%.2f"),
                "Preço": st.column_config.NumberColumn(format="R$ %.2f"),
            }
        )
        
        # Download dos resultados
        csv = df_rsi.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Baixar Resultados (CSV)",
            data=csv,
            file_name=f"rsi_scanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Nenhum ativo sobrecomprado ou sobrevendido encontrado no momento.")

st.divider()

# ============================
# Select stock for detailed analysis
# ============================
st.subheader("📊 Análise Detalhada de Ativo")
st.markdown("<sub>📊 Selecione um ativo para visualizar gráficos e previsões</sub>", unsafe_allow_html=True)

stock_choice = st.selectbox("📌 Escolha um ativo para análise:", list(all_stocks.keys()))
ticker = all_stocks[stock_choice] + ".SA"

col1, col2 = st.columns(2)
with col1:
    future_days = st.slider("Dias para previsão:", 7, 90, 30)
with col2:
    rsi_window = st.slider("Período RSI:", 7, 28, 14)

data = yf.download(ticker, start="2020-01-01", progress=False)

if data.empty:
    st.error("❌ Não foi possível buscar dados para este ativo.")
else:
    data["RSI"] = calculate_rsi(data["Close"], window=rsi_window)
    
    # RSI Plot
    st.subheader(f"📉 RSI - {stock_choice}")
    st.markdown(f"<sub>RSI (Relative Strength Index / Índice de Força Relativa)</sub>", unsafe_allow_html=True)
    
    fig_rsi, ax_rsi = plt.subplots(figsize=(14, 5))
    ax_rsi.plot(data.index, data['RSI'], label='RSI', color='purple', linewidth=2)
    ax_rsi.axhline(70, color='red', linestyle='--', label='Sobrecomprado (70)', linewidth=1.5)
    ax_rsi.axhline(30, color='green', linestyle='--', label='Sobrevendido (30)', linewidth=1.5)
    ax_rsi.fill_between(data.index, 70, 100, alpha=0.1, color='red')
    ax_rsi.fill_between(data.index, 0, 30, alpha=0.1, color='green')
    ax_rsi.set_title(f"RSI - {stock_choice}", fontsize=14, fontweight='bold')
    ax_rsi.set_ylabel("RSI", fontsize=12)
    ax_rsi.set_xlabel("Data", fontsize=12)
    ax_rsi.legend(loc='best')
    ax_rsi.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_rsi)
    
    # Current RSI Value
    current_rsi = data["RSI"].iloc[-1]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("RSI Atual", f"{current_rsi:.2f}")
    with col2:
        st.metric("Preço Atual", f"R$ {data['Close'].iloc[-1]:.2f}")
    with col3:
        st.metric("Variação (30d)", f"{((data['Close'].iloc[-1] / data['Close'].iloc[-30] - 1) * 100):.2f}%")

    # Historical Closing Price
    st.subheader("📊 Preço de Fechamento Histórico")
    st.markdown("<sub>Evolução do preço nos últimos anos</sub>", unsafe_allow_html=True)
    
    fig_price, ax_price = plt.subplots(figsize=(14, 5))
    ax_price.plot(data.index, data['Close'], label='Preço de Fechamento', color='blue', linewidth=2)
    ax_price.fill_between(data.index, data['Close'], alpha=0.3, color='blue')
    ax_price.set_title(f"Preço de Fechamento - {stock_choice}", fontsize=14, fontweight='bold')
    ax_price.set_ylabel("Preço (R$)", fontsize=12)
    ax_price.set_xlabel("Data", fontsize=12)
    ax_price.legend(loc='best')
    ax_price.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_price)

    # Prophet Forecast
    st.subheader(f"🔮 Previsão para os próximos {future_days} dias")
    st.markdown(f"<sub>Previsão utilizando Prophet (Meta)</sub>", unsafe_allow_html=True)
    
    try:
        df_forecast = data.reset_index()[['Date', 'Close']].copy()
        df_forecast.columns = ['ds', 'y']
        
        model = Prophet(daily_seasonality=True, interval_width=0.95)
        model.fit(df_forecast)
        
        future = model.make_future_dataframe(periods=future_days)
        forecast = model.predict(future)
        
        fig1 = model.plot(forecast, figsize=(14, 6))
        fig1.suptitle(f"Previsão - {stock_choice}", fontsize=14, fontweight='bold', y=1.00)
        st.pyplot(fig1)
        
        # Forecast Components
        st.subheader("📉 Componentes da Previsão")
        st.markdown("<sub>Decomposição da série temporal</sub>", unsafe_allow_html=True)
        
        fig2 = model.plot_components(forecast, figsize=(14, 10))
        st.pyplot(fig2)
        
        # Próximas previsões
        st.subheader("📋 Próximas Previsões")
        forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(future_days).copy()
        forecast_display.columns = ['Data', 'Previsão', 'Limite Inferior', 'Limite Superior']
        forecast_display['Data'] = forecast_display['Data'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(
            forecast_display.reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Previsão": st.column_config.NumberColumn(format="R$ %.2f"),
                "Limite Inferior": st.column_config.NumberColumn(format="R$ %.2f"),
                "Limite Superior": st.column_config.NumberColumn(format="R$ %.2f"),
            }
        )
    except Exception as e:
        st.error(f"❌ Erro ao gerar previsão: {str(e)}")

st.divider()
st.markdown("<sub>⚠️ Aviso: Este aplicativo é apenas para fins informativos. Não constitui recomendação de investimento.</sub>", unsafe_allow_html=True)
