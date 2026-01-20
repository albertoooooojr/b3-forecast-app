import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import matplotlib.pyplot as plt

st.set_page_config(page_title="B3 Stock Forecast", layout="centered")

# ============================
# Title
# ============================
st.markdown("## 📈 B3 (Brazil) Stock Forecast")
st.markdown("<sub>📈 Previsão de Ações da B3 (Brasil)</sub>", unsafe_allow_html=True)

# ============================
# Top Stocks
# ============================
top_stocks = {
    "RRRP3 - 3R Petroleum": "RRRP3",
    "ABCB4 - ABC Brasil": "ABCB4",
    "AERI3 - Aeris": "AERI3",
    "ALSO3 - Aliansce Sonae": "ALSO3",
    "ALPA4 - Alpargatas": "ALPA4",
    "ALUP11 - Alupar": "ALUP11",
    "AMBP3 - Ambipar": "AMBP3",
    "ABEV3 - Ambev": "ABEV3",
    "ANIM3 - Ânima": "ANIM3",
    "ARML3 - Armac": "ARML3",
    "ASAI3 - Assaí": "ASAI3",
    "AURE3 - Auren Energia": "AURE3",
    "AZUL4 - Azul": "AZUL4",
    "B3SA3 - B3": "B3SA3",
    "BBAS3 - Banco do Brasil": "BBAS3",
    "BPAN4 - Banco Pan": "BPAN4",
    "BRSR6 - Banrisul": "BRSR6",
    "BBSE3 - BB Seguridade": "BBSE3",
    "BLAU3 - Blau Farmacêutica": "BLAU3",
    "BMGB4 - BMG": "BMGB4",
    "BRBI11 - BR Partners": "BRBI11",
    "BBDC3 - Bradesco ON": "BBDC3",
    "BBDC4 - Bradesco PN": "BBDC4",
    "BRAP4 - Bradespar": "BRAP4",
    "BRFS3 - BRF": "BRFS3",
    "BRKM5 - Braskem": "BRKM5",
    "AGRO3 - BrasilAgro": "AGRO3",
    "BPAC11 - BTG Pactual": "BPAC11",
    "CEAB3 - C&A Modas": "CEAB3",
    "CAML3 - Camil": "CAML3",
    "BHIA3 - Casas Bahia": "BHIA3",
    "CBAV3 - CBA": "CBAV3",
    "CCRO3 - CCR": "CCRO3",
    "CMIG4 - Cemig": "CMIG4",
    "COGN3 - Cogna": "COGN3",
    "CSMG3 - Copasa": "CSMG3",
    "CPLE6 - Copel": "CPLE6",
    "CSAN3 - Cosan": "CSAN3",
    "CPFE3 - CPFL Energia": "CPFE3",
    "CSNA3 - CSN": "CSNA3",
    "CMIN3 - CSN Mineração": "CMIN3",
    "CURY3 - Cury": "CURY3",
    "CVCB3 - CVC": "CVCB3",
    "CYRE3 - Cyrela": "CYRE3",
    "DXCO3 - Dexco": "DXCO3",
    "ECOR3 - Ecorodovias": "ECOR3",
    "ELET3 - Eletrobras ON": "ELET3",
    "ELET6 - Eletrobras PN": "ELET6",
    "ELMD3 - Eletromidia": "ELMD3",
    "EMBR3 - Embraer": "EMBR3",
    "ENGI11 - Energisa": "ENGI11",
    "EGIE3 - Engie Brasil": "EGIE3",
    "ENEV3 - Eneva": "ENEV3",
    "EQTL3 - Equatorial": "EQTL3",
    "EVEN3 - Even Construtora": "EVEN3",
    "EZTC3 - EZTEC": "EZTC3",
    "FESA4 - Ferbasa": "FESA4",
    "FLRY3 - Fleury": "FLRY3",
    "FRAS3 - Fras-le": "FRAS3",
    "GFSA3 - Gafisa": "GFSA3",
    "GGBR4 - Gerdau": "GGBR4",
    "GOLL4 - Gol": "GOLL4",
    "GRND3 - Grendene": "GRND3",
    "SBFG3 - Grupo SBF": "SBFG3",
    "SOMA3 - Grupo Soma": "SOMA3",
    "GUAR3 - Guararapes": "GUAR3",
    "GGPS3 - GPS": "GGPS3",
    "HAPV3 - Hapvida": "HAPV3",
    "HBRE3 - HBR Realty": "HBRE3",
    "HBSA3 - Hidrovias do Brasil": "HBSA3",
    "HYPE3 - Hypera Pharma": "HYPE3",
    "IGTI11 - Iguatemi": "IGTI11",
    "INTB3 - Intelbras": "INTB3",
    "RANI3 - Irani": "RANI3",
    "IRBR3 - IRB Brasil RE": "IRBR3",
    "ITSA4 - Itaúsa": "ITSA4",
    "ITUB4 - Itaú Unibanco": "ITUB4",
    "JALL3 - Jalles Machado": "JALL3",
    "JBSS3 - JBS": "JBSS3",
    "JHSF3 - JHSF": "JHSF3",
    "JSLG3 - JSL": "JSLG3",
    "KEPL3 - Kepler Weber": "KEPL3",
    "KLBN11 - Klabin": "KLBN11",
    "LAVV3 - Lavvi": "LAVV3",
    "LEVE3 - Mahle-Metal Leve": "LEVE3",
    "RENT3 - Localiza": "RENT3",
    "LOGN3 - Log-In": "LOGN3",
    "LJQQ3 - Lojas Quero-Quero": "LJQQ3",
    "LREN3 - Lojas Renner": "LREN3",
    "LWSA3 - LWSA": "LWSA3",
    "MDIA3 - M. Dias Branco": "MDIA3",
    "MGLU3 - Magazine Luiza": "MGLU3",
    "POMO4 - Marcopolo": "POMO4",
    "MRFG3 - Marfrig": "MRFG3",
    "CASH3 - Méliuz": "CASH3",
    "GOAU4 - Metalúrgica Gerdau": "GOAU4",
    "MILS3 - Mills": "MILS3",
    "BEEF3 - Minerva": "BEEF3",
    "MTRE3 - Mitre": "MTRE3",
    "MDNE3 - Moura Dubeux": "MDNE3",
    "MOVI3 - Movida": "MOVI3",
    "MRVE3 - MRV": "MRVE3",
    "MULT3 - Multiplan": "MULT3",
    "NGRD3 - Neogrid": "NGRD3",
    "OPCT3 - Oceanpact": "OPCT3",
    "ONCO3 - Oncoclínicas": "ONCO3",
    "ORVR3 - Orizon": "ORVR3",
    "PGMN3 - Pague Menos": "PGMN3",
    "PCAR3 - Pão de Açúcar": "PCAR3",
    "PETR3 - Petrobras ON": "PETR3",
    "PETR4 - Petrobras PN": "PETR4",
    "PRIO3 - PetroRio": "PRIO3",
    "RECV3 - Petrorecôncavo": "RECV3",
    "PLPL3 - Plano & Plano": "PLPL3",
    "PSSA3 - Porto Seguro": "PSSA3",
    "POSI3 - Positivo": "POSI3",
    "PRNR3 - Priner": "PRNR3",
    "RADL3 - Raia Drogasil": "RADL3",
    "RAIZ4 - Raízen": "RAIZ4",
    "RAPT4 - Randon": "RAPT4",
    "RCSL4 - Recrusul": "RCSL4",
    "RDOR3 - Rede D'Or": "RDOR3",
    "RAIL3 - Rumo": "RAIL3",
    "SBSP3 - Sabesp": "SBSP3",
    "SANB11 - Santander": "SANB11",
    "SAPR11 - Sanepar": "SAPR11",
    "STBP3 - Santos Brasil": "STBP3",
    "SMTO3 - São Martinho": "SMTO3",
    "SEER3 - Ser Educacional": "SEER3",
    "SIMH3 - Simpar": "SIMH3",
    "SLCE3 - SLC Agrícola": "SLCE3",
    "SMFT3 - Smartfit": "SMFT3",
    "SUZB3 - Suzano": "SUZB3",
    "TAEE11 - Taesa": "TAEE11",
    "TGMA3 - Tegma": "TGMA3",
    "VIVT3 - Telefônica": "VIVT3",
    "TEND3 - Tenda": "TEND3",
    "TIMS3 - TIM": "TIMS3",
    "TOTS3 - Totvs": "TOTS3",
    "TFCO4 - Track & Field": "TFCO4",
    "TRIS3 - Trisul": "TRIS3",
    "TUPY3 - Tupy": "TUPY3",
    "UGPA3 - Ultrapar": "UGPA3",
    "UNIP6 - Unipar": "UNIP6",
    "USIM5 - Usiminas": "USIM5",
    "VALE3 - Vale": "VALE3",
    "VLID3 - Valid": "VLID3",
    "VAMO3 - Vamos": "VAMO3",
    "VBBR3 - Vibra Energia": "VBBR3",
    "VIVA3 - Vivara": "VIVA3",
    "VVEO3 - Viveo": "VVEO3",
    "VULC3 - Vulcabras": "VULC3",
    "WEGE3 - WEG": "WEGE3",
    "YDUQ3 - YDUQS": "YDUQ3",
    "ZAMP3 - Zamp": "ZAMP3"
}


