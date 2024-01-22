# Use quicksort for the list of stocks with the EPS, P/E, P/B, etc.
from stock_algo_and_csv import ticker_list, quicksort, HashMap
import yfinance as yf
import math
import ast

class Investor:
    def __init__(self, price_preference = 100, position = 'buy', risk = 'low', budget = 10000):
        self.price_preference = price_preference
        self.position = position 
        self.risk = risk
        self.budget = budget
        self.hash_map = HashMap() 
        self.sorted_stocks = []
        # self.industry = industry (soon, add a new feature that recommends stocks based on the user's desired industry)


    # Price preference is set to 100 and over (high-priced stock have lower risk and volatility than their cheap counterparts)
    # Give the consumer two choices: Their preferred stock price or, if they aren't sure, set it to a defaut of $100
    # There must be a more efficient way of iterating through the stocks: yf.Ticker('MSFT GOOG AAPL META'); once finished with the MVP, try to test this new method
    def sort_stocks_by_price(self):
        print('\n\nResearching all NASDAQ and NYSE securities:\n')
        print('DISCLAIMER: Due to the colossal dataset of indices, this process may take a while. Leave your device on for 5 minutes (or more depending on your internet speed)\n')

        for ticker in ticker_list():
            try:
                stock_price = yf.Ticker(ticker).info['currentPrice']

                if stock_price >= self.price_preference:
                    print(f'Match found: {ticker} - {stock_price}') # For feedback purposes only

                    self.hash_map.assign_hash(ticker, stock_price)

                    # Using this of sorted stocks, take the length of it, create a new hash map called new_hash_map = HashMap(len(self.sorted_stocks))
                    # For loop the list to get its ticker and put the ticker in retrieve_hash(ticker) to get its value
                    # In the new_hash_map, make the key the ticker and the value the value you received from retrieve_hash
                    self.sorted_stocks.append(ticker) 
                
                else:
                    print(f'{ticker} - {stock_price}') # For feedback purposes only

            except:
                continue # Skip this stock and continue searching
        

        self.new_hash_map(self.sorted_stocks)
    

    def new_hash_map(self, sorted_stocks):
        new_hash_map = HashMap(len(sorted_stocks))

        for ticker in sorted_stocks:
            price = self.hash_map.retrieve_hash(ticker)

            new_hash_map.assign_hash(ticker, price)
        
        self.hash_map = new_hash_map
        

    # Use recursion and add a stock_... default parameters; add a list parameter that iterates through a list using recursion +1 (index)
    # Retrieve all the stocks inside the hash map
    def pull_stock_data(self):
        for ticker in self.sorted_stocks:
            stock_price = self.hash_map.retrieve_hash(ticker)

            stock = yf.Ticker(ticker)

            # Above 10 = long
            try:
                stock_eps = stock.info['trailingEps']
            except:
                stock_eps = 0

            # Below 10 = long
            try:
                stock_pe = stock.info['trailingPE']
            except:
                stock_pe = 0
            try:
                stock_ps = stock.info['priceToSalesTrailing12Months']
            except:
                stock_ps = 0
            try:
                stock_pb = stock.info['priceToBook']
            except:
                stock_pb = 0
            try:
                stock_ev_ebitda = stock.info['enterpriseToEbitda']
            except:
                stock_ev_ebitda = 0

            # Above 0.05 = long
            try:
                stock_ra = stock.info['returnOnAssets']
            except:
                stock_ra = 0

            # Above 0.15 = long
            try:
                stock_re = stock.info['returnOnEquity']
            except:
                stock_re = 0 

            # Above 0.10 = long
            try:
                stock_gm = stock.info['grossMargins']
            except:
                stock_gm = 0
            try:
                stock_em = stock.info['ebitdaMargins']
            except:
                stock_em = 0
            try:
                stock_om = stock.info['operatingMargins']
            except:
                stock_om = 0
            try:
                stock_pm = stock.info['profitMargins']
            except:
                stock_pm = 0

            # Above 0.01 = long
            try:
                stock_qr = stock.info['quickRatio']
            except:
                stock_qr = 0
            try:
                stock_cr = stock.info['currentRatio']
            except:
                stock_cr - 0

            # Below 1.5 = long
            try:
                stock_de = stock.info['debtToEquity']
            except:
                stock_de = 0

            # Below 1,000 = extremely risky
            try:
                stock_daily_volume = stock.info['averageDailyVolume10Day'] # Only used as a precaution
            except:
                stock_daily_volume = 0

            # If higher than or equal to 9, the stock is worthy of buying long; otherwise, short
            points = 0

            # Call the helper function sort_stocks_by_long if the consumer wants to buy
            self.sort_stocks_by_long_or_short(ticker, stock_price, points, stock_eps, stock_pe, stock_ps, stock_pb, stock_ev_ebitda, stock_ra, stock_re, stock_gm, stock_em, stock_om, stock_pm, stock_qr, stock_cr, stock_de, stock_daily_volume)


    # Take the ticker and plug it inside the if/elif/else statements for EPS, P/E, PB, P/S, D/E, D/A analysis
    # If the stock passes the test, add +1 point (points is initiaized to 0)
    # A stock needs at least 9 points for it to be long/short position-worthy
    # Do not create a new hash map, simply adjust/change its value
    # For the tickers that passed the analysis, put it inside the hash map; key = ticker, value = [current_price, long/short, points]
    def sort_stocks_by_long_or_short(self, ticker, ticker_price, points, stock_eps, stock_pe, stock_ps, stock_pb, stock_ev_ebitda, stock_ra, stock_re, stock_gm, stock_em, stock_om, stock_pm, stock_qr, stock_cr, stock_de, stock_daily_volume):
        if stock_eps >= 10:
            points += 1 
        
        # Rather than manually defining if statements, implement a for loop to iterate through the price-to ratios and enterprise-valueto-EBITDA ratio
        for price_to_ratio in [stock_pe, stock_ps, stock_pb, stock_ev_ebitda]:
            if price_to_ratio < 10:
                points += 1
        
        if stock_ra > 0.05:
            points += 1
        
        if stock_re > 0.15:
            points += 1
        
        for margins_ratio in [stock_gm, stock_em, stock_om, stock_pm]:
            if margins_ratio > 10:
                points += 1
        
        for quick_and_current_ratio in [stock_qr, stock_cr]:
            if quick_and_current_ratio > 0.01:
                points += 1
        
        if stock_de <= 1.5:
            points += 1

        if stock_daily_volume <= 1000:
            points -= 5 # Stocks that trader under a daily volume of 1000 is extremely risky
        

        # Reassign the hashes with new information
        if points >= 11:
            self.hash_map.assign_hash(ticker, [ticker, ticker_price, 'Risk: Low', 'MUST BUY', points]) # Risk: Low
        elif points >= 8:
            self.hash_map.assign_hash(ticker, [ticker, ticker_price, 'Risk: Low-Medium', 'buy', points]) # Risk: Low-medium
        elif points < 8 and points > 5:
            self.hash_map.assign_hash(ticker, [ticker, ticker_price, 'Risk: Medium-High', 'short', points]) # Risk: Medium-high
        elif points >= 1:
            self.hash_map.assign_hash(ticker, [ticker, ticker_price, 'Risk: High', 'MUST SHORT', points]) # Risk: High (shorting is always 'high risk')
        else:
            self.hash_map.assign_hash(ticker, [ticker, ticker_price, 'Risk: Do not consider buying or shorting this equity', 'MUST NOT BUY/SHORT', points])


    # SOON MAKE THE LIST A CSV FILE INSTEAD OF JUST A LIST
    # Also used to find 
    # Return a list of stocks that are worthy of buying 
    # Implements the quicksort algorithm that sorts out the stocks with the most points (top of the list) and the stocks with the least points (bottom of the list)
    # Does not consider stocks that give the most bang for your buck
    def return_buy_stocks(self):
        buy_list = []
        
        for ticker in self.sorted_stocks:
            stock_info = self.hash_map.retrieve_hash(ticker)
            purchase_choice = stock_info[3]

            if purchase_choice == 'MUST BUY' or purchase_choice == 'buy':
                buy_list.append(stock_info)
                
        if buy_list is None:
            return 'We don\'t recommend buying any stocks at your preferred price; no stock passed our test'
            
        quicksort(buy_list, 0, len(buy_list) - 1)

        if self.risk is not None:
            return self.return_buy_risk_stocks(buy_list)
        else:
            print(f'\n\n\nBest stocks to {self.position}:\n')
            return buy_list
        
    
    # Takes the list from return_buy_stocks and futher filters it to match the investor's risk apetite
    def return_buy_risk_stocks(self, buy_list):
        buy_risk_list = []

        for stock_info in buy_list:
            if stock_info[2] == self.risk:
                buy_risk_list.append(stock_info)
        
        if buy_risk_list is None:
            return 'We don\'t recommend buying any stocks at your preferred risk apetite and price; no stock passed our test'
        
        print(f'\n\n\nBest stocks to {self.position}:\n')
        return buy_risk_list
    

    # Same as the return_buy_stocks but for shorting
    def return_short_stocks(self):
        short_list = []

        for ticker in self.sorted_stocks:
            stock_info = self.hash_map.retrieve_hash(ticker)
            purchase_choice = stock_info[3]

            if purchase_choice == 'MUST SHORT' or purchase_choice == 'short':
                short_list.append(stock_info)
        
        if short_list is None:
            return 'We don\'t recommend buying any shorting at your preferred price; no stock passed our test'
        
        quicksort(short_list, 0, len(short_list) - 1)

        if self.risk is not None:
            return self.return_short_risk_stocks(short_list)
        else:
            print(f'\n\n\nBest stocks to {self.position}:\n')
            return short_list
    

    def return_short_risk_stocks(self, short_list):
        short_risk_stocks = []

        for stock_info in short_list:
            if stock_info[2] == self.risk:
                short_risk_stocks.append(stock_info)
        
        if short_risk_stocks is None:
            return 'We don\'t recommend shorting any stocks at your preferred risk apetite and price; no stock passed our test'
        
        print(f'\n\n\nBest stocks to {self.position}:\n')
        return short_risk_stocks
    

    # Matrix and parameters will be initialized in stock_recommender.py, according to the investor's budget preference
    # In stock_recommender.py: Give the investor two options: 
            # 1. Return a list of stocks that give the most bang for your buck (if so, the knapsack method will activate)
            # 2. Return a list of stocks that purely has the best stats for buying or shorting (e.g., 'MUST BUY' and 'MUST SHORT'); knapsack is not needed for this
    # shares_buyable: [ticker, # of shares you can buy based off of your budget-per-stock] - this is a sublist --> [[####]]
    def knapsack(self, maximum_budget, budget_per_stock, shares_buyable):
        rows = len(budget_per_stock) + 1
        columns = maximum_budget + 1

        matrix = [[] for x in range(rows)]

        for row_index in range(rows):
            matrix[row_index] = [-1 for y in range(columns)]

            for column_index in range(columns):
                if row_index == 0 or column_index == 0:
                    matrix[row_index][column_index] = 0

                elif budget_per_stock[row_index - 1] <= column_index:
                    include_stock_from_portfolio = shares_buyable[row_index - 1][-1] + matrix[row_index - 1][column_index - budget_per_stock[row_index - 1]]
                    exclude_stock_from_portfolio = matrix[row_index - 1][column_index]

                    matrix[row_index][column_index] = max(include_stock_from_portfolio, exclude_stock_from_portfolio)
        

        ticker_and_shares_buyable = {}
        for ticker, shares_you_can_buy in shares_buyable:
            ticker_and_shares_buyable[ticker] = shares_you_can_buy
        
        max_shares = matrix[rows - 1][maximum_budget]
        buyable_tickers = self.knapsack_tickers(list(ticker_and_shares_buyable.keys()), max_shares,ticker_and_shares_buyable)


        return f'{int(max_shares)} shares you can buy with: {buyable_tickers}'
    

    # We have the # of shares an investor can buy, but what stocks?
    # The knapsack problem does not give us enough data to discover what stocks to buy based on the # of shares we can buy
    def knapsack_tickers(self, shares_buyable, number_of_shares, ticker_and_shares_buyable):
        def backtrack(target, ticker_list, start):
            if target == 0:
                result.append(list(ticker_list))
                return
            
            elif target < 0:
                return # If it is less than 0, this is invalid
            
            # If target is not negative and greater than zero:
            for index in range(start, len(shares_buyable)):
                ticker_list.append(shares_buyable[index])

                print(ticker_list)

                backtrack(target - ticker_and_shares_buyable[shares_buyable[index]], ticker_list, index + 1)
                ticker_list.pop()


        result = []    
        backtrack(number_of_shares, [], 0)
        return result
    

    def lookup_single_stock(self, ticker):
        return self.hash_map.retrieve_hash(ticker)


# Should any problems arise, use this code below to make tests
# investor = Investor(30, 'short', 'Risk: Medium-High', 90000)
# investor.sort_stocks_by_price()
# investor.pull_stock_data()
# print(investor.return_short_stocks())

