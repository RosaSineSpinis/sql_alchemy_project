def luhn_check(num_card_to_check):
    num_card_to_check = str(num_card_to_check)
    parse = num_card_to_check[0:(len(num_card_to_check)-1)]
    parse = luhn_algotirhm(parse)
    if parse[-1] == num_card_to_check[-1]:
        return True
    else:
        return False

def luhn_algotirhm(num):
    '''num comes in string'''
    tab_int = []
    for idx, digit in enumerate(num):
        if idx % 2 == 0:
            digit = int(digit) * 2
            if digit > 9:
                digit -= 9
        tab_int.append(int(digit))
    luhn_num = 0 if sum(tab_int) % 10 > 9 else 10 - sum(tab_int) % 10
    num += str(luhn_num)
    card_num = ""
    for digit in num:
        card_num += str(digit)
    return card_num


print("luhn_check", luhn_check(4000004729721691))