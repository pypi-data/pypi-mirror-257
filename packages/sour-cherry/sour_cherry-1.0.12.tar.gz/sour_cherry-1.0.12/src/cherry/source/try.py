import os


folder_path = os.path.dirname(os.path.abspath(__file__))
util_path = os.path.dirname(__file__)

print(folder_path)
print(util_path)
print(os.path.abspath(__file__))