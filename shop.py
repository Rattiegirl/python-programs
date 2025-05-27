goods = []
class Good:
  def __init__(self, name, amount, cost):
    self.name = name
    self.amount = amount
    self.cost = cost
def add_good():
  print("What are you adding?")
  name = input()
  print("How much of it are you adding?")
  amount = int(input())
  print("How much does one cost?")
  cost = int(input())
  goods.append(Good(name, amount, cost))

def see_goods():
  for i, good in enumerate(goods):
    print(good.name, good.amount, good.cost, sep=" ")
  
def remove_good():
  print("What are you removing?")
  name = input()
  found_index = -1
  for i, good in enumerate(goods):
    if good.name == name:
      found_index = i
      break
  if found_index == -1:
    print("We did not find your", name)

  else:
    goods.pop(found_index)
    print(name, "was removed")
    see_goods()

def buy_good():
  print("What would you like to buy?")
  name = input()
  found_index = -1
  found_good = None
  for i, good in enumerate(goods):
    if good.name == name:
      found_index = i
      found_good = good
      break
  if found_index == -1:
    print("You can't buy your", name)

  else:
    print("Each one costs", good.cost, ", how many would you like to buy? We have", good.amount, "in stock.")
    amount = int(input())
    if found_good.amount < amount:
      print("We don't have that many")
    
    else:
      found_good.amount -= amount
      price = found_good.cost * amount
      print("Thank you for shopping with us, you spent", price, "$")
   

print("Hello! Welcome to the stock shelves")

while True:
  print("What would you like to do with the goods? [Add] some, [Remove] some or [See] them all? Or would you like to [Leave]? Perhaphs you want to [buy] something?")
  action = input().lower()

  if action == "add":
    add_good()

  elif action == "remove":
    remove_good()

  elif action == "see":
    see_goods()

  elif action == "buy":
    buy_good()

  elif action == "leave":
    print("Goodbye")

    break

  else:
    print("What?")

