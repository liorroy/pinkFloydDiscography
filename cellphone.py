def cellphone_keypad(input_string):

    nums_and_letters = {
        2: ['a', 'b', 'c'],
        3: ['d', 'e', 'f'],
        4: ['g', 'h', 'i'],
        5: ['j', 'k', 'l'],
        6: ['m', 'n', 'o'],
        7: ['p', 'q', 'r', 's'],
        8: ['t', 'u', 'v'],
        9: ['w', 'x', 'y', 'z']
    }

    output_list = ['']  # element in first iteration (for the first char (digit) in the input string) -> blank ' '

    for char in input_string:
        current_char_list = []
        char = int(char)
        for element in output_list:
            for letter in nums_and_letters.get(char):
                current_char_list.append(element + letter)
        output_list = current_char_list

    return output_list

def main():
    print("Enter q / Q to quit\n")
    while True:
        input_string = input("Enter digits (only from 2-9): ")

        if input_string in ['q', 'Q']:  # or input_string.lower() == 'q'
            break
        if not input_string.isdigit():
            print("\tYou can only enter digits")
            continue
        if not (all(char in '23456789' for char in input_string)):
            print("\tYou can only enter digits from 2 to 9")
            continue

        print(cellphone_keypad(input_string))

if __name__ == '__main__':
    main()
