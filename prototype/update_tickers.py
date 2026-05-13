import pandas as pd
import requests


def update_combined_ticker_list():
    """나스닥 100과 S&P 500 리스트를 통합하여 저장합니다."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    combined_tickers = set()

    # 1. 나스닥 100 수집
    try:
        url_ndx = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        res = requests.get(url_ndx, headers=headers)
        tables = pd.read_html(res.text)
        for t in tables:
            if 'Ticker' in t.columns:
                combined_tickers.update(t['Ticker'].tolist())
                break
        print("나스닥 100 수집 완료.")
    except Exception as e:
        print(f"나스닥 100 수집 실패: {e}")

    # 2. S&P 500 수집 (미국 시장의 심장)
    try:
        url_spy = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        res = requests.get(url_spy, headers=headers)
        tables = pd.read_html(res.text)
        for t in tables:
            # S&P 500은 컬럼명이 'Symbol'인 경우가 많습니다
            target_col = 'Symbol' if 'Symbol' in t.columns else 'Ticker'
            if target_col in t.columns:
                combined_tickers.update(t[target_col].tolist())
                break
        print("S&P 500 수집 완료.")
    except Exception as e:
        print(f"S&P 500 수집 실패: {e}")

    # 3. 데이터 정제 (점(.)이 포함된 티커를 하이픈(-)으로 변경 - yfinance 호환용)
    clean_tickers = [str(t).replace('.', '-') for t in combined_tickers if pd.notna(t)]
    clean_tickers = sorted(list(set(clean_tickers)))

    # 4. 파일 저장
    with open('ticker_list.txt', 'w') as f:
        for ticker in clean_tickers:
            f.write(f"{ticker}\n")
    
    print("-" * 50)
    print(f"🎯 최종 통합 리스트: {len(clean_tickers)}개 종목 저장 완료!")
    print("-" * 50)

if __name__ == "__main__":
    update_combined_ticker_list()