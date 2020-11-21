''' Written by Kenny Cai z3375670 Assessment 6 - ZZEN9021 - 17/04/2020

This program uses the Iris data set to generate simple summary statistics,
plots involving the iris characteristics. It includes an interactive menu
allowing the user to chose what statistic is required, as well as which
characteristics to plot.
'''

import pandas as pd
import seaborn as sns


def read_and_process(filename):
    ''' This function reads and cleans the data
    '''
    df = pd.read_csv(filename)
    # Cleaning the data - drop all rows with missing values,
    # strip all units and change to floats.
    df.dropna(inplace=True)
    df['sepal_length'] = df['sepal_length'].str.strip('cm').astype(float)
    df['sepal_width'] = df['sepal_width'].str.strip('mm').astype(float)
    df['petal_length'] = df['petal_length'].str.strip('cm').astype(float)
    df['petal_width'] = df['petal_width'].str.strip('cm').astype(float)

    df['sepal_width'] = df['sepal_width']/10  # As required in spec

    return df


def user_menu():
    ''' The function shows the user menu and returns the choice.
    '''
    user_choice = input('1. Create textual analysis\n'
                        '2. Create graphical analysis\n'
                        '3. Exit\n'
                        'Please select an option: ')
    return user_choice


def species_choice(spec_type):
    ''' This function computes stage 3. Returns mean, quantiles and standard
    deviation of the user specified species.
    '''
    if spec_type == 'all':
        df_mean = df.mean()
        df_25 = df.quantile(0.25)
        df_med = df.quantile(0.50)
        df_75 = df.quantile(0.75)
        df_std = df.std()

    else:
        df_mean = df.loc[df['species'] == spec_type].mean()
        df_25 = df.loc[df['species'] == spec_type].quantile(0.25)
        df_med = df.loc[df['species'] == spec_type].quantile(0.50)
        df_75 = df.loc[df['species'] == spec_type].quantile(0.75)
        df_std = df.loc[df['species'] == spec_type].std()

    df_complete = pd.DataFrame({'Mean': df_mean, '25%': df_25, 'Median': df_med,
                                '75%': df_75, 'Std': df_std})
    print(df_complete.to_string())


def sorted_headers_input(df):
    ''' This function takes a the column headers of a dataframe and organises
    in alphabetaical order. It then presents the headers (species) as an
    input.
    '''
    header_list = list(df.species.unique())
    header_list.sort()
    header_list = [', '.join(header_list)]
    spec_choice = input('Select species (all, '+header_list[0]+'): ')
    
    return spec_choice


def x_and_y_features():
    ''' Prompts user with choice of what to plot. The user can do a pairplot
    of all features or a scatter plot of two chosen features.
    '''
    x_choice = input('Choose the x-axis characteristic '
                     '(all, sepal_length, sepal_width, petal_length, '
                     'petal_width): '
                     )

    if x_choice == 'all':
    # Generates pairplot and saves to file.
        save_name = input('Enter save file: ')
        sns.set(style="ticks", color_codes=True)
        sns_plot = sns.pairplot(df, diag_kind="hist", hue='species')
        sns_plot.savefig(save_name)
    else:
        # Generates scatter plot and saves to file.
        y_choice = input('Choose the y-axis characteristic '
                         '(sepal_length, sepal_width, petal_length, '
                         'petal_width): '
                         )
        save_name = input('Enter save file: ')
        fig = feature_plot(x_choice, y_choice)
        fig.savefig(save_name)


def feature_plot(x_feature, y_feature):
    ''' Seaborn scatterplot of two features. Returns figure.
    '''
    sns_plot = sns.scatterplot(x=x_feature, y=y_feature, hue='species', data=df)
    fig = sns_plot.get_figure()

    return fig


def conclusion():
    # Return the two (non-species) categories that best identify the species of iris
    ''' Graphical analysis:
    A good choice distinguishing species using two characteristics from the
    graph are petal_length and petal_width.
    - The three species are can be seen as distinct clusters in the 'all' plot.
    - There is only slight overlap between versicolor and virginica where the
    lower values of viginica begin to overlap with the upper values in versicolor.

    Textual analysis:
    - The middle 50% (Q1 - Q3) for all species is quite different
    - The mean of all the species are also quite distinct
    '''
    answer = ('petal_length', 'petal_width')
    return answer


if __name__ == '__main__':
    filename = input('Enter csv file: ')

    # Stage 2: Prompts user menu
    df = read_and_process(filename)

    while True:
        choice = user_menu()
        if choice == '1':
            # Stage 3: Text-based analysis
            spec_choice = sorted_headers_input(df)
            species_choice(spec_choice)

        elif choice == '2':
            # Stage 4: Graphics-based analysis
            x_and_y_features()

        elif choice == '3':
            exit()