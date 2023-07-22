
credit_limit = float(0)
billing_cycle = int(1)
outstanding_balance = float(0)
credits = float(0)
purchases = float(0)
finance_charges = float(0)
late_payment_charge = float(0)
total_amount_due = float(0)
minimum_amount_due = float(0)
previous_min_amount_due = float(0)
reward_points = {
    "previous_points_balance": int(0),
    "current_points_earned": int(0),
    "points_used": int(0),
    "total_credit_points": int(0)
}
overlimit_fee = float(500)
annual_fee = float(0)
willContinue = True
    
def check_if_positive_digit(num):
    if num <= 0:
        return False
    return True

def float_input(message):
    floatLoop = True
    while floatLoop:
        try:
            userInput = float(input(message))
            if check_if_positive_digit(userInput):
                print("if input {}".format(floatLoop))
                floatLoop = False
                return userInput
        except ValueError:
            print("Enter only positive value {}".format(floatLoop))
        else:
            floatLoop = False
            return userInput
        
def action_input(message, maxLength):
    actionLoop = True
    while actionLoop:
        try:
            userInput = int(input(message))
            if check_if_positive_digit(userInput) and userInput <= maxLength:
                actionLoop = False
                return userInput
        except ValueError:
            print("Enter only positive integer value")
        else:
            actionLoop = False
            return userInput

def display_input_credit():
    global credit_limit
    credit_limit = float_input("Enter credit limit: ")

def compute_earned_points(current_purchase):
    return int(current_purchase / 30)

def display_add_purchase():
    current_purchase = float_input("How much do you want to purchase?: ")
    global purchases
    global reward_points
    purchases = purchases + current_purchase
    reward_points["current_points_earned"] = reward_points["current_points_earned"] + compute_earned_points(current_purchase)

def display_previous_statetment():
    global outstanding_balance
    global previous_min_amount_due
    print("Your previous balance is {}".format(outstanding_balance))
    print("Your previous minimum amount due is {}".format(previous_min_amount_due))

def display_make_payment():
    global credits
    credits = float_input("How much do you want to pay?: ")
    print("Thank you for you payment! Redirecting you to the main menu")

def display_view_rewards_points():
    global reward_points
    print("Your total rewards points is {}".format(reward_points["total_credit_points"]))

def redeem(input):
    global reward_points
    print(rewards[input]["success_message"])
    reward_points["points_used"] = reward_points["points_used"] + 1000

def safeReturn(_x):
    return

rewards = [
    { 
        "name": "Php 100 eGift voucher for 1000 points", 
        "success_message": "Your eGift voucher has been sent to your registered mobile number",
        "function": redeem
    },
    { 
        "name": "Php 100 credits for 1000 points", 
        "success_message": "Php 100 has been credited to your account",
        "function": redeem
    },
    { 
        "name": "Cancel", 
        "success_message": "Php 100 has been credited to your account",
        "function": safeReturn
    },
]

def display_use_rewards_points():
    global reward_points
    if reward_points["total_credit_points"] - reward_points["points_used"] >= 1000:
        for idx, x in enumerate(rewards):
            print("{}. {}".format(idx + 1, x["name"]))
        user_action = action_input("Which would you like to redeem?: ", len(rewards) + 1)
        rewards[user_action - 1]["function"](user_action)
    else:
        print("You currently don't have enough points to redeem anything. Your current points are: {}".format(reward_points["total_credit_points"]))


def compute_finance_charges():
    global overlimit_fee
    global outstanding_balance
    global finance_charges
    current_finance_charge = 0
    if purchases > credit_limit:
        current_finance_charge = 500
    if outstanding_balance > 0:
        current_finance_charge = current_finance_charge + (outstanding_balance * 0.03) 
    finance_charges = current_finance_charge

def compute_late_charge_fee():
    current_late_charge = 0
    global late_payment_charge

    if previous_min_amount_due - credits > 0:
        if  previous_min_amount_due - credits > 850:
            current_late_charge = 850
        else:
            current_late_charge = previous_min_amount_due - credits
    late_payment_charge = current_late_charge

