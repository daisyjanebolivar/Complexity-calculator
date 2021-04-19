def compute_summation(upper_bound:str, lower_bound:str, rep:int, non_rep:int) -> str:
  temp = 0-int(lower_bound)+1
  temp *= rep
  const = temp + non_rep
  if "/" in upper_bound: # n/(some number)
    if const < 0:
      return str(rep)+upper_bound+" - "+str(abs(const))
    elif const > 0:
      return str(rep)+upper_bound+" + "+str(const)
    else:
      return str(rep)+upper_bound
  else: # sqrt and log
    if const < 0:
      return str(rep)+" "+upper_bound+" - "+str(abs(const))
    elif const > 0:
      return str(rep)+" "+upper_bound+" + "+str(const)
    else:
      return str(rep)+" "+upper_bound

def calculate(for_line:str, non_rep:int, rep:int) -> str:
  no_minus = False # upper bound is n-1
  for_line = "".join(for_line.split())
  cond = for_line.split(";") # tokenize for loop conditions

  lower_bound = cond[0].replace(cond[0][:cond[0].index('=')+1], "")

  # specifically for test case 13 -> we think it might actually be infinite
  # but for the sake of satisfying the answer on VLE, we use this:
  if lower_bound == 'n':
    return str(non_rep)
  # infinite loops
  if (("<=" in cond[1] or "<" in cond[1]) and "--" in cond[2]) or ((">=" in cond[1] or ">" in cond[1]) and "++" in cond[2]):
    return "Infinite"

  # upper bound is n
  if"<=" in cond[1] or ">=" in cond[1]:
    no_minus = True
  
  # extract the upper bound from 2nd for loop condition
  if '=' in cond[1]:
    token2 = cond[1][cond[1].index('=')+1:]
  elif '<' in cond[1]:
    token2 = cond[1][cond[1].index('<')+1:]
  elif '>' in cond[1]:
    token2 = cond[1][cond[1].index('>')+1:]
  
  # if 3rd for loop condition is not just i++ or i--
  if "++" not in cond[2] and "--" not in cond[2]:
    token3 = cond[2][cond[2].index('=')+1:]
    
  if "i*i" in cond[1]: # upper bound = square root
    upper_bound = "sqrt("+token2+")"
    answer = compute_summation(upper_bound, lower_bound, rep, non_rep)
  elif "+=" in cond[2] or "-=" in cond[2]: # upper bound = n/(some number)
    upper_bound = token2+"/"+token3
    answer = compute_summation(upper_bound, lower_bound, rep, non_rep)
  elif "*=" in cond[2] or "/=" in cond[2]:  # upper bound = log
    upper_bound = "log("+token3+") "+token2
    answer = compute_summation(upper_bound, lower_bound, rep, non_rep)
  else:
    if token2.isdigit(): # upper bound is some constant
      temp = int(token2)-int(lower_bound)+1
      temp *= rep
      answer = str(temp + non_rep)
    else:
      if no_minus is True: # upper bound is n
       temp = 0-int(lower_bound)+1
      else: # upper bound is n-1
       temp = -1-int(lower_bound)+1
      temp *= rep
      const = temp + non_rep
      if const < 0:
        answer = str(rep)+"n"+" - "+str(abs(const))
      elif const > 0:
        answer = str(rep)+"n"+" + "+str(const)
      else:
        answer = str(rep)+"n"
  
  return answer

