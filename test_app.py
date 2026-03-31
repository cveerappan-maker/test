from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Stock Screener" in response.data


def test_health():
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_stocks_returns_all():
    client = app.test_client()
    response = client.get("/api/stocks")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 20


def test_filter_by_sector():
    client = app.test_client()
    response = client.get("/api/stocks?sector=Energy")
    data = response.get_json()
    assert len(data) == 2
    assert all(s["sector"] == "Energy" for s in data)


def test_filter_by_price_range():
    client = app.test_client()
    response = client.get("/api/stocks?min_price=100&max_price=200")
    data = response.get_json()
    assert all(100 <= s["price"] <= 200 for s in data)


def test_filter_by_max_pe():
    client = app.test_client()
    response = client.get("/api/stocks?max_pe=15")
    data = response.get_json()
    assert all(s["pe_ratio"] <= 15 for s in data)


def test_filter_by_min_dividend():
    client = app.test_client()
    response = client.get("/api/stocks?min_dividend=3.0")
    data = response.get_json()
    assert all(s["dividend_yield"] >= 3.0 for s in data)


def test_sort_by_price_asc():
    client = app.test_client()
    response = client.get("/api/stocks?sort_by=price&sort_dir=asc")
    data = response.get_json()
    prices = [s["price"] for s in data]
    assert prices == sorted(prices)


def test_combined_filters():
    client = app.test_client()
    response = client.get("/api/stocks?sector=Technology&max_pe=35")
    data = response.get_json()
    assert all(s["sector"] == "Technology" and s["pe_ratio"] <= 35 for s in data)
