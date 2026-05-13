import pandas as pd
import requests

def update_nasdaq100_list():
    url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
    
    # 브라우저인 것처럼 속이는 헤더 추가
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # requests로 먼저 페이지 소스를 가져온 뒤 pandas로 넘깁니다
        response = requests.get(url, headers=headers)
        response.raise_for_status() # 200 OK가 아니면 에러 발생
        
        # 가져온 HTML 소스에서 테이블 추출
        tables = pd.read_html(response.text)
        
        # 나스닥 100 리스트는 보통 4번째(인덱스 4) 테이블에 있습니다
        # 위키피디아 구조 변경에 대비해 'Ticker' 컬럼이 있는 테이블을 찾습니다
        df = None
        for t in tables:
            if 'Ticker' in t.columns:
                df = t
                break
        
        if df is not None:
            tickers = df['Ticker'].tolist()
            
            # 파일 저장
            with open('ticker_list.txt', 'w') as f:
                for ticker in tickers:
                    f.write(f"{ticker}\n")
            print(f"성공: {len(tickers)}개 종목이 ticker_list.txt에 저장되었습니다.")
        else:
            print("오류: 종목 테이블을 찾을 수 없습니다.")

    except Exception as e:
        print(f"종목 갱신 실패: {e}")

if __name__ == "__main__":
    update_nasdaq100_list()