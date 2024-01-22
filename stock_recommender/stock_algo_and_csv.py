from random import randrange
import csv

def ticker_list(): 
    ticker_list = []

    with open(r'trading\stock_recommender\nasdaq_screener_1704944193582.csv') as tickers:
        ticker_file = csv.DictReader(tickers)

      # Commented code is used for testing purposes only (we can iterate though a couple dozen stocks instead of going through the entire CSV file  
      # count = 0
        for ticker in ticker_file:
            # if count > 100:
                # break
            ticker_list.append(ticker['Symbol'])
          # count += 1
    
    return ticker_list



# Note: This quicksort algorithm is MODIFIED to sort the best-quality stocks with their associated tickers
def quicksort(list, start, end):
    if start >= end:
        return
    
    pivot_index = randrange(start, end + 1)
    pivot_element = list[pivot_index][-1]

    list[end][-1], list[pivot_index][-1] = list[pivot_index][-1], list[end][-1]

    less_than_pointer = start

    for index in range(start, end):
        if list[index][-1] > pivot_element:
            list[index], list[less_than_pointer] = list[less_than_pointer], list[index]

            less_than_pointer += 1
        
    list[end], list[less_than_pointer] = list[less_than_pointer], list[end]

    quicksort(list, start, less_than_pointer - 1) # Left sublist
    quicksort(list, less_than_pointer + 1, end) # Right sublist


# Hash map
class HashMap:
    def __init__(self, array_len = len(ticker_list())):
        self.array_len = array_len
        self.array = [[None, None] for x in range(self.array_len)] # Modify the initial values to be [None, None] instead of None becase [0] represents the ticker symbol and [1] is the price and other information
        

    def hash(self, key, collison_count = 0):
        hash_code = sum(key.encode())
        return hash_code + collison_count # Returns the hash_code
    

    def compress(self, hash_code):
        return hash_code % self.array_len # Returns the index for where the key should be in the self.array
    

    def assign_hash(self, key, value, collisons = 0):
        array_index = self.compress(self.hash(key, collisons))
        current_array_value = self.array[array_index]
        
        if current_array_value[0] == key or current_array_value[0] == None:
            self.array[array_index] = [key, value]
            return
            
        if current_array_value[0] != key and current_array_value is not None:
            return self.assign_hash(key, value, collisons + 1) # Uses recursion if there is a collison


    # Give the user an option to pull stock data from their inputted ticker (instead of returning a list/csv)
    # For ex. if the user wants to see META only, then they can use this method retrieve_hash
    def retrieve_hash(self, key, collisons = 0):
        array_index = self.compress(self.hash(key, collisons))
        current_array_value = self.array[array_index]

        if current_array_value[0] == key:
            print(f'Finding the value of {key} and {current_array_value[1]}')
            return current_array_value[1]
            
        if current_array_value[0] is None:
            print(f'There is no {key} in this database')
            return None
           
        if current_array_value[0] != key and current_array_value is not None:
            return self.retrieve_hash(key, collisons + 1) # Use recursion if there is a collison
        
        return 'This item does not exist'
                

    
        


        
    






