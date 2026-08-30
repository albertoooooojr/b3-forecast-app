import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import timedelta
import numpy as np
from xgboost import XGBRegressor


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="B3 Stock Forecast",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# TÍTULO
# ============================================================

st.markdown("## 📈 B3 (Brazil) Stock Forecast")
st.markdown(
    "<sub>📈 Previsão de Ações da B3 (Brasil)</sub>",
    unsafe_allow_html=True
)


# ============================================================
# AÇÕES
# ============================================================

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
    "EZTC3 - EZTEC": "EZTEC3",
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


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalize_series(value, index=None):
    """
    Converte Series/DataFrame/ndarray/list para pandas Series.
    Evita problemas do yfinance com MultiIndex.
    """

    if isinstance(value, pd.DataFrame):

        if value.shape[1] == 0:
            return pd.Series(dtype=float, index=index)

        value = value.iloc[:, 0]

    elif isinstance(value, np.ndarray):

        value = value.flatten()

        if index is not None and len(value) == len(index):
            value = pd.Series(value, index=index)
        else:
            value = pd.Series(value)

    elif not isinstance(value, pd.Series):

        value = pd.Series(value, index=index)

    value = pd.to_numeric(
        value,
        errors="coerce"
    )

    return value


def normalize_yfinance_dataframe(data):
    """
    Normaliza DataFrames vindos do yfinance,
    incluindo MultiIndex.
    """

    if data is None or data.empty:
        return pd.DataFrame()

    data = data.copy()

    # --------------------------------------------------------
    # MultiIndex
    # --------------------------------------------------------

    if isinstance(data.columns, pd.MultiIndex):

        levels = [
            list(data.columns.get_level_values(i))
            for i in range(data.columns.nlevels)
        ]

        close_level = None

        for i, level in enumerate(levels):

            if "Close" in level:
                close_level = i
                break

        if close_level is not None:

            data.columns = data.columns.get_level_values(
                close_level
            )

        else:

            data.columns = [
                "_".join(
                    str(x)
                    for x in column
                    if str(x) not in ("", "None")
                )
                for column in data.columns
            ]

    # --------------------------------------------------------
    # Procurar Close
    # --------------------------------------------------------

    if "Close" not in data.columns:

        candidates = [
            column
            for column in data.columns
            if "close" in str(column).lower()
        ]

        if candidates:
            data["Close"] = data[candidates[0]]

    if "Close" not in data.columns:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Normalizar OHLCV
    # --------------------------------------------------------

    for column in [
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume"
    ]:

        if column in data.columns:

            data[column] = normalize_series(
                data[column],
                data.index
            )

    # --------------------------------------------------------
    # Garantir Close válido
    # --------------------------------------------------------

    data["Close"] = normalize_series(
        data["Close"],
        data.index
    )

    data = data.dropna(
        subset=["Close"]
    )

    data = data[
        data["Close"] > 0
    ]

    return data


def calculate_rsi(series, window=14):

    series = normalize_series(series)

    if series.empty:
        return pd.Series(dtype=float)

    delta = series.diff()

    gain = delta.clip(
        lower=0
    )

    loss = -delta.clip(
        upper=0
    )

    avg_gain = gain.rolling(
        window=window,
        min_periods=window
    ).mean()

    avg_loss = loss.rolling(
        window=window,
        min_periods=window
    ).mean()

    rs = avg_gain / avg_loss.replace(
        0,
        np.nan
    )

    rsi = 100 - (
        100 / (1 + rs)
    )

    # Sem perdas = RSI 100
    rsi = rsi.mask(
        (avg_loss == 0) & (avg_gain > 0),
        100
    )

    # Sem ganhos nem perdas = 50
    rsi = rsi.mask(
        (avg_loss == 0) & (avg_gain == 0),
        50
    )

    rsi = rsi.fillna(50.0)

    return rsi


def calculate_macd(series):

    series = normalize_series(series)

    ema_fast = series.ewm(
        span=12,
        adjust=False
    ).mean()

    ema_slow = series.ewm(
        span=26,
        adjust=False
    ).mean()

    macd = ema_fast - ema_slow

    signal = macd.ewm(
        span=9,
        adjust=False
    ).mean()

    histogram = macd - signal

    return macd, signal, histogram


