import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import time

st.set_page_config(page_title="B3 Stock Forecast", layout="wide")

# ============================
# Title
# ============================
st.markdown("## 📈 B3 (Brazil) Stock Forecast")
st.markdown("<sub>📈 Previsão de Ações da B3 (Brasil)</sub>",
            unsafe_allow_html=True)

# ============================
# Top Stocks (Duplicates Removed)
# ============================
top_stocks = {
    "ABEV3 - Ambev": "ABEV3",
    "ASAI3 - Assaí": "ASAI3",
    "B3SA3 - B3": "B3SA3",
    "BBAS3 - Banco do Brasil": "BBAS3",
    "BBDC3 - Bradesco ON": "BBDC3",
    "BBDC4 - Bradesco PN": "BBDC4",
    "BBSE3 - BB Seguridade": "BBSE3",
    "BEEF3 - Minerva": "BEEF3",
    "BPAC11 - BTG Pactual": "BPAC11",
    "BRAP4 - Bradespar": "BRAP4",
    "BRFS3 - BRF": "BRFS3",
    "CCRO3 - CCR": "CCRO3",
    "CMIG4 - Cemig": "CMIG4",
    "CPFE3 - CPFL Energia": "CPFE3",
    "CPLE6 - Copel": "CPLE6",
    "CSAN3 - Cosan": "CSAN3",
    "CSNA3 - CSN": "CSNA3",
    "CYRE3 - Cyrela": "CYRE3",
    "DXCO3 - Dexco": "DXCO3",
    "EGIE3 - Engie Brasil": "EGIE3",
    "ELET3 - Eletrobras ON": "ELET3",
    "ELET6 - Eletrobras PN": "ELET6",
    "EMBR3 - Embraer": "EMBR3",
    "ENGI11 - Energisa": "ENGI11",
    "EQTL3 - Equatorial": "EQTL3",
    "EVEN3 - Even Construtora": "EVEN3",
    "EZTC3 - EZTEC": "EZTC3",
    "GGBR4 - Gerdau": "GGBR4",
    "GOAU4 - Metalúrgica Gerdau": "GOAU4",
    "HAPV3 - Hapvida": "HAPV3",
    "HYPE3 - Hypera Pharma": "HYPE3",
    "IGTI11 - Iguatemi": "IGTI11",
    "IRBR3 - IRB Brasil": "IRBR3",
    "ITSA4 - Itaúsa": "ITSA4",
    "ITUB4 - Itaú Unibanco": "ITUB4",
    "JBSS3 - JBS": "JBSS3",
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
    "Small Cap - DESKTOP - DESK3": "DESK3",
    "Small Cap - DIMED - PNVL3": "PNVL3",
    "Small Cap - DIRECIONAL - DIRR3": "DIRR3",
    "Small Cap - ECORODOVIAS - ECOR3": "ECOR3",
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
    "Small Cap - INTELBRAS - INTB3": "INTB3",
    "Small Cap - IOCHP-MAXION - MYPK3": "MYPK3",
    "Small Cap - IRANI - RANI3": "RANI3",
    "Small Cap - JHSF PART - JHSF3": "JHSF3",
    "Small Cap - JSL - JSLG3": "JSLG3",
    "Small Cap - KEPLER WEBER - KEPL3": "KEPL3",
    "Small Cap - LAVVI - LAVV3": "LAVV3",
    "Small Cap - LOG COM PROP - LOGG3": "LOGG3",
    "Small Cap - LWSA - LWSA3": "LWSA3",
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
    "Small Cap - SANEPAR - SAPR11": "SAPR11",
    "Small Cap - SER EDUCA - SEER3": "SEER3",
    "Small Cap - SIMPAR - SIMH3": "SIMH3",
    "Small Cap - SMART FIT - SMFT3": "SMFT3",
    "Small Cap - SYN PROP TEC - SYNE3": "SYNE3",
    "Small Cap - TENDA - TEND3": "TEND3",
    "Small Cap - TRACK FIELD - TFCO4": "TFCO4",
    "Small Cap - TUPY - TUPY3": "TUPY3",
    "Small Cap - UNIPAR - UNIP6": "UNIP6",
    "Small Cap - VALID - VLID3": "VLID3",
    "Small Cap - VAMOS - VAMO3": "VAMO3",
    "Small Cap - VIVARA S.A. - VIVA3": "VIVA3",
    "Small Cap - VULCABRAS - VULC3": "VULC3",
}


