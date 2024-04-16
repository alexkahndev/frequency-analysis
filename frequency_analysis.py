import os
import re
import string


# Ansi codes for styling text in the terminal
class Styles:
    PURPLE = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    REVERSE = "\033[7m"


# Function to clear the terminal screen with the correct command for the OS
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Function to get the cypher text from the user
def get_cypher():
    # Ask the user for the cypher text or the path to a file containing the cypher text
    user_input = input(
        f"{Styles.GREEN}{Styles.BOLD}Enter the cypher text or the path to the file containing the cypher text: {Styles.RESET}"
    )

    # Try to use the input as a file path, if it is not a file path, use the input as the cypher text
    if os.path.isfile(user_input):
        with open(user_input, "r") as file:
            content = file.read()
            return content
    else:
        return user_input


# Function to get the frequency of characters in the cypher text
def get_frequency(text):
    # Create a dictionary to store the frequency of each character
    frequency = {}

    # Get the total count of characters in the text excluding spaces and new lines
    total_count = len(text.replace(" ", "").replace("\n", ""))

    # Loop through each character in the text and count the frequency of each character excluding spaces and new lines and punctuation
    for char in text:
        if char != " " and char != "\n" and char not in string.punctuation:
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

    # Loop through each character in the frequency dictionary and calculate the percentage of each character
    for char in frequency:
        frequency[char] = (frequency[char] / total_count) * 100

    # Return the frequency dictionary excluding spaces and new lines
    return {k: v for k, v in frequency.items() if k != " " and k != "\n"}


# Function to get the mapping of the cypher text to the known frequency
def get_mapping(known_frequency, frequency):
    # Sort the known frequency and frequency dictionaries by the frequency of the characters
    sorted_known_frequency = sorted(
        known_frequency.items(), key=lambda item: item[1], reverse=True
    )
    sorted_frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)

    # Create a dictionary to store the mapping of the cypher text to the known frequency
    mapping = {}

    # Loop through the sorted known frequency and frequency dictionaries and map the characters in the cypher text to the known frequency
    for i in range(min(len(sorted_known_frequency), len(sorted_frequency))):
    
        mapping[sorted_frequency[i][0]] = sorted_known_frequency[i][0]
        

    # Return the dictionary with the characters that have been mapped
    return mapping


# Function to substitute the characters in the cypher text with the mapped characters
def substitue_cypher(cypher_text, mapping):
    decrypted_text = ""

    # Loop through each character in the cypher text and substitute the character with the mapped character if it exists in the mapping otherwise keep the character the same
    for char in cypher_text:
        if char in mapping:
            decrypted_text += mapping[char]
        else:
            decrypted_text += char

    # Return the decrypted text according to the mapping
    return decrypted_text


# Function to allow the user to manually switch characters in the mapping to decrypt the cypher text
def manual_switch(cypher_text, mapping):
    # Create a variable to keep track of whether the user wants to keep switching characters
    switching = True

    # Decrypt the cypher text using the current mapping
    final_text = substitue_cypher(cypher_text, mapping)

    # Create variables to keep track of the last result of the user's input
    last_result = ""
    last_result_color = Styles.GREEN

    # Create a regular expression to validate the user's input in the form Letter (space) Letter
    input_format = r"^[a-zA-Z] [a-zA-Z]$"

    # Loop through the character switching mode until the user decides to exit
    while switching:
        # Clear the screen and print the current mapping, decrypted text and the last result
        clear_screen()
        print(f"{Styles.GREEN}Current Mapping:{Styles.RESET}")
        for k, v in mapping.items():
            print(f"{Styles.CYAN}{k}{Styles.RESET} -> {Styles.CYAN}{v}{Styles.RESET}")
        print(f"\n{Styles.BLUE}Current Decrypted Text:{Styles.RESET}\n{final_text}")
        print(
            f"\n{Styles.YELLOW}Last Result: {last_result_color}{last_result}{Styles.RESET}"
        )

        # Ask the user for the character they want to switch and the new character they want to switch to, or to exit the character switching mode
        user_input = input(
            f"\n{Styles.PURPLE}{Styles.BOLD}Enter a character in the mapping you want to change{Styles.RESET} "
            f"{Styles.PURPLE}{Styles.BOLD}\nFollowed by a space{Styles.RESET}"
            f"{Styles.PURPLE}\nThen the new character you want first input map to{Styles.RESET}"
            f"{Styles.PURPLE}\nOr enter 0 to exit the character switch mode{Styles.RESET}\n\n"
        )

        # Check if the user wants to exit the character switching mode
        if user_input == "0":
            switching = False
            clear_screen()

        # Check if the user's input matches the input format and if the characters are in the mapping
        elif re.match(input_format, user_input):
            old_char, new_char = user_input.upper().split(" ", 1)

            # Check if the old character is in the mapping and the new character was already in the mapping then switch what was already mapped to the new character to the old character
            if old_char in mapping and new_char in mapping.values():
                for k, v in mapping.items():
                    if v == new_char:
                        mapping[k] = mapping[old_char]
                mapping[old_char] = new_char
                final_text = substitue_cypher(cypher_text, mapping)
                last_result = (
                    f"Successfully switched {old_char} to {new_char} in the mapping."
                )
                last_result_color = Styles.GREEN

            # Check if the old character is in the mapping and the new character is not in the mapping then switch the old character to the new character
            elif old_char in mapping:
                mapping[old_char] = new_char
                final_text = substitue_cypher(cypher_text, mapping)
                last_result = (
                    f"Successfully changed {old_char} to {new_char} in the mapping."
                )
                last_result_color = Styles.GREEN

            # Otherwise the old character is not in the mapping
            else:
                last_result = "Character not found in the mapping."
                last_result_color = Styles.RED

        # Otherwise the user's input does not match the input format
        else:
            last_result = "Invalid input format."
            last_result_color = Styles.RED

    return final_text, mapping


# Known frequency of letters in the English language from https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
known_frequency = {
    "A": 8.4966,
    "B": 2.0720,
    "C": 4.5388,
    "D": 3.3844,
    "E": 11.1607,
    "F": 1.8121,
    "G": 2.4705,
    "H": 3.0034,
    "I": 7.5448,
    "J": 0.1965,
    "K": 1.1016,
    "L": 5.4893,
    "M": 3.0129,
    "N": 6.6544,
    "O": 7.1635,
    "P": 3.1671,
    "Q": 0.1962,
    "R": 7.5809,
    "S": 5.7351,
    "T": 6.9509,
    "U": 3.6308,
    "V": 1.0074,
    "W": 1.2899,
    "X": 0.2902,
    "Y": 1.7779,
    "Z": 0.2722,
}

# Start the program by clearing the screen
clear_screen()

# Get the cypher text from the user
cypher_text = get_cypher()

# Get the frequency of the characters in the cypher text
frequency = get_frequency(cypher_text)

# Get the mapping of the cypher text to the known frequency
mapping = get_mapping(known_frequency, frequency)

# Decrypt the cypher text using the mapping
decrypted_text = substitue_cypher(cypher_text, mapping)

# Allow the user to manually switch characters in the mapping
final_decrypted_text, final_mapping = manual_switch(cypher_text, mapping)

# Print the final mapping and decrypted text
print(f"{Styles.GREEN}Final Mapping:{Styles.RESET}")

for k, v in final_mapping.items():
    print(f"{Styles.CYAN}{k}{Styles.RESET} -> {Styles.CYAN}{v}{Styles.RESET}")

print(f"\n{Styles.BLUE}Final Decrypted Text:{Styles.RESET}\n{final_decrypted_text}\n")
