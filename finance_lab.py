import yahoo_fin.stock_info as si
import math

# Preferences for risk: High risk, low risk, moderate risk; preferences for long/short and call/put; preferences for dividends
# Create methods that calculate if a security is/not undervalued and volatile; combine these methods to create a single method that decides what stocks a consumer should buy/sell
# Use points system (e.g., if META scores 30 points (and the required passing score for buy/long is 25), META is a 'buy')
# Input for the preference of stock
class Stock:
    def __init__(self, ticker, price, eps, pe, ps, pb, ra, re, de, bvps, most_active, most_gain, most_lose, volume, dividends):
        self.ticker = ticker
        self.price = price
        self.eps = eps
        self.pe = pe
        self.ps = ps
        self.pb = pb
        self.ra = ra
        self.re = re
        self.de = de
        self.bvps = bvps
        self.most_active = most_active
        self.most_gain = most_gain
        self.most_lose = most_lose
        self.volume = volume
        self.dividends = dividends
        self.points = 0 # if the result is True, +1 point; minimum of 9 to pass; 12 max
        self.portfolio = []

    def __repr__(self):
        description = f'{self.ticker} is selling at {self.price}/share.'

        if self.ticker in self.most_active:
            description += f' {self.ticker} is an active stock.'
        if self.ticker in self.most_gain:
            description += f' {self.ticker} is ↑ in price.'
        if self.ticker in self.most_lose:
            description += f'{self.ticker} is ↓ in price.'

        return description

    def buy_low_risk_preference(self):
        stock_feedback = 'Be careful for the stock\'s: '

        if self.eps >= 10:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for eps; '
        else:
            stock_feedback += 'Low EPS; '

        if self.pe < 10:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for p/e; '
        else:
            stock_feedback += 'high P/E ratio; '
        
        if self.ps < 10:
            self.points += 1
        elif type(self.ps) == bool:
            stock_feedback += 'no info for p/s; '
        else:
            stock_feedback += 'high P/S ratio; '
        
        if self.pb < 10:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for p/b; '
        else:
            stock_feedback += 'high P/B ratio; '
        
        if self.ra > 5:
            self.points += 1
        elif type(self.ra) == bool:
            stock_feedback += 'no info for ra; '
        else:
            stock_feedback += 'low return-on-assets; '
        
        if self.re > 15:
            self.points += 1
        elif type(self.re) == bool:
            stock_feedback += 'no info for return-on-equity; '
        else:
            stock_feedback += 'low return-on-equity; '
        
        if self.de < 2:
            self.points += 1
        elif type(self.de) == bool:
            stock_feedback += 'no info for debt-to-equity; '
        else:
            stock_feedback += 'high debt-to-equity ratio; '

        if self.bvps > self.price:
            self.points += 1
        elif type(self.bvps) == bool:
            stock_feedback += 'no info for book-value-per-share; '
        else:
            stock_feedback += 'book-value-per-share is lower than stock price; '

        if self.ticker not in self.most_active:
            self.points += 1
        else:
            stock_feedback += 'stock is too volatile; '

        if self.ticker in self.most_gain or self.ticker not in self.most_gain or self.ticker not in self.most_lose:
            self.points += 1
        else:
            stock_feedback += 'stock is declining; '

        if self.volume > 25000000:
            self.points += 1
        elif type(self.volume) == bool:
            stock_feedback += 'no info for volume; '
        else:
            stock_feedback += 'stock\'s volume too low; '

        if self.dividends != False:
            self.points += 1

        if self.points == 12:
            stock_feedback = 'This stock is a STRONG buy.'
        elif 12 < self.points >= 9:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a good buy.' + stock_feedback
        else:
            self.portfolio.append(f'Do NOT buy {self.ticker}.')

        if 'STRONG' not in stock_feedback and 'good' not in stock_feedback:
            stock_feedback = list(stock_feedback)
            stock_feedback[-1] = '.'
            stock_feedback = ''.join(stock_feedback)

        return self.portfolio, stock_feedback

    def buy_moderate_risk_preference(self):
        stock_feedback = 'Be careful for the stock\'s: '

        if self.eps >= 10:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for eps; '
        else:
            stock_feedback += 'Low EPS; '

        if self.pe < 20:
            self.points += 1
        elif type(self.pe) == bool:
            stock_feedback += 'no info for p/e; '
        else:
            stock_feedback += 'high P/E ratio; '
        
        if self.ps < 20:
            self.points += 1
        elif type(self.ps) == bool:
            stock_feedback += 'no info for p/s; '
        else:
            stock_feedback += 'high P/S ratio; '
        
        if self.pb < 20:
            self.points += 1
        elif type(self.pb) == bool:
            stock_feedback += 'no info for p/b; '
        else:
            stock_feedback += 'high P/B ratio; '
        
        if self.ra > 5:
            self.points += 1
        elif type(self.ra) == bool:
            stock_feedback += 'no info for return-on-assets; '
        else:
            stock_feedback += 'low return-on-assets; '
        
        if self.re > 10:
            self.points += 1
        elif type(self.re) == bool:
            stock_feedback += 'no info for return-on-equity; '
        else:
            stock_feedback += 'low return-on-equity; '
        
        if self.de < 2:
            self.points += 1
        elif type(self.de) == bool:
            stock_feedback += 'no info for debt-to-equity; '
        else:
            stock_feedback += 'high debt-to-equity ratio; '

        if self.bvps > self.price:
            self.points += 1
        elif type(self.bvps) == bool:
            stock_feedback += 'no info for book-value-per-share; '
        else:
            stock_feedback += 'book-value-per-share is lower than stock price; '

        if self.ticker in self.most_active:
            self.points += 1
        else:
            stock_feedback += 'stock is too volatile; '

        if self.ticker in self.most_gain or self.ticker not in self.most_gain or self.ticker not in self.most_lose:
            self.points += 1
        else:
            stock_feedback += 'stock is declining; '

        if self.volume > 20000000:
            self.points += 1
        elif type(self.volume) == bool:
            stock_feedback += 'no info for volume; '
        else:
            stock_feedback += 'stock\'s volume too low; '

        if self.dividends != False:
            self.points += 1

        if self.points == 12:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a STRONG buy.'
        elif 12 < self.points >= 7:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a good buy.' + stock_feedback
        else:
            self.portfolio.append(f'Do NOT buy {self.ticker}.')
        
        if 'STRONG' not in stock_feedback and 'good' not in stock_feedback:
            stock_feedback = list(stock_feedback)
            stock_feedback[-1] = ''
            stock_feedback[-2] = '.'
            stock_feedback = ''.join(stock_feedback)

        return self.portfolio, stock_feedback

    def buy_high_risk_preference(self):
        stock_feedback = 'Be careful for the stock\'s: '

        if self.eps >= 10:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for eps; '
        else:
            stock_feedback += 'Low EPS; '

        if self.pe < 30:
            self.points += 1
        elif type(self.pe) == bool:
            stock_feedback += 'no info for p/e; '
        else:
            stock_feedback += 'high P/E ratio; '
        
        if self.ps < 30:
            self.points += 1
        elif type(self.ps) == bool:
            stock_feedback += 'no info for p/s; '
        else:
            stock_feedback += 'high P/S ratio; '
        
        if self.pb < 30:
            self.points += 1
        elif type(self.pb) == bool:
            stock_feedback += 'no info for p/b; '
        else:
            stock_feedback += 'high P/B ratio; '
        
        if self.ra > 5:
            self.points += 1
        elif type(self.ra) == bool:
            stock_feedback += 'no info for return-on-assets; '
        else:
            stock_feedback += 'low return-on-assets; '
        
        if self.re > 10:
            self.points += 1
        elif type(self.re) == bool:
            stock_feedback += 'no info for return-on-equity; '
        else:
            stock_feedback += 'low return-on-equity; '
        
        if self.de < 2:
            self.points += 1
        elif type(self.de) == bool:
            stock_feedback += 'no info for debt-to-equity; '
        else:
            stock_feedback += 'high debt-to-equity ratio; '

        if self.bvps > self.price:
            self.points += 1
        elif type(self.bvps) == bool:
            stock_feedback += 'no info for book-value-per-share; '
        else:
            stock_feedback += 'book-value-per-share is lower than stock price; '

        if self.ticker in self.most_active:
            self.points += 1
        else:
            stock_feedback += 'stock is too volatile; '

        if self.ticker in self.most_gain or self.ticker not in self.most_gain or self.ticker not in self.most_lose:
            self.points += 1
        else:
            stock_feedback += 'stock is declining; '

        if self.volume > 15000000:
            self.points += 1
        elif type(self.volume) == bool:
            stock_feedback += 'no info for volume; '
        else:
            stock_feedback += 'stock\'s volume too low; '

        if self.dividends != False:
            self.points += 1

        if self.points == 12:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a STRONG buy.'
        elif 12 < self.points >= 5:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a good buy.' + stock_feedback
        else:
            self.portfolio.append(f'Do NOT buy {self.ticker}.')
        
        if 'STRONG' not in stock_feedback and 'good' not in stock_feedback:
            stock_feedback = list(stock_feedback)
            stock_feedback[-1] = ''
            stock_feedback[-2] = '.'
            stock_feedback = ''.join(stock_feedback)

        return self.portfolio, stock_feedback

    # Should be a stock that is NOT in get_day_gainers() and IN get_day_losers
    # ALWAYS HIGH RISK
    # Calculate if the stock is overvalued
    def short_preference(self):
        stock_feedback = 'Be careful for the stock\'s: '

        if self.eps <= 20:
            self.points += 1
        elif type(self.eps) == bool:
            stock_feedback += 'no info for earnings-per-share; '
        else:
            stock_feedback += 'high EPS; '

        if self.pe > 20:
            self.points += 1
        elif type(self.pe) == bool:
            stock_feedback += 'no info for p/e; '
        else:
            stock_feedback += 'low P/E ratio; '
        
        if self.ps > 20:
            self.points += 1
        elif type(self.ps) == bool:
            stock_feedback += 'no info for p/s; '
        else:
            stock_feedback += 'low P/S ratio; '
        
        if self.pb > 20:
            self.points += 1
        elif type(self.pb) == bool:
            stock_feedback += 'no info for p/b; '
        else:
            stock_feedback += 'low P/B ratio; '
        
        if self.ra < 15:
            self.points += 1
        elif type(self.ra) == bool:
            stock_feedback += 'no info for return-on-assets; '
        else:
            stock_feedback += 'high return-on-assets; '
        
        if self.re < 30:
            self.points += 1
        elif type(self.re) == bool:
            stock_feedback += 'no info for return-on-equity; '
        else:
            stock_feedback += 'high return-on-equity; '
        
        if self.de > 1.5:
            self.points += 1
        elif type(self.de) == bool:
            stock_feedback += 'no info for debt-to-equity; '
        else:
            stock_feedback += 'high debt-to-equity ratio; '

        if self.bvps < self.price:
            self.points += 1
        elif type(self.bvps) == bool:
            stock_feedback += 'no info for book-value-per-share; '    
        else:
            stock_feedback += 'book-value-per-share is higher than stock price; '

        if self.ticker in self.most_active:
            self.points += 1
        else:
            stock_feedback += 'stock is not active enough; '

        if self.ticker not in self.most_gain or self.ticker in self.most_lose or self.ticker not in self.most_lose:
            self.points += 1
        else:
            stock_feedback += 'stock is going up; '

        if self.volume < 20000000:
            self.points += 1
        elif type(self.volume) == bool:
            stock_feedback += 'no info for volume; '
        else:
            stock_feedback += 'stock\'s volume too high; '

        if self.dividends != False:
            self.points += 1

        if self.points == 12:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a STRONG short.'
        elif self.points < 12 and self.points >= 7:
            self.portfolio.append(self.ticker)
            stock_feedback = 'This stock is a good short. ' + stock_feedback
        else:
            self.portfolio.append(f'Do NOT short {self.ticker}.')
        
        if 'STRONG' not in stock_feedback and 'good' not in stock_feedback:
            stock_feedback = list(stock_feedback)
            stock_feedback[-1] = ''
            stock_feedback[-2] = '.'
            stock_feedback = ''.join(stock_feedback)

        return self.portfolio, stock_feedback