# ============================================================
# FEATURES XGBOOST
# ============================================================

def create_features(df):

    df = df.copy()

    df["Close"] = normalize_series(
        df["Close"],
        df.index
    )

    # RSI
    df["RSI"] = calculate_rsi(
        df["Close"]
    )

    # Médias
    df["SMA_5"] = df["Close"].rolling(5).mean()
    df["SMA_10"] = df["Close"].rolling(10).mean()
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()

    # Retornos
    df["Return_1d"] = df["Close"].pct_change(1)
    df["Return_5d"] = df["Close"].pct_change(5)
    df["Return_10d"] = df["Close"].pct_change(10)

    # Volatilidade
    df["Volatility_5d"] = (
        df["Return_1d"]
        .rolling(5)
        .std()
    )

    df["Volatility_10d"] = (
        df["Return_1d"]
        .rolling(10)
        .std()
    )

    # Volume
    if "Volume" in df.columns:

        volume = normalize_series(
            df["Volume"],
            df.index
        )

        volume_ma = (
            volume
            .rolling(5, min_periods=1)
            .mean()
        )

        volume_ma = volume_ma.replace(
            0,
            1
        )

        df["Volume_Ratio"] = (
            volume / volume_ma
        )

    else:

        df["Volume_Ratio"] = 1.0

    # MACD
    macd, signal, histogram = calculate_macd(
        df["Close"]
    )

    df["MACD"] = macd
    df["MACD_Signal"] = signal
    df["MACD_Hist"] = histogram

    # Bollinger
    sma = (
        df["Close"]
        .rolling(20)
        .mean()
    )

    std = (
        df["Close"]
        .rolling(20)
        .std()
    )

    upper = sma + (
        std * 2
    )

    lower = sma - (
        std * 2
    )

    bb_range = (
        upper - lower
    )

    bb_range = bb_range.replace(
        0,
        np.nan
    )

    df["BB_Width"] = (
        bb_range / df["Close"]
    )

    df["Price_to_BB"] = (
        (df["Close"] - lower)
        / bb_range
    )

    # Features temporais
    if isinstance(df.index, pd.DatetimeIndex):

        df["DayOfWeek"] = df.index.dayofweek
        df["Month"] = df.index.month
        df["DayOfMonth"] = df.index.day

    else:

        df["DayOfWeek"] = 0
        df["Month"] = 1
        df["DayOfMonth"] = 1

    # --------------------------------------------------------
    # Limpeza
    # --------------------------------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.ffill()
    df = df.bfill()
    df = df.fillna(0)

    return df


# ============================================================
# TREINAMENTO XGBOOST
# ============================================================

