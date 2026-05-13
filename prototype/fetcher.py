import yfinance as yf
import pandas as pd

# 1. 출력 시 가독성 설정
pd.set_option('display.max_columns', None)  # 모든 컬럼 표시
pd.set_option('display.width', 1000)        # 출력 너비 충분히 확보
pd.set_option('display.float_format', '{:.2f}'.format) # 소수점 2자리 제한

def get_nasdaq_4h(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    
    # 데이터 가져오기 (7일치 60분봉)
    df = ticker.history(interval="60m", period="7d")
    
    if df.empty:
        return None
        
    # 한국 시간(KST)으로 변환
    df.index = df.index.tz_convert('Asia/Seoul') 
    
    # 2. 트레이딩뷰 스타일 4시간 봉 분류 로직 (서머타임 반영 KST 기준)
    def classify_nasdaq_time_kst(dt):
        # 22:30 ~ 익일 02:29 까지를 하나의 봉으로 묶음
        if dt.hour >= 22 or dt.hour < 2:
            if dt.hour >= 22:
                return dt.replace(hour=22, minute=30, second=0, microsecond=0)
            else: # 새벽 00:00 ~ 01:59 사이 데이터
                prev_day = dt - pd.Timedelta(days=1)
                return prev_day.replace(hour=22, minute=30, second=0, microsecond=0)
        else:
            # 02:30 ~ 장 마감까지를 두 번째 봉으로 묶음
            return dt.replace(hour=2, minute=30, second=0, microsecond=0)

    df = df.reset_index()
    df['group_time'] = df['Datetime'].apply(classify_nasdaq_time_kst)

    # OHLCV 데이터 집계
    ohlc_dict = {
        'Open': 'first', 
        'High': 'max', 
        'Low': 'min', 
        'Close': 'last', 
        'Volume': 'sum'
    }
    
    df_4h = df.groupby('group_time').agg(ohlc_dict)
    
    # 3. 시간 표시 포맷 변경 (보기 좋게 'YYYY-MM-DD HH:MM' 형식으로)
    df_4h.index = df_4h.index.strftime('%Y-%m-%d %H:%M')
    
    return df_4h

# 실행 및 결과 출력
if __name__ == "__main__":
    ticker = "TSLA"
    result = get_nasdaq_4h(ticker)
    
    if result is not None:
        print(f"\n--- {ticker} 트레이딩뷰 스타일 4시간 봉 (KST 기준) ---")
        print(result.tail(6)) # 최근 3일치(하루 2봉씩) 출력
        
        
        
        