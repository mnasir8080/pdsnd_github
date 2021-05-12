#Adding this for the reviwer to see title in commit
import time
import pandas as pd
import numpy as np

#Array declearations
#and assignment od values
#added for refactoring
#added for refactoring 2
CITY_DATA = { 'chicago': 'chicago.csv', 'new york': 'new_york_city.csv', 'washington': 'washington.csv' }
cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    #Asks user to specify which city, month or day to analyze.
    #Returns:  (str) city - name of the city to analyze, month - name of the month to filter and day - name of the day of week to filter
    print("Initiating US bikeshare data")   
    # Get the city the user wants to analyse. 
    while True:
        city =input("Please type one from the following cities for analysis:\nChicago, New York or Washington\n").lower()
        if city in cities:
            break
        else:
            city =input("Wrong selection, Please type one from the following cities below for analysis:\nChicago, New York or Washington\n").lower()          
    # Get how user wants to filter data.
    while True:
        choice = input("Type how you want the data fitered; month or day\n").lower()
        if choice == 'month':
            month = input("Please enter the month you want to explore. \nChoices: January, February, March, April, May, June\n").lower()
            day = 'All Days'
            if month in months:
                break
            else:
                month = input("Error: Please enter the month you want to explore. \nChoices: January, February, March, April, May, June\n").lower()
        elif choice == 'day':
            day = input("Please enter the day of the week you want to explore.'. \nChoices:Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()
            month = 'All Months'
            if day in days:
                break
            else:
                print('Please enter a valid day')
                day = input("Please enter the day of the week you want to explore. \nChoices: All, Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday\n").lower()
    print('..'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
        (str) city - name of the city to analyze, month - name of the month to filter by, or "all" to apply no month filter and day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])     # Load data file into a dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time']) # Convert the Start Time column to datetime
    df['month'] = df['Start Time'].dt.month # Extract month from Start Time to create new columns
    df['day_of_week'] = df['Start Time'].dt.weekday_name #day of week from Start Time to create new columns

    # Filter by month if applicable
    if month == 'month':     
        months = ['january', 'february', 'march', 'april', 'may', 'june'] # Use the index of the months list to get the integer value
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # Filter by day of week if applicable
    if day == 'day': 
        df = df[df['day_of_week'] == day.title()]  # Filter by day of week to create the new dataframe
    return df

#Print statistics on the most frequent times of travel.
def time_stats(df):
    print('\nCalculating The Most frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month     # Extract month from start time column to create month column 
    pPmonth = df['month'].mode()[0]   
    #convert the int values to months
    if pPmonth == 1:
        pPmonth = "January"
    elif pPmonth == 2:
        pPmonth = "February"
    elif pPmonth == 3:
        pPmonth = "March"
    elif pPmonth == 4:
        pPmonth = "April"
    elif pPmonth == 5:
        pPmonth = "May"
    elif pPmonth == 6:
        pPmonth = "June"
    print('Most Frequent Month: ', pPmonth)
    pPday = df['day_of_week'].mode()[0] 
    print('Most Common Day of the Week: ', pPday)    # Display the most common day of the week after start time has been extracted to make day info
    df['hour'] = df['Start Time'].dt.hour 
    pPhour = df['hour'].mode()[0] 
    if pPhour < 12:
        print('Most Common Start Hour: ', pPhour, 'AM')
    elif pPhour >= 12:
        if pPhour > 12:
            pPhour -= 12
        print('Most Common Start Hour: ', pPhour, 'PM')
    print("This took %s seconds." % (time.time() - start_time))
    print('..'*20)

#Printing statistics on the most popular stations and trip for bikeshare users.
def station_stats(df):
        print('Calculating The Most Popular Stations and Trip\n')
        start_time = time.time()
        pSstation = df['Start Station'].mode()[0] # most common starting station
        pEstation = df['End Station'].mode()[0] #Mostcommon End station
        pCstation = df['Start Station'] + " to " +  df['End Station'] #Frequently combine start and end stations
        cpCstation = pCstation.mode()[0]
        print("Most Common Start Station: ", pSstation, "\nMost Common End Station: ", pEstation, "\nMost Common Trip from Start to End: {}".format(cpCstation))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('..'*20)

    #Printing statistics for all bikeshare users.
def user_stats(df, city):
    print('Calculating User Statistics\n')
    start_time = time.time()
    print("Counts of Each User Type:\n", df['User Type'].value_counts()) # Display counts of gender  
    try:
        print('..' * 20)
        print('Counts of Each User Gender:\n', df['Gender'].value_counts())
    except:
        print('Error, gender not available on count for each user for {} City'.format(city.title()))
    # Display earliest, most recent, and most common year of birth
    try:
        comm = df['Birth Year'].mode() 
        erl = df['Birth Year'].min() 
        rct = df['Birth Year'].max() 
        print('..' * 20)
        print('Counts for User Birth per Year:')
        print('..' * 20)
        print('Oldest Birth Year of User: ', int(erl), '\nYoungest Birth Year of users: ', int(rct), '\nThe most Common Birth Year: ', int(comm))
    except:
        print('Count analysis for Users Birth Year data not available for {} City'.format(city.title()))
    print("\nAnalysis took %s seconds." % (time.time() - start_time))
    print('..'*20)


#Analysis for total and average trip duration
def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # print total travel time
    tTtime = df['Trip Duration'].sum()
    tTtime = (str(int(tTtime//86400)) +
                         'd ' +  str(int((tTtime % 86400)//3600)) +
                         'h ' +  str(int(((tTtime % 86400) % 3600)//60)) +
                         'm ' +  str(int(((tTtime % 86400) % 3600) % 60)) + 's')
    print('For the selected filters, the total travel time is : ' + tTtime + '.')  
    mTtime = df['Trip Duration'].mean()# display mean travel time all
    mTtime = (str(int(mTtime//60)) + 'm ' + str(int(mTtime % 60)) + 's')
    print("For the selected filters, the mean travel time is : " +  mTtime + ".")
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('..'*20)

# individual trip data after a user has been asked and confirmed
def individual_data(df):
    sdata = 0
    edata = 10
    dfLength = len(df.index)  
    while sdata < dfLength:
        responce = input("\nWould you like to see individual trip data? Enter 'Y' or 'N'.\n").lower()
        if responce == 'y':
            print("\nDisplaying only 10 rows of data per view.\n")
            if edata > dfLength:
                edata = dfLength
            print(df.iloc[sdata:edata])
            sdata += 10
            edata += 10
        else:
            break
                    
def main():
    while True:
        city, month, day = get_filters()
        print("Printing Analysis for {}, {}, and {}.".format(city.title(), month.title(), day.title()))
        df = load_data(city, month, day)
       # print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input("\nWould you like to restart analysis? Enter y or n.\n")
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
    main()
