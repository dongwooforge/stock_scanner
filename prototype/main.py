"""
프로젝트 목적 : 국내 주식시장의 가격정보를 취합하여 가공, 분석, 실별하여 투자활동에
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