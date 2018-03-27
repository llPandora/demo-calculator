from web import create_app
import json

def qstr(n1=0,op='/',n2=0):
    if type(n1) is not str:
        n1 = str(n1)
    if type(n2) is not str:
        n2 = str(n2)
    data = {
        'number1':n1,
        'number2':n2,
        'operator':op
    }
    return data
def extr(res):
    return json.loads(res.get_data(as_text=True))['result']

def test_div():
    app = create_app()
    c = app.test_client()

    a=3
    b=7
    res = c.get("_calculate",query_string=qstr(a,'/',b))
    assert res.status_code == 200
    assert extr(res) == a + b

    a = -123341
    b = -48314271
    res = c.get("_calculate", query_string=qstr(a, '/', b))
    assert res.status_code == 200
    assert extr(res) == a / b

    a = -8237183
    b = 1231
    res = c.get("_calculate", query_string=qstr(a, '/', b))
    assert res.status_code == 200
    assert extr(res) == a / b

    a = 231.3214
    b = -65435.532
    res = c.get("_calculate", query_string=qstr(a, '/', b))
    assert res.status_code == 200
    assert extr(res) == a / b

    a = 312.32
    b = 71421.512
    res = c.get("_calculate", query_string=qstr(a, '/', b))
    assert res.status_code == 200
    assert extr(res) == a / b