def train_xgboost_model(
    df,
    forecast_days
):

    if len(df) < 60:
        return None

    try:

        features = create_features(
            df
        )

    except Exception as e:

        st.warning(
            f"⚠️ Erro ao criar indicadores: {e}"
        )

        return None

    feature_cols = [
        "RSI",
        "SMA_5",
        "SMA_10",
        "SMA_20",
        "SMA_50",
        "Return_1d",
        "Return_5d",
        "Return_10d",
        "Volatility_5d",
        "Volatility_10d",
        "Volume_Ratio",
        "MACD",
        "MACD_Signal",
        "MACD_Hist",
        "BB_Width",
        "Price_to_BB",
        "DayOfWeek",
        "Month"
    ]

    feature_cols = [
        column
        for column in feature_cols
        if column in features.columns
    ]

    if len(feature_cols) < 5:
        return None

    # --------------------------------------------------------
    # Criar target
    #
    # O modelo aprende o retorno futuro de cada horizonte.
    # Isso evita prever simplesmente o preço absoluto.
    # --------------------------------------------------------

    max_training_horizon = min(
        forecast_days,
        30
    )

    predictions = []

    last_close = float(
        normalize_series(
            df["Close"]
        ).iloc[-1]
    )

    progress = st.progress(0)
    status = st.empty()

    # --------------------------------------------------------
    # Para cada dia futuro
    # --------------------------------------------------------

    for day in range(
        1,
        max_training_horizon + 1
    ):

        temp = features.copy()

        # Target = retorno futuro
        temp["Target"] = (
            temp["Close"]
            .shift(-day)
            / temp["Close"]
            - 1
        )

        temp = temp.replace(
            [np.inf, -np.inf],
            np.nan
        )

        temp = temp.dropna(
            subset=["Target"]
        )

        if len(temp) < 40:

            predictions.append(
                last_close
            )

            continue

        X = temp[
            feature_cols
        ]

        y = temp[
            "Target"
        ]

        split = int(
            len(temp) * 0.8
        )

        if split < 20:
            split = len(temp) - 10

        X_train = X.iloc[:split]
        y_train = y.iloc[:split]

        try:

            model = XGBRegressor(
                n_estimators=150,
                max_depth=3,
                learning_rate=0.05,
                subsample=0.85,
                colsample_bytree=0.85,
                objective="reg:squarederror",
                random_state=42,
                n_jobs=-1
            )

            model.fit(
                X_train,
                y_train,
                verbose=False
            )

            # Features mais recentes
            last_features = features[
                feature_cols
            ].iloc[-1:]

            predicted_return = float(
                model.predict(
                    last_features
                )[0]
            )

            # Limitar previsões absurdas
            predicted_return = float(
                np.clip(
                    predicted_return,
                    -0.15,
                    0.15
                )
            )

            prediction = (
                last_close
                * (
                    1
                    + predicted_return
                )
            )

            predictions.append(
                prediction
            )

        except Exception:

            predictions.append(
                last_close
            )

        progress.progress(
            day / max_training_horizon
        )

        status.text(
            f"🤖 Treinando XGBoost: "
            f"{day}/{max_training_horizon}"
        )

    progress.empty()
    status.empty()

    # --------------------------------------------------------
    # Completar dias 31-90 usando extrapolação suave
    # --------------------------------------------------------

    if forecast_days > max_training_horizon:

        current = predictions[-1]

        if len(predictions) >= 2:

            recent_returns = []

            for i in range(
                1,
                min(6, len(predictions))
            ):

                previous = predictions[
                    -i - 1
                ]

                current_value = predictions[
                    -i
                ]

                if previous > 0:

                    recent_returns.append(
                        current_value
                        / previous
                        - 1
                    )

            if recent_returns:

                trend = float(
                    np.mean(
                        recent_returns
                    )
                )

            else:

                trend = 0.0

        else:

            trend = 0.0

        trend = float(
            np.clip(
                trend,
                -0.02,
                0.02
            )
        )

        for _ in range(
            max_training_horizon,
            forecast_days
        ):

            # Reduz gradualmente a tendência
            trend *= 0.97

            current = (
                current
                * (
                    1 + trend
                )
            )

            predictions.append(
                current
            )

    return predictions


# ============================================================
# FORECAST XGBOOST
# ============================================================

def get_xgboost_forecast(
    data,
    future_days
):

    close = normalize_series(
        data["Close"],
        data.index
    )

    close = close.dropna()

    if close.empty:
        return pd.DataFrame()

    last_price = float(
        close.iloc[-1]
    )

    # --------------------------------------------------------
    # Volatilidade histórica
    # --------------------------------------------------------

    returns = (
        close
        .pct_change()
        .dropna()
    )

    if len(returns) > 5:

        volatility = float(
            returns.std()
        )

    else:

        volatility = 0.02

    if not np.isfinite(volatility):
        volatility = 0.02

    volatility = max(
        volatility,
        0.005
    )

    # --------------------------------------------------------
    # Treinar
    # --------------------------------------------------------

    predictions = train_xgboost_model(
        data,
        future_days
    )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if predictions is None:

        st.info(
            "📊 XGBoost não conseguiu treinar "
            "com os dados disponíveis. "
            "Usando tendência histórica."
        )

        avg_return = float(
            returns.mean()
        ) if len(returns) > 0 else 0.0

        avg_return = float(
            np.clip(
                avg_return,
                -0.03,
                0.03
            )
        )

        predictions = []

        current = last_price

        for _ in range(
            future_days
        ):

            current *= (
                1 + avg_return
            )

            predictions.append(
                current
            )

    # --------------------------------------------------------
    # Datas
    # --------------------------------------------------------

    last_date = data.index[-1]

    if isinstance(
        last_date,
        pd.Timestamp
    ):

        last_date = last_date.to_pydatetime()

    future_dates = [
        last_date
        + timedelta(days=i)
        for i in range(
            1,
            future_days + 1
        )
    ]

    forecast_df = pd.DataFrame({
        "ds": future_dates,
        "yhat": predictions
    })

    # --------------------------------------------------------
    # Intervalo de confiança
    # --------------------------------------------------------

    days = np.arange(
        1,
        future_days + 1
    )

    scale = np.sqrt(days)

    multiplier = 1.96

    lower = (
        forecast_df["yhat"]
        * (
            1
            - multiplier
            * volatility
            * scale
        )
    )

    upper = (
        forecast_df["yhat"]
        * (
            1
            + multiplier
            * volatility
            * scale
        )
    )

    forecast_df[
        "yhat_lower"
    ] = lower.clip(
        lower=0
    )

    forecast_df[
        "yhat_upper"
    ] = upper.clip(
        lower=0
    )

    return forecast_df


