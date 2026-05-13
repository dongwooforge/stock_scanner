import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# 1. 출력 및 경로 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_nasdaq_4h(ticker_symbol):
    file_path = os.path.join(DATA_DIR, f"{ticker_symbol}_4h.csv")
    
    # [STEP 1] 날짜 설정 (오늘부터 300일 전까지)
    end_dt = datetime.now()
    start_dt = end_dt - timedelta(days=300)
    
    start_str = start_dt.strftime('%Y-%m-%d')
    end_str = end_dt.strftime('%Y-%m-%d')
    
    # 데이터 가져오기 (안전한 호출을 위해 start/end 사용)
    ticker = yf.Ticker(ticker_symbol)
    new_df = ticker.history(interval="60m", start=start_str, end=end_str)
    
    if new_df.empty:
        print(f"[{ticker_symbol}] 데이터를 불러오지 못했습니다.")
        return None
        
    # 한국 시간(KST) 변환
    new_df.index = new_df.index.tz_convert('Asia/Seoul')
    
    # [STEP 2] 4시간 봉 가공 로직
    def classify_nasdaq_time_kst(dt):
        if dt.hour >= 22 or dt.hour < 2:
            if dt.hour >= 22:
                return dt.replace(hour=22, minute=30, second=0, microsecond=0)
            else:
                prev_day = dt - timedelta(days=1)
                return prev_day.replace(hour=22, minute=30, second=0, microsecond=0)
        else:
            return dt.replace(hour=2, minute=30, second=0, microsecond=0)

    new_df = new_df.reset_index()
    new_df['group_time'] = new_df['Datetime'].apply(classify_nasdaq_time_kst)
    
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
    new_df_4h = new_df.groupby('group_time').agg(ohlc_dict)
    
    # 인덱스를 문자열 포맷으로 통일 (저장용)
    new_df_4h.index = new_df_4h.index.strftime('%Y-%m-%d %H:%M')

    # [STEP 3] 기존 파일 로드 및 병합
    if os.path.exists(file_path):
        # index_path -> index_col로 수정
        old_df = pd.read_csv(file_path, index_col='group_time')
        
        # 합치기 전 데이터 타입 통일
        combined_df = pd.concat([old_df, new_df_4h])
        # 중복 제거 (최신 데이터 우선)
        combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
        combined_df = combined_df.sort_index()
    else:
        combined_df = new_df_4h

    # [STEP 4] 하드디스크 저장
    combined_df.to_csv(file_path)
    
    return combined_df

if __name__ == "__main__":
    ticker = "TSLA"
    result = get_nasdaq_4h(ticker)
    if result is not None:
        print(f"\n--- {ticker} 300일 데이터 수집 및 저장 완료 ---")
        print(f"전체 봉 개수: {len(result)}")
        print(result.tail(6))