# ============================
# FUNÇÕES AUXILIARES
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


def calculate_ma(series, window):
    return series.rolling(window=window).mean()


def calculate_macd(series, fast=12, slow=26, signal=9):
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist


def calculate_bollinger(series, window=20, num_std=2):
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return upper, lower


def create_features(df):
    df = df.copy()
    df['RSI'] = calculate_rsi(df['Close'])
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['Return_1d'] = df['Close'].pct_change(1)
    df['Return_5d'] = df['Close'].pct_change(5)
    df['Return_10d'] = df['Close'].pct_change(10)
    df['Volatility_5d'] = df['Return_1d'].rolling(5).std()
    df['Volatility_10d'] = df['Return_1d'].rolling(10).std()

    try:
        if 'Volume' in df.columns and len(df['Volume'].dropna()) > 0:
            volume_vals = df['Volume'].values
            volume_ma = pd.Series(volume_vals).rolling(5, min_periods=1).mean().values
            for j in range(len(volume_ma)):
                if volume_ma[j] == 0:
                    volume_ma[j] = 1
            df['Volume_Ratio'] = volume_vals / volume_ma
        else:
            df['Volume_Ratio'] = 1.0
    except:
        df['Volume_Ratio'] = 1.0

    try:
        close_vals = df['Close'].values
        exp1 = pd.Series(close_vals).ewm(span=12, adjust=False).mean().values
        exp2 = pd.Series(close_vals).ewm(span=26, adjust=False).mean().values
        macd = exp1 - exp2
        macd_signal = pd.Series(macd).ewm(span=9, adjust=False).mean().values
        macd_hist = macd - macd_signal
        df['MACD'] = macd
        df['MACD_Signal'] = macd_signal
        df['MACD_Hist'] = macd_hist
    except:
        df['MACD'] = 0
        df['MACD_Signal'] = 0
        df['MACD_Hist'] = 0

    try:
        close_vals = df['Close'].values
        sma = pd.Series(close_vals).rolling(window=20).mean().values
        std = pd.Series(close_vals).rolling(window=20).std().values
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        for j in range(len(close_vals)):
            if close_vals[j] == 0:
                close_vals[j] = 1
        df['BB_Width'] = (upper - lower) / close_vals
        bb_range = upper - lower
        for j in range(len(bb_range)):
            if bb_range[j] == 0:
                bb_range[j] = 1
        df['Price_to_BB'] = (close_vals - lower) / bb_range
    except:
        df['BB_Width'] = 0
        df['Price_to_BB'] = 0.5
    
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['DayOfMonth'] = df.index.day
    df = df.fillna(0)
    return df


