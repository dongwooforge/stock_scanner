"""
프로젝트 목적 : 주식시장의 가격정보를 취합하여 가공, 분석, 실별하여 투자활동에
적극적으로 도움을 줄 수 있는 기능을 실현한다.

프로젝트 구성 :
    (1) Fetcher : data를 수집하여 가공 및 저장
    (2) Scanner : 데이터를 분석하여 strategy에 맞는 종목을 선별
    (2-1) Strategy : 전략을 작성
    (3) Backtester : 선별된 종목의 과거 데이터를 stategy에 투입하여 전략의 신뢰성 분석
    
    (4) Main : 위 모듈들을 순서대로 실행하고 최종 리포트를 출력
    
stock_scanner/
├── main.py                # 전체 프로세스 실행
├── fetcher.py             # 데이터 수집 및 가공 로직
├── update_tickers.py      # 조건에 맞는 종목 리스트 생성기(예:나스닥 상위 100개 종목)
├  └── ticker_list.txt
├── scanner.py             # 종목 선별 로직 (Strategy 활용)
├── strategy.py            # 다양한 투자 전략 모음
├── backtester.py          # 과거 데이터 검증 로직(매수)
├── optimizer.py           # 익,손절 최적값 계산(매도)
├── requirements.txt       # 사용한 라이브러리 목록 (pandas, yfinance 등)
└── data/                  # (선택) 수집한 데이터 저장 폴더 (.gitignore 설정 권장)

main에서 ticker_list.txt를 가져와서 fetcher.py에게 전달, 
fetcher.py에서는 list에 있는 종목들의 ohlcv 데이터를 저장


"""


import os
from fetcher import get_nasdaq_4h
from scanner import scan_tickers, generate_report
from backtester import get_entry_signals
from optimizer import find_best_exit_settings
import sys

def load_tickers(file_path):
    """텍스트 파일에서 티커 리스트를 읽어옵니다."""
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일이 없습니다.")
        return []
    
    with open(file_path, 'r') as f:
        tickers = [line.strip().upper() for line in f if line.strip()]
        return sorted(list(set(tickers)))

def main():
    # 1. 티커 로드
    ticker_file = 'ticker_list.txt'
    tickers = load_tickers(ticker_file)
    total_tickers = len(tickers)
    
    if not tickers:
        print("수집할 종목이 없습니다. ticker_list.txt를 확인하세요.")
        return

    # 2. Fetcher: 데이터 업데이트 (진행률 표시)
    print(f"--- [1/3] 데이터 업데이트 시작 (총 {total_tickers}개) ---")
    # for i, ticker in enumerate(tickers):
    #     progress = (i + 1) / total_tickers * 100
    #     sys.stdout.write(f"\r진행률: {progress:5.1f}% | [{i+1}/{total_tickers}] {ticker:<6} 업데이트 중...")
    #     sys.stdout.flush()
    #     get_nasdaq_4h(ticker)

    # 3. Scanner: 시그널 종목 선별
    print("\n\n--- [2/3] 전략 스캔 시작 ---")
    signals = scan_tickers(tickers)
    total_signals = len(signals)

    # 4. Optimizer: 시그널 종목 정밀 분석 및 데이터 바인딩
    print(f"\n--- [3/3] 종목별 최적화 분석 시작 (대상: {total_signals}개) ---")
    
    final_briefing = []
    
    for i, s in enumerate(signals):
        ticker = s['ticker']
        progress = (i + 1) / total_signals * 100
        
        sys.stdout.write(f"\r분석 중: {progress:5.1f}% | [{i+1}/{total_signals}] {ticker:<6} 최적화 계산 중...")
        sys.stdout.flush()
        
        # 과거 진입 시점들 추출
        entries = get_entry_signals(ticker) 
        # 최적 익절/손절 값 및 기대 수익률 계산
        best_set, score = find_best_exit_settings(ticker, entries)
        
        if best_set:
            # 리포트에서 사용할 상세 데이터를 개별 키로 저장
            s['tp'] = best_set[0] * 100
            s['sl'] = best_set[1] * 100
            s['score'] = score * 100
            s['entry_count'] = len(entries)
            s['has_opt'] = True
        else:
            s['has_opt'] = False
        
        final_briefing.append(s)

    # 5. 최종 리포트 출력 (전문 브리핑 형식)
    print("\n")
    generate_report(final_briefing)

if __name__ == "__main__":
    main()