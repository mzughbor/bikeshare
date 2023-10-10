import time
from datetime import timedelta, datetime
import pandas as pd

CITY_DATA: dict[str, str] = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}


def get_city():

    """
    This function responsible for getting city name from the user, and return filename back
    to main() for next process...
    Args: none
    Returns: (str) Filename for a city's bike-share data
    """

    city = ''
    while city.lower() not in CITY_DATA:
        # we'll exit while with return statements too
        city = input('\nHello! Let\'s explore some US bike-share data!\n'
                     'Would you like to see data for Chicago, New York, or Washington?\n\n')

        if city.lower() == 'chicago':
            return CITY_DATA['chicago']
        elif city.lower() == 'new york' or city.lower() == 'newyork' or city.lower() == 'new-york':
            return CITY_DATA['new york']
        elif city.lower() == 'washington':
            return CITY_DATA['washington']
        else:
            # do while will reactivate question again until getting an answer
            print('Sorry, I do not understand your input! Please input correct name: Chicago,'
                  'New York, or Washington.')
            print('------------------------------------------------------------------------')


def get_time_period():

    """
    This function asks the user for a time period and returns the specified filter.
    Args: none
    Returns: (str) Time filter for the bike-share data
    """

    time_period = ''
    while time_period.lower() not in ['month', 'day', 'none']:
        time_period = input('Would you like to filter the data by month, day, or not at all? '
                            'Type "none" for no time filter.\n>>> If you like to start over by other city? '
                            'Type \'Restart\' as your answer! \n')
        print('------------------------------------------------------------------------')

        if time_period.lower() == 'restart':
            main()
            break

        elif time_period.lower() not in ['month', 'day', 'none']:
            print('Sorry, I do not understand your input please choose month, day, or none.')
            print('------------------------------------------------------------------------')

    return time_period


def get_month():

    """
    This function asks the user for a month and returns it to next process.
    Args: none
    Returns: (tuple) Lower limit and the upper limit of month for the data.
    """

    month_input = ''
    months_dic = {'january': 1, 'february': 2, 'march': 3, 'april': 4,
                  'may': 5, 'june': 6}
    while month_input.lower() not in months_dic.keys():
        month_input = input('\nWhich month? January, February, March, April,'
                            ' May, or June?\n')
        print('------------------------------------------------------------------------')

        if month_input.lower() not in months_dic.keys():
            print('------------------------------------------------------------------------')
            print("Sorry, I do not understand your input. Please type in a month between "
                  "January and June to filter by...\n>>> If you like to start over by other city? "
                  "Type \'Restart\' as your answer!! \n")
        if month_input.lower() == 'restart':
            main()
            break
    month = months_dic[month_input.lower()]
    print(f"Your filtration duration is : 2017-{month}", f"2017-{month + 1}")
    print('------------------------------------------------------------------------')
    return '2017-{}'.format(month), '2017-{}'.format(month + 1)


def popular_month(df):

    """
    This function finds and prints the most popular month for started time.
    args: bike-share dataframe
    Returns: none
    """

    months = ['January', 'February', 'March', 'April', 'May', 'June']
    index = int(df['start_time'].dt.month.mode()[0])

    most_pop_month = months[index - 1]
    print(f"The most popular month was {most_pop_month}.")


def get_day():

    """
    This function asks the user for a day and returns it.
    Args none
    Returns: (tuple) Lower limit, upper limit of date for data.
    """

    # global start_date
    this_month = get_month()[0]
    month = int(this_month[5:])

    valid_date: bool = False
    while not valid_date:
        is_int: bool = False
        day = input("\nWhich day? Please type your response as an integer?\n")
        print('------------------------------------------------------------------------')

        while not is_int:
            try:
                day = int(day)
                is_int = True
            except ValueError:
                print("Sorry, I do not understand your input. Please type your"
                      " answer as an integer from 1 to 6 ...")
                print('------------------------------------------------------------------------')

                day = input('\nWhich day you pick?\n')
                print('------------------------------------------------------------------------')

        if 1 <= day <= 6:
            valid_date = True
            start_date = datetime(2017, month, day)
        else:
            pass
    end_date = start_date + timedelta(days=1)
    return str(start_date), str(end_date)


