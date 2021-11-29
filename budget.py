class Category:
    
    def __init__(self, name):
        self.name = name
        self.ledger = list()
    
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        balance = 0
        for x in self.ledger:
            items += f"{x['description'][0:23]:23}" + f"{x['amount']:>7.2f}" + "\n"
            balance += x["amount"]
        output = title + items + "Total: " + str(balance)
        return output
    
    """
    accepts an amount and description.
    If no description is given, it should default to an empty string."""
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    """
    is similar to the `deposit` method, but the amount passed in should be stored in the ledger as a negative number. 
    If there are not enough funds, nothing should be added to the ledger. 
    This method should return `True` if the withdrawal took place, and `False` otherwise.
    """
    def withdraw(self, amount, description = ""):
        if (self.check_funds(amount)):
            self.ledger.append({"amount": amount, "description": description})
            return True
        return False

    """
    returns the current balance of the budget category based on the deposits and withdrawals that have occurred
    """
    def get_balance(self):
        balance = 0
        for x in self.ledger:
            balance += x["amount"]
        return balance
    
    """
    accepts an amount and another budget category as arguments. 
    The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". 
    The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". 
    If there are not enough funds, nothing should be added to either ledgers. 
    This method should return `True` if the transfer took place, and `False` otherwise.
    """
    def transfer(self, amount, otherBudget):
        if (self.check_funds(amount)): 
            otherBudget.deposit(amount, "Transfer from " + self.name)
            self.withdraw(amount, "Transfer to " + otherBudget.name)
            return True
        return False

    """
    accepts an amount as an argument. 
    It returns `False` if the amount is greater than the balance of the budget category and returns `True` otherwise. 
    This method should be used by both the `withdraw` method and `transfer` method.
    """
    def check_funds(self, amount):
        if (self.get_balance() >= amount):
            return True
        return False
    
    def get_withdrawls(self):
        balance = 0
        for x in self.ledger:
            if x['amount'] < 0:
                balance += x['amount']
        return balance

def truncate(n):
    multiplier = 10
    return int(x * multiplier)/multiplier

def getTotals(categories):
    total = 0
    breakdown = []
    for x in categories:
        total += x.get_withdrawls()
        breakdown.append(x.get_withdrawls())
    rounded = list(map(lambda x: truncate(x/total), breakdown))
    return rounded

def create_spend_chart(categories):
    res = "Percentage spent in category \n"
    i = 100
    totals = getTotals(categories)
    while i >= 0:
        spaces = " "
        for x in totals:
            if x * 100 >= i:
                spaces += "o  "
            else:
                spaces += "   "
        res += str(i).rjust(3) + "|" + spaces + ("\n")
        i-=10
        
    dashes = "-" + "---"*len(categories)
    names = []
    x_axis = ""
    for cate in categories:
        names.append(cate.name)
    
    maxi = max(names, key=len)
    
    for x in range(len(maxi)):
        nameStr = ""
        for name in names:
            if x >= len(name):
                nameStr += "   "
            else:
                nameStr += name[x] + ""
        if (x != len(maxi)-1):
            nameStr += "\n"
        x_axis += nameStr
    res+= dashes.rjust(len(dashes)+4) + "\n" + x_axis
    return res