# ============================================================
# DOWNLOAD DE DADOS
# ============================================================

@st.cache_data(ttl=300)
def get_stock_data(
    ticker_code
):

    try:

        data = yf.download(
            ticker_code,
            start="2020-01-01",
            progress=False,
            timeout=60,
            auto_adjust=False
        )

        if data.empty:

            data = yf.download(
                ticker_code,
                period="2y",
                progress=False,
                timeout=60,
                auto_adjust=False
            )

        if data.empty:

            ticker = yf.Ticker(
                ticker_code
            )

            data = ticker.history(
                period="2y",
                auto_adjust=False
            )

        data = normalize_yfinance_dataframe(
            data
        )

        return data

    except Exception as e:

        st.error(
            f"❌ Erro ao carregar "
            f"{ticker_code}: {e}"
        )

        return pd.DataFrame()


# ============================================================
# FILTRO DE AÇÕES
# ============================================================

@st.cache_data(ttl=300)
def get_filtered_stocks(
    stocks_dict,
    min_price
):

    filtered = {}

    progress = st.progress(0)

    total = len(
        stocks_dict
    )

    for i, (
        name,
        code
    ) in enumerate(
        stocks_dict.items()
    ):

        try:

            data = yf.download(
                code + ".SA",
                period="5d",
                progress=False,
                timeout=20,
                auto_adjust=False
            )

            data = normalize_yfinance_dataframe(
                data
            )

            if data.empty:
                continue

            price = float(
                data["Close"].iloc[-1]
            )

            if price > min_price:
                filtered[name] = code

        except Exception:
            pass

        progress.progress(
            (i + 1) / total
        )

    progress.empty()

    return filtered


# ============================================================
# RSI SCANNER
# ============================================================

@st.cache_data(ttl=300)
def get_scanner_data(
    stocks_dict,
    min_price
):

    results = []

    progress = st.progress(0)

    total = len(
        stocks_dict
    )

    for i, (
        name,
        code
    ) in enumerate(
        stocks_dict.items()
    ):

        try:

            data = yf.download(
                code + ".SA",
                period="6mo",
                interval="1d",
                progress=False,
                timeout=20,
                auto_adjust=False
            )

            data = normalize_yfinance_dataframe(
                data
            )

            if data.empty:
                continue

            close = normalize_series(
                data["Close"],
                data.index
            )

            if len(close) < 20:
                continue

            rsi = calculate_rsi(
                close
            )

            price = float(
                close.iloc[-1]
            )

            rsi_value = float(
                rsi.iloc[-1]
            )

            if price <= min_price:
                continue

            if rsi_value >= 70:

                results.append([
                    name,
                    price,
                    rsi_value,
                    "🔴 Overbought"
                ])

            elif rsi_value <= 30:

                results.append([
                    name,
                    price,
                    rsi_value,
                    "🟢 Oversold"
                ])

        except Exception:
            pass

        progress.progress(
            (i + 1) / total
        )

    progress.empty()

    return results


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header(
    "⚙️ Configurações de Filtro"
)

