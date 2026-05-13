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
├── scanner.py             # 종목 선별 로직 (Strategy 활용)
├── strategy.py            # 다양한 투자 전략 모음
├── backtester.py          # 과거 데이터 검증 로직
├── requirements.txt       # 사용한 라이브러리 목록 (pandas, yfinance 등)
└── data/                  # (선택) 수집한 데이터 저장 폴더 (.gitignore 설정 권장)

"""


import os
from fetcher import get_nasdaq_4h

def load_tickers(file_path):
    """텍스트 파일에서 티커 리스트를 읽어옵니다."""
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일이 없습니다.")
        return []
    
    with open(file_path, 'r') as f:
        # 줄바꿈 제거, 빈 줄 제외, 중복 제거
        tickers = [line.strip().upper() for line in f if line.strip()]
        return sorted(list(set(tickers)))

def main():
    # 1. 감시할 종목 리스트 불러오기
    ticker_file = 'ticker_list.txt'
    tickers = load_tickers(ticker_file)
    
    if not tickers:
        print("수집할 종목이 없습니다. ticker_list.txt를 확인하세요.")
        return

    print(f"--- 총 {len(tickers)}개 종목 데이터 수집 시작 ---")
    
    all_data = {}
    failed_tickers = []

    # 2. 루프를 돌며 데이터 수집 (Fetcher 활용)
    for i, ticker in enumerate(tickers):
        try:
            print(f"[{i+1}/{len(tickers)}] {ticker} 수집 중...", end='\r')
            df = get_nasdaq_4h(ticker)
            
            if df is not None and not df.empty:
                all_data[ticker] = df
            else:
                failed_tickers.append(ticker)
        except Exception as e:
            print(f"\n{ticker} 수집 중 오류 발생: {e}")
            failed_tickers.append(ticker)

    print(f"\n\n--- 수집 완료: {len(all_data)}종목 성공 / {len(failed_tickers)}종목 실패 ---")
    
    if failed_tickers:
        print(f"실패 종목: {', '.join(failed_tickers)}")

    # 3. 데이터 확인 (예: 첫 번째 성공 종목의 마지막 데이터)
    if all_data:
        first_ticker = list(all_data.keys())[0]
        print(f"\n[{first_ticker}] 최신 4시간 봉 데이터:")
        print(all_data[first_ticker].tail(2))
        
    return all_data

if __name__ == "__main__":
    # 수집된 데이터를 메모리에 유지하거나 분석기로 넘깁니다.
    scanner_data = main()