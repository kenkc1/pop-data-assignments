import pandas as pd


def read_grade_rubric():
    grade_file = input('Enter grades file: ')
    rubric_file = input('Enter rubric file: ')
    grade_df = pd.read_csv(grade_file)
    rubric_df = pd.read_csv(rubric_file)
    return grade_df, rubric_df

def main_user_menu():
    user_choice = input('1. Print question average (mean)\n'
                        '2. Print question average (quantiles)\n'
                        '3. Print student totals\n'
                        '4. Print student percentages\n'
                        '5. Print student ranking\n'
                        'Please enter your choice: '
                        )
    return user_choice


def mean(df):
    df = df.drop(['Student ID'], axis=1)
    df_mean = df.mean(axis=0)
    df_mean = pd.DataFrame({'Mean': df_mean})
    print(df_mean.to_string())


def quantiles(df):
    df = df.drop(['Student ID'], axis=1)
    q2 = df.quantile(q=0.5)
    q1 = df.quantile(q=0.25)
    q3 = df.quantile(q=0.75)

    frame = {'25%': q1, 'Median': q2, '75%': q3}
    quantiles_df = pd.DataFrame(frame)
    print(quantiles_df.to_string())


def student_total(df):
    df = grade_df.drop(['Student ID'], axis=1)
    df = df.sum(axis=1)
    grade_df['Total'] = df
    print(grade_df[['Student ID', 'Total']].to_string())


def student_percentages(grade_df, rubric_df):
    df = grade_df.drop(['Student ID'], axis=1)
    df = df*100
    df = df.T
    df = df.reset_index(drop=True)

    weighted_marks = df.div(rubric_df['Max score'], axis='index')
    weighted_marks = weighted_marks.T
    weighted_marks.rename(columns={0: 'Question 1', 1: 'Question 2',
                                   2: 'Question 3', 3: 'Question 4',
                                   4: 'Question 5', 5: 'Question 6'}
                                   , inplace=True)

    student_id = grade_df['Student ID']
    weighted_marks.insert(loc=0, column='Student ID', value=student_id)
    print(weighted_marks.to_string())


def choice_5(grade_df, rubric_df):
    df = grade_df.drop(['Student ID'], axis=1)
    df = df*100
    df = df.T
    df = df.reset_index(drop=True)

    weighted_marks = df.div(rubric_df['Max score'], axis='index')
    weighted_marks = weighted_marks.T
    weighted_marks.rename(columns={0: 'Question 1', 1: 'Question 2',
                                   2: 'Question 3', 3: 'Question 4',
                                   4: 'Question 5', 5: 'Question 6'}
                                   , inplace=True)

    student_id = grade_df['Student ID']
    weighted_marks.insert(loc=0, column='Student ID', value=student_id)
    # ------------------------------------------------------------
    weighted_marks.drop(['Student ID'], axis=1, inplace=True)
    weighted_marks['Mean'] = weighted_marks.mean(axis=1)
    weighted_marks.insert(loc=0, column='Student ID', value=student_id)

    weighted_marks.sort_values(by=['Mean','Student ID'], ascending=[False, True], inplace=True)

    weighted_marks = weighted_marks['Student ID']
    marks_sorted = pd.DataFrame({'Student ID': weighted_marks})
    print(marks_sorted.to_string())


if __name__ == "__main__":
    grade_df, rubric_df = read_grade_rubric()

    #print(grade_df)
    user_choice = main_user_menu()
    if user_choice == '1':
        mean(grade_df)
    elif user_choice == '2':
        quantiles(grade_df)
    elif user_choice == '3':
        student_total(grade_df)
    elif user_choice == '4':
        student_percentages(grade_df, rubric_df)
    elif user_choice == '5':
        choice_5(grade_df, rubric_df)