def compute_total_amount_due():
    global total_amount_due
    total_amount_due = outstanding_balance + purchases + finance_charges + late_payment_charge - credits

def compute_minimum_amount_due():
    global minimum_amount_due
    current_min_due = 0
    if total_amount_due <= 850:
        minimum_amount_due = total_amount_due
        print(" 1 min_amount_due here {}".format(minimum_amount_due))
        return
    current_min_due = total_amount_due * 0.0357
    if current_min_due <= 850:
        minimum_amount_due = 850
    else:
        minimum_amount_due = current_min_due
    print("min_amount_due here {}".format(minimum_amount_due))

def compute_prev_balance():
    global outstanding_balance
    outstanding_balance = total_amount_due

def compute_prev_points_balance():
    global reward_points
    reward_points["previous_points_balance"] = reward_points["total_credit_points"]

def compute_total_points():
    global reward_points
    reward_points["total_credit_points"] = reward_points["total_credit_points"] + reward_points["current_points_earned"] - reward_points["points_used"]


def reset_values():
    global reward_points
    global purchases
    global credits
    global billing_cycle
    global annual_fee
    reward_points["current_points_earned"] = 0
    reward_points["points_used"] = 0
    purchases = 0
    credits = 0 
    if billing_cycle % 12 == 0:
        annual_fee = 4000
    else:
        annual_fee = 0
    billing_cycle = billing_cycle + 1

def compute_purchases_with_annual_fee():
    global purchases
    purchases = purchases + annual_fee

def display_end_billing_cycle():
    compute_prev_balance()
    print("Previous Balance: {}".format(outstanding_balance))
    print("(-) Payments / Credits: {}".format(credits))
    compute_purchases_with_annual_fee()
    print("(+) Purchases: {}".format(purchases))
    compute_finance_charges()
    print("Finance Charges: {}".format(finance_charges))
    compute_late_charge_fee()
    print("Late Payment Charges: {}".format(late_payment_charge))
    compute_total_amount_due()
    print("Total Amount Due: {}".format(total_amount_due))
    compute_minimum_amount_due()
    print("Minimum Amount Due: {}".format(minimum_amount_due))
    compute_prev_points_balance()
    print("Previous Cards Points Balance: {}".format(reward_points["previous_points_balance"]))
    print("(+) Current Points Earned: {}".format(reward_points["current_points_earned"]))
    print("(-) Current Points Used: {}".format(reward_points["points_used"]))
    compute_total_points()
    print("Total Credit Points: {}".format(reward_points["total_credit_points"]))
    reset_values()

def safeExit():
    global willContinue
    willContinue = False

actions = [
    { "name": "Add purchase", "function": display_add_purchase },
    { "name": "View previous statement", "function": display_previous_statetment },
    { "name": "Make payment", "function": display_make_payment },
    { "name": "View rewards points", "function": display_view_rewards_points },
    { "name": "Use rewards points", "function": display_use_rewards_points },
    { "name": "End billing cycle", "function": display_end_billing_cycle },
    { "name": "Exit", "function": safeExit },
]

def display_current_state():
    print("\n")
    print("Billing Cycle {}".format(billing_cycle))
    print("Credit Limit {}".format(credit_limit))
    print("Total Amount Due {}".format(total_amount_due))
    print("Minimum Amount Due {}".format(minimum_amount_due))
    print("Outstanding Balance {}".format(outstanding_balance))
    print("Current Purchases {}".format(purchases))
    print("Current Credits {}".format(credits))

def display_user_action():
    print("What is the transaction?")
    for idx, x in enumerate(actions):
        print("{}. {}".format(idx + 1, x["name"]))
    user_action = action_input("\nEnter the number of your transaction: ", len(actions) + 1)
    actions[user_action - 1]["function"]()

def main_menu():
    global willContinue
    while willContinue:
        display_current_state()
        display_user_action()

def display_start_message():
    print("Welcome to ETC Credit Card Bank!")
    print("This is a bill generation application. \n")

def main():
    display_start_message()
    display_input_credit()
    main_menu()

main()
