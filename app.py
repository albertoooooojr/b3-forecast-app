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
    # Small Caps
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
    """Calcula média móvel"""
    return series.rolling(window=window).mean()


def calculate_macd(series, fast=12, slow=26, signal=9):
    """Calcula MACD e retorna como Series"""
    exp1 = series.ewm(span=fast, adjust=False).mean()
    exp2 = series.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    macd_signal = macd.ewm(span=signal, adjust=False).mean()
    macd_hist = macd - macd_signal
    return macd, macd_signal, macd_hist


def calculate_bollinger(series, window=20, num_std=2):
    """Calcula Bandas de Bollinger"""
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return upper, lower


def create_features(df):
    """Cria features técnicas para o XGBoost - Versão ultra robusta"""
    df = df.copy()

    # RSI
    df['RSI'] = calculate_rsi(df['Close'])

    # Médias Móveis
    df['SMA_5'] = df['Close'].rolling(window=5).mean()
    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # Retornos
    df['Return_1d'] = df['Close'].pct_change(1)
    df['Return_5d'] = df['Close'].pct_change(5)
    df['Return_10d'] = df['Close'].pct_change(10)

    # Volatilidade
    df['Volatility_5d'] = df['Return_1d'].rolling(5).std()
    df['Volatility_10d'] = df['Return_1d'].rolling(10).std()

    # Volume - versão simplificada
    try:
        if 'Volume' in df.columns and len(df['Volume'].dropna()) > 0:
            volume_vals = df['Volume'].values
            volume_ma = pd.Series(volume_vals).rolling(5, min_periods=1).mean().values
            # Evitar divisão por zero
            for j in range(len(volume_ma)):
                if volume_ma[j] == 0:
                    volume_ma[j] = 1
            df['Volume_Ratio'] = volume_vals / volume_ma
        else:
            df['Volume_Ratio'] = 1.0
    except:
        df['Volume_Ratio'] = 1.0

    # MACD - versão simplificada
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

    # Bandas de Bollinger - versão simplificada
    try:
        close_vals = df['Close'].values
        sma = pd.Series(close_vals).rolling(window=20).mean().values
        std = pd.Series(close_vals).rolling(window=20).std().values
        upper = sma + (std * 2)
        lower = sma - (std * 2)

        # Evitar divisão por zero
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

    # Features de tempo
    df['DayOfWeek'] = df.index.dayofweek
    df['Month'] = df.index.month
    df['DayOfMonth'] = df.index.day

    # Preencher NaN com 0 (simples e eficaz)
    df = df.fillna(0)

    return df