# ============================
# RSI Function
# ============================
def calculate_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# ============================
# RSI Scanner
# ============================
st.subheader("🔎 RSI Scanner - Overbought/oversold stocks")
st.markdown("<sub>🔎 Scanner RSI - Ações Sobrecompradas/Sobrevendidas</sub>", unsafe_allow_html=True)

results = []
for name, code in list(top_stocks.items())[:35]:  # first 35 for performance
    try:
        df = yf.download(code + ".SA", period="6mo", interval="1d", progress=False)
        if df.empty:
            continue
        df["RSI"] = calculate_rsi(df["Close"])
        last_rsi = df["RSI"].iloc[-1]
        status = ""
        if last_rsi >= 70:
            status = "🔴 Overbought"
        elif last_rsi <= 30:
            status = "🟢 Oversold"
        if status:
            results.append([name, round(last_rsi, 2), status])
    except:
        continue

df_rsi = pd.DataFrame(results, columns=["Stock", "RSI", "Status"])
st.dataframe(df_rsi, use_container_width=True)

# ============================
# Select stock
# ============================
stock_choice = st.selectbox("📌 Now choose a stock to see details:", list(top_stocks.keys()))
ticker = top_stocks[stock_choice] + ".SA"

future_days = st.slider("How many days ahead do you want to forecast?", 7, 90, 30)
data = yf.download(ticker, start="2020-01-01", progress=False)

