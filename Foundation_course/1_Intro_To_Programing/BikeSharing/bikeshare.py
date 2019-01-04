import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    cities = ('chicago','new york city','washington')
    months = ('january','february','march','april','may','june','all')
    days = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all')
    print('Hello! Let\'s explore some US bikeshare data!')
    invalidCity = True
    invalidMonth = True
    invalidDay = True
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while invalidCity:
        city = input('Enter one of the following city names (Chicago / New York City / Washington) : ')
        invalidCity = not (city.lower() in cities)
        if(invalidCity):
            print ('Invalid city name selected !')
        city = city.lower()
        
    while invalidMonth:
        month = input('Enter month for which you want to filter(January .... June ), or "all" for no filter : ')
        invalidMonth = not (month.lower() in months)
        if (invalidMonth):
            print ('Invalid month selected !')
        month = month.lower()    

    while invalidDay:
        day = input('Enter day for which you want to filter(Monday .... Sunday ), or "all" for no filter : ')
        invalidDay = not (day.lower() in days)
        if (invalidDay):
            print ('Invalid day selected !')
        day = day.lower()  
        
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
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.strftime('%B')
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost Common Month of travel:')
    print (df['month'].mode()[0])


    # display the most common day of week
    print('\nMost Common day of week for travel:')
    print (df['day_of_week'].mode()[0])

    # display the most common start hour
    print('\nMost common hour of travel:')
    print (df['Start Time'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost Commonly used Start Station')
    print (df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nMost Commonly used End Station')
    print (df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    print ('\nMost frequent combination of start station and end station trip')
    trip_frequency = df.groupby(['Start Station','End Station']).size().reset_index(name="trips");
    print (trip_frequency[trip_frequency['trips'] == trip_frequency['trips'].max()])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print ('\nTotal Travel Time: ')
    secs = df['Trip Duration'].sum().astype(float)
    data = str(datetime.timedelta(seconds=secs))
    print ('Days: ',data.split(',')[0])
    print ('Hours: ',(data.split(',')[1]).split(':')[0])
    print ('Minutes: ',(data.split(',')[1]).split(':')[1])
    print ('Seconds: ',(data.split(',')[1]).split(':')[2])


    # display mean travel time
    print ('\nMean Travel Time: ')
    secs = df['Trip Duration'].mean()
    mins = (secs/60).astype(int)
    print ('Minutes: ', mins)
    print ('Seconds: ', (secs - (mins * 60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print ('\nCalculating count of each User Types:')
    print (df['User Type'].value_counts())

    # Display counts of gender
    print ('\nCalculating count of each Gender:')
    if 'Gender' in df.columns:
        print (df['Gender'].value_counts())
    else:
        print ('No "Gender" data available for this filter')

    # Display earliest, most recent, and most common year of birth
    print ('\nCalculating Birth Year stats:')
    if 'Birth Year' in df.columns:
        print ('\nMost common year of birth:')
        print (df['Birth Year'].mode()[0].astype(int))
        
        print ('\nMost recent Year of Birth:')
        print (df['Birth Year'].max().astype(int))
        
        print ('\nMost earliest Year of Birth:')
        print (df['Birth Year'].min().astype(int))
    else:
        print ('No "Birth Year available for this filter"')
      
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        data_fetch_counter = 0
        df = load_data(city, month, day)
        print (df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            show_more_data = input('\n Would you like to see 5 data at time ? Enter yes or no.\n')
            if show_more_data.lower() == 'no':
                break
            else:
                for line in range (data_fetch_counter,data_fetch_counter+5):
                    try:
                        print (df.iloc[line])
                        print('-'*40)
                    except IndexError:
                        print ('--------- No More Data to show ----------')
                        break
                data_fetch_counter = data_fetch_counter + 5
            

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
