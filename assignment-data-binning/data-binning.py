''' Written by Kenny Cai z3375670 Assessment 3 - ZZEN9021

This is a data binning program. It asks the user to input a data file, and
asks for an input (bin size) of the user's choice. There is also an option of
displaying the frequency analysis and writing the results to an
external file.
'''

import os.path
import math
import numpy as np
import decimal
from os import path


def read_from_file(filename):
    ''' Reads a data file, and returns a list of the data file as floats
    '''
    f = open(filename, 'r')
    data = f.read()
    f.close()

    # Puts each line of the file as element in list.
    data_list = [elem for elem in data.split()]

    # Checks for '-' and removes them.
    data_list = list(filter(('-').__ne__, data_list))

    # Converts all elements to floats and returns list.
    data_list_float = []
    for i in range(len(data_list)):
        data_list_float.append(float(data_list[i]))
    return data_list_float


def write_to_file(filename, binned_data):
    ''' Writes a dictionary of the binned data to an external file.
    '''
    keys = list(binned_data.keys())
    values = list(binned_data.values())
    complete_list = []

    for i in range(len(keys)):
        complete_list.append(str(keys[i])+': '+str(values[i]))

    f = open(filename, 'w')
    f.write('\n'.join(complete_list))
    f.close()


def bin_data(data, binsize):
    ''' Places the data into bins.
    '''
    def round_2dp(argument):
        ''' To avoid float rounding errors, this function rounds the arugment
        to 2 decimal places correctly.

        e.g round(1.555, 2) = 1.55, thus we convert 1.555 to a decimal using the
        decimal library, rounds it to 4 places, then rounds to 2 decimal places.

        ie. ans = round(decimal.Decimal(1.555), 4) = 1.555
            round(ans, 2) = 1.56
        '''
        context = decimal.getcontext()
        context.rounding = decimal.ROUND_HALF_UP
        rounded = float(round(round(decimal.Decimal(argument), 4), 2))
        return rounded

    data.sort()
    binned_data = {}

    binsize = round_2dp(binsize)
    bin_low = round_2dp(min(data))  # initial bin_low which is min(data)
    bin_high = round_2dp(bin_low + binsize)

    # Calculates no. of bins needed for numpy histogram.
    bins = math.ceil(round_2dp((max(data)-min(data)))/binsize)

    max_range = round_2dp(bin_low + (bins)*binsize)

    # Since last bin is inclusive of right boundary [a, b], add one
    # more bin if highest data point is equal to the last value on the bin.
    if data[-1] == max_range:
        bins += 1
        max_range = round_2dp(max_range + binsize)

    # Gets a list of the bin frequncies from numpy histogram.
    freq_list = bin_freq_list(data, bins, bin_low, max_range)

    # Loop that creates the dictionary of bin keys and frequency count.
    for i in freq_list:
        key = str(bin_low) + ' - ' + str(bin_high)
        binned_data[key] = i
        bin_low_temp = round_2dp(bin_low)
        bin_high_temp = round_2dp(bin_high)
        bin_low = round_2dp(bin_low_temp + binsize)
        bin_high = round_2dp(bin_high_temp + binsize)
    return binned_data


def display_freq_analysis(binned_data):
    ''' Displays frequency analysis.
    '''
    for key, value in binned_data.items():
        print(key, value, sep=': ')


def bin_freq_list(data, bins, minimum, maximum):
    ''' Returns a list of frequencies in each bin
    using the numpy histogram function.
    '''
    hist, bin_edges = np.histogram(data, bins=bins, range=(minimum, maximum))
    freq_list = np.array(hist).tolist()
    return freq_list


def display_menu():
    ''' Returns the user choice for the interaction menu.
    '''
    user_choice = input('1. Set bin size\n'
                        '2. Display frequency analysis\n'
                        '3. Exit\n'
                        'Please enter your choice: ')
    return user_choice


def save_file_menu():
    ''' Returns the user choice for the save file interaction.
    '''
    save = input('Save analysis to file? (Y/N) ')
    return save


# Stages 4 and 5: Interact with the user with menus and error handling.
# The following line suppresses the code when the file is imported.
if __name__ == '__main__':
    while True:
        x = input('Enter data file: ')

        # Outer loop to check file exists in directory.
        if path.exists(x) is True:

            # Menu interaction loop
            while True:
                user_choice = display_menu()
                if user_choice == '1':
                    # Checks for valid bin size.
                    while True:
                        binsize = float(input('Enter bin size: '))
                        if binsize > 0:
                            break
                        elif binsize <= 0:
                            print('Invalid bin size, try again')

                elif user_choice == '2' and 'binsize' not in locals():
                    print('Please set a bin size first')

                # Shows frequency and gives user option to write file.
                elif user_choice == '2':
                    bin_data_var = bin_data(read_from_file(x), binsize)
                    display_freq_analysis(bin_data_var)

                    # Save file choice loop.
                    while True:
                        save = save_file_menu()
                        if save == 'Y':
                            file_name = input('Enter file name: ')
                            write_to_file(file_name, bin_data_var)
                            break
                        elif save == 'N':
                            break
                        else:
                            print('Not a valid option')

                elif user_choice == '3':
                    exit()
                else:
                    print('Not a valid option')

        else:
            print('File not available')
