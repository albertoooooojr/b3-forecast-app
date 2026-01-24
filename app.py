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
# All Stocks
# ============================
all_stocks = {
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
    "3TENTOS - ON      NM": "3TENTOS",
    "ABC BRASIL - PN      N2": "ABC BRASIL",
    "ALLOS - ON  ED  NM": "ALLOS",
    "ALPARGATAS - PN      N1": "ALPARGATAS",
    "ALUPAR - UNT     N2": "ALUPAR",
    "ANIMA - ON      NM": "ANIMA",
    "ARMAC - ON      NM": "ARMAC",
    "ASSAI - ON      NM": "ASSAI",
    "AUREN - ON      NM": "AUREN",
    "AUTOMOB - ON      NM": "AUTOMOB",
    "AZZAS 2154 - ON      NM": "AZZAS 2154",
    "BANCO PAN - PN      N1": "BANCO PAN",
    "BANRISUL - PNB     N1": "BANRISUL",
    "BEMOBI TECH - ON      NM": "BEMOBI TECH",
    "BLAU - ON      NM": "BLAU",
    "BOA SAFRA - ON      NM": "BOA SAFRA",
    "BR PARTNERS - UNT     N2": "BR PARTNERS",
    "BRADESPAR - PN      N1": "BRADESPAR",
    "BRASILAGRO - ON      NM": "BRASILAGRO",
    "BRASKEM - PNA     N1": "BRASKEM",
    "BRAVA - ON      NM": "BRAVA",
    "CAMIL - ON      NM": "CAMIL",
    "CASAS BAHIA - ON      NM": "CASAS BAHIA",
    "CBA - ON      NM": "CBA",
    "CEA MODAS - ON      NM": "CEA MODAS",
    "COGNA ON - ON      NM": "COGNA ON",
    "COPASA - ON      NM": "COPASA",
    "COSAN - ON      NM": "COSAN",
    "CURY S/A - ON      NM": "CURY S/A",
    "CVC BRASIL - ON      NM": "CVC BRASIL",
    "CYRELA REALT - ON      NM": "CYRELA REALT",
    "CYRELA REALT - PN      NM": "CYRELA REALT",
    "DESKTOP - ON      NM": "DESKTOP",
    "DEXCO - ON      NM": "DEXCO",
    "DIMED - ON  EJ  NM": "DIMED",
    "DIRECIONAL - ON      NM": "DIRECIONAL",
    "ECORODOVIAS - ON      NM": "ECORODOVIAS",
    "EVEN - ON      NM": "EVEN",
    "EZTEC - ON      NM": "EZTEC",
    "FERBASA - PN      N1": "FERBASA",
    "FLEURY - ON      NM": "FLEURY",
    "FRAS-LE - ON      N1": "FRAS-LE",
    "GAFISA - ON      NM": "GAFISA",
    "GERDAU MET - PN      N1": "GERDAU MET",
    "GPS - ON      NM": "GPS",
    "GRENDENE - ON      NM": "GRENDENE",
    "GRUPO MATEUS - ON      NM": "GRUPO MATEUS",
    "GRUPO SBF - ON      NM": "GRUPO SBF",
    "GUARARAPES - ON      NM": "GUARARAPES",
    "HAPVIDA - ON      NM": "HAPVIDA",
    "HELBOR - ON      NM": "HELBOR",
    "HIDROVIAS - ON      NM": "HIDROVIAS",
    "HYPERA - ON      NM": "HYPERA",
    "IGUATEMI S.A - UNT     N1": "IGUATEMI S.A",
    "INTELBRAS - ON      NM": "INTELBRAS",
    "IOCHP-MAXION - ON      NM": "IOCHP-MAXION",
    "IRANI - ON      NM": "IRANI",
    "IRBBRASIL RE - ON      NM": "IRBBRASIL RE",
    "JHSF PART - ON  ED  NM": "JHSF PART",
    "JSL - ON      NM": "JSL",
    "KEPLER WEBER - ON      NM": "KEPLER WEBER",
    "LAVVI - ON      NM": "LAVVI",
    "LOG COM PROP - ON      NM": "LOG COM PROP",
    "LOJAS RENNER - ON      NM": "LOJAS RENNER",
    "LWSA - ON      NM": "LWSA",
    "M.DIASBRANCO - ON  ED  NM": "M.DIASBRANCO",
    "MAGAZ LUIZA - ON      NM": "MAGAZ LUIZA",
    "MARCOPOLO - PN      N2": "MARCOPOLO",
    "MELIUZ - ON      NM": "MELIUZ",
    "METAL LEVE - ON      NM": "METAL LEVE",
    "MILLS - ON      NM": "MILLS",
    "MINERVA - ON      NM": "MINERVA",
    "MOURA DUBEUX - ON      NM": "MOURA DUBEUX",
    "MOVIDA - ON      NM": "MOVIDA",
    "MRV - ON      NM": "MRV",
    "MULTIPLAN - ON      N2": "MULTIPLAN",
    "NATURA - ON      NM": "NATURA",
    "ODONTOPREV - ON      NM": "ODONTOPREV",
    "ONCOCLINICAS - ON      NM": "ONCOCLINICAS",
    "ORIZON - ON      NM": "ORIZON",
    "P.ACUCAR-CBD - ON      NM": "P.ACUCAR-CBD",
    "PAGUE MENOS - ON      NM": "PAGUE MENOS",
    "PETRORECSA - ON      NM": "PETRORECSA",
    "PETZCOBASI - ON      NM": "PETZCOBASI",
    "PLANOEPLANO - ON      NM": "PLANOEPLANO",
    "POSITIVO TEC - ON      NM": "POSITIVO TEC",
    "PRINER - ON      NM": "PRINER",
    "QUALICORP - ON      NM": "QUALICORP",
    "QUERO-QUERO - ON      NM": "QUERO-QUERO",
    "RAIZEN - PN      N2": "RAIZEN",
    "RANDON PART - PN      N1": "RANDON PART",
    "RECRUSUL - ON": "RECRUSUL",
    "RECRUSUL - PN": "RECRUSUL",
    "SANEPAR - UNT     N2": "SANEPAR",
    "SAO MARTINHO - ON      NM": "SAO MARTINHO",
    "SER EDUCA - ON      NM": "SER EDUCA",
    "SID NACIONAL - ON": "SID NACIONAL",
    "SIMPAR - ON      NM": "SIMPAR",
    "SLC AGRICOLA - ON      NM": "SLC AGRICOLA",
    "SMART FIT - ON      NM": "SMART FIT",
    "SYN PROP TEC - ON      NM": "SYN PROP TEC",
    "TAESA - UNT     N2": "TAESA",
    "TEGMA - ON      NM": "TEGMA",
    "TENDA - ON      NM": "TENDA",
    "TRACK FIELD - PN      N2": "TRACK FIELD",
    "TUPY - ON      NM": "TUPY",
    "UNIPAR - PNB": "UNIPAR",
    "USIMINAS - PNA     N1": "USIMINAS",
    "VALID - ON      NM": "VALID",
    "VAMOS - ON      NM": "VAMOS",
    "VIVARA S.A. - ON      NM": "VIVARA S.A.",
    "VULCABRAS - ON      NM": "VULCABRAS",
    "YDUQS PART - ON      NM": "YDUQS PART"
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
