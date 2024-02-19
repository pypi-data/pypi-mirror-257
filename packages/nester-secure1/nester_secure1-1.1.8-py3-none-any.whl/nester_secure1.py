"""
This is the module code for the printing lists in lists function
They are then uploaded to Python Package Index
A good syntax is to comment even in your functions

"""

"""
This is the nester.py module and it provides one function called print_list_of_list which
prints lists that may or may not include nested lists

"""
def print_list_of_lists(item_list):
    """
    This function takes a positional argument called item_list which is any python list which may contain nested lists
    Each data item in the provided list is recursively printed on the screen on its own line
    
    """
    for item in item_list:
        if isinstance(item,list):
            print_list_of_lists(item) # recursion
        else:
            print(item)
def say_hello():
    print ("Hello this is my new function")