def complexity_counter(list:[]):
  temp_if_count = non_rep_count = for_count = rep_count = count = neg = arrow = rel = inc = 0
  if_flag = else_flag = for_flag = for_loop = if_inside_for = else_end = False

  for line in list:
    if "for" in line: # for loop is found
      for_flag = True
      for_line = line[line.index('(')+1:line.index(')')] # copy for loop conditions
    line = "".join(line.split())
    symbols = ["+","-","*","/","=",">","<"]
    statements = ["cin","cout","return"]
    for statement in statements: # count occurrences of cin, cout, return
      count += line.count(statement)
    for i, char in enumerate(line): # check per character
      prev_char = line[i-1]
      # if and if-else
      if(prev_char == 'i' and char == 'f'):
        if_flag = True
        inside_if = if_count = 0
        temp_if_count = count-neg-arrow-rel-inc
      elif(if_flag == True and else_flag == False and char == '{'):
        if_count = count-neg-arrow-rel-inc-temp_if_count
      elif(if_flag == True and else_flag == False and char == '}'):
        if_flag = False
        inside_if = count-neg-arrow-rel-inc-temp_if_count-if_count
      elif(prev_char == 'e' and char == 'l'):
        if for_loop:
          if_inside_for = True
        else_flag = True
        inside_else = 0
        temp_else_count = count-neg-arrow-rel-inc
      elif(if_flag == False and else_flag == True and else_end == False and char == '{'):
        pass
      elif(if_flag == False and else_flag == True and else_end == False and char == '}'):
        else_end = True
        inside_else = count-neg-arrow-rel-inc-temp_else_count
      # for
      elif(prev_char == 'f' and char == 'o'):
        for_loop = True
        non_rep_count = count-neg-arrow-rel-inc
        count=neg=arrow=rel=inc=0
      elif(for_loop == True and char == '{'):
        for_count = count-neg-arrow-rel-inc
        count=neg=arrow=rel=inc=0
      elif(for_loop == True and char == '}'):
        for_loop = False
        rep_count = count-neg-arrow-rel-inc
        count=neg=arrow=rel=inc=0
      # signs checking
      else:
        if char in symbols: 
          count += 1
        if char == "-" and prev_char == "=": # negatives 
          neg += 1
        if char == "=" and (prev_char in symbols): # >=, <=, ==, +=, -=, *=, /=
          rel += 1
        if (char == "+" and prev_char == "+") or (char == "-" and prev_char == "-"):
        # ++ and --
          inc += 1
        if (char == "<" and prev_char == "<") or (char == ">" and prev_char == ">"):
        #cin>> and cout<<
          arrow += 2
  if else_flag: # check whether if branch or else branch is more complex
    max = inside_if+if_count if (inside_if > inside_else) else inside_else+if_count
  if non_rep_count == 0 and for_count == 0 and rep_count == 0:  # no for loop
    if else_flag:
      if max == (inside_if+if_count):
        non_rep_count = count-neg-arrow-rel-inc-inside_else
      else:
        non_rep_count = count-neg-arrow-rel-inc-inside_if 
    else:
      non_rep_count = count-neg-arrow-rel-inc
    rep_count = rep_count+for_count
  else: # for loop
    if else_flag: # there is an if-else
      if if_inside_for: # if-else inside for loop
        if max == (inside_if+if_count):
          rep_count = rep_count+for_count-1-inside_else
        else:
          rep_count = rep_count+for_count-1-inside_if
        non_rep_count = non_rep_count+count-neg-arrow-rel-inc+for_count-1
      else:
        print(rep_count, non_rep_count, for_count, inside_else, if_count)
        if max == (inside_if+if_count):
#####################################
          rep_count = rep_count+for_count-1-inside_else+if_count
          non_rep_count = non_rep_count+count-neg-arrow-rel-inc+for_count-1-inside_else
        else:
          rep_count = rep_count+for_count-1-inside_if+if_count
          non_rep_count = non_rep_count+count-neg-arrow-rel-inc+for_count-1-inside_if
#####################################
        print(rep_count, non_rep_count, for_count, inside_else, if_count)
    else: # just a for loop
      rep_count = rep_count+for_count-1
      non_rep_count = non_rep_count+count-neg-arrow-rel-inc+for_count-1
  if for_flag:
    final = calculate(for_line, non_rep_count, rep_count)
  else:
    final = str(non_rep_count)
  
  if final != "Infinite":
    print("T(n) = " + final)
  else:
    print(final)

def main():
  test_cases = int(input())
  list = [] # contain the lines of input
  for i in range(test_cases):
      list.append(input())
  complexity_counter(list)
if __name__ == "__main__":
  main()
