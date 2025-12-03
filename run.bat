@echo off
echo Starting IMDb Review Sentiment Analyzer...
echo.
echo Checking dependencies...
python -c "import flask; import tensorflow; import nltk" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    python -c "import nltk; nltk.download('stopwords')"
)
echo.
echo Starting Flask server...
echo Opening http://localhost:5000 in your browser...
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