def train_xgboost_model(df, forecast_days):
    """Treina modelo XGBoost e faz previsões - Versão robusta"""

    # Verificar se há dados suficientes
    if len(df) < 30:
        return None, None

    # Criar features
    try:
        df_features = create_features(df)
    except Exception as e:
        st.warning(f"⚠️ Erro ao criar features: {str(e)}")
        return None, None

    if len(df_features) < 10:
        return None, None

    # Definir features e target
    feature_cols = ['RSI', 'SMA_5', 'SMA_10', 'SMA_20', 'SMA_50',
                    'Return_1d', 'Return_5d', 'Return_10d',
                    'Volatility_5d', 'Volatility_10d',
                    'Volume_Ratio', 'MACD', 'MACD_Signal', 'MACD_Hist',
                    'BB_Width', 'Price_to_BB', 'DayOfWeek', 'Month']

    # Verificar features disponíveis
    available_features = [col for col in feature_cols if col in df_features.columns]

    if len(available_features) < 5:
        return None, None

    # Criar target: preço futuro
    max_days = min(forecast_days, 30)
    for i in range(1, max_days + 1):
        df_features[f'target_{i}d'] = df_features['Close'].shift(-i)

    # Remover linhas com NaN
    df_features = df_features.dropna()

    if len(df_features) < 10:
        return None, None

    # Preparar dados de treino
    X = df_features[available_features]

    # Previsões para diferentes horizontes
    predictions = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    for i in range(1, forecast_days + 1):
        target_col = f'target_{i}d'

        if target_col not in df_features.columns:
            # Extrapolação
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

        # Dividir treino/validação
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
            # Fallback
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
    """Gera previsão com XGBoost e cria dataframe no formato esperado - Versão robusta"""

    # Calcular retorno médio e volatilidade para fallback
    if len(data) >= 5:
        returns = data['Close'].pct_change().dropna()
        if len(returns) > 0:
            avg_return = float(returns.mean())  # Converter para float
            volatility = float(returns.std()) if len(returns) > 0 else 0.02  # Converter para float
            daily_volatility = volatility / np.sqrt(252) if volatility > 0 else 0.01
        else:
            avg_return = 0
            daily_volatility = 0.01
    else:
        avg_return = 0
        daily_volatility = 0.01

    # Tentar treinar o modelo XGBoost
    result = train_xgboost_model(data, future_days)

    if result[0] is None:
        # Fallback: previsão simples baseada em média móvel
        st.info("📊 Usando previsão baseada em tendência histórica...")
        last_price = float(data['Close'].iloc[-1])

        predictions = []
        current_price = last_price
        for i in range(future_days):
            # Adicionar um pouco de aleatoriedade
            random_shock = np.random.normal(0, daily_volatility * 0.5)
            current_price = current_price * (1 + avg_return + random_shock)
            predictions.append(current_price)
    else:
        predictions, _ = result

    # Criar datas futuras
    last_date = data.index[-1]
    future_dates = [last_date + timedelta(days=i) for i in range(1, future_days + 1)]

    # Criar dataframe de previsão
    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': predictions
    })

    # Calcular intervalo de confiança
    confidence_multiplier = 1.96

    # Garantir que scale_factor tenha o tamanho correto
    days_array = np.arange(1, future_days + 1)
    scale_factor = np.sqrt(days_array)

    # Calcular intervalo de confiança usando numpy diretamente para evitar problemas
    lower_bound = []
    upper_bound = []

    for idx, price in enumerate(predictions):
        factor = 1 - confidence_multiplier * daily_volatility * scale_factor[idx]
        lower = price * max(factor, 0.5)  # Não permite queda maior que 50%
        upper = price * (1 + confidence_multiplier * daily_volatility * scale_factor[idx])
        lower_bound.append(lower)
        upper_bound.append(upper)

    forecast_df['yhat_lower'] = lower_bound
    forecast_df['yhat_upper'] = upper_bound

    # Garantir que os intervalos não sejam negativos
    forecast_df['yhat_lower'] = forecast_df['yhat_lower'].clip(lower=0)
    forecast_df['yhat_upper'] = forecast_df['yhat_upper'].clip(lower=0)

    return forecast_df


# ============================
# NOVO: Slider para escolher o valor mínimo
# ============================
st.sidebar.header("⚙️ Configurações de Filtro")
min_price = st.sidebar.slider(
    "💵 Preço mínimo da ação (R$):",
    min_value=1.0,
    max_value=50.0,
    value=7.0,
    step=0.5,
    help="Selecione o valor mínimo para filtrar as ações. Apenas ações com preço acima deste valor serão mostradas."
)

# NOVO: Seletor de modelo
st.sidebar.markdown("---")
st.sidebar.subheader("🤖 Modelo de Previsão")
modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo de previsão:",
    ["Prophet (Simples e Rápido)", "XGBoost (Avançado - Mais Preciso)"],
    help="Prophet: bom para tendências gerais. XGBoost: melhor para capturar padrões complexos"
)

# Mostrar valor selecionado no sidebar
st.sidebar.info(f"🔎 Mostrando ações com preço > R$ {min_price:.2f}")

if modelo_escolhido == "XGBoost (Avançado - Mais Preciso)":
    st.sidebar.warning("⚠️ XGBoost pode ser mais lento na primeira execução")
    st.sidebar.info(
        "📊 O XGBoost usa múltiplos indicadores: RSI, Médias Móveis, MACD, Bandas de Bollinger, Volume e mais!")


# ============================
# FUNÇÃO ATUALIZADA: Filtrar ações por preço dinâmico
# ============================
@st.cache_data(ttl=300)
def get_filtered_stocks(stocks_dict, min_price_value):
    """
    Retorna um dicionário apenas com ações cujo preço atual > min_price_value
    """
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

            except Exception as e:
                continue

    progress_bar.empty()
    return filtered_stocks


# ============================
# FUNÇÃO ATUALIZADA: Scanner RSI com filtro dinâmico
# ============================
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


# ============================
# RSI Scanner
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

    st.caption(f"📊 {len(scanner_results)} ações encontradas com RSI extremo e preço > R$ {min_price:.2f}")

else:
    st.warning(f"⚠️ Nenhuma ação encontrada com RSI extremo e preço > R$ {min_price:.2f}")
    selected_stock_name = None
    df_rsi = pd.DataFrame()

# ============================
# Selectbox com filtro dinâmico
# ============================
st.subheader("📌 Stock Details")

with st.spinner(f"Carregando lista de ações com preço > R$ {min_price:.2f}..."):
    filtered_stocks = get_filtered_stocks(top_stocks, min_price)

