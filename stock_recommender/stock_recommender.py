# Implement the knapsack problem and algorithm
# Put the best canidates into a list
# Use the quicksort algorithm to sort the list of stocks based on their given score (higher score = better quality equity)
# Return the 1. Stock and a list of its forerunners using 2. Stock, 3. Stock, etc., with a new line for each number
from stock_picker import Investor
import time

class Terminal:
    def __init__(self):
        self.investor = None 
        self.sorted_stocks = []
        self.start_time = None
        self.end_time = None

    def terminal(self):
        self.start_time = time.time()

        self.greet()
        self.collect_investor_preferences()
        self.research_equities()
        self.give_user_option()
        self.farewell()

        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        print(f'\n\n{elapsed_time:.3f} seconds\n\n')


    def greet(self):
        print('Chicagotrade® Securities Advisor™')
        print('\nChicagotrade® is a high-frequency trading and technology deployment company, headquartered in Chicago, Illinois, U.S.A\n')
        print('\nTHIS PRODUCT IS RESEARCHED, BUILT, AND DEPLOYED BY Chicagotrade®\n')
        print('\nThis product is assuming that the customer\'s endevour is:\n 1. To get the most \'bang for your buck\' per share\n 2. Maximize returns\n 3. Avoid unhealthy/dangerous stocks\n')
        print('\nThis product is assuming that the customer\'s endevour is NOT: Minimizing risk through low volatility (low volatility = low ROI (which violates this product\'s assumptions))')
        print('\n\nProcessing request user\'s request now...\n\n')


    def collect_investor_preferences(self):
        print('Fill out this preference sheet:')

        # Price preference
        user_preferred_price = input( 'Price of stock (this product will recommend stocks that are equal to or above this price): $')
        while True:
            try:
                user_preferred_price = float(user_preferred_price)
                break

            except ValueError:
                print('Invalid: Enter a valid answer')
                user_preferred_price = float(input( 'Price of stock (this product will recommend stocks that are equal to or above this price): $'))


        # Buy or short 
        user_preferred_position = input( 'Buy or short stocks?: ').lower()
        
        while user_preferred_position != 'buy' and user_preferred_position != 'short':
            print('Enter \'buy\' or \'short\'')
            user_preferred_position = input( 'Buy or short stocks?: ').lower()
            

        # Risk apetite
        user_preferred_risk = input( 'Risk appetite (1) Low (2) Low-medium (3) Medium-high (4) High (if undecided, put \'none\'): ').title()
        if 'None' in user_preferred_risk:
            user_preferred_risk = None

        else:
            while user_preferred_risk != 'Low' and user_preferred_risk != 'Low-Medium' and user_preferred_risk != 'Medium-High' and user_preferred_risk != 'High':
                print('Enter a valid response')
                user_preferred_risk = input( 'Risk appetite (1) Low (2) Low-medium (3) Medium-high (4) High (if undecided, put \'none\'): ').title()
            
            user_preferred_risk = 'Risk: ' + user_preferred_risk
                

        # Budget
        user_budget = input( 'Budget (if you don\'t have a set budget, put \'none\'): $')
        if 'none' in user_budget or 'None' in user_budget:
            user_budget = None

        else:
            while True:
                try: 
                    user_budget = float(user_budget)
                    break
                except ValueError:
                    print('Invalid: Enter a valid answer')
                    user_budget = input( 'Budget (if you don\'t have a set budget, put \'none\'): $')


        self.investor = Investor(user_preferred_price, user_preferred_position, user_preferred_risk, user_budget)
        self.investor.sort_stocks_by_price()

        # Once the sorting is completed
        print('All information received and sorted')
        print(f'\n\nYour preferences:\n Price of stock: {user_preferred_price}\n Method of purchase: {user_preferred_position}\n Risk apetite: {user_preferred_risk}\n Budget: {user_budget}\n\n')


    # Researches all of the stocks that are equal to or are above the preferred stock price
    # Returns a list of recommended stocks, all filtered and researched
    def research_equities(self):
        print('\nResearching the sorted equities\n')

        self.investor.pull_stock_data()

        print('\n\nHere are the most recommended stocks for you to buy (excluding budget constraints):\n')
        print(f'\n\nYour preferences:\n Price of stock: {self.investor.price_preference}\n Method of purchase: {self.investor.position}\n Risk apetite: {self.investor.risk}\n Budget: {self.investor.budget}\n\n')

        if self.investor.position == 'buy':
            self.sorted_stocks = self.investor.return_buy_stocks() 
            print(self.sorted_stocks)

        elif self.investor.position == 'short':
            self.sorted_stocks = self.investor.return_short_stocks()
            print(self.sorted_stocks)


    # Give the user an option to see the completely filtered list of stocks
    def give_user_option(self):
        if self.investor.budget is None: 
            return 'Since you don\'t have a budget, the product had returned a list of stocks without considering its budget'

        else:
            user_choice = input('\nWould you like to see the list of stocks that match your budget constraints?\n ').lower()

            if 'no' in user_choice:
                user_exit_confirmation = input('Are you sure you want to end this program?\n ').lower()

                while user_exit_confirmation != 'no':
                    if 'yes' in user_exit_confirmation:
                        self.end_time = time.time()
                        elapsed_time = self.end_time - self.start_time

                        return f'\n\n{elapsed_time:.3f} seconds\n\n'

                    if 'n' in user_exit_confirmation:
                        user_choice = input('\nWould you like to see the list of stocks that match your budget constraints?\n ').lower()


            budget = int(round(self.investor.budget, 0))
            budget_per_stock = [budget // len(self.sorted_stocks) for x in range(len(self.sorted_stocks))] # Divides the investor's budget by the number of stocks returned by the research_equities() function
            budget_per_stock_num = budget_per_stock[0] # Takes the number for the budget_per_stock, because budget_per_stock is in a list
            shares_buyable = [[stock_info[0], budget_per_stock_num // stock_info[1]] for stock_info in self.sorted_stocks]

            knapsacked_stocks = self.investor.knapsack(budget, budget_per_stock, shares_buyable)

            print(f'\n\nYour preferences:\n Price of stock: {self.investor.price_preference}\n Method of purchase: {self.investor.position}\n Risk apetite: {self.investor.risk}\n Budget: {self.investor.budget}\n\n')
            print(f'\n\nFinal \'basket\' of stocks: {knapsacked_stocks}\n\n')


    def farewell(self):
        rerun_program = input('Would you like to find more stocks to research and buy and sell?\nIf you want to lookup a single stock (without a list), enter \'single\'\n ').lower()
        
        if 'yes' in rerun_program:
            return self.new_preferences()

        elif 'sin' in rerun_program:
            self.single_stock_lookup()

        print('\n\nChicagotrade® aims to provide the highest-quality stock recommendations and research')
        print('\nThe company bids farewell and hopes your investing ends up beating the S&P 500\n')


    
    def new_preferences(self):
        # Pricing
        print(f'\nCurrent price preference: {self.investor.price_preference}')
        pricing_question = input('Will the price of the stock be the same, or different (enter \'same\' or \'different\')?: ').lower()

        if 'diff' in pricing_question:
            new_price = input('New price of stock: $ ')
            while True:
                try:
                    new_price = float(new_price)
                    break
                
                except ValueError:
                    print('Invalid: Enter a valid answer')
                    new_price = input('New price of stock: $')
        else:
            new_price = self.investor.price_preference
        

        # Buy or short
        # Used in the question input below
        print(f'\nCurrent position: {self.investor.position}')

        if self.investor.position == 'buy':
            new_position = 'short'
        else:
            new_position = 'buy'

        position_question = input(f'Will you still {self.investor.position} stocks or will you now {new_position} (enter \'buy\' or \'short\'?: ').lower()

        if position_question == self.investor.position:
            new_position = self.investor.position # Otherwise, it will be the opposite position
            

        # Risk apetite
        print(f'\nCurrent risk apetite: {self.investor.risk}')
        risk_question = input('Will the risk be the same, or different?: ').lower()

        if risk_question == 'different':
            new_risk = input('New risk apetite (1) Low (2) Low-medium (3) Medium-high (4) High (if undecided, put \'none\'): ').title()

            if 'None' in new_risk:
                new_risk = None

            else:
                while user_preferred_risk != 'Low' and user_preferred_risk != 'Low-Medium' and user_preferred_risk != 'Medium-High' and user_preferred_risk != 'High':
                    print('Enter a valid response')
                    user_preferred_risk = input( 'New risk appetite (1) Low (2) Low-medium (3) Medium-high (4) High (if undecided, put \'none\'): ').title()
        
        else:
            new_risk = self.investor.risk

        
        # Budget
        print(f'\nCurrent budget: {self.investor.budget}')

        budget_question = input('Will your budget remain the same (enter \'yes\' or \'no\')?: ').lower()
        print(' Attention: If you still choose to have no budget, enter \'none\'')

        if 'none' in budget_question:
            new_budget = None

        if budget_question == 'no':
            new_budget = input('Enter the amount of your new budget: $ ')

            while True:
                try: 
                    new_budget = float(new_budget)
                    break

                except ValueError:
                    print('Invalid: Enter a valid answer')
                    new_budget = input( 'Budget (if you don\'t have a set budget, put \'none\'): $')
        else:
            new_budget = self.investor.budget
        

        # Terminal; we just have to adjut the preferences
        if new_price != self.investor.price_preference:
            self.investor.price_preference = new_price
            self.investor.sort_stocks_by_price()

        if new_risk != self.investor.risk:
            self.investor.risk = new_risk

        # For feedback purposes, return the list regardless
        if new_position == 'buy':
            self.investor.return_buy_stocks()
        else:
            self.investor.return_short_stocks()
        
        if new_budget != self.investor.budget:
            self.investor.budget = new_budget
            self.give_user_option()


    def single_stock_lookup(self):
        stock_lookup = input('Enter the ticker of the stock you want to lookup (to exit, enter \'exit\'):\n ').upper()

        while stock_lookup != 'EXIT':
            try:
                print(self.investor.lookup_single_stock(stock_lookup))

            except:
                print('This stock doesn\'t exist')

            stock_lookup = input('Enter the ticker of the stock you want to lookup (to exit, enter \'exit\'):\n ').upper()


user_terminal = Terminal()
run_program = user_terminal.terminal()
print(run_program)

    

