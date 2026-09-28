@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ========================================================
echo 1. Python 버전 확인
python --version
if errorlevel 1 goto PYTHON_ERR

echo.
echo 2. 라이브러리 설치 상태 점검
pip install streamlit google-api-python-client pandas

echo.
echo 3. Streamlit 실행 시도
streamlit run app.py
if errorlevel 1 (
    echo.
    echo [재시도] python -m streamlit 방식으로 실행합니다...
    python -m streamlit run app.py
)

pause
exit /b

:PYTHON_ERR
echo [오류] Python이 설치되어 있지 않거나 환경 변수에 등록되지 않았습니다.
pause