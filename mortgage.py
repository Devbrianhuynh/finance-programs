# Mortgage calculator that calculates fixed-rate, APR, and other mortgage types by inputting a homebuyer's down payment; if they are buying cash, else: 'No need for a mortgage! Good luck with your new home!'
# Unfortunately, I couldn't scrape the live interest rate  
# Once finished with the architecture, add a new feature that takes the consumer's budget and checks if they are able to amortize the loan
class Buyer:
    def __init__(self, name, mortgage_duration, down_payment, interest_rate, home_price, prop_taxes, prop_insurance, hoa_fee, balloon_payment_after):
        self.name = name
        self.mortgage_duration = mortgage_duration
        self.down_payment = down_payment
        self.interest = interest_rate
        self.home_price = home_price
        self.prop_taxes = prop_taxes
        self.prop_insurance = prop_insurance
        self.hoa_fee = hoa_fee
        self.balloon_payment_after = balloon_payment_after
        self.mortgage_amount = self.home_price - (self.home_price * self.down_payment)
    
    def __repr__(self):
        description = f'Hello, {self.name}.'
        return description

    def fixed_rate_jumbo_fha_va_usda_mortgage(self):
        monthly_payment = self.mortgage_amount * (self.interest / 12) / (1 - (1 + self.interest / 12)**(self.mortgage_duration * -1))
        return monthly_payment

    def arm_mortgage(self):
        monthly_payment = self.mortgage_amount * (self.interest / 12) / (1 - (1 + self.interest / 12)**(self.mortgage_duration * -1)) # Same as fixed-rate; changes periodically based on market rates
        return monthly_payment

    def interest_only_mortgage(self):
        monthly_payment = self.mortgage_amount *  (self.interest / 12) # Pays only the interest; will pay principle at a specified date
        return monthly_payment

    def balloon_mortgage(self):
        months = 0
        amount_paid_monthly = 0
        principle_left = 0
        balloon_payment = 0
        while months < self.balloon_payment_after:
            monthly_payment = self.mortgage_amount * (self.interest / 12) / (1 - (1 + self.interest / 12)**-self.mortgage_duration)
            amount_paid_monthly += monthly_payment
            principle_left += self.mortgage_amount / 360
            months += 1
        
        balloon_payment = ((self.mortgage_amount - principle_left) * self.interest) + (self.mortgage_amount - principle_left)

        return f'Your monthly payment before the balloon is: {amount_paid_monthly}.', f'Your balloon payment is: {balloon_payment}.'

# Terminal
print('Welcome to the Mortgage Calculux™, served by Corpple Labs®')
print('What is your name?')
name = input()
name = name.title()

print('What mortgage are you planning to get? Fixed-rate, ARM, interest-only, balloon, jumbo, FHA, VA, USDA?')
print('Note: Balloon mortgage calculator has 94% accuracy.')
mortgage = input()
mortgage = mortgage.lower()
if 'balloon' in mortgage:
    print('When are you going to pay the balloon payment (years)?')
    balloon_payment_after = input()
    while True:
        try:
            if 'years' in balloon_payment_after:
                balloon_payment_after = int(balloon_payment_after.split()[0]) * 12
            if type(balloon_payment_after) == str:
                balloon_payment_after = int(balloon_payment_after) * 12
        except ValueError:
            print('Invalid answer! Try again!')
            balloon_payment_after = input()
else:
    balloon_payment_after = False

print('How long is the mortgage term? Ex: 30 years, 15 years, 5 years, 20 months, 13 months')
mortgage_term = input()
mortgage_term = mortgage_term.lower()
if 'years' in mortgage_term:
    mortgage_term = int(mortgage_term.split()[0]) * 12
if type(mortgage_term) == str:
    mortgage_term = int(mortgage_term)

print('How much are you going to down (%)?')
down_payment = input()
while True:
    try:
        if '%' in down_payment:
            down_payment = down_payment.split('%')
            down_payment = float(''.join(down_payment)) / 100
        if type(down_payment) == str:
            down_payment = float(down_payment) / 100
        break
    except ValueError:
        print('Invalid! Please try again.')
        down_payment = input()

print('How much interest are you paying?')
interest = input()
while True:
    try:
        if '%' in interest:
            interest = interest.split('%')
            interest = float(''.join(interest)) / 100
        if type(interest) == str:
            interest = float(interest) / 100
        break
    except ValueError:
        print('Invalid! Please try again.')
        interest = input()

print('Enter the home price (USD).')
purchase_price = input()
print('Enter yearly property taxes (USD).')
taxes = input()
print('Enter yearly homeowners insurance (USD).')
insurance = input()
print('Enter monthly homeowners association (HOA) fee (put $0 if your property does not have any HOA fees).')
hoa = input()
while True:
    try:
        if '$' in purchase_price or '$' in taxes or '$' in insurance or '$' in hoa:
            purchase_price, taxes, insurance, hoa = purchase_price.split('$'), taxes.split('$'), insurance.split('$'), hoa.split('$')
            purchase_price, taxes, insurance, hoa = int(''.join(purchase_price)), int(''.join(taxes)), int(''.join(insurance)), int(''.join(hoa))
        if ',' in purchase_price or ',' in taxes or ',' in insurance or ',' in hoa:
            purchase_price, taxes, insurance, hoa = purchase_price.split(','), taxes.split(','), insurance.split(','), hoa.split(',')
            purchase_price, taxes, insurance, hoa = int(''.join(purchase_price)), int(''.join(taxes)), int(''.join(insurance)), int(''.join(hoa))
        if type(purchase_price) == str or type(taxes) == str or type(insurance) == str or type(hoa) == str:
            purchase_price, taxes = int(purchase_price), int(taxes), int(insurance), int(hoa)
        break
    except ValueError:
        print('Not a valid $ amount.')
        purchase_price = input()
        taxes = input()
        insurance = input()
        hoa = input()

# Call the instance variable of the object, 'Buyer'
buyer_one = Buyer(name, mortgage_term, down_payment, interest, purchase_price, taxes, insurance, hoa, balloon_payment_after)

if 'fixed' in mortgage or 'jumbo' in mortgage or 'federal housing administration' in mortgage or 'fha' in mortgage or 'veterans affairs' in mortgage or 'va' in mortgage or 'united states department of agriculture' in mortgage or 'usda' in mortgage:
    print(buyer_one)
    print(f'Your monthly payment is: ${buyer_one.fixed_rate_jumbo_fha_va_usda_mortgage()}.')

if 'arm' in mortgage or 'adjustable' in mortgage:
    print(f'Your monthly payment is: ${buyer_one.arm_mortgage()} (payment amount may fluctuate based on interest-rate adjustments)')

if 'interest' in mortgage:
    print(f'Your monthly payment is: ${buyer_one.interest_only_mortgage()}')

if 'balloon' in mortgage:
    print({buyer_one.balloon_mortgage()})

if 'jumbo' in mortgage:
    print(f'Your monthly payment is: ${buyer_one.fixed_rate_jumbo_fha_va_usda_mortgage()}')

if 'federal housing administration' in mortgage or 'fha' in mortgage:
    print(buyer_one.fixed_rate_jumbo_fha_va_usda_mortgage())

if 'veterans affairs' in mortgage or 'va'in mortgage:
    print(buyer_one.fixed_rate_jumbo_fha_va_usda_mortgage())