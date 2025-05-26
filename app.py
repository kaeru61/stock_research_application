import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf
from plotly.subplots import make_subplots

# 日本語フォント設定
plt.rcParams["font.family"] = "IPAexGothic"

# 黒とミントグリーンを基調としたスタイル設定
mint_green = "#3EB489"
dark_bg = "#121212"
light_mint = "#8ED3B5"
text_color = "#FFFFFF"

# Matplotlibのスタイル設定
plt.style.use("dark_background")
mpl.rcParams["figure.facecolor"] = dark_bg
mpl.rcParams["axes.facecolor"] = dark_bg
mpl.rcParams["axes.edgecolor"] = text_color
mpl.rcParams["axes.labelcolor"] = text_color
mpl.rcParams["text.color"] = text_color
mpl.rcParams["xtick.color"] = text_color
mpl.rcParams["ytick.color"] = text_color
mpl.rcParams["grid.color"] = "#333333"
mpl.rcParams["axes.prop_cycle"] = plt.cycler(
    "color", [mint_green, light_mint, "#FFD700", "#FF6B6B", "#4682B4"]
)

# ページ設定
st.set_page_config(
    page_title="株価相関分析アプリ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# モダンなデザインのカスタムCSS - 黒とミントグリーンのテーマに変更
st.markdown(
    """
<style>
    /* 全体のテーマカラー - 黒とミントグリーン */
    :root {
        --primary: #3EB489;
        --secondary: #2D8E6E;
        --accent: #8ED3B5;
        --background: #121212;
        --text: #FFFFFF;
        --light-text: #AAAAAA;
        --card-bg: #1E1E1E;
        --positive: #4CAF50;
        --negative: #F44336;
        --neutral: #8ED3B5;
    }
    
    /* 全体の背景色を黒に */
    .stApp {
        background-color: var(--background);
    }
    
    /* メインヘッダー */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--primary);
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1.5rem 0;
    }
    
    /* サブヘッダー */
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--secondary);
        margin: 1.5rem 0 1rem 0;
        border-left: 5px solid var(--accent);
        padding-left: 0.8rem;
    }
    
    /* カードスタイル */
    .card {
        padding: 1.8rem;
        border-radius: 12px;
        background-color: var(--card-bg);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
        margin-bottom: 1.8rem;
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.4);
    }
    
    /* 相関ガイド */
    .correlation-guide {
        background-color: rgba(62, 180, 137, 0.1);
        padding: 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid var(--accent);
    }
    
    /* 免責事項 */
    .disclaimer {
        font-size: 0.8rem;
        color: var(--light-text);
        font-style: italic;
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        background-color: rgba(30, 30, 30, 0.7);
        border-radius: 8px;
    }
    
    /* ボタンスタイル */
    .stButton>button {
        background-color: var(--primary);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: var(--secondary);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* タブスタイル */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0px 0px;
        padding: 10px 16px;
        background-color: #2A2A2A;
        color: var(--text);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent) !important;
        color: black !important;
    }
    
    /* テキストインプットスタイル */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #444444;
        padding: 10px;
        background-color: #2A2A2A;
        color: var(--text);
    }
    
    .stTextInput input:focus {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(62, 180, 137, 0.3);
    }
    
    /* リスト項目と目安の表示改善 */
    .correlation-scale {
        display: flex;
        align-items: center;
        margin-bottom: 0.5rem;
        color: var(--text);
    }
    
    .scale-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    /* Streamlit要素のテキスト色調整 */
    .stMarkdown, h1, h2, h3, h4, h5, p, span, label {
        color: var(--text) !important;
    }
    
    /* レスポンシブ調整 */
    @media only screen and (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

# アプリのヘッダーとイントロダクション
st.markdown(
    '<h1 class="main-header">📈 株価相関分析アプリ</h1>', unsafe_allow_html=True
)

st.markdown(
    """
<div style="text-align: center; padding-bottom: 1.5rem;">
株式市場における2つの銘柄間の関係性を分析し、投資判断の参考にしましょう。<br>
証券コードを入力し、分析期間を選択するだけで、株価チャートと相関係数を自動的に計算します。
""",
    unsafe_allow_html=True,
)

# 入力フォーム（モダンなカードデザイン）
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        ticker1 = st.text_input(
            "証券コード1（例: 7203.T）",
            value="7203.T",
            help="日本株の場合、コードの後に '.T' を付けてください",
        )
    with col2:
        ticker2 = st.text_input(
            "証券コード2（例: 6758.T）",
            value="6758.T",
            help="日本株の場合、コードの後に '.T' を付けてください",
        )

    # 期間選択
    period_options = {
        "1ヶ月": "1mo",
        "3ヶ月": "3mo",
        "6ヶ月": "6mo",
        "1年": "1y",
        "2年": "2y",
        "5年": "5y",
        "最大": "max",
    }

    selected_period = st.select_slider(
        "分析期間を選択", options=list(period_options.keys()), value="1年"
    )

    theme = "グリーン"

    period = period_options[selected_period]

# テーマ設定
theme_colors = {
    "ブルー": {
        "primary": "#4361ee",
        "secondary": "#3f37c9",
        "accent": "#4895ef",
        "divergent": "RdBu",
    },
    "グリーン": {
        "primary": "#2D936C",
        "secondary": "#1F6E54",
        "accent": "#38B09D",
        "divergent": "BrBG",
    },
    "レッド": {
        "primary": "#FF5A5F",
        "secondary": "#C73E42",
        "accent": "#FF8A8E",
        "divergent": "RdGy",
    },
    "ダーク": {
        "primary": "#374151",
        "secondary": "#1F2937",
        "accent": "#4B5563",
        "divergent": "inferno",
    },
}

current_theme = theme_colors[theme]

if ticker1 and ticker2:
    try:
        # データ取得
        with st.spinner("データを取得中..."):
            stock1 = yf.Ticker(ticker1)
            stock2 = yf.Ticker(ticker2)

            # 選択した期間のデータを取得
            data1 = stock1.history(period=period)
            data2 = stock2.history(period=period)

        # データが正常に取得できたか確認
        if data1.empty or data2.empty:
            st.error(
                f"証券コード {ticker1} または {ticker2} のデータを取得できませんでした。証券コードを確認してください。"
            )
        else:
            # データ整形 - それぞれから終値のみ抽出
            df = pd.DataFrame(
                {ticker1: data1["Close"], ticker2: data2["Close"]}
            ).dropna()

            if df.empty:
                st.warning("取得したデータが空です。別の証券コードを試してください。")
            else:
                # リターン計算
                returns = df.pct_change().dropna()

                # データ期間の表示
                start_date = df.index.min().strftime("%Y年%m月%d日")
                end_date = df.index.max().strftime("%Y年%m月%d日")

                # 会社名を取得（可能な場合）
                try:
                    company1 = stock1.info.get("shortName", ticker1)
                    company2 = stock2.info.get("shortName", ticker2)
                except:
                    company1 = ticker1
                    company2 = ticker2

                # 分析期間とデータサマリーを表示

                st.markdown(
                    """
                <div style="background-color: rgba(62, 180, 137, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 4px solid var(--accent);">
                    <p style="margin-top: 0; color: var(--primary);">📅 分析期間</p>
                    <p style="margin-bottom: 0; color: var(--text);"><strong>{start}</strong> 〜 <strong>{end}</strong> のデータを分析</p>
                </div>
                """.format(start=start_date, end=end_date),
                    unsafe_allow_html=True,
                )

                # タブ形式で分析結果を表示
                tab1, tab2, tab3 = st.tabs(
                    ["📈 株価推移", "📊 相関分析", "📉 詳細データ"]
                )

                with tab1:
                    st.markdown(
                        '<h3 class="sub-header">株価チャート</h3>',
                        unsafe_allow_html=True,
                    )

                    # Plotlyで株価チャート作成
                    fig = make_subplots(specs=[[{"secondary_y": True}]])

                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df[ticker1],
                            name=company1,
                            line=dict(color=current_theme["primary"], width=2),
                        ),
                        secondary_y=False,
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=df[ticker2],
                            name=company2,
                            line=dict(color=current_theme["secondary"], width=2),
                        ),
                        secondary_y=True,
                    )

                    # 軸ラベル設定
                    fig.update_layout(
                        title=f"{company1} と {company2} の株価推移 ({selected_period})",
                        title_font_size=20,
                        hovermode="x unified",
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                        ),
                        template="plotly_white",
                        height=500,
                        margin=dict(l=10, r=10, t=70, b=30),
                    )

                    fig.update_xaxes(title_text="日付", rangeslider_visible=True)
                    fig.update_yaxes(title_text=f"{company1} (円)", secondary_y=False)
                    fig.update_yaxes(title_text=f"{company2} (円)", secondary_y=True)

                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with tab2:
                    # 相関分析カード

                    col1, col2 = st.columns([1, 1])

                    with col1:
                        # 相関係数
                        correlation = returns[ticker1].corr(returns[ticker2])

                        # 相関係数の強さに応じた色と説明
                        if abs(correlation) >= 0.7:
                            corr_color = mint_green if correlation > 0 else "#F44336"
                            strength = "強い"
                        elif abs(correlation) >= 0.4:
                            corr_color = light_mint if correlation > 0 else "#FF8A8E"
                            strength = "中程度の"
                        else:
                            corr_color = "#4682B4"  # スチールブルー
                            strength = "弱い"

                        blue = "#4682B4"
                        red = "#F44336"
                        orange = "#FF9800"
                        # 相関係数の視覚的表示
                        fig_gauge = go.Figure(
                            go.Indicator(
                                mode="gauge+number",
                                value=correlation,
                                title={
                                    "text": "相関係数 (日次リターン)",
                                    "font": {"color": text_color},
                                },
                                gauge={
                                    "axis": {
                                        "range": [-1, 1],
                                        "tickwidth": 1,
                                        "tickcolor": text_color,
                                        "tickfont": {"color": text_color},
                                    },
                                    "bar": {"color": corr_color},
                                    "bgcolor": "rgba(30, 30, 30, 0.8)",  # 暗い背景色
                                    "borderwidth": 2,
                                    "bordercolor": "#333333",
                                    "steps": [
                                        {
                                            "range": [-1, -0.7],
                                            "color": red,
                                        },  # 赤（強い負の相関）
                                        {
                                            "range": [-0.7, -0.4],
                                            "color": orange,
                                        },  # 薄い赤（中程度の負の相関）
                                        {
                                            "range": [-0.4, 0.4],
                                            "color": blue,
                                        },  # スチールブルー（弱い相関）
                                        {
                                            "range": [0.4, 0.7],
                                            "color": light_mint,
                                        },  # 薄いミントグリーン（中程度の正の相関）
                                        {
                                            "range": [0.7, 1],
                                            "color": mint_green,
                                        },  # ミントグリーン（強い正の相関）
                                    ],
                                },
                                number={
                                    "suffix": "",
                                    "font": {"size": 26, "color": text_color},
                                },
                            )
                        )

                        # レイアウト設定を追加
                        fig_gauge.update_layout(
                            height=300,
                            margin=dict(l=10, r=10, t=60, b=10),
                            paper_bgcolor="rgba(0,0,0,0)",  # 透明な背景
                            plot_bgcolor="rgba(0,0,0,0)",  # 透明な背景
                            font={"color": text_color},
                        )

                        st.plotly_chart(fig_gauge, use_container_width=True)

                        st.markdown(
                            f"""
                        <div style="text-align:center; margin-top:-1rem; margin-bottom:1rem; font-size:1.2rem;">
                           <span style="color:{corr_color}; font-weight:bold;">{strength}{"正" if correlation > 0 else "負" if correlation < 0 else ""}の相関</span> があります
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col2:
                        # 散布図で相関関係を可視化
                        fig_scatter = px.scatter(
                            x=returns[ticker1],
                            y=returns[ticker2],
                            labels={
                                "x": f"{company1} 日次リターン",
                                "y": f"{company2} 日次リターン",
                            },
                            trendline="ols",
                            title="リターン相関散布図",
                        )

                        fig_scatter.update_layout(
                            height=300,
                            template="plotly_white",
                            margin=dict(l=10, r=10, t=60, b=10),
                        )

                        st.plotly_chart(fig_scatter, use_container_width=True)

                    # 相関係数の解釈
                    st.markdown(
                        """
                        <div style="background-color: rgba(62, 180, 137, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border-left: 4px solid var(--accent);">
                            <p style="margin-top: 0; color: var(--primary);">相関係数の解釈</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    col3, col4 = st.columns([3, 2])

                    with col3:
                        st.markdown(
                            f"""
                        <p style="margin-bottom: 0.8rem;">相関係数 <strong>{correlation:.4f}</strong> は、これらの銘柄間に<span style="color:{corr_color}; font-weight:bold;">{strength}{"正" if correlation > 0 else "負" if correlation < 0 else ""}の相関</span>があることを示しています。</p>
                        
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#4CAF50;"></div><strong>0.7~1.0:</strong> 強い正の相関（同じ方向に強く動く）</div>
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#FF9800;"></div><strong>0.4~0.7:</strong> 中程度の正の相関（同じ方向に動く傾向）</div>
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#2196F3;"></div><strong>0.0~0.4:</strong> 弱い正の相関（あまり関連性がない）</div>
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#2196F3;"></div><strong>-0.4~0.0:</strong> 弱い負の相関（あまり関連性がない）</div>
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#FF9800;"></div><strong>-0.7~-0.4:</strong> 中程度の負の相関（逆方向に動く傾向）</div>
                        <div class="correlation-scale"><div class="scale-indicator" style="background-color:#F44336;"></div><strong>-1.0~-0.7:</strong> 強い負の相関（逆方向に強く動く）</div>
                        """,
                            unsafe_allow_html=True,
                        )

                    with col4:
                        st.markdown("### 投資への応用")

                        if abs(correlation) < 0.4:
                            st.markdown(
                                """
                            <div style="background-color: rgba(76, 175, 80, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #4CAF50;">
                                <p style="margin: 0;"><span style="color:#4CAF50;">✅</span> <strong>分散投資に適している可能性</strong></p>
                                <p style="margin: 0; font-size: 0.9rem;">低相関の銘柄を組み合わせることで、ポートフォリオ全体のリスク低減効果が期待できます。</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        elif abs(correlation) >= 0.7:
                            st.markdown(
                                """
                            <div style="background-color: rgba(255, 152, 0, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #FF9800;">
                                <p style="margin: 0;"><span style="color:#FF9800;">⚠️</span> <strong>分散効果は限定的</strong></p>
                                <p style="margin: 0; font-size: 0.9rem;">高相関の銘柄同士では、分散投資によるリスク低減効果が小さくなる傾向があります。</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.markdown(
                                """
                            <div style="background-color: rgba(33, 150, 243, 0.1); padding: 12px; border-radius: 8px; border-left: 4px solid #2196F3;">
                                <p style="margin: 0;"><span style="color:#2196F3;">ℹ️</span> <strong>適度な分散効果</strong></p>
                                <p style="margin: 0; font-size: 0.9rem;">中程度の相関を持つ銘柄の組み合わせでは、一定の分散効果が期待できます。</p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                with tab3:
                    # タブ内にサブタブを作成
                    subtab1, subtab2 = st.tabs(
                        ["📅 リターンチャート", "📋 データテーブル"]
                    )

                    with subtab1:
                        # リターンチャートの表示
                        fig_returns = px.line(
                            returns,
                            y=[ticker1, ticker2],
                            labels={
                                "value": "日次リターン (%)",
                                "variable": "銘柄",
                                "date": "日付",
                            },
                            title="日次リターン比較",
                        )

                        fig_returns.update_layout(
                            hovermode="x unified",
                            legend_title_text="",
                            template="plotly_white",
                            height=400,
                        )

                        st.plotly_chart(fig_returns, use_container_width=True)

                        # ヒートマップで相関の時間変化を可視化
                        st.markdown("#### 相関係数の時間変化")

                        window_days = st.slider("移動窓サイズ（日数）", 20, 120, 60, 5)

                        # 移動相関係数を計算
                        rolling_corr = (
                            returns[ticker1]
                            .rolling(window=window_days)
                            .corr(returns[ticker2])
                        )
                        rolling_corr = rolling_corr.dropna()

                        fig_rolling = go.Figure(
                            go.Scatter(
                                x=rolling_corr.index,
                                y=rolling_corr,
                                mode="lines",
                                line=dict(color=current_theme["primary"], width=2),
                                fill="tozeroy",
                                fillcolor=f"rgba({int(current_theme['primary'][1:3], 16)}, {int(current_theme['primary'][3:5], 16)}, {int(current_theme['primary'][5:7], 16)}, 0.2)",
                            )
                        )

                        fig_rolling.update_layout(
                            title=f"{window_days}日移動相関係数",
                            xaxis_title="日付",
                            yaxis_title="相関係数",
                            yaxis=dict(range=[-1, 1]),
                            hovermode="x unified",
                            template="plotly_white",
                            height=300,
                        )

                        # ゼロラインを追加
                        fig_rolling.add_hline(y=0, line_dash="dash", line_color="gray")

                        # 相関係数の強さを示す背景色を追加
                        fig_rolling.add_hrect(
                            y0=0.7,
                            y1=1,
                            line_width=0,
                            fillcolor="rgba(76, 175, 80, 0.1)",
                        )
                        fig_rolling.add_hrect(
                            y0=0.4,
                            y1=0.7,
                            line_width=0,
                            fillcolor="rgba(255, 152, 0, 0.1)",
                        )
                        fig_rolling.add_hrect(
                            y0=-0.4,
                            y1=0.4,
                            line_width=0,
                            fillcolor="rgba(33, 150, 243, 0.1)",
                        )
                        fig_rolling.add_hrect(
                            y0=-0.7,
                            y1=-0.4,
                            line_width=0,
                            fillcolor="rgba(255, 152, 0, 0.1)",
                        )
                        fig_rolling.add_hrect(
                            y0=-1,
                            y1=-0.7,
                            line_width=0,
                            fillcolor="rgba(244, 67, 54, 0.1)",
                        )

                        st.plotly_chart(fig_rolling, use_container_width=True)

                    with subtab2:
                        # 統計サマリー
                        st.markdown("#### 統計サマリー")
                        col_stats1, col_stats2 = st.columns(2)

                        with col_stats1:
                            st.markdown(f"##### {company1} ({ticker1})")
                            stats1 = returns[ticker1].describe().to_frame().T
                            stats1.rename(index={ticker1: "日次リターン"}, inplace=True)
                            st.dataframe(
                                stats1.style.format("{:.4f}"), use_container_width=True
                            )

                        with col_stats2:
                            st.markdown(f"##### {company2} ({ticker2})")
                            stats2 = returns[ticker2].describe().to_frame().T
                            stats2.rename(index={ticker2: "日次リターン"}, inplace=True)
                            st.dataframe(
                                stats2.style.format("{:.4f}"), use_container_width=True
                            )

                        # データテーブル表示
                        st.markdown("#### 価格データ")

                        # データテーブルの列名を会社名に変更
                        df_display = df.copy()
                        df_display.columns = [company1, company2]

                        with st.expander("株価データを表示"):
                            st.dataframe(
                                df_display.style.format("{:.2f}"),
                                use_container_width=True,
                                height=400,
                            )

                        # リターンデータテーブル
                        st.markdown("#### リターンデータ")
                        returns_display = returns.copy()
                        returns_display.columns = [company1, company2]

                        with st.expander("リターンデータを表示"):
                            st.dataframe(
                                returns_display.style.format("{:.2%}"),
                                use_container_width=True,
                                height=400,
                            )

                    st.markdown("</div>", unsafe_allow_html=True)

                # 免責事項
                st.markdown(
                    '<p class="disclaimer">注意: このアプリは情報提供のみを目的としており、投資アドバイスではありません。過去のパフォーマンスは将来の結果を保証するものではありません。投資判断は自己責任で行ってください。</p>',
                    unsafe_allow_html=True,
                )

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info(
            "証券コードが正しいことを確認してください。日本株の場合は通常、コードの後に '.T' を付けます（例: 7203.T）"
        )
else:
    # 初期表示時のプレースホルダー
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; background-color: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
            <img src="https://em-content.zobj.net/source/microsoft-teams/363/chart-increasing_1f4c8.png" style="width: 80px; margin-bottom: 1rem;">
            <h3>株価相関分析を開始するには、証券コードを入力してください</h3>
            <p style="color: #6c757d;">例: トヨタ自動車（7203.T）とソニー（6758.T）</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