def train_xgboost_model(df, forecast_days):
    if len(df) < 30:
        return None, None

    try:
        df_features = create_features(df)
    except Exception as e:
        st.warning(f"⚠️ Erro ao criar features: {str(e)}")
        return None, None

    if len(df_features) < 10:
        return None, None

    feature_cols = ['RSI', 'SMA_5', 'SMA_10', 'SMA_20', 'SMA_50',
                    'Return_1d', 'Return_5d', 'Return_10d',
                    'Volatility_5d', 'Volatility_10d',
                    'Volume_Ratio', 'MACD', 'MACD_Signal', 'MACD_Hist',
                    'BB_Width', 'Price_to_BB', 'DayOfWeek', 'Month']

    available_features = [col for col in feature_cols if col in df_features.columns]

    if len(available_features) < 5:
        return None, None

    max_days = min(forecast_days, 30)
    for i in range(1, max_days + 1):
        df_features[f'target_{i}d'] = df_features['Close'].shift(-i)

    df_features = df_features.dropna()

    if len(df_features) < 10:
        return None, None

    X = df_features[available_features]
    predictions = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(1, forecast_days + 1):
        target_col = f'target_{i}d'

        if target_col not in df_features.columns:
            if len(predictions) >= 2:
                recent_trend = np.mean([predictions[j] - predictions[j - 1] for j in
                                        range(max(0, len(predictions) - 3), len(predictions))])
                next_pred = predictions[-1] + recent_trend
                predictions.append(next_pred)
            elif len(predictions) == 1:
                predictions.append(predictions[0] * 1.001)
            else:
                predictions.append(df_features['Close'].iloc[-1])
            continue

        y = df_features[target_col]
        split_idx = int(len(X) * 0.8)
        if split_idx < 5:
            split_idx = len(X) - 5

        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]

        try:
            model = XGBRegressor(
                n_estimators=50,
                max_depth=3,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
            model.fit(X_train, y_train, verbose=False)
            last_features = X.iloc[-1:].values
            pred = model.predict(last_features)[0]
            predictions.append(pred)
        except Exception as e:
            if len(predictions) > 0:
                predictions.append(predictions[-1])
            else:
                predictions.append(df_features['Close'].iloc[-1])

        progress_bar.progress(i / forecast_days)
        status_text.text(f"Treinando modelo para dia {i} de {forecast_days}...")

    progress_bar.empty()
    status_text.empty()
    return predictions, df_features


def get_xgboost_forecast(data, future_days):
    if len(data) >= 5:
        returns = data['Close'].pct_change().dropna()
        if len(returns) > 0:
            avg_return = float(returns.mean())
            volatility = float(returns.std()) if len(returns) > 0 else 0.02
            daily_volatility = volatility / np.sqrt(252) if volatility > 0 else 0.01
        else:
            avg_return = 0
            daily_volatility = 0.01
    else:
        avg_return = 0
        daily_volatility = 0.01

    result = train_xgboost_model(data, future_days)

    if result[0] is None:
        st.info("📊 Usando previsão baseada em tendência histórica...")
        last_price = float(data['Close'].iloc[-1])
        predictions = []
        current_price = last_price
        for i in range(future_days):
            random_shock = np.random.normal(0, daily_volatility * 0.5)
            current_price = current_price * (1 + avg_return + random_shock)
            predictions.append(current_price)
    else:
        predictions, _ = result

    last_date = data.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, future_days + 1)]
    forecast_df = pd.DataFrame({'ds': future_dates, 'yhat': predictions})

    confidence_multiplier = 1.96
    days_array = np.arange(1, future_days + 1)
    scale_factor = np.sqrt(days_array)

    lower_bound = []
    upper_bound = []

    for idx, price in enumerate(predictions):
        factor = 1 - confidence_multiplier * daily_volatility * scale_factor[idx]
        lower = price * max(factor, 0.5)
        upper = price * (1 + confidence_multiplier * daily_volatility * scale_factor[idx])
        lower_bound.append(lower)
        upper_bound.append(upper)

    forecast_df['yhat_lower'] = lower_bound
    forecast_df['yhat_upper'] = upper_bound
    forecast_df['yhat_lower'] = forecast_df['yhat_lower'].clip(lower=0)
    forecast_df['yhat_upper'] = forecast_df['yhat_upper'].clip(lower=0)

    return forecast_df


# ============================
# CONFIGURAÇÕES DO SIDEBAR
# ============================
st.sidebar.header("⚙️ Configurações de Filtro")
min_price = st.sidebar.slider(
    "💵 Preço mínimo da ação (R$):",
    min_value=1.0,
    max_value=50.0,
    value=7.0,
    step=0.5,
    help="Selecione o valor mínimo para filtrar as ações."
)

st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Modelo de Previsão")
modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo de previsão:",
    ["Prophet (Simples e Rápido)", "XGBoost (Avançado - Mais Preciso)"],
    help="Prophet: bom para tendências gerais. XGBoost: melhor para capturar padrões complexos"
)

st.sidebar.info(f"🔎 Mostrando ações com preço > R$ {min_price:.2f}")

if modelo_escolhido == "XGBoost (Avançado - Mais Preciso)":
    st.sidebar.warning("⚠️ XGBoost pode ser mais lento na primeira execução")
    st.sidebar.info("📊 O XGBoost usa múltiplos indicadores")


# ============================
# FUNÇÕES COM CACHE
# ============================
@st.cache_data(ttl=300)
def get_filtered_stocks(stocks_dict, min_price_value):
    filtered_stocks = {}
    with st.spinner(f"🔍 Filtrando ações com preço > R$ {min_price_value:.2f}..."):
        progress_bar = st.progress(0)
        total = len(stocks_dict)
        for i, (name, code) in enumerate(stocks_dict.items()):
            try:
                ticker = yf.Ticker(code + ".SA")
                hist = ticker.history(period="1d")
                if not hist.empty:
                    last_price = float(hist['Close'].iloc[-1])
                    if last_price > min_price_value:
                        filtered_stocks[name] = code
                progress_bar.progress((i + 1) / total)
            except:
                continue
    progress_bar.empty()
    return filtered_stocks


