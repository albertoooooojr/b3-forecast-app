import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
# NOVO: Slider para escolher o valor mínimo
# ============================
st.sidebar.header("⚙️ Configurações de Filtro")
min_price = st.sidebar.slider(
    "💵 Preço mínimo da ação (R$):",
    min_value=1.0,
    max_value=50.0,
    value=7.0,  # Valor padrão
    step=0.5,
    help="Selecione o valor mínimo para filtrar as ações. Apenas ações com preço acima deste valor serão mostradas."
)

# Mostrar valor selecionado no sidebar
st.sidebar.info(f"🔎 Mostrando ações com preço > R$ {min_price:.2f}")


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
                # Pegar apenas o último preço disponível (mais rápido)
                ticker = yf.Ticker(code + ".SA")
                hist = ticker.history(period="1d")

                if not hist.empty:
                    last_price = float(hist['Close'].iloc[-1])

                    # Só incluir se preço > min_price_value
                    if last_price > min_price_value:
                        filtered_stocks[name] = code

                # Atualizar progresso
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

            # FILTRO DINÂMICO: Usar o valor do slider
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
# RSI Scanner (AGORA USANDO O FILTRO DINÂMICO)
# ============================
st.subheader("🔎 RSI Scanner - Overbought/oversold stocks")
st.markdown(f"<sub>🔎 Scanner RSI - Ações Sobrecompradas/Sobrevendidas (Preço > R$ {min_price:.2f})</sub>",
            unsafe_allow_html=True)

# Usar a função com cache e o valor dinâmico do slider
scanner_results = get_scanner_data(top_stocks, min_price)

# Criar DataFrame e ordenar por RSI de forma crescente (ascending)
if scanner_results:
    df_rsi = pd.DataFrame(scanner_results, columns=["Stock", "Price", "RSI", "Status"])
    df_rsi = df_rsi.sort_values(by="RSI", ascending=True)

    # Configuração de colunas para centralizar
    column_config = {
        "Stock": st.column_config.TextColumn("Stock", width="medium"),
        "Price": st.column_config.NumberColumn("Price", format="R$ %.2f", width="small"),
        "RSI": st.column_config.NumberColumn("RSI", format="%.2f", width="small"),
        "Status": st.column_config.TextColumn("Status", width="medium"),
    }

    # Tabela com seleção habilitada
    event = st.dataframe(
        df_rsi,
        use_container_width=True,
        column_config=column_config,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        key="rsi_scanner"
    )

    # Lógica de seleção: Se clicar na tabela, usa essa ação.
    selected_stock_name = None
    if event and event.selection and len(event.selection.rows) > 0:
        row_idx = event.selection.rows[0]
        selected_stock_name = df_rsi.iloc[row_idx]["Stock"]

    # Mostrar contagem de resultados
    st.caption(f"📊 {len(scanner_results)} ações encontradas com RSI extremo e preço > R$ {min_price:.2f}")

else:
    st.warning(f"⚠️ Nenhuma ação encontrada com RSI extremo e preço > R$ {min_price:.2f}")
    selected_stock_name = None
    df_rsi = pd.DataFrame()

# ============================
# Selectbox com filtro dinâmico
# ============================
st.subheader("📌 Stock Details")

# Mostrar indicador de carregamento enquanto filtra
with st.spinner(f"Carregando lista de ações com preço > R$ {min_price:.2f}..."):
    # Usar cache com o valor dinâmico do slider
    filtered_stocks = get_filtered_stocks(top_stocks, min_price)

# Verificar se temos ações filtradas
if not filtered_stocks:
    st.warning(f"⚠️ Nenhuma ação encontrada com preço superior a R$ {min_price:.2f} no momento.")
    st.stop()

# Criar lista apenas com ações filtradas
filtered_stock_list = list(filtered_stocks.keys())

# Selectbox com apenas ações filtradas
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

# Mostrar contagem de ações disponíveis
st.caption(f"📊 {len(filtered_stock_list)} ações disponíveis com preço > R$ {min_price:.2f}")

ticker = filtered_stocks[stock_choice] + ".SA"
future_days = st.slider("How many days ahead do you want to forecast?", 7, 90, 30)


# Cache para o download da ação individual
@st.cache_data(ttl=300)
def get_stock_data(ticker_code):
    return yf.download(ticker_code, start="2000-01-01", progress=False)


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

    # Prophet Forecast
    df_forecast = data.reset_index()[['Date', 'Close']].copy()
    df_forecast.columns = ['ds', 'y']

    # Modelo Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(df_forecast)

    future = model.make_future_dataframe(periods=future_days)
    forecast = model.predict(future)

    st.subheader(f"🔮 Forecast for the next {future_days} days")
    st.markdown(f"<sub>🔮 Previsão para os próximos {future_days} dias</sub>", unsafe_allow_html=True)

    # ============================
    # Cálculo das informações de preço atual vs previsão
    # ============================
    preco_atual = float(data['Close'].iloc[-1])

    # Pegar a previsão para o último dia do período selecionado
    data_previsao = future['ds'].iloc[-1]
    previsao_final = float(forecast[forecast['ds'] == data_previsao]['yhat'].iloc[0])

    # Calcular diferenças
    diferenca_valor = previsao_final - preco_atual
    diferenca_percentual = (diferenca_valor / preco_atual) * 100

    # Layout em duas colunas: gráfico (75%) e métricas (25%)
    col_graf, col_metric = st.columns([0.75, 0.25])

    with col_graf:
        # Gráfico de Previsão Interativo
        fig_forecast = go.Figure()
        # Dados Históricos
        fig_forecast.add_trace(go.Scatter(x=df_forecast['ds'], y=df_forecast['y'], name='Histórico', mode='markers',
                                          marker=dict(size=2, color='black')))
        # Previsão
        fig_forecast.add_trace(
            go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Previsão', line=dict(color='blue')))
        # Intervalo de Confiança
        fig_forecast.add_trace(
            go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], fill=None, mode='lines',
                       line_color='rgba(0,0,255,0)',
                       showlegend=False))
        fig_forecast.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], fill='tonexty', mode='lines',
                                          line_color='rgba(0,0,255,0.2)', name='Intervalo de Confiança'))

        fig_forecast.update_layout(
            title=f"Previsão para {stock_choice}",
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

            st.markdown(f'''
            <div style="background-color: #f0f2f6; padding: 0.5rem; border-radius: 0.3rem; font-size: 0.9rem;">
                <b>📊 Intervalo de Confiança (95%)</b><br>
                <span style="font-size: 1.5rem; font-weight: bold;">R$ {forecast['yhat_lower'].iloc[-1]:.2f} - R$ {forecast['yhat_upper'].iloc[-1]:.2f}</span>
            </div>
            ''', unsafe_allow_html=True)

            st.markdown(
                f'<p style="font-size: 0.8rem; color: #666; margin-top: 0.5rem; text-align: right;">📅 {data_previsao.strftime("%d/%m/%Y")}</p>',
                unsafe_allow_html=True)

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