min_price = st.sidebar.slider(
    "💵 Preço mínimo da ação (R$):",
    min_value=1.0,
    max_value=50.0,
    value=7.0,
    step=0.5
)

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🤖 Modelo de Previsão"
)

modelo_escolhido = st.sidebar.selectbox(
    "Escolha o modelo:",
    [
        "Prophet (Simples e Rápido)",
        "XGBoost (Avançado)"
    ]
)

st.sidebar.info(
    f"🔎 Preço > R$ {min_price:.2f}"
)


# ============================================================
# RSI SCANNER
# ============================================================

st.subheader(
    "🔎 RSI Scanner - "
    "Overbought/oversold stocks"
)

st.markdown(
    f"<sub>🔎 Scanner RSI - "
    f"Ações Sobrecompradas/Sobrevendidas "
    f"(Preço > R$ {min_price:.2f})</sub>",
    unsafe_allow_html=True
)

with st.spinner(
    "🔍 Escaneando ações da B3..."
):

    scanner_results = get_scanner_data(
        top_stocks,
        min_price
    )


selected_stock_name = None

if scanner_results:

    df_rsi = pd.DataFrame(
        scanner_results,
        columns=[
            "Stock",
            "Price",
            "RSI",
            "Status"
        ]
    )

    df_rsi = df_rsi.sort_values(
        by="RSI",
        ascending=True
    )

    st.dataframe(
        df_rsi,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Stock": st.column_config.TextColumn(
                "Ação"
            ),
            "Price": st.column_config.NumberColumn(
                "Preço",
                format="R$ %.2f"
            ),
            "RSI": st.column_config.NumberColumn(
                "RSI",
                format="%.2f"
            ),
            "Status": st.column_config.TextColumn(
                "Status"
            )
        }
    )

    st.caption(
        f"📊 {len(scanner_results)} "
        f"ações encontradas"
    )

else:

    st.warning(
        f"⚠️ Nenhuma ação encontrada "
        f"com RSI extremo e "
        f"preço > R$ {min_price:.2f}"
    )


# ============================================================
# STOCK DETAILS
# ============================================================

st.subheader(
    "📌 Stock Details"
)

with st.spinner(
    "🔍 Carregando lista de ações..."
):

    filtered_stocks = get_filtered_stocks(
        top_stocks,
        min_price
    )

if not filtered_stocks:

    st.error(
        "❌ Nenhuma ação encontrada "
        "com o filtro atual."
    )

    st.stop()


filtered_stock_list = list(
    filtered_stocks.keys()
)

stock_choice = st.selectbox(
    "📌 Escolha uma ação:",
    filtered_stock_list
)

st.caption(
    f"📊 {len(filtered_stock_list)} "
    f"ações disponíveis"
)

ticker = (
    filtered_stocks[
        stock_choice
    ]
    + ".SA"
)


# ============================================================
# DIAS DE PREVISÃO
# ============================================================

future_days = st.slider(
    "Quantos dias para previsão?",
    min_value=7,
    max_value=90,
    value=30,
    step=1
)


# ============================================================
# CARREGAR DADOS
# ============================================================

with st.spinner(
    f"📥 Carregando dados de {stock_choice}..."
):

    data = get_stock_data(
        ticker
    )


if data.empty:

    st.error(
        f"❌ Não foi possível "
        f"carregar dados para "
        f"{stock_choice}."
    )

    st.stop()


if "Close" not in data.columns:

    st.error(
        "❌ Coluna Close não encontrada."
    )

    st.stop()


data["Close"] = normalize_series(
    data["Close"],
    data.index
)

data = data.dropna(
    subset=["Close"]
)


if len(data) < 30:

    st.warning(
        f"⚠️ Poucos dados históricos: "
        f"{len(data)} dias."
    )


# ============================================================
# RSI
# ============================================================

data["RSI"] = calculate_rsi(
    data["Close"]
)

st.subheader(
    f"📉 RSI - {stock_choice}"
)

fig_rsi = go.Figure()

fig_rsi.add_trace(
    go.Scatter(
        x=data.index,
        y=data["RSI"],
        name="RSI",
        line=dict(
            color="purple",
            width=2
        )
    )
)

