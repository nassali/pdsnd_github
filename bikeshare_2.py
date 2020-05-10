import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_selection = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
day_selection = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def user_choice(user_input):
    """
    Gets user input and returns True if user introduces 'yes' or False for 'no'

    args:
        (str) user_input - input introduced by the user

    Returns:
        (bool) result - True if user introduced 'yes' and false for 'no'
    """
    yes_no = ['yes', 'no']
    result = False
    while user_input not in yes_no:
        user_input = input('The information you introduced is incorrect. Enter yes or no\n').lower()
    if user_input == 'yes':
        result = True

    return result


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWould you like to see data for Chicago, New York or Washington ?\n').lower()
    while city not in CITY_DATA:
        city = input('\nThe information you introduced is incorrect. Choose between Chicago, New York or Washington ?\n').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('\nWhat month would you like the data for? Choose between: all, january, february, march, april, may, june.\n').lower()
    while month not in month_selection:
        month = input('\nThe information you introduced is incorrect. Choose between: all, january, february, march, april, may, june.\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('\nWhat day of week would you like the data for? Choose between: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday.\n').lower()
    while day not in day_selection:
        day = input('\nThe information you introduced is incorrect. Choose between: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday.\n').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month , day of week and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of month_selection list to get the corresponding int
        month = month_selection.index(month)
        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month only if all months are specified
    if month == 'all':
        print('\nCalculating the Most Common Month:')
        most_common_month, month_count = most_common_compute(df['Month'])
        #convert most_common_month digit in str through a list comprehension in case of more than one month
        most_common_month = [month_selection[month].title() for month in most_common_month]
        display_result(most_common_month, month_count)
        nan_count(df['Month']) # displays if there is any NaN values 

    # display the most common day of week only if all day of week are specified
    if day == 'all':
        print('\nCalculating the Most Common Day of Week:')
        most_common_dow, dow_count = most_common_compute(df['Day of Week'])
        display_result(most_common_dow, dow_count)
        nan_count(df['Day of Week'])

    # display the most common start hour
    print('\nCalculating the Most Common Start Hour:')
    most_common_hour, hour_count = most_common_compute(df['Hour'])
    display_result(most_common_hour, hour_count)
    nan_count(df['Hour'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nCalculating the Most Commonly used Start Station:')
    most_start_station, start_count = most_common_compute(df['Start Station'])
    display_result(most_start_station, start_count)
    nan_count(df['Start Station'])

    # display most commonly used end station
    print('\nCalculating the Most Commonly used End Station:')
    most_end_station, end_count = most_common_compute(df['End Station'])
    display_result(most_end_station, end_count)
    nan_count(df['End Station'])

    # display most frequent combination of start station and end station trip
    print('\nCalculating the Most Frequent Trip (Start Station, End Station):')
    trip_ds = df.groupby(['Start Station', 'End Station'])['Start Station'].count()
    startend_most_count = trip_ds.max()
    trip_stations = trip_ds[trip_ds == startend_most_count].index
    display_result(trip_stations, startend_most_count)
    nan_count(trip_ds)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nCalculating Total Travel Time:')
    hours, minutes, seconds = convert_sec(df['Trip Duration'].sum())
    print('{} Hours {} Minutes {} Seconds'.format(hours, minutes, seconds))
    nan_count(df['Trip Duration'])

    # display mean travel time
    print('\nCalculating Mean Travel Time:')
    hours, minutes, seconds = convert_sec(round(df['Trip Duration'].mean()))
    print('{} Hours {} Minutes {} Seconds'.format(hours, minutes, seconds))
    nan_count(df['Trip Duration'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCalculating Count of User Types in percentage:')
    user_ds = round(df['User Type'].value_counts(normalize = True)*100, 4)
    #iterates through a loop to display the different user types and the count from it
    for i in range(len(user_ds)):
        print('{}: {}%'.format(user_ds.index[i], user_ds[i]))
    nan_count(df['User Type'])

    if city != 'washington':
        # Display counts of gender
        print('\nCalculating Count of Gender in percentage:')
        gender_ds = round(df['Gender'].value_counts(normalize=True)*100, 2)
        #iterates through a loop to display the different Gender and the count from it
        for i in range(len(gender_ds)):
            print('{}: {}%'.format(gender_ds.index[i], gender_ds[i]))
        nan_count(df['Gender'])

        # Display earliest, most recent, and most common year of birth
        birth_year_ds = df['Birth Year']
        print('\nCalculating Earliest Year of Birth User:')
        min_year = round(birth_year_ds.min())
        min_year_count = number_trip(birth_year_ds, min_year)
        display_result(min_year, min_year_count)

        print('\nCalculating Most Recent Year of Birth User:')
        max_year = round(birth_year_ds.max())
        max_year_count = number_trip(birth_year_ds, max_year)
        display_result(max_year, max_year_count)

        print('\nCalculating Most Common Year of Birth User:')
        most_year, most_year_count = most_common_compute(birth_year_ds)
        display_result(most_year, most_year_count)
        nan_count(birth_year_ds)
    else:
        print('\nSorry, we don\'t have any Gender or Year of Birth Data to display for {}.\n'.format(city.title()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def most_common_compute(ds):
    """
    Calculate the most common data in a DataSeries

    Arg:
        ds - DataSeries
    Returns:
         index - the most common data(s)
         nb_trip - number of trips linked to this most common data
    """
    index = ds.mode()
    nb_trip = number_trip(ds, index[0])

    return index, nb_trip


def number_trip(ds, data):
    """
    Calculates the number of trips in a DataSeries from a specific data

    Args:
        ds - DataSeries
        data - the data where the counts needs to be computed
    Returns:
        nb_trip - Number of trips
    """
    nb_trip = ds[ds == data].count()

    return nb_trip


def display_result(data, nb_trip):
    """
    Displays a data and the number of trips from that data

    Args:
        data - data to display
        nb_trips - number of trips related to that data
    """
    #in case there is more than one data to display
    try:
        for i in data:
            print(i)
    except TypeError:
        print(data)

    print('Number of Trips: {}'.format(nb_trip))
    print('That represents {}% of the trips'.format(percentage(nb_trip, tot_trip_count)))


def percentage(val, total):
    """
    Calculates the ratio from one value to another as a fraction of 100

    Args:
        (int) val: the value that we want to get the percentage from
        (int) total: the value that represents 100%
    Returns:
        (float) Percentage of val comparing to the total till the fourth decimal
    """
    return round(val/total*100,4)


def nan_count(ds):
    """
    Count if there is any Nan values from a DataSeries and displays it
    """
    if ds.isnull().any():
        nan_count = ds.isnull().sum()
        print('Count of No Data: {}. It represents {}% of the trips'.format(nan_count, percentage(nan_count, tot_trip_count)))


def convert_sec(time):
    """
    Converts a number to hour, minutes and seconds

    Args:
        (int) time - number to convert. time is in seconds
    Returns:
        (int) hour - number of hour included in time
        (int) minute - number of minutes remaining by removing the hour
        (int) second - number of seconds remaining by removing the minutes
    """
    hour, remainder_time = divmod(time, 3600)
    minute, second = divmod(remainder_time, 60)

    return hour, minute, second


while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)

    #if the created dataframe is empty, we don't go through the different computations
    if not df.empty:
        #calculate the total number of trips from subdataframe created
        tot_trip_count = df['Start Station'].count()
        print('\nNumber of Trips:\n{}'.format(tot_trip_count))

        time_stat_view = user_choice(input('\nWould you like to see some statistics about Time Travel? Enter yes or no.\n').lower())
        if time_stat_view:
            time_stats(df)

        station_stat_view = user_choice(input('\nWould you like to see some statistics about Stations and Trip? Enter yes or no.\n').lower())
        if station_stat_view:
            station_stats(df)

        trip_duration_stat_view = user_choice(input('\nWould you like to see some statistics about Trip Duration? Enter yes or no.\n').lower())
        if trip_duration_stat_view:
            trip_duration_stats(df)

        user_stat_view = user_choice(input('\nWould you like to see some statistics about Users? Enter yes or no.\n').lower())
        if user_stat_view:
            user_stats(df)

        raw_data = user_choice(input('\nWould you like to see some Individual Trip Data? Enter yes or no.\n').lower())
        if raw_data:
            i=0
            while True:
                #display raw data 5 by 5
                print(df.iloc[i:i+5])
                i += 5
                next_data = user_choice(input('\nWould you like to see more Individual Trip Data? Enter yes or no.\n').lower())
                if not next_data:
                    break
                if df.iloc[i:i+5].empty:
                    print('\nNo more data to display\n')
                    break
    else:
        print('\nThere was 0 trip for the combination you introduced !\n')

    restart = user_choice(input('\nWould you like to restart? Enter yes or no.\n').lower())
    print('-'*40)
    if not restart:
        break
