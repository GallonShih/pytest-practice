from tasks.task1 import ETL

etl = ETL(a=4, b=2)

def test_plus_func():
    assert etl.plus() == 6

def test_minus_func():
    assert etl.minus() == 2
