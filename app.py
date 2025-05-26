import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import yfinance as yf

st.title("📈 株価相関分析アプリ")

st.markdown("""
2つの日本株の証券コードを入力してください（例：7203.T, 6758.T）  
過去1年のデータを元に、株価チャートと日次リターンの相関係数を表示します。
""")

# 入力欄
ticker1 = st.text_input("証券コード1（例: 7203.T）", value="7203.T")
ticker2 = st.text_input("証券コード2（例: 6758.T）", value="6758.T")

if ticker1 and ticker2:
    try:
        # データ取得
        stock1 = yf.Ticker(ticker1)
        stock2 = yf.Ticker(ticker2)

        # 過去1年間のデータを取得
        data1 = stock1.history(period="1y")
        data2 = stock2.history(period="1y")

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

                # 相関係数
                correlation = returns[ticker1].corr(returns[ticker2])
                st.metric("📊 相関係数（日次リターン）", f"{correlation:.4f}")

                # 株価チャートの表示
                st.subheader("📈 株価チャート（1年）")
                fig, ax = plt.subplots()
                df.plot(ax=ax)
                ax.set_ylabel("調整後終値（円）")
                ax.set_title("株価推移")
                st.pyplot(fig)

                # リターンチャートの表示（オプション）
                with st.expander("📉 日次リターンのチャートを見る"):
                    fig2, ax2 = plt.subplots()
                    returns.plot(ax=ax2)
                    ax2.set_title("日次リターン")
                    st.pyplot(fig2)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        st.info(
            "証券コードが正しいことを確認してください。日本株の場合は通常、コードの後に '.T' を付けます（例: 7203.T）"
        )
