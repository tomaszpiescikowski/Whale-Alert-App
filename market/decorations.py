

def better_numbers_template(number):
    split = str(round(number, 2)).split('.')
    number, temp = split[0], split[1]
    number_length = len(number)
    count = 0
    if number_length > 3:
        number_out = ''
        for i in range(number_length - 1, -1, -1):
            if count % 3 == 0 and count != 0:
                number_out = ' ' + number_out
            number_out = number[i] + number_out
            count += 1
        if len(temp) == 1:
            return number_out + ', ' + temp + '0'
        return number_out + ', ' + temp

    else:
        if len(temp) == 1:
            return number + ', ' + temp + '0'
        return number + ', ' + temp