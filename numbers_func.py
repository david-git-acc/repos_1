
def into_numbers(string):
    allowed = set([0,1,2,3,4,5,6,7,8,9])
    
    nums = []
    
    the_list = list(string)
    
    this_num = ""
    
    for char in the_list:
        if char in allowed:
            this_num += char
        else:
            nums.append(int(this_num))
            this_num = ""