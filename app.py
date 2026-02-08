from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

STOCKS = [
    {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology", "price": 189.84, "market_cap": 2940, "pe_ratio": 31.2, "dividend_yield": 0.55, "volume": 54200000, "change_pct": 1.23},
    {"ticker": "MSFT", "name": "Microsoft Corp.", "sector": "Technology", "price": 378.91, "market_cap": 2810, "pe_ratio": 36.8, "dividend_yield": 0.74, "volume": 22100000, "change_pct": 0.87},
    {"ticker": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "price": 141.80, "market_cap": 1780, "pe_ratio": 25.4, "dividend_yield": 0.0, "volume": 25400000, "change_pct": -0.45},
    {"ticker": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "price": 178.25, "market_cap": 1850, "pe_ratio": 60.1, "dividend_yield": 0.0, "volume": 47300000, "change_pct": 2.15},
    {"ticker": "NVDA", "name": "NVIDIA Corp.", "sector": "Technology", "price": 495.22, "market_cap": 1220, "pe_ratio": 65.3, "dividend_yield": 0.04, "volume": 41200000, "change_pct": 3.42},
    {"ticker": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "price": 390.42, "market_cap": 1000, "pe_ratio": 28.9, "dividend_yield": 0.36, "volume": 18700000, "change_pct": -1.12},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services", "price": 172.45, "market_cap": 497, "pe_ratio": 10.8, "dividend_yield": 2.38, "volume": 9800000, "change_pct": 0.56},
    {"ticker": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "price": 156.74, "market_cap": 378, "pe_ratio": 22.1, "dividend_yield": 3.01, "volume": 7200000, "change_pct": -0.34},
    {"ticker": "V", "name": "Visa Inc.", "sector": "Financial Services", "price": 271.89, "market_cap": 556, "pe_ratio": 30.5, "dividend_yield": 0.77, "volume": 6500000, "change_pct": 0.92},
    {"ticker": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Defensive", "price": 152.31, "market_cap": 358, "pe_ratio": 25.7, "dividend_yield": 2.46, "volume": 6100000, "change_pct": 0.18},
    {"ticker": "UNH", "name": "UnitedHealth Group", "sector": "Healthcare", "price": 527.35, "market_cap": 486, "pe_ratio": 21.9, "dividend_yield": 1.42, "volume": 3400000, "change_pct": -0.78},
    {"ticker": "HD", "name": "Home Depot Inc.", "sector": "Consumer Cyclical", "price": 345.12, "market_cap": 343, "pe_ratio": 23.4, "dividend_yield": 2.51, "volume": 3900000, "change_pct": 0.65},
    {"ticker": "XOM", "name": "Exxon Mobil Corp.", "sector": "Energy", "price": 104.56, "market_cap": 418, "pe_ratio": 11.2, "dividend_yield": 3.54, "volume": 15600000, "change_pct": -1.87},
    {"ticker": "BAC", "name": "Bank of America Corp.", "sector": "Financial Services", "price": 33.21, "market_cap": 263, "pe_ratio": 9.4, "dividend_yield": 2.89, "volume": 38200000, "change_pct": 1.05},
    {"ticker": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "price": 28.95, "market_cap": 163, "pe_ratio": 15.3, "dividend_yield": 5.68, "volume": 28700000, "change_pct": -2.34},
    {"ticker": "KO", "name": "Coca-Cola Co.", "sector": "Consumer Defensive", "price": 58.92, "market_cap": 255, "pe_ratio": 23.8, "dividend_yield": 3.12, "volume": 12100000, "change_pct": 0.41},
    {"ticker": "CVX", "name": "Chevron Corp.", "sector": "Energy", "price": 152.87, "market_cap": 289, "pe_ratio": 12.6, "dividend_yield": 3.98, "volume": 7800000, "change_pct": -1.53},
    {"ticker": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical", "price": 245.34, "market_cap": 780, "pe_ratio": 72.8, "dividend_yield": 0.0, "volume": 118500000, "change_pct": 4.67},
    {"ticker": "WMT", "name": "Walmart Inc.", "sector": "Consumer Defensive", "price": 163.45, "market_cap": 440, "pe_ratio": 27.3, "dividend_yield": 1.38, "volume": 8200000, "change_pct": 0.29},
    {"ticker": "DIS", "name": "Walt Disney Co.", "sector": "Communication Services", "price": 91.23, "market_cap": 167, "pe_ratio": 42.5, "dividend_yield": 0.0, "volume": 10500000, "change_pct": -0.98},
]

SECTORS = sorted({s["sector"] for s in STOCKS})


@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE, sectors=SECTORS)


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/stocks")
def api_stocks():
    filtered = list(STOCKS)

    sector = request.args.get("sector")
    if sector:
        filtered = [s for s in filtered if s["sector"] == sector]

    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    if min_price is not None:
        filtered = [s for s in filtered if s["price"] >= min_price]
    if max_price is not None:
        filtered = [s for s in filtered if s["price"] <= max_price]

    min_cap = request.args.get("min_market_cap", type=float)
    max_cap = request.args.get("max_market_cap", type=float)
    if min_cap is not None:
        filtered = [s for s in filtered if s["market_cap"] >= min_cap]
    if max_cap is not None:
        filtered = [s for s in filtered if s["market_cap"] <= max_cap]

    max_pe = request.args.get("max_pe", type=float)
    if max_pe is not None:
        filtered = [s for s in filtered if s["pe_ratio"] <= max_pe]

    min_div = request.args.get("min_dividend", type=float)
    if min_div is not None:
        filtered = [s for s in filtered if s["dividend_yield"] >= min_div]

    min_vol = request.args.get("min_volume", type=float)
    if min_vol is not None:
        filtered = [s for s in filtered if s["volume"] >= min_vol]

    sort_by = request.args.get("sort_by", "market_cap")
    sort_dir = request.args.get("sort_dir", "desc")
    if sort_by in ("price", "market_cap", "pe_ratio", "dividend_yield", "volume", "change_pct"):
        filtered.sort(key=lambda s: s[sort_by], reverse=(sort_dir == "desc"))

    return jsonify(filtered)


HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Screener</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
        }
        header {
            background: #1e293b;
            border-bottom: 1px solid #334155;
            padding: 1rem 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        header h1 { font-size: 1.5rem; color: #38bdf8; }
        header .subtitle { font-size: 0.85rem; color: #94a3b8; }
        .layout {
            display: flex;
            max-width: 1400px;
            margin: 0 auto;
            gap: 1.5rem;
            padding: 1.5rem;
        }
        .filters {
            width: 280px;
            flex-shrink: 0;
            background: #1e293b;
            border-radius: 0.75rem;
            padding: 1.25rem;
            border: 1px solid #334155;
            height: fit-content;
            position: sticky;
            top: 1.5rem;
        }
        .filters h2 { font-size: 1rem; margin-bottom: 1rem; color: #38bdf8; }
        .filter-group { margin-bottom: 1rem; }
        .filter-group label {
            display: block;
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 0.3rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .filter-group select,
        .filter-group input {
            width: 100%;
            padding: 0.5rem;
            border-radius: 0.375rem;
            border: 1px solid #475569;
            background: #0f172a;
            color: #e2e8f0;
            font-size: 0.9rem;
        }
        .filter-row {
            display: flex;
            gap: 0.5rem;
        }
        .filter-row input { width: 50%; }
        .btn {
            width: 100%;
            padding: 0.6rem;
            border: none;
            border-radius: 0.375rem;
            cursor: pointer;
            font-size: 0.9rem;
            font-weight: 600;
            margin-top: 0.25rem;
        }
        .btn-primary { background: #38bdf8; color: #0f172a; }
        .btn-primary:hover { background: #7dd3fc; }
        .btn-secondary { background: #334155; color: #94a3b8; margin-top: 0.5rem; }
        .btn-secondary:hover { background: #475569; }
        .results { flex: 1; min-width: 0; }
        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }
        .results-header h2 { font-size: 1rem; color: #94a3b8; }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 0.75rem;
            overflow: hidden;
            border: 1px solid #334155;
        }
        th {
            text-align: left;
            padding: 0.75rem 1rem;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            background: #1e293b;
            border-bottom: 1px solid #334155;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }
        th:hover { color: #38bdf8; }
        th.sorted { color: #38bdf8; }
        td {
            padding: 0.65rem 1rem;
            font-size: 0.9rem;
            border-bottom: 1px solid #1e293b;
        }
        tr:hover { background: #263347; }
        .ticker { font-weight: 700; color: #38bdf8; }
        .name { color: #94a3b8; font-size: 0.8rem; }
        .positive { color: #4ade80; }
        .negative { color: #f87171; }
        .number { text-align: right; font-variant-numeric: tabular-nums; }
        .sector-badge {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            background: #334155;
            color: #cbd5e1;
        }
        .loading { text-align: center; padding: 3rem; color: #64748b; }
        @media (max-width: 768px) {
            .layout { flex-direction: column; }
            .filters { width: 100%; position: static; }
        }
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Stock Screener</h1>
            <span class="subtitle">Filter and sort stocks by key metrics</span>
        </div>
    </header>
    <div class="layout">
        <aside class="filters">
            <h2>Filters</h2>
            <div class="filter-group">
                <label>Sector</label>
                <select id="sector">
                    <option value="">All Sectors</option>
                    {% for s in sectors %}
                    <option value="{{ s }}">{{ s }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="filter-group">
                <label>Price Range ($)</label>
                <div class="filter-row">
                    <input type="number" id="min_price" placeholder="Min" step="0.01">
                    <input type="number" id="max_price" placeholder="Max" step="0.01">
                </div>
            </div>
            <div class="filter-group">
                <label>Market Cap ($B)</label>
                <div class="filter-row">
                    <input type="number" id="min_market_cap" placeholder="Min" step="1">
                    <input type="number" id="max_market_cap" placeholder="Max" step="1">
                </div>
            </div>
            <div class="filter-group">
                <label>Max P/E Ratio</label>
                <input type="number" id="max_pe" placeholder="e.g. 30" step="0.1">
            </div>
            <div class="filter-group">
                <label>Min Dividend Yield (%)</label>
                <input type="number" id="min_dividend" placeholder="e.g. 2.0" step="0.1">
            </div>
            <div class="filter-group">
                <label>Min Volume</label>
                <input type="number" id="min_volume" placeholder="e.g. 10000000" step="1000000">
            </div>
            <button class="btn btn-primary" onclick="fetchStocks()">Screen Stocks</button>
            <button class="btn btn-secondary" onclick="resetFilters()">Reset Filters</button>
        </aside>
        <main class="results">
            <div class="results-header">
                <h2 id="results-count">Loading...</h2>
            </div>
            <table>
                <thead>
                    <tr>
                        <th onclick="sortBy('ticker')">Ticker</th>
                        <th onclick="sortBy('sector')">Sector</th>
                        <th onclick="sortBy('price')" class="number">Price</th>
                        <th onclick="sortBy('change_pct')" class="number">Change</th>
                        <th onclick="sortBy('market_cap')" class="number">Mkt Cap ($B)</th>
                        <th onclick="sortBy('pe_ratio')" class="number">P/E</th>
                        <th onclick="sortBy('dividend_yield')" class="number">Div Yield</th>
                        <th onclick="sortBy('volume')" class="number">Volume</th>
                    </tr>
                </thead>
                <tbody id="stock-table"></tbody>
            </table>
        </main>
    </div>
    <script>
        let currentSort = 'market_cap';
        let currentDir = 'desc';

        function sortBy(field) {
            if (currentSort === field) {
                currentDir = currentDir === 'desc' ? 'asc' : 'desc';
            } else {
                currentSort = field;
                currentDir = 'desc';
            }
            document.querySelectorAll('th').forEach(th => th.classList.remove('sorted'));
            event.target.classList.add('sorted');
            fetchStocks();
        }

        function getParams() {
            const params = new URLSearchParams();
            const fields = ['sector', 'min_price', 'max_price', 'min_market_cap',
                          'max_market_cap', 'max_pe', 'min_dividend', 'min_volume'];
            fields.forEach(f => {
                const val = document.getElementById(f).value;
                if (val) params.set(f, val);
            });
            params.set('sort_by', currentSort);
            params.set('sort_dir', currentDir);
            return params;
        }

        async function fetchStocks() {
            const params = getParams();
            const resp = await fetch('/api/stocks?' + params.toString());
            const stocks = await resp.json();
            const tbody = document.getElementById('stock-table');
            document.getElementById('results-count').textContent =
                stocks.length + ' stock' + (stocks.length !== 1 ? 's' : '') + ' found';
            tbody.innerHTML = stocks.map(s => `
                <tr>
                    <td><span class="ticker">${s.ticker}</span><br><span class="name">${s.name}</span></td>
                    <td><span class="sector-badge">${s.sector}</span></td>
                    <td class="number">$${s.price.toFixed(2)}</td>
                    <td class="number ${s.change_pct >= 0 ? 'positive' : 'negative'}">
                        ${s.change_pct >= 0 ? '+' : ''}${s.change_pct.toFixed(2)}%
                    </td>
                    <td class="number">$${s.market_cap}B</td>
                    <td class="number">${s.pe_ratio.toFixed(1)}</td>
                    <td class="number">${s.dividend_yield.toFixed(2)}%</td>
                    <td class="number">${(s.volume / 1e6).toFixed(1)}M</td>
                </tr>
            `).join('');
        }

        function resetFilters() {
            document.querySelectorAll('.filters input, .filters select').forEach(el => el.value = '');
            currentSort = 'market_cap';
            currentDir = 'desc';
            fetchStocks();
        }

        fetchStocks();
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
