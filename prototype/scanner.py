# scanner.py
import pandas as pd
import os
from strategy import apply_strategy

DATA_DIR = "data"

def scan_tickers(ticker_list):
    """
    메모리 대신 하드디스크의 CSV 파일을 하나씩 읽어서 전략을 적용합니다.
    """
    signals = []
    
    print("\n--- 🔍 하드디스크 데이터 기반 스캔 시작 ---")
    
    for ticker in ticker_list:
        file_path = os.path.join(DATA_DIR, f"{ticker}_4h.csv")
        
        if not os.path.exists(file_path):
            # print(f"[{ticker}] 데이터 파일이 없어 스킵합니다.")
            continue
            
        try:
            # 1. 하드에서 데이터 로드
            df = pd.read_csv(file_path, index_col='group_time')
            
            # 2. 전략 적용 (보안 엔진 호출)
            analyzed_df = apply_strategy(df)
            
            # 3. 시그널 확인
            if 'Signal' in analyzed_df.columns and not analyzed_df.empty:
                if analyzed_df['Signal'].iloc[-1] == True:
                    signals.append({
                        'ticker': ticker,
                        'price': analyzed_df['Close'].iloc[-1],
                        'time': analyzed_df.index[-1]
                    })
        except Exception as e:
            print(f"[{ticker}] 분석 중 오류 발생: {e}")
                
    return signals

def generate_report(signals):
    # 기존과 동일 (결과 출력 로직)
    print("=" * 50)
    if not signals:
        print("현재 시그널이 발생한 종목이 없습니다.")
    else:
        print(f"🎯 총 {len(signals)}개의 종목에서 매수 시그널이 발견되었습니다!")
        print("-" * 50)
        for s in signals:
            print(f"▶ [{s['ticker']}] 현재가: {s['price']:.2f} | 발생시간: {s['time']}")
    print("=" * 50)