if not filtered_stocks:
    st.warning(f"⚠️ Nenhuma ação encontrada com preço superior a R$ {min_price:.2f} no momento.")
    st.stop()

filtered_stock_list = list(filtered_stocks.keys())

if selected_stock_name and selected_stock_name in filtered_stock_list:
    st.info(f"Ação selecionada na tabela: **{selected_stock_name}**")
    default_idx = filtered_stock_list.index(selected_stock_name)
    stock_choice = st.selectbox(
        f"📌 Escolha uma ação para ver os detalhes (apenas ações > R$ {min_price:.2f}):",
        filtered_stock_list,
        index=default_idx
    )
else:
    stock_choice = st.selectbox(
        f"📌 Escolha uma ação para ver os detalhes (apenas ações > R$ {min_price:.2f}):",
        filtered_stock_list
    )

st.caption(f"📊 {len(filtered_stock_list)} ações disponíveis com preço > R$ {min_price:.2f}")

ticker = filtered_stocks[stock_choice] + ".SA"
future_days = st.slider("How many days ahead do you want to forecast?", 7, 90, 30)


# Cache para o download da ação individual
@st.cache_data(ttl=300)
def get_stock_data(ticker_code):
    return yf.download(ticker_code, start="2020-01-01", progress=False)


data = get_stock_data(ticker)

if data.empty:
    st.error("❌ Could not fetch data for this ticker.")
