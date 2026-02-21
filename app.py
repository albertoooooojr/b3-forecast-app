import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
import plotly.graph_objects as go

st.set_page_config(page_title="B3 Stock Forecast", layout="wide")

# ============================
# Title
# ============================
st.markdown("## 📈 B3 (Brazil) Stock Forecast")
st.markdown("<sub>📈 Previsão de Ações da B3 (Brasil) - Seleção por Clique & Calculadora de Retorno Manual</sub>",
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
# Cache Data (5 minutes)
# ============================
@st.cache_data(ttl=300)
def get_scanner_data(stocks_dict):
    results = []
    for name, code in stocks_dict.items():
        try:
            df = yf.download(code + ".SA", period="6mo", interval="1d", progress=False)
            if df.empty:
                continue
            df["RSI"] = calculate_rsi(df["Close"])
            last_rsi_val = float(df["RSI"].iloc[-1])
            last_price_val = float(df["Close"].iloc[-1])

            # FILTRO: Apenas ações com preço maior que R$ 7,00
            if last_price_val > 7.0:
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
st.markdown("<sub>🔎 Scanner RSI - Ações Sobrecompradas/Sobrevendidas (Preço > R$ 7,00)</sub>", unsafe_allow_html=True)

# Usar a função com cache
scanner_results = get_scanner_data(top_stocks)

# Criar DataFrame e ordenar por RSI de forma crescente (ascending)
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
selected_rows = st.dataframe(
    df_rsi,
    use_container_width=True,
    column_config=column_config,
    hide_index=True,
    on_select="rerun",
    selection_mode="single-row"
)

# Lógica de seleção: Se clicar na tabela, usa essa ação. Senão, usa o selectbox.
selected_stock_name = None
if selected_rows and len(selected_rows["selection"]["rows"]) > 0:
    row_idx = selected_rows["selection"]["rows"][0]
    selected_stock_name = df_rsi.iloc[row_idx]["Stock"]

# ============================
# Select stock
# ============================
st.subheader("📌 Stock Details")
stock_list = list(top_stocks.keys())

if selected_stock_name:
    st.info(f"Ação selecionada na tabela: **{selected_stock_name}**")
    default_idx = stock_list.index(selected_stock_name)
    stock_choice = st.selectbox("📌 Or choose another stock manually:", stock_list, index=default_idx)
else:
    stock_choice = st.selectbox("📌 Choose a stock to see details:", stock_list)

ticker = top_stocks[stock_choice] + ".SA"
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

    # Prophet Forecast
    df_forecast = data.reset_index()[['Date', 'Close']].copy()
    df_forecast.columns = ['ds', 'y']

    # Modelo Prophet
    model = Prophet(daily_seasonality=True)
    model.fit(df_forecast)

    future = model.make_future_dataframe(periods=90)
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

    # Layout em duas colunas: gráfico (70%) e métricas (30%)
    col_graf, col_metric = st.columns([0.7, 0.3])

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
            )
        )

        # Adicionar range slider para zoom
        fig_forecast.update_xaxes(rangeslider_visible=True)

        st.plotly_chart(fig_forecast, use_container_width=True)

    with col_metric:
        st.markdown("### 📊 Resumo da Operação")

        with st.container():
            # Preço Atual
            st.metric("💰 Preço Atual", f"R$ {preco_atual:.2f}")

            # Linha de separação visual
            st.divider()

            # Previsão
            sinal = "+" if diferenca_valor >= 0 else ""
            st.metric("🎯 Previsão", f"R$ {previsao_final:.2f}",
                      delta=f"{sinal}{diferenca_valor:.2f}" if abs(diferenca_valor) > 0.01 else "0.00")

            # Diferença em R$
            st.metric("📈 Diferença (R$)", f"R$ {diferenca_valor:+.2f}")

            # Variação Percentual
            st.metric("📊 Variação (%)", f"{diferenca_percentual:+.2f}%")

            # Linha de separação
            st.divider()

            # Intervalo de Confiança
            st.info(
                f"📊 **Intervalo de Confiança (95%):**\n\nR$ {forecast['yhat_lower'].iloc[-1]:.2f} - R$ {forecast['yhat_upper'].iloc[-1]:.2f}")

            # Data da previsão
            st.caption(f"📅 Previsão para: {data_previsao.strftime('%d/%m/%Y')}")

    # ============================
    # CALCULADORA DE RETORNO MANUAL (SIMPLIFICADA)
    # ============================
    st.divider()
    st.subheader("🧮 Calculadora de Retorno Manual")
    st.markdown("<sub>Insira os valores para calcular a variação em R$ e %</sub>", unsafe_allow_html=True)

    # Layout em linha com 4 colunas para campos e resultados
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

    # Cálculo da variação
    variacao_brl = preco_final - preco_inicial
    variacao_pct = (variacao_brl / preco_inicial) * 100

    # Determinar a cor do delta baseado no valor (positivo = verde, negativo = vermelho)
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
