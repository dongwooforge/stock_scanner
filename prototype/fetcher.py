import yfinance as yf
import pandas as pd
import os

# 1. 출력 및 경로 설정
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_nasdaq_4h(ticker_symbol):
    file_path = os.path.join(DATA_DIR, f"{ticker_symbol}_4h.csv")
    
    #데이터 가져오기 (7일치)
    ticker = yf.Ticker(ticker_symbol)
    new_df = ticker.history(interval="60m", period="7d")
    
    if new_df.empty:
        return None
        
    # 한국 시간(KST) 변환 및 4시간 봉 가공
    new_df.index = new_df.index.tz_convert('Asia/Seoul')
    
    def classify_nasdaq_time_kst(dt):
        if dt.hour >= 22 or dt.hour < 2:
            if dt.hour >= 22:
                return dt.replace(hour=22, minute=30, second=0, microsecond=0)
            else:
                prev_day = dt - pd.Timedelta(days=1)
                return prev_day.replace(hour=22, minute=30, second=0, microsecond=0)
        else:
            return dt.replace(hour=2, minute=30, second=0, microsecond=0)

    new_df = new_df.reset_index()
    new_df['group_time'] = new_df['Datetime'].apply(classify_nasdaq_time_kst)
    
    ohlc_dict = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}
    new_df_4h = new_df.groupby('group_time').agg(ohlc_dict)
    new_df_4h.index = new_df_4h.index.strftime('%Y-%m-%d %H:%M')

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path, index_path='group_time')
        # 새로운 데이터와 합친 후 인덱스 기준 중복 제거 (최신 데이터 우선)
        combined_df = pd.concat([old_df, new_df_4h])
        combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
        combined_df = combined_df.sort_index()
    else:
        combined_df = new_df_4h


    combined_df.to_csv(file_path)
    
    return combined_df

if __name__ == "__main__":
    ticker = "TSLA"
    result = get_nasdaq_4h(ticker)
    if result is not None:
        print(f"\n--- {ticker} 데이터 로드 및 저장 완료 ---")
        print(result.tail(6))