# If they prefer long, the security must be undervalued, and vice versa for shorting
class Person:
    def __init__(self, buy_or_short, risk_appetite, want_dividends, portfolio, name):
        self.buy_or_short = buy_or_short
        self.risk_appetite = risk_appetite
        self.want_dividends = want_dividends
        self.portfolio = portfolio
        self.name = name
        self.partners = []
    
    def __repr__(self):
        description = f'Hello {self.name}.'
        return description

    def exchange(self, other_person):
        if self.buy_or_short == other_person.buy_or_short and self.risk_appetite == other_person.risk_appetite:
            self.partners.append(other_person.name)
            print('You two should be investing/trading partners!')
        else:
            print('He/she may not be the right investing/trader for you!')
        
# Terminal
# Asks consumer what stock he/she wishes to screen
print('What stock would you like us to screen? NASDAQ securities only.')
ticker = input()
ticker = ticker.upper()
if ticker in si.tickers_nasdaq():
    # Gets the: price, eps, p/e ratio, volume
    data_info = si.get_quote_table(ticker)
    price = data_info['Quote Price']
    if math.isnan(data_info['EPS (TTM)']) == True:
        eps = bool
    else:
        eps = data_info['EPS (TTM)'] # Higher than or equal to 10 = good
    if math.isnan(data_info['PE Ratio (TTM)']) == True:
        pe = bool
    else:
        pe = data_info['PE Ratio (TTM)'] # Lower than 10 = good
    if math.isnan(data_info['Avg. Volume']) == True:
        volume_of_stock = bool
    else:
        volume_of_stock = data_info['Avg. Volume'] # If volume OVER than 20M = good; high volume = safe and LESS volatile; low volume = risky and MORE volatile (for shorting)

    # Gets the: p/s ratio, p/b ratio
    data_price_to = si.get_stats_valuation(ticker)
    if type(data_price_to.loc[5][1]) == float:
        ps = bool
    else:
        ps = float(data_price_to.loc[5][1]) # Lower than 10 = good
    if type(data_price_to.loc[6][1]) == float:
        pb = bool
    else:
        pb = float(data_price_to.loc[6][1]) # Lower than 10 = good

    # Gets the: return-on-assets, return-on-equity, debt-equity ratio, book-value-per-share, dividend-yield
    data_returns = si.get_stats(ticker)
    if type(data_returns['Value'][33]) == float:
        ra = bool
    else:
        ra = float(data_returns['Value'][33].strip('%')) # Higher than 5% = good
    if type(data_returns['Value'][34]) == float:
        re = bool
    else:
        re = float(data_returns['Value'][34].strip('%')) # Higher than 15% = good
    if type(data_returns['Value'][46]) == float:
        de = bool
    else:
        de = float(data_returns['Value'][46].strip('%')) / 100 # Lower than 2 = undervalued
    if type(data_returns['Value'][48]) == float:
        bvps = bool
    else:
        bvps = float(data_returns['Value'][48].strip('%')) # BVPS HIGHER than stock price = undervalued; BVPS LOWER than stock price = overvalued
    if type(data_returns['Value'][20]) == float:
        dividends_of_stock = bool
    else:
        dividends_of_stock = float(data_returns['Value'][20].strip('%'))

    # Gets the: most active stocks, stocks with the highest gains; volatility
    active_stocks = si.get_day_most_active() # For volatility if self.ticker in self.active_stocks:...
    gaining_stocks = si.get_day_gainers() # For buy/long positions
    losing_stocks = si.get_day_losers() # In the object, use: if self.ticker in self.losing_stocks: print('This stock is for shorting')

    # Inputs the instance variables
    stock_one = Stock(ticker, price, eps, pe, ps, pb, ra, re, de, bvps, active_stocks, gaining_stocks, losing_stocks, volume_of_stock, dividends_of_stock)

    # Asks a follow up question
    print('Do you want to buy/long or sell/short?')
    buy_or_sell = input()
    buy_or_sell = buy_or_sell.lower()

    if buy_or_sell == 'buy' or buy_or_sell == 'long' or buy_or_sell == 'buy/long':
        print('What is your risk appetite: Low risk, moderate risk, or high risk?')
        risk = input()
        risk = risk.lower()

        print('Do you want the stock to pay dividends? Answer: \'Yes\' OR \'No\'')
        dividend = input()
        dividend = dividend.lower()

        if risk == 'low risk' or risk == 'low':
            if dividend == 'yes':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'low', True, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

            elif dividend == 'no':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'low', False, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

        elif risk == 'moderate risk' or risk == 'moderate':
            if dividend == 'yes':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'moderate', True, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

            elif dividend == 'no':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'moderate', False, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

        elif risk == 'high risk' or risk == 'high':
            if dividend == 'yes':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'high', True, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

            elif dividend == 'no':
                print('What is your name?')
                name = input()
                name = name.title()
                person_one = Person('buy', 'high', False, ticker, name)
                print(stock_one.buy_low_risk_preference())
                print(stock_one)

                print('Would you like to continue?')
                continue_person = input()
                if continue_person == 'yes':
                    print(person_one)

                    print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
                    partner = input()
                    partner = partner.title()
                    if partner == 'No':
                        print('We hope you find your future investing/trading partner soon!')
                    else:
                        print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                        purchase = input()
                        print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                        other_risk = input()
                        print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                        other_dividend = input()
                        if other_dividend == 'dividend':
                            other_dividend_input = True
                        else:
                            other_dividend_input = False
                        print('What stock are they currently looking at or talking about? Put the ticker.')
                        other_ticker = input()
                        other_ticker.upper()

                        person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                        print(person_one.exchange(person_two))
                else:
                    print('We hope you use our product again soon!')

    elif buy_or_sell == 'sell' or buy_or_sell == 'short' or buy_or_sell == 'sell/short':
        print('What is your name?')
        name = input()
        name = name.title()
        person_one = Person('buy', 'low', True, ticker, name)
        print(stock_one.buy_low_risk_preference())
        print(stock_one)

        print('Would you like to continue?')
        continue_person = input()
        if continue_person == 'yes':
            print(person_one)

            print('Is there someone else you know who also invests/trades stocks/bonds/crypto? If so, put their name! If not, put, \'no\'.')
            partner = input()
            partner = partner.title()
            if partner == 'No':
                print('We hope you find your future investing/trading partner soon!')
            else:
                print('What are his/her purchasing preferences? Does he/she buy or short? Put either \'buy\' or \'short\'.')
                purchase = input()
                print('What is his/her risk appetite? Low, moderate, or high? Put either \'low\' or \'moderate\' or\'high\'.')
                other_risk = input()
                print('Do they prefer dividend stocks or growth stocks? Put either \'diviend\' or \'growth\'')
                other_dividend = input()
                if other_dividend == 'dividend':
                    other_dividend_input = True
                else:
                    other_dividend_input = False
                print('What stock are they currently looking at or talking about? Put the ticker.')
                other_ticker = input()
                other_ticker.upper()

                person_two = Person(purchase, other_risk, other_dividend_input, other_ticker, partner)
                print(person_one.exchange(person_two))
        else:
            print('We hope you use our product again soon!')

    else:
        print('Sorry, this is not an option.')

else:
    print('This stock is not in NASDAQ exchange.')