@st.cache_data(ttl=300)
def get_scanner_data(stocks_dict, min_price_value):
    results = []
    for name, code in stocks_dict.items():
        try:
            df = yf.download(code + ".SA", period="6mo", interval="1d", progress=False)
            if df.empty:
                continue
            df["RSI"] = calculate_rsi(df["Close"])
            last_rsi_val = float(df["RSI"].iloc[-1])
            last_price_val = float(df["Close"].iloc[-1])
            if last_price_val > min_price_value:
                status = ""
                if last_rsi_val >= 70:
                    status = "🔴 Overbought"
                elif last_rsi_val <= 30:
                    status = "🟢 Oversold"
                if status:
                    results.append([name, round(last_price_val, 2), round(last_rsi_val, 2), status])
        except:
            continue
    return results


@st.cache_data(ttl=300)
def get_stock_data(ticker_code):
    try:
        data = yf.download(ticker_code, start="2020-01-01", progress=False, timeout=60)
        if data.empty:
            data = yf.download(ticker_code, period="6mo", progress=False, timeout=60)
        if data.empty:
            ticker = yf.Ticker(ticker_code)
            hist = ticker.history(period="1y")
            if not hist.empty:
                return hist
        return data
    except Exception as e:
        return pd.DataFrame()


# ============================
# RSI SCANNER
# ============================
st.subheader("🔎 RSI Scanner - Overbought/oversold stocks")
st.markdown(f"<sub>🔎 Scanner RSI - Ações Sobrecompradas/Sobrevendidas (Preço > R$ {min_price:.2f})</sub>",
            unsafe_allow_html=True)

scanner_results = get_scanner_data(top_stocks, min_price)

if scanner_results:
    df_rsi = pd.DataFrame(scanner_results, columns=["Stock", "Price", "RSI", "Status"])
    df_rsi = df_rsi.sort_values(by="RSI", ascending=True)

    column_config = {
        "Stock": st.column_config.TextColumn("Stock", width="medium"),
        "Price": st.column_config.NumberColumn("Price", format="R$ %.2f", width="small"),
        "RSI": st.column_config.NumberColumn("RSI", format="%.2f", width="small"),
        "Status": st.column_config.TextColumn("Status", width="medium"),
    }

    event = st.dataframe(
        df_rsi,
        use_container_width=True,
        column_config=column_config,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="rsi_scanner"
    )

    selected_stock_name = None
    if event and event.selection and len(event.selection.rows) > 0:
        row_idx = event.selection.rows[0]
        selected_stock_name = df_rsi.iloc[row_idx]["Stock"]

    st.caption(f"📊 {len(scanner_results)} ações encontradas")
else:
    st.warning(f"⚠️ Nenhuma ação encontrada com RSI extremo e preço > R$ {min_price:.2f}")
    selected_stock_name = None
    df_rsi = pd.DataFrame()


# ============================
# SELECTBOX COM FILTRO
# ============================
st.subheader("📌 Stock Details")

with st.spinner(f"Carregando lista de ações..."):
    filtered_stocks = get_filtered_stocks(top_stocks, min_price)

if not filtered_stocks:
    st.warning(f"⚠️ Nenhuma ação encontrada com preço superior a R$ {min_price:.2f}")
    st.stop()

filtered_stock_list = list(filtered_stocks.keys())

if selected_stock_name and selected_stock_name in filtered_stock_list:
    st.info(f"Ação selecionada na tabela: **{selected_stock_name}**")
    default_idx = filtered_stock_list.index(selected_stock_name)
    stock_choice = st.selectbox(
        f"📌 Escolha uma ação:",
        filtered_stock_list,
        index=default_idx
    )
else:
    stock_choice = st.selectbox(
        f"📌 Escolha uma ação:",
        filtered_stock_list
    )

st.caption(f"📊 {len(filtered_stock_list)} ações disponíveis")

ticker = filtered_stocks[stock_choice] + ".SA"
future_days = st.slider("Quantos dias para previsão?", 7, 90, 30)