def popular_day(df):

    """
    This function finds and prints the most popular day of week for started time.
    Args: bike-share dataframe
    Returns: none
    """

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    index = int(df['start_time'].dt.dayofweek.mode()[0])
    most_pop_day = days_of_week[index]
    print(f"The most popular day of week for start time was {most_pop_day}.")


def popular_hour(df):

    """
    This function finds and prints the most popular hour of day for started time...
    Args: bike-share dataframe
    Returns: none
    """

    global am_pm, pop_hour_readable
    most_pop_hour = int(df['start_time'].dt.hour.mode()[0])
    am_pm = 'am' if most_pop_hour < 12 else 'pm'
    pop_hour_readable = most_pop_hour if most_pop_hour < 13 else most_pop_hour - 12
    print(f"The most popular hour of day for started time is {pop_hour_readable}{am_pm}.")


def trip_duration(df):

    """
    This function finds and prints the total trip duration and average in hours, minutes, and seconds...
    Args: bike-share dataframe
    Returns:  none
    """

    total_duration = timedelta(seconds=int(df['trip_duration'].sum()))
    average_duration = round(df['trip_duration'].mean(), 0)

    print(f"The total trip duration is {total_duration.total_seconds() // 3600} hours,"
          f" {total_duration.total_seconds() % 3600 // 60} minutes and "
          f"{total_duration.total_seconds() % 60} seconds.")
    print(f"The average trip duration is {average_duration // 60} minutes and {average_duration % 60} seconds.")


def popular_stations(df):

    """
    This function finds and prints the most popular start and end station...
    Args: bike-share dataframe
    Returns: none
    """

    pop_start = df['start_station'].mode().to_string(index=False)
    pop_end = df['end_station'].mode().to_string(index=False)
    print(f"The most popular start station is {pop_start}.")
    print(f"The most popular end station is {pop_end}.")


def popular_trip(df):

    """
    This function finds and prints the most popular trip from selected dataframe
    Args: bike-share dataframe
    Returns:  none
    """
    # adding one more column named journey ...
    most_pop_trip = df['journey'].mode().to_string(index=False)
    print(f"The most popular trip is {most_pop_trip}.")


def users(df):

    """
    This function finds and prints the counts of each user type
    Args: bike-share dataframe
    Returns: none
    """

    subs = df.query('user_type == "Subscriber"').user_type.count()
    cust = df.query('user_type == "Customer"').user_type.count()
    print(f"There are {subs} Subscribers and {cust} Customers!")


def display_data(df):

    """
    This function present five lines of data if the user specifies that they would like
    to see more and keep asking until they say no stop.
    Args: bike-share data frame
    Returns: none
    """

    display = input('\nWould you like to view individual trip data? Type \'yes\' or \'no\'.\n')
    if display.lower() == 'yes':
        # prints every column except the 'journey' column created in main function...
        print(df[df.columns[0:-1]].head(5))

        while True:
            display_more = input('\nWould you like to view more individual trip data? '
                                 'Type \'yes\' or \'no\'.\n')
            if display_more.lower() == 'yes':
                print(df[df.columns[0:-1]].iloc[5:])
                break
            elif display_more.lower() == 'no':
                break
            else:
                print("Sorry, I do not understand your input. Please type 'yes' or 'no'...!")


def gender(df):

    """
    This function present and prints the counts of gender.
    Args: bike-share dataframe
    Returns: none
    """

    male_count = df.query('gender == "Male"').gender.count()
    female_count = df.query('gender == "Male"').gender.count()

    print(f"There are {male_count} male users and {female_count} female users.")


