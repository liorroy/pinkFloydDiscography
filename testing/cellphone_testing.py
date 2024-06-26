def phone(input_string):
    """  Example = user_string = '23'

        outer loop (for char in list_of_chars_from_input:) will run twice:

        first time: char == '2' (we change to int because of how the numbers (keys) are saved in the dict

            element == '' # first iteration - it's blank ' ' (output_list = [''] )
            in the dictionary:         2: ['a', 'b', 'c']

            for element in output_list: (element = ''):
            for letter in list(nums_and_letters.get(char)): # nums_and_letters list == ['a', 'b', 'c'] = list(nums_and_letters.get(2)
                first iteration # letter is 'a' -> current_char_list = ['a'] # ('' + 'a' from nums_and_letters) # current_char_list.append(element + letter)
                second iteration # letter is 'b' -> current_char_list = ['a', 'b']
                third iteration # letter is 'c' -> current_char_list = ['a', 'b', 'c']

            So that when we finish the first outer loop iteration,
            output_list = current_char_list = ['a', 'b', 'c']

        second time: char == '3'

            in the dictionary:         3: ['d', 'e', 'f']
            for element in output_list: (element = 'a'):
            for letter in list(nums_and_letters.get(char)):
                first iteration # letter is 'd' -> current_char_list = ['ad'] * ['ad'] ('a' + 'd' from nums_and_letters) #current_char_list.append(element + letter)
                second iteration # letter is 'e' -> current_char_list = ['ad', 'ae']
                third iteration # letter is 'f' -> current_char_list =  ['ad', 'ae', 'af']

            we finished with the element 'a',
            another iteration of for element in output_list: for element = 'b' (output_list = ['a', 'b', 'c'])
            for letter in list(nums_and_letters.get(char)):
                first iteration # letter is 'd' -> current_char_list = ['ad', 'ae', 'af', 'bd']
                second iteration # letter is 'e' -> current_char_list = ['ad', 'ae', 'af', 'bd', 'be']
                third iteration # letter is 'f' -> current_char_list = ['ad', 'ae', 'af',  'bd', 'be', 'bf']

             we finished with the element 'b',
            another iteration of for element in output_list: for element = 'c' (output_list = ['a', 'b', 'c'])
            for letter in list(nums_and_letters.get(char)):
                first iteration # letter is 'd' -> current_char_list = ['ad', 'ae', 'af',  'bd', 'be', 'bf', 'cd']
                second iteration # letter is 'e' -> current_char_list = ['ad', 'ae', 'af',  'bd', 'be', 'bf', 'cd', 'ce']
                third iteration # letter is 'f' -> current_char_list = ['ad', 'ae', 'af',  'bd', 'be', 'bf', 'cd', 'ce', 'cf']

            and now we update output_list for the second (and last) time:

            output_list = current_char_list = ['ad', 'ae', 'af',  'bd', 'be', 'bf', 'cd', 'ce', 'cf']

        and we return output_list to be printed
        """
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

    list_of_chars_from_input = list(input_string)
    print(list_of_chars_from_input)

    output_list = ['']  # We initialize the result list with an empty string

    for char in list_of_chars_from_input:  # iterate through each digit in the input string
        print("\t\tNEW OUTER FOR LOOP:")
        # print(isinstance(char, str))
        current_char_list = []  # For each digit, we create a new empty list for intermediate letter combinations
        char = int(char)
        # print(isinstance(char, str))
        # print(isinstance(char, int))
        print("char= ", char, "\n")
        for element in output_list:  # iterates through our current combinations # first iteration - it's blank ' ' (output_list = [''] )
            print("\t\tNEW element FOR LOOP:")
            print("element= ", element, "\n")
            for letter in list(nums_and_letters.get(char)): # iterate through our letter for the current digit in the input
                print("letter= ", letter, "\n", "nums_and_letters = ", nums_and_letters.get(char), "\n")
                current_result = element + letter #
                current_char_list.append(current_result)  # append each letter to each existing combination
                print("\ncurrent_char_list =", current_char_list)
        print("\t\t\t\t CHANGING output_list again\n")
        print("before = ", output_list)
        output_list = current_char_list  # after finishing for a digit in the user input, we update our result (the starting list for the for loop - for element in output_list:)
        print("after = ", output_list, "\n\n\n\n\n\n")
    return output_list  # after we processed for all chars / digits in the user's input string


def main():
    input_string = input("Enter digits (only from 2-9): ")

    if input_string.isdigit():
        if all(char in '23456789' for char in input_string):
            print(phone(input_string))
        else:
            print("You can only enter digits from 2 to 9")
            return None
    else:
        print("You can only enter digits")

    # for char in input_string:  # Check each char from user input:
    #     if char not in '23456789':  # ['2','3',...]
    #         print("You can only enter digits from 2 to 9")
    #         return None

if __name__ == '__main__':
    main()

#
# # Old script (only works for 2 digit input_string, e.g: '23' '29' etc...
# def phone(num1, num2):
#     nums_and_letters = {
#         2: ['a', 'b', 'c'],
#         3: ['d', 'e', 'f'],
#         4: ['g', 'h', 'i'],
#         5: ['j', 'k', 'l'],
#         6: ['m', 'n', 'o'],
#         7: ['p', 'q', 'r', 's'],
#         8: ['t', 'u', 'v'],
#         9: ['w', 'x', 'y', 'z']
#     }
#
#     num1_letter_list = []
#     num2_letter_list = []
#
#     for key in nums_and_letters:
#         if key == num1:
#             num1_letter_list = list(nums_and_letters.get(key))
#         if key == num2:
#             num2_letter_list = list(nums_and_letters.get(key))
#
#     output_list = []
#
#     i = 0
#     j = 0
#     for i in range(len(num1_letter_list)):
#         for j in range(len(num2_letter_list)):
#             output_list.append(num1_letter_list[i] + num2_letter_list[j])
#
#     return output_list
# def menu():
#     choice = input("Enter the digits (from 2-9): ")
#     if len(choice) != 2:
#         print("You can only enter 2 digits (from 2-9)")
#         return None
#     else: # entered a string with indeed only 2 chars\
#         if choice.isdigit():
#             num1 = int(choice[0])
#             num2 = int(choice[1])
#             print(phone(num1, num2))
#         else:
#             print("You can only enter digits (from 2-9)")
#             return None
#     # else:
#     #     if (choice[0] not in [2, 3, 4, 5, 6, 7, 8, 9]) or (choice[1] not in [2, 3, 4, 5, 6, 7, 8, 9]):
#     #         print("You can only enter digits (from 2-9)!!!!")
#     #         return None
#
# if __name__ == '__main__':
#     menu()