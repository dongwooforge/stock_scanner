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
    print("\n" + "Selection Report: Quantitative Strategy Analysis".center(70, "="))
    
    for s in signals:
        ticker = s['ticker']
        price = s['price']
        
        print(f"▶ [{ticker}] 현 시점 기준 매수 시그널이 식별되었습니다.")
        print(f"   - 현재가: ${price:.2f}")
        
        # has_opt 플래그를 확인하여 안전하게 데이터에 접근
        if s.get('has_opt'):
            tp = s['tp']
            sl = s['sl']
            score = s['score']
            count = s['entry_count']
            
            print(f"   - 과거 {count}회의 동일 패턴을 분석한 결과,")
            print(f"   - 최적의 대응 가이드는 [익절 {tp:.1f}% / 손절 {sl:.1f}%] 입니다.")
            print(f"   - 해당 원칙 준수 시 기대 누적 수익률은 약 {score:.1f}%로 시뮬레이션되었습니다.")
        else:
            print("   - [주의] 과거 데이터 부족으로 인해 시뮬레이션 결과가 제공되지 않습니다.")
        
        print("-" * 70)
    print("=" * 70 + "\n")