def birth_years(df):

    """
    This function find and present the oldest user/the youngest user and birth years.
    Args: bike-share dataframe
    Returns: none
    """

    earliest = int(df['birth_year'].min())
    latest = int(df['birth_year'].max())
    mode = int(df['birth_year'].mode()[0])

    print(f"The oldest users are born on {earliest}.\nThe youngest users are born on {latest}. \n"
          f"The most popular birth year is {mode}.")


def main():

    """
    This function calculates, print out the statistics based on user input
    and counting time consumed in each task...

    Args: none
    Returns: none
    """

    global start_time
    start_time = time.time()
    global filter_lower, df_filtered, filter_upper

    # Get the city from the user
    city = get_city()
    # Load the data from the city CSV file
    print('\n>>> Please wait while loading the data ...\n')
    df = pd.read_csv(city, parse_dates=['Start Time', 'End Time'])

    # Rename the columns to lowercase and replace spaces with underscores
    new_labels = []

    for col in df.columns:
        new_labels.append(col.replace(' ', '_').lower())
    df.columns = new_labels

    # using popular_trip()
    # Create a 'journey' column that concatenates 'start_station' with 'end_station'
    df['journey'] = df['start_station'].str.cat(df['end_station'], sep=' to ')

    # Filter by time period (month, day, none)
    time_period = get_time_period()
    if time_period == 'none':
        df_filtered = df
    elif time_period == 'month' or time_period == 'day':
        if time_period == 'month':
            filter_lower, filter_upper = get_month()
        elif time_period == 'day':
            filter_lower, filter_upper = get_day()
        print('Filtering data...')
        df_filtered = df[(df['start_time'] >= filter_lower) & (df['start_time'] < filter_upper)]
    print('\nCalculating the first statistic...')
    print('------------------------------------------------------------------------')

    if time_period == 'none':
        start_time = time.time()
        # Question
        # What is the most popular month for start time?
        popular_month(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        print('------------------------------------------------------------------------')
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()

        # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
        popular_day(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        print('------------------------------------------------------------------------')
        start_time = time.time()

    # What is the total trip duration and average trip duration?
    trip_duration(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    print('------------------------------------------------------------------------')
    start_time = time.time()

    # What is the most popular hour of day for start time?
    popular_hour(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    print('------------------------------------------------------------------------')
    start_time = time.time()

    # What is the most popular start station and most popular end station?
    popular_stations(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    print('------------------------------------------------------------------------')
    start_time = time.time()

    # What is the most popular trip?
    popular_trip(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))
    print("\nCalculating the next statistic...")
    print('------------------------------------------------------------------------')
    start_time = time.time()

    # What are the counts of each user type?
    users(df_filtered)
    print("That took %s seconds." % (time.time() - start_time))

    # Only for more two columns data
    if city == 'chicago.csv' or city == 'new_york_city.csv':
        print("\nCalculating the next statistic...")
        print('------------------------------------------------------------------------')
        start_time = time.time()

        # What are the counts of gender?
        gender(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print("\nCalculating the next statistic...")
        print('------------------------------------------------------------------------')

        start_time = time.time()

        # What are the earliest (i.e. oldest user), most recent (i.e. youngest
        # user), and most popular birth years?
        birth_years(df_filtered)
        print("That took %s seconds." % (time.time() - start_time))
        print('------------------------------------------------------------------------')

    # Display five lines of data at a time if user specifies that they would like to
    display_data(df_filtered)

    # Do you wanna restart?
    restart = input("\nWould you like to restart? Type \'yes\' or \'no\'.\n")
    while restart.lower() not in ["yes", "no"]:
        print("Invalid input. Please type \'yes\' or \'no\'.")
        restart = input("\nWould you like to restart? Type \'yes\' or \'no\'.\n")
    if restart.lower() == "yes":
        print("Thanks, 0*_0 for using our program!")
        main()


if __name__ == "__main__":
    main()