if data.empty:
    st.error("❌ Could not fetch data for this ticker.")
else:
    data["RSI"] = calculate_rsi(data["Close"])

    # RSI Plot
    st.subheader(f"📉 RSI - {stock_choice}")
    st.markdown(f"<sub>📉 RSI - {stock_choice} (Relative Strength Index / Índice de Força Relativa)</sub>",
                unsafe_allow_html=True)

    fig_rsi, ax_rsi = plt.subplots()
    ax_rsi.plot(data.index, data['RSI'], label='RSI', color='purple')
    ax_rsi.axhline(70, color='red', linestyle='--', label='Overbought (70)')
    ax_rsi.axhline(30, color='green', linestyle='--', label='Oversold (30)')
    ax_rsi.set_title("RSI - Relative Strength Index")
    ax_rsi.set_ylabel("RSI")
    ax_rsi.legend()
    plt.tight_layout()
    st.pyplot(fig_rsi)

    # Prophet Forecast
    df_forecast = data.reset_index()[['Date', 'Close']].copy()
    df_forecast.columns = ['ds', 'y']

    st.subheader("📊 Historical Closing Price")
    st.markdown("<sub>📊 Preço de fechamento histórico</sub>", unsafe_allow_html=True)
    st.line_chart(df_forecast.set_index('ds'))

    model = Prophet(daily_seasonality=True)
    model.fit(df_forecast)

    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)

    st.subheader(f"🔮 Forecast for the next {future_days} days")
    st.markdown(f"<sub>🔮 Previsão para os próximos {future_days} dias</sub>", unsafe_allow_html=True)

    fig1 = model.plot(forecast)
    st.pyplot(fig1)

    st.subheader("📉 Forecast Components")
    st.markdown("<sub>📉 Componentes da previsão</sub>", unsafe_allow_html=True)

    fig2 = model.plot_components(forecast)
    st.pyplot(fig2)