else:
    data["RSI"] = calculate_rsi(data["Close"])

    # RSI Plot (Plotly Interativo)
    st.subheader(f"📉 RSI - {stock_choice}")
    st.markdown(f"<sub>📉 RSI - {stock_choice} (Relative Strength Index / Índice de Força Relativa)</sub>",
                unsafe_allow_html=True)

    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI', line=dict(color='purple')))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
    fig_rsi.update_layout(title="RSI - Relative Strength Index", yaxis_title="RSI", height=400)
    st.plotly_chart(fig_rsi, use_container_width=True)

    # ============================
    # PREVISÃO COM O MODELO ESCOLHIDO
    # ============================

    st.subheader(f"🔮 Forecast for the next {future_days} days")

    # Mostrar qual modelo está sendo usado
    if modelo_escolhido == "Prophet (Simples e Rápido)":
        st.info("📊 Usando **Prophet** - Modelo especializado em séries temporais")
    else:
        st.info("🚀 Usando **XGBoost** - Modelo avançado com múltiplos indicadores técnicos")

    st.markdown(f"<sub>🔮 Previsão para os próximos {future_days} dias</sub>", unsafe_allow_html=True)

    # Executar previsão conforme modelo escolhido
    if modelo_escolhido == "Prophet (Simples e Rápido)":
        # Prophet - código original
        df_forecast = data.reset_index()[['Date', 'Close']].copy()
        df_forecast.columns = ['ds', 'y']

        model = Prophet(daily_seasonality=True)
        model.fit(df_forecast)

        future = model.make_future_dataframe(periods=future_days)
        forecast = model.predict(future)

        # Preparar dados para o gráfico
        historical_data = df_forecast
        forecast_data = forecast

    else:
        # XGBoost - nova implementação
        with st.spinner("🚀 Treinando modelo XGBoost com múltiplos indicadores..."):
            forecast_df = get_xgboost_forecast(data, future_days)

        # Criar formato compatível com o esperado pelo resto do código
        historical_data = data.reset_index()[['Date', 'Close']].copy()
        historical_data.columns = ['ds', 'y']


        # Criar objeto forecast similar ao Prophet
        class ForecastObject:
            pass


        forecast = ForecastObject()
        forecast.ds = pd.concat([historical_data['ds'], forecast_df['ds']]).reset_index(drop=True)
        forecast.yhat = pd.concat([historical_data['y'], forecast_df['yhat']]).reset_index(drop=True)
        forecast.yhat_lower = pd.concat([historical_data['y'], forecast_df['yhat_lower']]).reset_index(drop=True)
        forecast.yhat_upper = pd.concat([historical_data['y'], forecast_df['yhat_upper']]).reset_index(drop=True)

        # Para referência futura
        future = forecast_df

    # ============================
    # Cálculo das informações de preço atual vs previsão
    # ============================
    preco_atual = float(data['Close'].iloc[-1])

    # Pegar a previsão para o último dia do período selecionado
    if modelo_escolhido == "Prophet (Simples e Rápido)":
        data_previsao = future['ds'].iloc[-1]
        previsao_final = float(forecast[forecast['ds'] == data_previsao]['yhat'].iloc[0])
    else:
        data_previsao = forecast_df['ds'].iloc[-1]
        previsao_final = forecast_df['yhat'].iloc[-1]

    # Calcular diferenças
    diferenca_valor = previsao_final - preco_atual
    diferenca_percentual = (diferenca_valor / preco_atual) * 100

    # Layout em duas colunas: gráfico (75%) e métricas (25%)
    col_graf, col_metric = st.columns([0.75, 0.25])

    with col_graf:
        # Gráfico de Previsão Interativo
        fig_forecast = go.Figure()

        # Dados Históricos
        fig_forecast.add_trace(go.Scatter(
            x=historical_data['ds'],
            y=historical_data['y'],
            name='Histórico',
            mode='markers',
            marker=dict(size=2, color='black')
        ))

        # Previsão
        if modelo_escolhido == "Prophet (Simples e Rápido)":
            # Prophet: linha contínua
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat'],
                    name='Previsão',
                    line=dict(color='blue')
                )
            )
            # Intervalo de Confiança
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_upper'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(0,0,255,0)',
                    showlegend=False
                )
            )
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast['ds'],
                    y=forecast['yhat_lower'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(0,0,255,0.2)',
                    name='Intervalo de Confiança'
                )
            )
        else:
            # XGBoost: mostrar apenas a previsão futura
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat'],
                    name='Previsão XGBoost',
                    line=dict(color='orange', width=2)
                )
            )
            # Intervalo de Confiança aproximado
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat_upper'],
                    fill=None,
                    mode='lines',
                    line_color='rgba(255,165,0,0)',
                    showlegend=False
                )
            )
            fig_forecast.add_trace(
                go.Scatter(
                    x=forecast_df['ds'],
                    y=forecast_df['yhat_lower'],
                    fill='tonexty',
                    mode='lines',
                    line_color='rgba(255,165,0,0.2)',
                    name='Intervalo de Confiança (95%)'
                )
            )

        fig_forecast.update_layout(
            title=f"Previsão para {stock_choice} - {modelo_escolhido}",
            yaxis_title="Preço (R$)",
            height=500,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            dragmode='zoom',
            hovermode='x unified'
        )

        fig_forecast.update_layout(
            xaxis=dict(
                rangeslider=dict(visible=False),
                type='date'
            ),
            yaxis=dict(
                fixedrange=False
            )
        )

        st.plotly_chart(fig_forecast, use_container_width=True)

    with col_metric:
        # CSS para ajustar fontes
        st.markdown("""
        <style>
        .small-font {
            font-size: 0.9rem !important;
        }
        .metric-container {
            margin-bottom: 0.5rem;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 0.2rem;
        }
        .metric-value {
            font-size: 1.6rem;
            font-weight: bold;
        }
        .metric-value-large {
            font-size: 1.8rem;
            font-weight: bold;
        }
        .metric-value-medium {
            font-size: 1.6rem;
            font-weight: bold;
        }
        .delta-positive {
            color: #00cc00;
            font-size: 1.6rem;
        }
        .delta-negative {
            color: #ff4444;
            font-size: 1.6rem;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<p class="small-font" style="font-size: 1rem; font-weight: bold;">📊 Resumo da Operação</p>',
                    unsafe_allow_html=True)

        with st.container():
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown('<p class="metric-label">💰 Preço Atual</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value-large">R$ {preco_atual:.2f}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.3;'>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<p class="metric-label">🎯 Previsão</p>', unsafe_allow_html=True)
                st.markdown(f'<p class="metric-value-medium">R$ {previsao_final:.2f}</p>', unsafe_allow_html=True)
            with col2:
                st.markdown('<p class="metric-label">Delta</p>', unsafe_allow_html=True)
                sinal = "+" if diferenca_valor >= 0 else ""
                delta_valor = f"{sinal}{diferenca_valor:.2f}" if abs(diferenca_valor) > 0.01 else "0.00"
                cor_delta = "delta-positive" if diferenca_valor >= 0 else "delta-negative"
                st.markdown(f'<p class="metric-value-medium {cor_delta}">R$ {delta_valor}</p>',
                            unsafe_allow_html=True)

            st.markdown('<p class="metric-label">📈 Diferença (R$)</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value-medium">R$ {diferenca_valor:+.2f}</p>', unsafe_allow_html=True)

            st.markdown('<p class="metric-label">📊 Variação (%)</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="metric-value-medium">{diferenca_percentual:+.2f}%</p>', unsafe_allow_html=True)

            st.markdown("<hr style='margin: 0.5rem 0; opacity: 0.3;'>", unsafe_allow_html=True)

            if modelo_escolhido == "Prophet (Simples e Rápido)":
                intervalo_inferior = forecast[forecast['ds'] == data_previsao]['yhat_lower'].iloc[0]
                intervalo_superior = forecast[forecast['ds'] == data_previsao]['yhat_upper'].iloc[0]
            else:
                intervalo_inferior = forecast_df['yhat_lower'].iloc[-1]
                intervalo_superior = forecast_df['yhat_upper'].iloc[-1]

            st.markdown(f'''
            <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.3rem; font-size: 0.9rem;">
                <b>📊 Intervalo de Confiança (95%)</b><br>
                <span style="font-size: 1.5rem; font-weight: bold;">R$ {intervalo_inferior:.2f} - R$ {intervalo_superior:.2f}</span>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown(
                f'<p style="font-size: 0.8rem; color: #666; margin-top: 0.5rem; text-align: right;">📅 {data_previsao.strftime("%d/%m/%Y")}</p>',
                unsafe_allow_html=True)

    # ============================
    # SEÇÃO DE FEATURES DO XGBOOST (mostrar apenas quando selecionado)
    # ============================
    if modelo_escolhido == "XGBoost (Avançado - Mais Preciso)":
        st.divider()
        with st.expander("🔬 Detalhes do Modelo XGBoost - Indicadores Utilizados"):
            st.markdown("""
            ### 📊 Indicadores Técnicos Utilizados no XGBoost:

            **Indicadores de Tendência:**
            - Médias Móveis (5, 10, 20, 50 dias)
            - MACD (Moving Average Convergence Divergence)

            **Indicadores de Momentum:**
            - RSI (Relative Strength Index)
            - Retornos (1, 5, 10 dias)

            **Indicadores de Volatilidade:**
            - Volatilidade (5 e 10 dias)
            - Bandas de Bollinger (largura e posição relativa)

            **Indicadores de Volume:**
            - Volume relativo à média
            - Média móvel do volume

            **Features Temporais:**
            - Dia da semana
            - Mês
            - Dia do mês

            **Total:** 18 features diferentes para máxima precisão!
            """)

            # Mostrar últimas features calculadas
            st.markdown("### 📈 Últimos valores calculados:")
            try:
                df_features = create_features(data)
                last_row = df_features.iloc[-1]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RSI", f"{last_row['RSI']:.2f}")
                    st.metric("SMA 20", f"R$ {last_row['SMA_20']:.2f}")
                    st.metric("MACD", f"{last_row['MACD']:.4f}")
                with col2:
                    st.metric("Volatilidade 5d", f"{last_row['Volatility_5d']:.4f}")
                    st.metric("BB Width", f"{last_row['BB_Width']:.4f}")
                    st.metric("Volume Ratio", f"{last_row['Volume_Ratio']:.2f}")
                with col3:
                    st.metric("Retorno 1d", f"{last_row['Return_1d'] * 100:.2f}%")
                    st.metric("Retorno 5d", f"{last_row['Return_5d'] * 100:.2f}%")
                    st.metric("Dia da semana", f"{last_row['DayOfWeek']:.0f}")
            except Exception as e:
                st.info(f"Carregando dados...")

    # ============================
    # CALCULADORA DE RETORNO MANUAL
    # ============================
    st.divider()
    st.subheader("🧮 Calculadora de Retorno Manual")
    st.markdown("<sub>Insira os valores para calcular a variação em R$ e %</sub>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        preco_inicial = st.number_input(
            "Preço Inicial (R$)",
            min_value=0.01,
            value=float(data['Close'].iloc[-1]),
            step=0.01,
            format="%.2f",
            key="preco_inicial"
        )

    with col2:
        preco_final = st.number_input(
            "Preço Final (R$)",
            min_value=0.01,
            value=float(data['Close'].iloc[-1]),
            step=0.01,
            format="%.2f",
            key="preco_final"
        )

    variacao_brl = preco_final - preco_inicial
    variacao_pct = (variacao_brl / preco_inicial) * 100 if preco_inicial > 0 else 0

    delta_color = "normal" if variacao_brl >= 0 else "inverse"

    with col3:
        st.metric(
            "Variação (R$)",
            f"R$ {variacao_brl:+.2f}",
            delta=f"{variacao_brl:+.2f}",
            delta_color=delta_color
        )

    with col4:
        st.metric(
            "Variação (%)",
            f"{variacao_pct:+.2f}%",
            delta=f"{variacao_pct:+.2f}%",
            delta_color=delta_color
        )
