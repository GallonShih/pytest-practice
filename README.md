<!-- GETTING STARTED -->
## Getting Started

1. 建立虛擬環境
```
python -m venv test-env
```
2. 啟動虛擬環境

3. 安裝套件
```
pip install -r requirements.txt
```
4. 執行 ETL 程式
```
python main.py
```
5. 執行測試
```
pytest -vv --cov tasks/
```
6. 查看 coverage 情況
```
coverage report -m
```
