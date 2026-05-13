import pandas as pd
import os
import numpy as np

DATA_DIR = "data"

def find_best_exit_settings(ticker, entry_signals):
    if not entry_signals:
        return None, 0

    file_path = os.path.join(DATA_DIR, f"{ticker}_4h.csv")
    if not os.path.exists(file_path):
        return None, 0
        
    df = pd.read_csv(file_path, index_col='group_time')
    
    # 익절/손절 후보 설정 (가장 현실적인 범위로 셋팅)
    tp_range = [0.03, 0.05, 0.07, 0.10, 0.15, 0.2, 0.3, 0.4, 0.5]
    sl_range = [0.02, 0.03, 0.05, 0.07]
    
    best_total_return = -999.0  # 비교 변수명 통일
    best_settings = (0.05, 0.03)

    # 1. 각 진입 시점별로 이후의 모든 봉 수익률을 미리 리스트화 (벡터화 준비)
    entry_results = []
    for entry in entry_signals:
        entry_time, entry_price = entry[0], entry[1]
        try:
            # 진입 시점 이후의 종가들을 가져와 수익률 배열 생성
            post_prices = df.loc[entry_time:].iloc[1:]['Close'].values
            if len(post_prices) > 0:
                returns = (post_prices - entry_price) / entry_price
                entry_results.append(returns)
        except KeyError:
            continue

    # 2. 최적화 루프 (iterrows 없이 Numpy 배열로 고속 연산)
    for tp in tp_range:
        for sl in sl_range:
            current_combination_return = 0.0
            
            for returns in entry_results:
                # 익절(tp) 혹은 손절(-sl)에 처음 도달하는 위치(index) 탐색
                hits = np.where((returns >= tp) | (returns <= -sl))[0]
                
                if len(hits) > 0:
                    # 첫 번째 도달한 지점의 수익률을 더함
                    current_combination_return += returns[hits[0]]
                else:
                    # 기간 내 도달 못했다면 마지막 봉의 수익률(미청산 상태) 적용
                    current_combination_return += returns[-1]
            
            # 3. 최고 성적 업데이트 (변수명 오타 수정 완료)
            if current_combination_return > best_total_return:
                best_total_return = current_combination_return
                best_settings = (tp, sl)
                
    return best_settings, best_total_return