fig_rsi.add_hline(
    y=70,
    line_dash="dash",
    line_color="red",
    annotation_text="Overbought"
)

fig_rsi.add_hline(
    y=30,
    line_dash="dash",
    line_color="green",
    annotation_text="Oversold"
)

fig_rsi.update_layout(
    title="RSI - Relative Strength Index",
    yaxis_title="RSI",
    xaxis_title="Data",
    height=400,
    yaxis=dict(
        range=[0, 100]
    )
)

st.plotly_chart(
    fig_rsi,
    use_container_width=True
)


# ============================================================
# PREVISÃO
# ============================================================

st.subheader(
    f"🔮 Previsão para os próximos "
    f"{future_days} dias"
)


# ============================================================
# PROPHET
# ============================================================

if modelo_escolhido == "Prophet (Simples e Rápido)":

    st.info(
        "📊 Usando **Prophet** - "
        "Modelo de séries temporais."
    )

    historical_data = pd.DataFrame({
        "ds": pd.to_datetime(
            data.index
        ),
        "y": data["Close"].values
    })

    historical_data = (
        historical_data
        .dropna()
    )

    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        interval_width=0.95
    )

    model.fit(
        historical_data
    )

    future = model.make_future_dataframe(
        periods=future_days,
        freq="D"
    )

    forecast = model.predict(
        future
    )

    forecast_df = forecast[
        [
            "ds",
            "yhat",
            "yhat_lower",
            "yhat_upper"
        ]
    ].copy()


# ============================================================
# XGBOOST
# ============================================================

else:

    st.info(
        "🚀 Usando **XGBoost** - "
        "Modelo avançado com múltiplos indicadores."
    )

    with st.spinner(
        "🤖 Treinando modelo XGBoost..."
    ):

        forecast_df = get_xgboost_forecast(
            data,
            future_days
        )

    if forecast_df.empty:

        st.error(
            "❌ Não foi possível gerar "
            "a previsão XGBoost."
        )

        st.stop()

    historical_data = pd.DataFrame({
        "ds": pd.to_datetime(
            data.index
        ),
        "y": data["Close"].values
    })


# ============================================================
# PREÇOS
# ============================================================

preco_atual = float(
    data["Close"].iloc[-1]
)

previsao_final = float(
    forecast_df["yhat"].iloc[-1]
)

data_previsao = pd.to_datetime(
    forecast_df["ds"].iloc[-1]
)

diferenca_valor = (
    previsao_final
    - preco_atual
)

if preco_atual != 0:

    diferenca_percentual = (
        diferenca_valor
        / preco_atual
        * 100
    )

else:

    diferenca_percentual = 0


intervalo_inferior = float(
    forecast_df[
        "yhat_lower"
    ].iloc[-1]
)

intervalo_superior = float(
    forecast_df[
        "yhat_upper"
    ].iloc[-1]
)


# ============================================================
# GRÁFICO
# ============================================================

col_grafico, col_metricas = st.columns(
    [0.75, 0.25]
)

with col_grafico:

    fig_forecast = go.Figure()

    # Histórico
    fig_forecast.add_trace(
        go.Scatter(
            x=historical_data["ds"],
            y=historical_data["y"],
            name="Histórico",
            mode="lines",
            line=dict(
                color="black",
                width=1.5
            )
        )
    )

    # Previsão
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_df["ds"],
            y=forecast_df["yhat"],
            name="Previsão",
            line=dict(
                color=(
                    "blue"
                    if modelo_escolhido
                    == "Prophet (Simples e Rápido)"
                    else "orange"
                ),
                width=3
            )
        )
    )

    # Limite superior
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_df["ds"],
            y=forecast_df["yhat_upper"],
            mode="lines",
            line=dict(
                color="rgba(0,0,0,0)"
            ),
            showlegend=False
        )
    )

    # Limite inferior
    fig_forecast.add_trace(
        go.Scatter(
            x=forecast_df["ds"],
            y=forecast_df["yhat_lower"],
            mode="lines",
            fill="tonexty",
            fillcolor=(
                "rgba(0,0,255,0.10)"
                if modelo_escolhido
                == "Prophet (Simples e Rápido)"
                else "rgba(255,165,0,0.10)"
            ),
            line=dict(
                color="rgba(0,0,0,0)"
            ),
            name="Intervalo 95%"
        )
    )

    fig_forecast.update_layout(
        title=(
            f"📈 Previsão - "
            f"{stock_choice}"
        ),
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        height=550,
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )


