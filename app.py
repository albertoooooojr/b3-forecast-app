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
    "3TENTOS - TTEN3": "TTEN3",
    "ABC BRASIL - ABCB4": "ABCB4",
    "ALLOS - ALOS3": "ALOS3",
    "ALPARGATAS - ALPA4": "ALPA4",
    "ALUPAR - ALUP11": "ALUP11",
    "ANIMA - ANIM3": "ANIM3",
    "ARMAC - ARML3": "ARML3",
    "ASSAI - ASAI3": "ASAI3",
    "AUREN - AURE3": "AURE3",
    "AUTOMOB - AMOB3": "AMOB3",
    "AZZAS 2154 - AZZA3": "AZZA3",
    "BANCO PAN - BPAN4": "BPAN4",
    "BANRISUL - BRSR6": "BRSR6",
    "BEMOBI TECH - BMOB3": "BMOB3",
    "BLAU - BLAU3": "BLAU3",
    "BOA SAFRA - SOJA3": "SOJA3",
    "BR PARTNERS - BRBI11": "BRBI11",
    "BRADESPAR - BRAP4": "BRAP4",
    "BRASILAGRO - AGRO3": "AGRO3",
    "BRASKEM - BRKM5": "BRKM5",
    "BRAVA - BRAV3": "BRAV3",
    "CAMIL - CAML3": "CAML3",
    "CASAS BAHIA - BHIA3": "BHIA3",
    "CBA - CBAV3": "CBAV3",
    "CEA MODAS - CEAB3": "CEAB3",
    "COGNA ON - COGN3": "COGN3",
    "COPASA - CSMG3": "CSMG3",
    "COSAN - CSAN3": "CSAN3",
    "CURY S/A - CURY3": "CURY3",
    "CVC BRASIL - CVCB3": "CVCB3",
    "CYRELA REALT - CYRE3": "CYRE3",
    "CYRELA REALT - CYRE4": "CYRE4",
    "DESKTOP - DESK3": "DESK3",
    "DEXCO - DXCO3": "DXCO3",
    "DIMED - PNVL3": "PNVL3",
    "DIRECIONAL - DIRR3": "DIRR3",
    "ECORODOVIAS - ECOR3": "ECOR3",
    "EVEN - EVEN3": "EVEN3",
    "EZTEC - EZTC3": "EZTC3",
    "FERBASA - FESA4": "FESA4",
    "FLEURY - FLRY3": "FLRY3",
    "FRAS-LE - FRAS3": "FRAS3",
    "GAFISA - GFSA3": "GFSA3",
    "GERDAU MET - GOAU4": "GOAU4",
    "GPS - GGPS3": "GGPS3",
    "GRENDENE - GRND3": "GRND3",
    "GRUPO MATEUS - GMAT3": "GMAT3",
    "GRUPO SBF - SBFG3": "SBFG3",
    "GUARARAPES - GUAR3": "GUAR3",
    "HAPVIDA - HAPV3": "HAPV3",
    "HELBOR - HBOR3": "HBOR3",
    "HIDROVIAS - HBSA3": "HBSA3",
    "HYPERA - HYPE3": "HYPE3",
    "IGUATEMI S.A - IGTI11": "IGTI11",
    "INTELBRAS - INTB3": "INTB3",
    "IOCHP-MAXION - MYPK3": "MYPK3",
    "IRANI - RANI3": "RANI3",
    "IRBBRASIL RE - IRBR3": "IRBR3",
    "JHSF PART - JHSF3": "JHSF3",
    "JSL - JSLG3": "JSLG3",
    "KEPLER WEBER - KEPL3": "KEPL3",
    "LAVVI - LAVV3": "LAVV3",
    "LOG COM PROP - LOGG3": "LOGG3",
    "LOJAS RENNER - LREN3": "LREN3",
    "LWSA - LWSA3": "LWSA3",
    "M.DIASBRANCO - MDIA3": "MDIA3",
    "MAGAZ LUIZA - MGLU3": "MGLU3",
    "MARCOPOLO - POMO4": "POMO4",
    "MELIUZ - CASH3": "CASH3",
    "METAL LEVE - LEVE3": "LEVE3",
    "MILLS - MILS3": "MILS3",
    "MINERVA - BEEF3": "BEEF3",
    "MOURA DUBEUX - MDNE3": "MDNE3",
    "MOVIDA - MOVI3": "MOVI3",
    "MRV - MRVE3": "MRVE3",
    "MULTIPLAN - MULT3": "MULT3",
    "NATURA - NATU3": "NATU3",
    "ODONTOPREV - ODPV3": "ODPV3",
    "ONCOCLINICAS - ONCO3": "ONCO3",
    "ORIZON - ORVR3": "ORVR3",
    "P.ACUCAR-CBD - PCAR3": "PCAR3",
    "PAGUE MENOS - PGMN3": "PGMN3",
    "PETRORECSA - RECV3": "RECV3",
    "PETZCOBASI - AUAU3": "AUAU3",
    "PLANOEPLANO - PLPL3": "PLPL3",
    "POSITIVO TEC - POSI3": "POSI3",
    "PRINER - PRNR3": "PRNR3",
    "QUALICORP - QUAL3": "QUAL3",
    "QUERO-QUERO - LJQQ3": "LJQQ3",
    "RAIZEN - RAIZ4": "RAIZ4",
    "RANDON PART - RAPT4": "RAPT4",
    "RECRUSUL - RCSL3": "RCSL3",
    "RECRUSUL - RCSL4": "RCSL4",
    "SANEPAR - SAPR11": "SAPR11",
    "SAO MARTINHO - SMTO3": "SMTO3",
    "SER EDUCA - SEER3": "SEER3",
    "SID NACIONAL - CSNA3": "CSNA3",
    "SIMPAR - SIMH3": "SIMH3",
    "SLC AGRICOLA - SLCE3": "SLCE3",
    "SMART FIT - SMFT3": "SMFT3",
    "SYN PROP TEC - SYNE3": "SYNE3",
    "TAESA - TAEE11": "TAEE11",
    "TEGMA - TGMA3": "TGMA3",
    "TENDA - TEND3": "TEND3",
    "TRACK FIELD - TFCO4": "TFCO4",
    "TUPY - TUPY3": "TUPY3",
    "UNIPAR - UNIP6": "UNIP6",
    "USIMINAS - USIM5": "USIM5",
    "VALID - VLID3": "VLID3",
    "VAMOS - VAMO3": "VAMO3",
    "VIVARA S.A. - VIVA3": "VIVA3",
    "VULCABRAS - VULC3": "VULC3",
    "YDUQS PART - YDUQ3": "YDUQ3"
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
