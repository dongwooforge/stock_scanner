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
├── backtester.py          # 과거 데이터 검증 로직
├── requirements.txt       # 사용한 라이브러리 목록 (pandas, yfinance 등)
└── data/                  # (선택) 수집한 데이터 저장 폴더 (.gitignore 설정 권장)

main에서 ticker_list.txt를 가져와서 fetcher.py에게 전달, 
fetcher.py에서는 list에 있는 종목들의 ohlcv 데이터를 저장


"""


import os
from fetcher import get_nasdaq_4h
from scanner import scan_tickers, generate_report

def load_tickers(file_path):
    """텍스트 파일에서 티커 리스트를 읽어옵니다."""
    if not os.path.exists(file_path):
        print(f"오류: {file_path} 파일이 없습니다.")
        return []
    
    with open(file_path, 'r') as f:
        # 줄바꿈 제거, 빈 줄 제외, 중복 제거
        tickers = [line.strip().upper() for line in f if line.strip()]
        return sorted(list(set(tickers)))

# main.py 핵심 부분만 발췌
def main():
    # 1. 티커 로드
    ticker_file = 'ticker_list.txt'
    tickers = load_tickers(ticker_file)
    
    # 2. Fetcher: 데이터 수집 (하드디스크 업데이트용)
    print("--- [1/3] 데이터 업데이트 시작 ---")
    for i, ticker in enumerate(tickers):
        print(f"[{i+1}/{len(tickers)}] {ticker} 업데이트 중...", end='\r')
        get_nasdaq_4h(ticker) # 결과값을 변수에 담지 않고 하드 저장만 수행

    # 3. Scanner: 하드디스크의 데이터를 직접 읽어 분석
    print("\n\n--- [2/3] 전략 스캔 시작 ---")
    # 메모리에 올리지 않고 티커 리스트만 전달
    signals = scan_tickers(tickers)

    # 4. 리포트
    generate_report(signals)

if __name__ == "__main__":
    main()