# ============================
# CARREGAR DADOS DA AÇÃO COM VERIFICAÇÕES
# ============================
data = get_stock_data(ticker)

# ========== VERIFICAÇÕES DE SEGURANÇA ==========
if data.empty:
    st.error(f"❌ Não foi possível carregar dados para {stock_choice}")
    st.info("🔧 Dicas:\n- Tente outra ação\n- Aguarde alguns minutos e recarregue")
    st.stop()

if 'Close' not in data.columns:
    st.error(f"❌ Dados de preço não disponíveis para {stock_choice}")
    st.stop()

if len(data) < 10:
    st.warning(f"⚠️ Poucos dados históricos ({len(data)} dias). A previsão pode ser imprecisa.")
    if len(data) < 5:
        st.stop()

# ========== CONTINUA O CÓDIGO NORMAL ==========
data["RSI"] = calculate_rsi(data["Close"])

# RSI Plot
st.subheader(f"📉 RSI - {stock_choice}")
st.markdown(f"<sub>📉 RSI - {stock_choice} (Relative Strength Index)</sub>",
            unsafe_allow_html=True)

fig_rsi = go.Figure()
fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')))
fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
fig_rsi.update_layout(title="RSI - Relative Strength Index", yaxis_title="RSI", height=400)
st.plotly_chart(fig_rsi, use_container_width=True)


# ============================
# PREVISÃO
# ============================
st.subheader(f"🔮 Previsão para os próximos {future_days} dias")

if modelo_escolhido == "Prophet (Simples e Rápido)":
    st.info("📊 Usando **Prophet** - Modelo especializado em séries temporais")
else:
    st.info("🚀 Usando **XGBoost** - Modelo avançado com múltiplos indicadores")

if modelo_escolhido == "Prophet (Simples e Rápido)":
    df_forecast = data.reset_index()[['Date', 'Close']].copy()
    df_forecast.columns = ['ds', 'y']
    model = Prophet(daily_seasonality=True)
    model.fit(df_forecast)
    future = model.make_future_dataframe(periods=future_days)
    forecast = model.predict(future)
    historical_data = df_forecast
else:
    with st.spinner("🚀 Treinando modelo XGBoost..."):
        forecast_df = get_xgboost_forecast(data, future_days)
    historical_data = data.reset_index()[['Date', 'Close']].copy()
    historical_data.columns = ['ds', 'y']
    class ForecastObject:
        pass
    forecast = ForecastObject()
    forecast.ds = pd.concat([historical_data['ds'], forecast_df['ds']]).reset_index(drop=True)
    forecast.yhat = pd.concat([historical_data['y'], forecast_df['yhat']]).reset_index(drop=True)
    forecast.yhat_lower = pd.concat([historical_data['y'], forecast_df['yhat_lower']]).reset_index(drop=True)
    forecast.yhat_upper = pd.concat([historical_data['y'], forecast_df['yhat_upper']]).reset_index(drop=True)
    future = forecast_df


# ============================
# CÁLCULO DE PREÇOS
# ============================
preco_atual = float(data['Close'].iloc[-1])

if modelo_escolhido == "Prophet (Simples e Rápido)":
    data_previsao = future['ds'].iloc[-1]
    previsao_final = float(forecast[forecast['ds'] == data_previsao]['yhat'].iloc[0])
else:
    data_previsao = forecast_df['ds'].iloc[-1]
    previsao_final = forecast_df['yhat'].iloc[-1]

diferenca_valor = previsao_final - preco_atual
diferenca_percentual = (diferenca_valor / preco_atual) * 100


# ============================
# GRÁFICO E MÉTRICAS
# ============================
col_graf, col_metric = st.columns([0.75, 0.25])