# ============================================================
# MÉTRICAS
# ============================================================

with col_metricas:

    st.markdown(
        "### 📊 Resumo"
    )

    st.metric(
        "💰 Preço Atual",
        f"R$ {preco_atual:.2f}"
    )

    st.metric(
        "🎯 Previsão",
        f"R$ {previsao_final:.2f}",
        delta=f"R$ {diferenca_valor:+.2f}"
    )

    st.metric(
        "📈 Variação",
        f"{diferenca_percentual:+.2f}%"
    )

    st.markdown("---")

    st.markdown(
        "### 📊 Intervalo 95%"
    )

    st.write(
        f"R$ {intervalo_inferior:.2f} "
        f"→ "
        f"R$ {intervalo_superior:.2f}"
    )

    st.markdown("---")

    st.caption(
        f"📅 Previsão até "
        f"{data_previsao.strftime('%d/%m/%Y')}"
    )


# ============================================================
# SINAL
# ============================================================

st.divider()

st.subheader(
    "🚦 Indicador de Tendência"
)

if diferenca_percentual >= 5:

    st.success(
        f"🟢 Tendência positiva: "
        f"+{diferenca_percentual:.2f}%"
    )

elif diferenca_percentual > 0:

    st.info(
        f"🟡 Tendência levemente positiva: "
        f"+{diferenca_percentual:.2f}%"
    )

elif diferenca_percentual <= -5:

    st.error(
        f"🔴 Tendência negativa: "
        f"{diferenca_percentual:.2f}%"
    )

else:

    st.warning(
        f"🟡 Tendência levemente negativa: "
        f"{diferenca_percentual:.2f}%"
    )


# ============================================================
# DETALHES XGBOOST
# ============================================================

if modelo_escolhido == "XGBoost (Avançado)":

    st.divider()

    with st.expander(
        "🔬 Detalhes do Modelo XGBoost"
    ):

        st.markdown(
            """
            ### Indicadores utilizados

            - RSI
            - Média móvel de 5 dias
            - Média móvel de 10 dias
            - Média móvel de 20 dias
            - Média móvel de 50 dias
            - Retorno de 1 dia
            - Retorno de 5 dias
            - Retorno de 10 dias
            - Volatilidade de 5 dias
            - Volatilidade de 10 dias
            - Volume relativo
            - MACD
            - Sinal do MACD
            - Histograma MACD
            - Largura das Bandas de Bollinger
            - Posição do preço nas Bandas de Bollinger
            - Dia da semana
            - Mês

            **Total: 18 indicadores/features.**
            """
        )


# ============================================================
# CALCULADORA
# ============================================================

st.divider()

st.subheader(
    "🧮 Calculadora de Retorno Manual"
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    preco_inicial = st.number_input(
        "Preço Inicial (R$)",
        min_value=0.01,
        value=preco_atual,
        step=0.01,
        format="%.2f"
    )

with col2:

    preco_final = st.number_input(
        "Preço Final (R$)",
        min_value=0.01,
        value=preco_atual,
        step=0.01,
        format="%.2f"
    )


variacao_brl = (
    preco_final
    - preco_inicial
)

if preco_inicial > 0:

    variacao_pct = (
        variacao_brl
        / preco_inicial
        * 100
    )

else:

    variacao_pct = 0


with col3:

    st.metric(
        "Variação (R$)",
        f"R$ {variacao_brl:+.2f}",
        delta=f"{variacao_brl:+.2f}"
    )


with col4:

    st.metric(
        "Variação (%)",
        f"{variacao_pct:+.2f}%",
        delta=f"{variacao_pct:+.2f}%"
    )


# ============================================================
# AVISO
# ============================================================

st.divider()

st.caption(
    "⚠️ Esta aplicação apresenta estimativas "
    "baseadas em dados históricos e modelos "
    "estatísticos. Previsões não garantem "
    "resultados futuros e não constituem "
    "recomendação de investimento."
)
