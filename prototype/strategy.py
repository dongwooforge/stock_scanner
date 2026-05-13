# strategy.py (엔진 역할 - Git 포함 가능)
import os
import pandas as pd
import numpy as np

def apply_strategy(df):
    """외부 로직 파일을 읽어서 실행하는 엔진"""
    logic_file = "my_private_logic.txt"
    
    if not os.path.exists(logic_file):
        return df

    with open(logic_file, "r", encoding="utf-8") as f:
        logic_code = f.read()
        
    local_vars = {'df': df.copy()} # 원본 훼손 방지를 위해 카피본 전달
    try:
        exec(logic_code, {}, local_vars)
        return local_vars['df']
    except Exception as e:
        print(f"전략 로직 실행 중 오류 발생: {e}")
        return df
    
    
if __name__ == "__main__":
    print("--- 🛠️ Strategy.py 장기 수렴(Squeeze) 테스트 모드 ---")
    
    # 1. 800봉 데이터 생성 (계산 여유분 확보)
    # FutureWarning 방지를 위해 '4H' 대신 '4h' 사용
    dates = pd.date_range(start="2024-01-01", periods=800, freq='4h')
    
    # 초기 300봉: 큰 변동성 (임계치를 높여두기 위함)
    prices = [100 + (np.sin(i/10) * 5) for i in range(300)]
    
    # 중간 400봉: 극도로 정적인 수렴 구간 (변동성 거의 제로)
    last_price = prices[-1]
    for _ in range(400):
        prices.append(last_price) # 가격 고정 (완벽한 수렴)
        
    # 마지막 100봉: 돌파 발생
    for i in range(1, 101):
        prices.append(prices[-1] * (1.10 if i == 1 else 1.01))

    df_test = pd.DataFrame({
        'Close': prices,
        'Volume': np.random.randint(100, 1000, size=len(prices))
    }, index=dates)

    # 2. 전략 적용
    result_df = apply_strategy(df_test)

    # 3. 결과 분석
    if 'Signal' in result_df.columns:
        # 수렴 지속 시간 확인
        duration_col = 'constrict_duration'
        if duration_col in result_df.columns:
            max_dur = result_df[duration_col].max()
            print(f"📊 최대 수렴 지속 시간 기록: {max_dur}봉")
            
            # 임계값과 현재 밴드폭 비교 (디버깅용)
            last_bw = result_df['bandwidth'].iloc[690]
            curr_th = result_df['bandwidth'].rolling(window=500).quantile(0.20).iloc[690]
            print(f"🔍 [체크] 수렴 구간 밴드폭: {last_bw:.6f} | 임계치: {curr_th:.6f}")

        signals = result_df[result_df['Signal'] == True]
        if len(signals) > 0:
            print(f"✅ 시그널 발견! 최초 발생 시점: {signals.index[0]}")
            print(signals[['Close', 'Signal']].head(1))
        else:
            print("\n⚠️ 여전히 시그널이 없습니다.")
            print("팁: my_private_logic.txt에서 threshold 계산 시 window를 500에서 300으로 줄여보세요.")