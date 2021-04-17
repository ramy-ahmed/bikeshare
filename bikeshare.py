import time
import pandas as pd
import numpy as np
import os.path
import sys
import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def check_data_files():
    for file in CITY_DATA.values():
        if not os.path.isfile(file):
            print ("Sorry, File {} is missing, kindly add the file and try again".format(file))
            sys.exit()

def seconds_to_days(n):
    """
    Convert seconds to days.

    Returns:
        (int) day - number of days in seconds
        (int) hour - number of hours in seconds
        (int) minutes - number of minutes in seconds
        (int) seconds - number of seconds
    """
    day = n // (24 * 3600)

    n = n % (24 * 3600)
    hour = n // 3600

    n %= 3600 
    minutes = n // 60

    n %= 60
    seconds = n

    return day, hour, minutes, seconds



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    check_data_files()
    print('You can exit at any time by pressing Crtl+z !')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see the data for {}, {}, or {}? \n'.format(*[key.title() for key in list(CITY_DATA.keys())])).strip().lower()
            if city in CITY_DATA.keys():
                break
            else :
                print('Invalid city kindly try again \n')
        except:
            print('Invalid city kindly try again \n')
    
    
    # get user input for filter type (month, day, both, none)
    filter_keys = ['month', 'day', 'both', 'none']
    while True:
        try:
            filter = input('\nWould you like to filter the data by {}, {}, {}, or not at all? type "{}" for no time filter. \n'.format(*filter_keys)).strip().lower()
            if filter in filter_keys:
                break
            else :
                print('Invalid filter kindly try again \n')
        except:
            print('Invalid filter kindly try again \n')


    # get user input for month (all, january, february, ... , june)
    
    if filter == 'month' or filter == 'both':
        while True:
            try:
                month = input('\nWhich month? {}, {}, {}, {}, {}, or {}? \n'.format(*[key.title() for key in MONTHS])).strip().lower()
                if month in MONTHS:
                    break
                else :
                    print('Invalid month kindly try again \n')
            except:
                print('Invalid month kindly try again \n')                
    else :
        month = 'all'
    


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = pd.Series(data=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],index=[1,2,3,4,5,6,7])
    if filter == 'day' or filter == 'both':
        while True:
            try:
                day_index = int(input('\nWhich day? Please type your response as an integer (e.g., 1=Sunday).\n'))
                if day_index in days:
                    day = days[day_index]
                    break
                else :
                     print('Invalid day')
            except:
                print('Invalid integer kindly try again')               
    else :
        day = 'all'

    print('-'*40)
    return city, month, day, filter


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

    # load the data file into a pandas DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Strt Time column to datatime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # convert the End Time column to datatime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract hour from Start Time column to create a start_hour column
    df['start_hour'] = df['Start Time'].dt.hour

    # extract month from Start Time column to create a start_month column
    df['start_month'] = df['Start Time'].dt.month

    # extract month day of week from Start Time column to create a start_day_of_week column
    df['start_day_of_week'] = df['Start Time'].dt.day_name()

    # create trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station']


    # filter by month if applicable
    if month != 'all':
        # get month number
        month = MONTHS.index(month) + 1

        # filter by month to
        df = df[df['start_month'] == month]
    
    # filter by dat of week if applicable
    if day != 'all':
        df = df[df['start_day_of_week'] == day]

    return df


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # get the most common month
    most_common_month = MONTHS[ df['start_month'].mode()[0] - 1 ].title() 

    # get the most common day of week
    most_common_day_of_week = df['start_day_of_week'].mode()[0]

    # get the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]

    # count number of most popular hour
    count_most_common_start_hour = len(df[df['start_hour'] == most_common_start_hour])

    # disply statistics
    if filter == 'both':
        print("Most popular hour:{}, Count:{}, Filter:{}".format(most_common_start_hour, count_most_common_start_hour , filter))

    elif filter == 'day':
        # count number of most popular month
        count_most_common_month = len(df[df['start_month'] == most_common_month])

        print("Most popular hour:{}, Count:{}, Filter:{}".format(most_common_start_hour, count_most_common_start_hour , filter)) 
        print("Most popular month:{}, Count:{}, Filter:{}".format(most_common_month, count_most_common_month , filter))

    elif filter == 'month':
        # count number of most popular week of day and month
        count_most_common_day_of_week = len(df[df['start_day_of_week'] == most_common_day_of_week])

        print("Most popular hour:{}, Count:{}, Filter:{}".format(most_common_start_hour, count_most_common_start_hour , filter)) 
        print("Most popular day of week:{}, Count:{}, Filter:{}".format(most_common_day_of_week, count_most_common_day_of_week , filter))  

    elif filter == 'none':
        # count number of most popular week of day and month
        count_most_common_day_of_week = len(df[df['start_day_of_week'] == most_common_day_of_week])
        count_most_common_month = len(df[df['start_month'] == most_common_month])

        print("Most popular hour:{}, Count:{}, Filter:{}".format(most_common_start_hour, count_most_common_start_hour , filter)) 
        print("Most popular day of week:{}, Count:{}, Filter:{}".format(most_common_day_of_week, count_most_common_day_of_week , filter))  
        print("Most popular month:{}, Count:{}, Filter:{}".format(most_common_month, count_most_common_month , filter))    


    print("This took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # get most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]

    # count number of most popular start station
    count_most_common_start_station = len(df[df['Start Station'] == most_common_start_station])

    # get most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]

    # count number of most popular end station
    count_most_common_end_station = len(df[df['End Station'] == most_common_end_station])


    # display most commonly used start station, end station
    print(f"""Start Station:{most_common_start_station}, Count:{count_most_common_start_station} - 
    End Station:{most_common_end_station}, Count:{count_most_common_end_station}, 
    Filter:{filter}""")


    # get most frequent combination of start station and end station trip
    most_frequent_trip = df['trip'].mode()[0]

    # count number of most frequent combination of start station and end station trip
    count_most_frequent_trip = len(df[df['trip'] == most_frequent_trip])

    # display most frequent combination of start station and end station trip
    print("Most popular trip:('{}'), Count:{}, Filter:{}".format(most_frequent_trip, count_most_frequent_trip , filter))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...')
    start_time = time.time()

    # display total and mean travel time
    total_travel_time = df['Trip Duration'].sum()
    avg_travel_time = df['Trip Duration'].mean()
    count_travel_time = len(df['Trip Duration']) 

    day, hour, minutes, seconds = seconds_to_days(total_travel_time)
    total_travel_time_in_days = '{} Day(s), {} Hour(s), {} Minute(s) , {} Second(s)'.format(day, hour, minutes, seconds)
    day, hour, minutes, seconds = seconds_to_days(avg_travel_time)
    avg_travel_time_in_days = '{} Day(s), {} Hour(s), {} Minute(s) , {} Second(s)'.format(day, hour, minutes, seconds)

    print('Total Duration:{} sec ({}), Count:{}, Avg Duration:{} sec ({}), Filter:{}\n'.format(
        total_travel_time , 
        total_travel_time_in_days, 
        count_travel_time, 
        avg_travel_time,
        avg_travel_time_in_days, 
        filter))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    count_subscriber_users = len(df[df['User Type'] == 'Subscriber'])
    count_customer_users = len(df[df['User Type'] == 'Customer'])

    print('Number of Subscribers:{}, Number of Customers:{}, Filter:{}'.format(count_subscriber_users, count_customer_users, filter))


    # Display counts of gender
    if 'Gender' in df.columns:
        count_male_gender = len(df[df['Gender']  == 'Male'])
        count_female_gender = len(df[df['Gender']  == 'Female'])
        print('Number of Male:{}, Number of Female:{}, Filter:{}'.format(count_male_gender, count_female_gender, filter))


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year_of_birth = df['Birth Year'].dropna().min()
        most_recent_year_of_birth = df['Birth Year'].dropna().max()
        most_common_year_of_birth = df['Birth Year'].dropna().mode()[0]
        count_most_common_year_of_birth = len(df[df['Birth Year'] == most_common_year_of_birth])

        print('Earliest year of birth:{}, Most recent year of birth:{},Most recent year of birth:{} , Count:{}, Filter:{}'.format(
            earliest_year_of_birth, 
            most_recent_year_of_birth, 
            most_common_year_of_birth,
            count_most_common_year_of_birth,
            filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """
    Asks user to display raw data and print 5 rows at time
    """
    index = 0
    while True:
        try:
            data = input('Would you like to view individual trip Data? Type \'yes\' or \'no\'. \n').strip().lower()
            if data == 'yes':
                if index + 5 > len(df):
                    records = df.iloc[index:len(df)-1]
                    pprint.pprint(records.to_dict(orient='records'))
                    print('no more records available') 
                else :
                    records = df.iloc[index:index + 5]
                    pprint.pprint(records.to_dict(orient='records'))
                    index += 5
            elif data == 'no':
                break
            else :
                print('Invalid answer try again. Type \'yes\' or \'no\'  \n')
        except:
            print('Invalid answer try again. Type \'yes\' or \'no\'  \n')

def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, filter)
        station_stats(df, filter)
        trip_duration_stats(df, filter)
        user_stats(df, filter)
        display_raw_data(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
            if restart == 'no':
                sys.exit()
            elif restart == 'yes':
                break
            else:
                print('\nInvalid answer try again. Type \'yes\' or \'no\'  \n')


if __name__ == "__main__":
	main()