with col_graf:
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=historical_data['ds'], y=historical_data['y'],
                                      name='Histórico', mode='markers',
                                      marker=dict(size=2, color='black')))

    if modelo_escolhido == "Prophet (Simples e Rápido)":
        fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
                                          name='Previsão', line=dict(color='blue')))
        fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'],
                                          fill=None, mode='lines',
                                          line_color='rgba(0,0,255,0)', showlegend=False))
        fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'],
                                          fill='tonexty', mode='lines',
                                          line_color='rgba(0,0,255,0.2)',
                                          name='Intervalo de Confiança'))
    else:
        fig_forecast.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat'],
                                          name='Previsão XGBoost',
                                          line=dict(color='orange', width=2)))
        fig_forecast.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'],
                                          fill=None, mode='lines',
                                          line_color='rgba(255,165,0,0)', showlegend=False))
        fig_forecast.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'],
                                          fill='tonexty', mode='lines',
                                          line_color='rgba(255,165,0,0.2)',
                                          name='Intervalo de Confiança (95%)'))

    fig_forecast.update_layout(title=f"Previsão para {stock_choice} - {modelo_escolhido}",
                               yaxis_title="Preço (R$)", height=500,
                               legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                               dragmode='zoom', hovermode='x unified')
    fig_forecast.update_layout(xaxis=dict(rangeslider=dict(visible=False), type='date'),
                               yaxis=dict(fixedrange=False))
    st.plotly_chart(fig_forecast, use_container_width=True)


with col_metric:
    st.markdown("""
    <style>
    .metric-value-large { font-size: 1.8rem; font-weight: bold; }
    .metric-value-medium { font-size: 1.6rem; font-weight: bold; }
    .delta-positive { color: #00cc00; }
    .delta-negative { color: #ff4444; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("**📊 Resumo da Operação**", unsafe_allow_html=True)
    st.markdown(f"💰 Preço Atual\n\n**R$ {preco_atual:.2f}**")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"🎯 Previsão\n\n**R$ {previsao_final:.2f}**")
    with col2:
        sinal = "+" if diferenca_valor >= 0 else ""
        cor = "delta-positive" if diferenca_valor >= 0 else "delta-negative"
        st.markdown(f"Delta\n\n**<span class='{cor}'>R$ {sinal}{diferenca_valor:.2f}</span>**", 
                   unsafe_allow_html=True)
    
    st.markdown(f"📈 Diferença (R$)\n\n**R$ {diferenca_valor:+.2f}**")
    st.markdown(f"📊 Variação (%)\n\n**{diferenca_percentual:+.2f}%**")
    st.markdown("---")
    
    if modelo_escolhido == "Prophet (Simples e Rápido)":
        intervalo_inferior = forecast[forecast['ds'] == data_previsao]['yhat_lower'].iloc[0]
        intervalo_superior = forecast[forecast['ds'] == data_previsao]['yhat_upper'].iloc[0]
    else:
        intervalo_inferior = forecast_df['yhat_lower'].iloc[-1]
        intervalo_superior = forecast_df['yhat_upper'].iloc[-1]
    
    st.markdown(f"**📊 Intervalo de Confiança (95%)**\n\n**R$ {intervalo_inferior:.2f} - R$ {intervalo_superior:.2f}**")
    st.caption(f"📅 {data_previsao.strftime('%d/%m/%Y')}")


# ============================
# FEATURES DO XGBOOST
# ============================
if modelo_escolhido == "XGBoost (Avançado - Mais Preciso)":
    st.divider()
    with st.expander("🔬 Detalhes do Modelo XGBoost"):
        st.markdown("""
        **Indicadores Técnicos Utilizados:**
        - Médias Móveis (5, 10, 20, 50 dias)
        - MACD, RSI, Bandas de Bollinger
        - Retornos e Volatilidade
        - Volume relativo
        - Features temporais
        **Total:** 18 features diferentes!
        """)


# ============================
# CALCULADORA DE RETORNO
# ============================
st.divider()
st.subheader("🧮 Calculadora de Retorno Manual")

col1, col2, col3, col4 = st.columns(4)

with col1:
    preco_inicial = st.number_input("Preço Inicial (R$)", min_value=0.01,
                                    value=float(data['Close'].iloc[-1]), step=0.01, format="%.2f")
with col2:
    preco_final = st.number_input("Preço Final (R$)", min_value=0.01,
                                  value=float(data['Close'].iloc[-1]), step=0.01, format="%.2f")

variacao_brl = preco_final - preco_inicial
variacao_pct = (variacao_brl / preco_inicial) * 100 if preco_inicial > 0 else 0
delta_color = "normal" if variacao_brl >= 0 else "inverse"

with col3:
    st.metric("Variação (R$)", f"R$ {variacao_brl:+.2f}", delta=f"{variacao_brl:+.2f}", delta_color=delta_color)
with col4:
    st.metric("Variação (%)", f"{variacao_pct:+.2f}%", delta=f"{variacao_pct:+.2f}%", delta_color=delta_color)
