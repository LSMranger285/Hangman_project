import random

def main():
    username = "lmcd653"

    # Load words from file
    words = get_words("source_words.txt")

    # Pick a random word
    word = random.choice(words)

    # Create encryption and tracking dictionaries
    encryption_dict = get_encryption_dictionary(word)
    consonant_dict = get_consonant_status_dictionary(word)

    # Display banner
    print_banner(username)

    # Start game
    result = play_game(word, consonant_dict, encryption_dict)

    # Final result message
    if result:
        print(f"Congratulations! You have decrypted '{word}' successfully!")
    else:
        print(f"Bad luck! The word was '{word}'! Try again!")

def print_banner(username):
    banner = "The Decryption Game by " + username.lower()
    
    
    for i in range(len(banner) + 4):
        print("*", end="")
    print()
    
    print("* " + banner + " *")
    for i in range(len(banner) + 4):
        print("*", end="")
    print()


# Reads words from a file and returns them as a list
def get_words(filename):
    words = []
    with open(filename, "r") as file:
        for line in file:
            words.append(line.strip())
    return words



def get_consonant_status_dictionary(word):
    vowels = "aeiou"
    consonant_dict = {}

    # Add each consonant to dictionary and set to False so the constant is encrypted
    for letter in word:
        if letter not in vowels:
            consonant_dict[letter] = False
    return consonant_dict


def print_puzzle(word, consonant_status_dict, encryption_dict):
    vowels = "aeiou"
    
    for letter in word:
        # vowels visible
        if letter in vowels:
            print(" " + letter, end="")

        # decrypted consonants
        elif consonant_status_dict[letter]:
            print(" " + letter, end="")

        # hidden consonants
        else:
            print(" __", end="")
    print()

    # Shows encryption codes under hidden consonants
    for letter in word:
        if letter not in vowels and not consonant_status_dict[letter]:
            code = encryption_dict[letter]
            print(f"{code:2}", end=" ")
        else:
            print("   ", end="")
    print()



def choose_valid_encryption_code(consonant_status_dict, encryption_dict):
    valid = False

    while not valid:
        chosen = input("Choose an encryption code to decrypt: ")

        # Must be a number
        if not chosen.isdigit():
            print("Please enter a non-negative integer for your choice!")
        else:
            chosen = int(chosen)

            # Must exist in encryption dictionary
            if chosen not in encryption_dict.values():
                print(f"{chosen} is not a valid code!")
            else:
                # Check if already decrypted
                for letter in encryption_dict:
                    if encryption_dict[letter] == chosen:
                        if consonant_status_dict[letter]:
                            print("This encryption code has already been decrypted!")
                        else:
                            valid = True

    print(f"You have chosen the code: {chosen}")
    return chosen
    


def choose_valid_consonant(consonant_status_dict):
    vowels = "aeiou"
    valid = False

    while not valid:
        chosen = input("Enter a consonant for the code: ")

        # Must be a letter
        if not chosen.isalpha():
            print("Please enter a consonant only!")
        
        # Must not be a vowel
        elif chosen.lower() in vowels:
            print("Please enter a consonant only!")
        
        # Must not already be decrypted
        elif chosen.lower() in consonant_status_dict and consonant_status_dict[chosen.lower()]:
            print(f"'{chosen.lower()}' has already been decrypted!")
        
        else:
            valid = True

    chosen = chosen.lower()
    print(f"You have chosen the consonant: '{chosen}'")
    return chosen


def play_round(round_number, mistakes_remaining, word,
               consonant_status_dict, encryption_dict):

    print(f"ROUND {round_number} - {mistakes_remaining} mistake(s) remaining:\n")

    # Show current puzzle
    print_puzzle(word, consonant_status_dict, encryption_dict)
    print()

    # Get user inputs
    chosen_code = choose_valid_encryption_code(
        consonant_status_dict, encryption_dict
    )
    chosen_consonant = choose_valid_consonant(consonant_status_dict)

    # Find correct consonant for selected code
    correct_consonant = None
    for letter in encryption_dict:
        if encryption_dict[letter] == chosen_code:
            correct_consonant = letter

    # Check if user is correct
    if chosen_consonant == correct_consonant:
        print(f"Well done! The consonant '{chosen_consonant}' "
              f"corresponds to the code {chosen_code}!")

        consonant_status_dict[correct_consonant] = True
        return True
    else:
        print(f"Bad luck! The consonant '{chosen_consonant}' "
              f"does not correspond to the code {chosen_code}!")
        return False


def play_game(word, consonant_status_dict, encryption_dict):
    mistakes_remaining = 10
    round_number = 1

    all_decrypted = False

    # Continue until no mistakes left or all consonants decrypted
    while mistakes_remaining > 0 and not all_decrypted:

        correct = play_round(
            round_number,
            mistakes_remaining,
            word,
            consonant_status_dict,
            encryption_dict
        )

        # Reduce mistakes if incorrect
        if not correct:
            mistakes_remaining -= 1

        round_number += 1
        print()

        # Check if all consonants are decrypted
        all_decrypted = True
        for letter in consonant_status_dict:
            if not consonant_status_dict[letter]:
                all_decrypted = False

    return all_decrypted


#Do not alter
def get_word(words):
    return words[random.randrange(len(words))]

#Do not alter
def get_encryption_dictionary(word):
    vowels = "aeiou"
    codes_used = []
    encryption_dict = {}
    for letter in word:
        if letter not in vowels and letter not in encryption_dict:
            code = random.randrange(0,21)
            while code in codes_used:
                code = random.randrange(0,21)
            codes_used.append(code)
            encryption_dict[letter] = code
    return encryption_dict
      
main()
        
