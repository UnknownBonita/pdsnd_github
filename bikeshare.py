import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january':1,'february':2, 
          'march':3,'april':4, 
          'may':5,'june':6}

DAYS = {'sunday':1,'monday':2, 
        'tuesday':3, 'wednesday':4, 
        'thursday:':5, 'friday':6, 
        'saturday':7}

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
    while True:
        city = input('Enter the name of the city you want to explore:\n \t-Chicago\t-New York City\t-Washington\n  Your choice: ')
        city = city.lower()
        if city in CITY_DATA.keys():
            break;
        else:
            print('Error! Invalid choice. Please Try Again..\n')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Enter the month you want to explore(January-June): ')
        month = month.lower()
        if month in MONTHS.keys() or month == 'all':
            break;
        else:
            print('Error! Invalid choice. Please Try Again..\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the name of the day you want to explore: ')
        day = day.lower()
        if day in DAYS.keys() or day == 'all':
            break;
        else:
            print('Error! Invalid choice. Please Try Again..\n')
    
    print('\nSelected attributes:\n\t City: {} \n\t Month: {} \n\t Day: {}'.format(city.title(),month.title(),day.title()))
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
    # load data
    print('Loading Data..')
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time and End Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day from Start Time
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.dayofweek

    if month != 'all':
        month = MONTHS[month]
        df = df[df['Month'] == month]
        
    if day != 'all':
        day = DAYS[day]
        df = df[df['Day'] == day]
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month= df['Month'].mode()[0]
    month_name = [key for key, value in MONTHS.items() if value == common_month]
    print('Most popular month: {}'.format(''.join(month_name).title()))

    # display the most common day of week
    common_day= df['Day'].mode()[0]
    day_name = [key for key, value in DAYS.items() if value == common_day]
    print('Most popular day: {}'.format(''.join(day_name).title()))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    common_startHour= df['Hour'].mode()[0]
    print('Most popular start hour: {}'.format(common_startHour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startStation = df['Start Station'].mode()[0]
    print('Most popular start station: {}'.format(common_startStation))
    
    # display most commonly used end station
    common_endStation = df['End Station'].mode()[0]
    print('Most popular end station: {}'.format(common_endStation))

    # display most frequent combination of start station and end station trip
    common_stationComb = df[['Start Station','End Station']].mode().loc[0]
    print('Most popular Combination of start station and end station: {}, {}'.format(common_stationComb[0],common_stationComb[1]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    sum_tripDur = df['Trip Duration'].sum()
    print('Total travel time: {}'.format(sum_tripDur))
    
    # display mean travel time
    avg_tripDur = df['Trip Duration'].mean()
    print('Average travel time: {}'.format(avg_tripDur))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    users = df['User Type'].value_counts()
    print('Count of user types:')
    print('Subscriber    : {}\nCustomer      : {}'.format(users[0],users[1]))
    
    try:
        # Display counts of gender
        print('\nCount of genders:')
        genders = df['Gender'].value_counts()
        print('Male      :{}\nFemale    :{}'.format(genders[0],genders[1]))
    except:
        print('\tThere is no \'Gender\' insights.')
        
    try:
        # Display earliest, most recent, and most common year of birth
        print('\nBirth Year insights:')
        earliest_birthYear = df['Birth Year'].min()
        recent_birthYear = df['Birth Year'].max()
        common_birthYear = df['Birth Year'].mode()[0]
        print('\nEarliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Year of Birth: {}'.format(earliest_birthYear,recent_birthYear,common_birthYear))
    except:
            print('\tThere is no \'Birth Year\' insights.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks user if it want to display raw data

    Returns:
        (dataframe) df - 5 rows of the specified city, day, and month.
    """
    counter = 0
    while True:
        display_data = input('Would you like to display 5 rows of data? Enter yes or no: ')
        if display_data.lower() != 'yes':
            break
        else:
            pd.set_option('display.max_columns',200)
            print(df.iloc[counter:counter+5])
            counter += 5
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
