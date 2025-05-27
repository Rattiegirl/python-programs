def print_list(tasks):
  for i, task in enumerate(tasks):
    print(i+1, task, sep=". ")

def add_task(tasks):
  while (True):
    print("\n")
    print("Say your task, or type 'exit'!")
    stuff = input()
    if (stuff == "exit"):
      break
    # cycle_times += 1
    print("Your task of", stuff, "has been added to the list")
    # print(str(cycle_times) + ". " + stuff)
    tasks.append(stuff)
    print_list(tasks)

def remove_task(tasks):
  print("\n")
  print_list(tasks)
  print("Which one of your tasks have you completed?")
  done_task = int(input())
  if done_task < len(tasks) and done_task >= 0:
    tasks.pop(done_task - 1)
    print_list(tasks)
  else:
    print("no")

print("Write stuff you need to achieve here")
# cycle_times = 0
tasks = []
while (True):
  print("\n")
  print("Would you like to add a task (1), remove a task (2), recieve a gift (3) or exit the program (4)?")
  action = int(input())
  if (action == 1):
    add_task(tasks)
  elif (action == 2):
    remove_task(tasks)
  elif (action == 3):
    print("Here you go!🍬")
  elif (action == 4):
    print("Goodbye 😤")
    break
  else:
    print("what in the world is that")