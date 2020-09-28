import time
import pandas as pd
import numpy as np
from scipy import stats


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }



months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    try:
        city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()
        while city not in CITY_DATA:
            print('Sorry! You must enter either Chicago, New York or Washington. Try again!: ')
            city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()


        month = input('Which month would you like to look at? (January-June, or all?): ').lower()
        while month not in months:
            print('Sorry! You must enter a valid month between January-June, or all. Try again!')
            month = input('Which month would you like to look at? (January-June, or all?): ').lower()


        day = input('Which day you would like to look at? (Monday-Sunday, or all?: ').lower()
        while day not in days:
            print('Sorry! You must enter a valid day (Monday-Sunday, or all): ')
            day = input('Which day you would like to look at? (Monday-Sunday, or all?: ').lower()

        return city, month, day

    except Exception as e:
        print('Cannot compute from given inputs. Error: {}'.format(e))
    print('-'*40)


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
    try:
        #convert to datetime in order to be able to sort and filter through the DataFrame
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])
        df['month'] = df['Start Time'].dt.month
        df['day'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour

        if month != 'all': #if user chooses a month, filter DataFrame with given month
            months_list = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months_list.index(month) + 1

            df = df[df['month'] == month]

        if day != 'all': #if user chooses a day, filter DataFrame with given day
            df = df[df['day'] == day.title()]
        return df
    except Exception as e:
        print('Cannot load. Error: {}'.format(e))

def time_stats(df, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #find the month number and name that appears the most in the Start Time column in the DataFrame
    try:
        most_common_month_num = df['Start Time'].dt.month.mode()[0]
        most_common_month_name = months[most_common_month_num-1].title()
        print('Most common month to rent bikes in ', city, ': ', most_common_month_name)
    except Exception as e:
        print('Cannot find most common month. Error: {}'.format(e))

    #find the day that appears the most in the Start Time column in the DataFrame
    try:
        most_common_day = df['day'].mode()[0]
        print('Most common day to rent bikes in ', city, ' is: ', most_common_day)
    except Exception as e:
        print('Cannot find most common day. Error: {}'.format(e))


    #find the hour that appears the most in the Start Time column in the DataFrame
    try:
        most_common_hour = df['hour'].mode()[0]
        print('Most common hour to rent bikes in ', city, ' is: ', most_common_hour)
    except Exception as e:
        print('Cannot find most common hour. Error: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #find the most common start station that bikers use by sorting through the Start Station column in the df
    try:
        most_common_start_station = df['Start Station'].mode()[0]
        most_common_start_station_count = df['Start Station'].value_counts()[0]
        print('Most common start station in ', city, ' is: ', most_common_start_station, '\n', most_common_start_station, 'was used: ', most_common_start_station_count, ' times')

    except Exception as e:
        print('Cannot find most common start station. Error: {}'.format(e))

    #find the most common end station that bikers use by sorting through the End Station column in the df
    try:
        most_common_end_station = df['End Station'].mode()[0]
        most_common_end_station_count = df['End Station'].value_counts()[0]
        print('Most common end station in ', city, ' is: ', most_common_end_station, '\n', most_common_end_station, 'was used: ', most_common_end_station_count, ' times')

    except Exception as e:
        print('Cannot find most common end station. Error: {}'.format(e))

    #find the most common route bikers follow by looking at Start to End Stations and finding the most common routes in the df
    try:
        most_common_route = df.loc[:, 'Start Station':'End Station'].mode()[0:]
        most_common_route_count = df.groupby(["Start Station", "End Station"]).size().max()
        print('Most common route in ', city, ' is: ',most_common_route, '\n', most_common_route, 'was used: ', most_common_route_count, ' times')

    except Exception as e:
        print('Cannot find most common route. Error: {}'.format(e))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #find the duration by creating a new column of the difference of End Time and Start Time from the df
    try:
        df['Duration'] = df['End Time'] - df['Start Time']
        total_duration = df['Duration'].sum()
        print('Total duration: ', total_duration)

    except Exeption as e:
        print('Cannot find total duration. Error: {}'.format(e))

    #find the average duration by simply taking the mean of the new Duration column in the df
    try:
        average_duration = df['Duration'].mean()
        print('Mean duration: ', average_duration)

    except Exception as e:
        print('Cannot find mean duration. Error: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #find the count of user types from the User Type column in the df
    try:
        print('Count and types of users in ', city, ': ', df['User Type'].value_counts())

    except Execption as e:
        print('Cannot find count and types of users. Error: {}'.format(e))

    #find the count of each gender from the Gender columns in the df
    try:
        print('Count and genders of users in ', city, ': ', df['Gender'].value_counts())

    except Exception as e:
        print('Cannot find count and genders of users. Error: {}'.format(e))

     #find the earliest, most recent, and most common birth year from of the Birth Year column in the df
    try:
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()
        print('Oldest user in ', city, 'born in: ', int(earliest_yob), '\n Youngest user in ', city, 'born in: ', int(most_recent_yob),'\n Most common birth year: ', int(most_common_yob))

    except Exception as e:
        print('Cannot find earliest birth year, most recent birth year, or most common birth year. Error: {}'.format(e))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df, city):

    count = 0
    answer = input('Would you like to see 5 lines of raw data? Enter yes or no: ').lower()
    while True:
        if answer == 'yes':
            print(df[count: count + 5])
            count += 5
        else:
            break
        answer = input("Would you like to see five more lines of raw data? Enter yes or no").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df, city)
        raw_data(df, city)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
