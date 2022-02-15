# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


def fib(idx):
    """
    Finds a certain term in the Fibbonacci sequence

    Parameters
    ----------
    idx : int
        The index of the term in the fib. sequence you wish to know

    Returns
    -------
    int
        The term at the given index of the fib. sequence

    """
    # Create fivb sequence up until your index
    seq = [0, 1]
    for k in range(1, idx):
        # Add previous two numbers
        seq.append(seq[k] + seq[k - 1])

    return seq[idx]


def main():
    """
    Asks for user input and return number in fib. sequence

    Returns
    -------
    None.

    """
    # loop until user gets bored
    bored = False
    while bored is False:
        # Get the first number
        i = 0
        while i == 0:
            try:
                f0 = int(input("Type a non negative integer: "))

                # Test to see if it's valid
                if f0 >= 0:
                    i = 1

                else:
                    print("Number was not positive")

            # Test to see if number is valid
            except ValueError:
                print("Please input an integer")

        print(fib(f0))

        # Check to see if user wants to keep going
        j = 0
        while j == 0:
            check = input("Continue? (y/n): ")

            # User wants to continue
            if check == "y":
                j = 1

            # User does not want to continue
            elif check == "n":
                j = 1
                bored = True

            # User did not provide a valid response
            else:
                print("Please type either 'y' or 'n'.")


if __name__ == "__main__":
    main()
