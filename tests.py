from app import client


def test_simple():
    mylist = [1, 2, 3, 4, 5]

    assert 3 in mylist

def test_issues():
    res = client.get('/issues')

    assert res.status_code == 200

    json = (res.get_json())
    print(f'json = {json}')

    assert len(res.get_json()) == 10

    assert True
