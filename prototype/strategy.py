# strategy.py (엔진 역할 - Git 포함 가능)
import os

def apply_strategy(df):
    """
    외부 로직 파일을 읽어서 실행하는 보안 엔진
    """
    logic_file = "my_private_logic.txt" # 혹은 .py
    
    if not os.path.exists(logic_file):
        # 전략 파일이 없을 경우 기본값 반환
        return df

    # 외부 파일의 로직을 읽어옴
    with open(logic_file, "r", encoding="utf-8") as f:
        logic_code = f.read()
        print(logic_code)
    # 로컬 변수 환경에서 로직 실행
    # df 변수가 로직 안에서 수정되도록 전달
    local_vars = {'df': df}
    try:
        exec(logic_code, {}, local_vars)
        return local_vars['df']
    except Exception as e:
        print(f"전략 로직 실행 중 오류 발생: {e}")
        return df