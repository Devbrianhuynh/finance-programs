import csv

# Appends the ticker for each S & P 500 stock into the sp500_stocks list
def sp500_dataset():
    sp500_stocks = []

    with open(r'trading\options_research\SP500.csv') as tickers:
        ticker_file = csv.DictReader(tickers)

        major_stocks = ['AAPL', 'ADBE', 'AMZN', 'BA', 'BAC', 'BRK.B', 'C',
                        'CAT', 'CVX', 'DIS', 'DWDP', 'FB', 'GE', 'GOOG', 'GS',
                        'HD', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM', 
                        'MRK', 'MSFT', 'NKE', 'ORCL', 'PEP', 'PG', 'T', 'TRV', 
                        'UNH', 'UTX', 'V', 'VZ', 'WFC', 'WMT', 'XOM']

        for ticker in ticker_file:
            if ticker['Symbol'] in major_stocks:
                sp500_stocks.append(ticker['Symbol'])
    
    return sp500_stocks


# Same thing as the sp500_dataset but for ETFs
def etf_dataset():
    etf_options = []

    with open(r'trading\options_research\etfs.csv') as etfs:
        etf_file = csv.DictReader(etfs)

        major_etfs = ["GLD", "EEM", "EFA", "QQQ", "IVV", "VTI", "LQD", "IWF", "IWM", "BND",
                        "HYG", "IWD", "DIA", "JNK", "VNQ", "IJH", "VIG", "EWZ", "MDY", "IAU",
                        "XLK", "XLE", "VEA", "XLF", "VUG", "IWB", "VEU", "GDX", "FXI", "XLU",
                        "VTV", "EWJ", "XLP", "IVE", "IEF", "EMB", "IWO", "XLV", "IYR", "TBT",
                        "IWP", "OEF", "XLI", "EPP", "IWV", "VV", "VYM", "RSP", "BIV", "TLT",
                        "VOO", "VGK", "ACWI", "VGT", "IJS", "IEI", "VBK"]

        for etf in etf_file:
            if etf['Symbol'] in major_etfs:
                etf_options.append(etf['Symbol'])
    
    return etf_options


# Combine the stock and ETF lists together to get the full package
def full_options_list():
    return sp500_dataset() + etf_dataset()



