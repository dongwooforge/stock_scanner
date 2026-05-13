# backtester.py
import pandas as pd
import os
from strategy import apply_strategy

DATA_DIR = "data"

def get_entry_signals(ticker): # 인자명을 df에서 ticker로 변경
    """
    티커를 받아 하드디스크의 데이터를 읽고, 
    매수 시그널(Entry)이 발생한 모든 지점을 반환합니다.
    """
    file_path = os.path.join(DATA_DIR, f"{ticker}_4h.csv")
    
    if not os.path.exists(file_path):
        return []
        
    # 1. 하드디스크에서 데이터 로드
    df = pd.read_csv(file_path, index_col='group_time')
    
    # 2. 전략 적용
    df = apply_strategy(df)
    
    # 3. 시그널 확인 (df가 문자열이 아닌 데이터프레임인지 확인)
    if not isinstance(df, pd.DataFrame) or 'Signal' not in df.columns:
        return []
    
    # 4. 시그널이 True인 지점의 데이터 추출
    entries = df[df['Signal'] == True].copy()
    
    # [인덱스, 진입가격] 리스트 반환
    return entries[['Close']].reset_index().values.tolist()