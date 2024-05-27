def first(G, current_nonterminal, calculed=None, visited=None):  #  with default values of None for calculed and visited.
    """

    parameters :
        G = {'S': ['AS', 'A'], 'A': ['a']} 
        G (dict): the grammar represented as a dictionary where keys are the nonterminals and values are lists of the productions for each nt
        current_nonterminal(str): current nonterminal that we are calculating its first 
        calculed (dict): dictionary to save first sets of each nonterminal to know which have already been calculated
        visited(set): set for nonterminals that have been visited during the calculation to prevent infinite recursion

    Returns the set of the first of the NT.
    """
    
    if calculed is None:  # creating the calculed dict when is empty and the visited set when first() is called
        calculed = {}  
        
    if visited is None: 
        visited = set()  

    # before calculating first a nt it is checked if it is already calculated, if it is then return it
    if current_nonterminal in calculed:  
        return calculed[current_nonterminal]  

    non_terminals = list(G.keys())  # ['S', 'A']
    first_results = set()  # a set to save the first set of the current NT and not repeat values
    visited.add(current_nonterminal)  # -> {S}

    for production in G[current_nonterminal]:  # 'S': ['AS', 'A'] <- each element of the list is a prod
        if production == 'e':  
            first_results.add('e') # -> {e}
        elif production[0].islower(): 
            first_results.add(production[0])  # -> ex: aS -> {a}
        elif production[0].isupper():  # -> ex: AS -> A
            for symbol in production:  # ex case: S -> ABC if A derives in epsilon it is needed to check the first of next symbol
                if symbol.islower():  
                    first_results.add(symbol)  
                    break  # exit the loop bc terminals dont produce epsilon
                
                elif symbol.isupper():  # -> ex A
                    if symbol not in visited:  # this is to control infinite recursion, 1st execution A is not visited
                        first_set = first(G, symbol, calculed, visited)  # first of the symbol with recursion
                        first_results.update(first_set)  # adding the first set of the symbol to the first set of the current NT.
                        if 'e' not in first_set:  
                            break  # if we dont find epsilon we can stop going into each nt
                        
                    else:  # symbol in visited
                        if symbol in calculed: 
                            first_results.update(calculed[symbol])  # already calculed, update is to add the already calculed set and stop
                        break 
        else:  # we complted the loop w/o a break -> all symbols produce epsilon so we add epsilon
            first_results.add('e') 
    
    visited.remove(current_nonterminal)  # after calculating first(S) -> del S of {}
    calculed[current_nonterminal] = first_results  # calculated first set of the current nt to not calculate again if we already have.
    return first_results # {}

def get_first_results(G):  
    first_results = {} 

    for nonterminal in G:  
        first_results[nonterminal] = first(G, nonterminal)  

    return first_results  # dict

def follow(G):  
    
    """
    Parameters:
        G = {'S': ['AS', 'A'], 'A': ['a']}
        G (dict): the grammar represented as a dictionary where keys are the nonterminals and values are lists of the productions for each nonterminal
        
    Returns:
        follow (dict): -> dictionary where the keys are the nonterminals and the values are sets that contain the follow sets for each nonterminal
    """
    
    non_terminals = list(G.keys()) 
    
    follow = {}
    
    for non_terminal in non_terminals:
        follow[non_terminal] = set() # -> {S: {}}
    
    start_symbol = non_terminals[0] 
    follow[start_symbol].add('$')  

    first_results = get_first_results(G)  
    
    while True: 
        
        updated_flag = False  # flag -> if any follow set is updated in the iteration -> true
        
        for non_terminal in non_terminals: # ['S', 'A']
            for production in G[non_terminal]:  # 'S': ['AS', 'A'] <- each element of the list is a prod
                follow_set_temp = follow[non_terminal].copy()  #  copy of the follow set of the current NT to not modify original
                # print("follow set temp")
                # print(follow_set_temp)
                # print("-------------")
                for symbol in reversed(production):  # 'AS' -> 'SA' or 'Sa' -> 'aS'
                    # print("*")
                    # print(symbol)
                    # print("*")
                    if symbol in non_terminals: 
                         # if there are elements in follow_set_temp that are not in follow[symbol] its needed to update follow[symbol] with those additional elements.
                        if not follow_set_temp.issubset(follow[symbol]): 
                            follow[symbol].update(follow_set_temp) 
                            updated_flag = True  
                        if 'e' in first_results[symbol]: 
                            follow_set_temp.update(first_results[symbol] - {'e'})
                        else:  # doesnt derive in epsilon 
                            follow_set_temp = first_results[symbol] 
                    else:  # if the symbol is a terminal:
                        follow_set_temp = {symbol}  # -> {a}
        
        if not updated_flag:  # -> false -> if no follow set was updated in this iteration break
            break  
    
    for key, value in follow.items():  
        follow[key] = value - {'e'}     

    return follow  # dict

def get_follow_results(G):
    follow_results = {}  
    follow_sets = follow(G)  
    
    for non_terminal, follow_set in follow_sets.items():  
        follow_results[non_terminal] = follow_set  
        
    return follow_results  # dict

def print_output(final_output):
    for result in final_output:
        for type_, unique_result in result.items():
            if type_ == "First":
                for non_terminal, first_set in unique_result.items():  
                    print(f"First({non_terminal}) = {first_set}") 
            else:
                for non_terminal, follow_set in unique_result.items():  
                    print(f"Follow({non_terminal}) = {follow_set}") 
    

def main():
    final_output = []
    c = int(input())  # receive how many grammars we're going to process
    for _ in range(c):  # for each grammar, ask
        n = int(input())  # read the line containing the number of production rules, e.g., 5
        G = {}  # initialize the dictionary that will store the grammar
        j = 0  # initialize the integer variable that will store the production rules
        while j < n:  # n[0] >> number of G / for each production rule
            l = input()  # what's to the right of the variables - read the production rule
            l = l.split()  # split the production rule into a list of symbols | ex., A BA a | ['A', 'BA', 'a']
            G[l[0]] = []  # add an entry for the non terminal in the dictionary G | ex., G[A] = []
            for i in range(1, len(l)):  # for each terminal symbol in the production rule | ex., iterates over BA and a
                G[l[0]].append(l[i])  # add the terminal symbol to the corresponding list in G | first adds BA | G[A] = ['BA'] | then adds a | G[A] = ['BA', 'a']
            j += 1
        i = 0
        final_output.append({"First": get_first_results(G)})
        final_output.append({"Follow": get_follow_results(G)})
    print_output(final_output) # this prints the final output after inserting input
    # print(G)
# example grammar
# G = {'S': ['AS', 'A'], 'A': ['a']} 
main()

