import time
import pandas as pd
import numpy as np

#This a comment about a change for the 3rd project

#Creating a dictionary containing the data from the csv files of Chicago, New York City and Washington
CITY_DATA = { 'chicago': 'chicago.csv', 'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv', 'New york city': 'new_york_city.csv',
              'new york city': 'new_york_city.csv', 'washington': 'washington.csv',
             'Washington': 'washington.csv' }

#Filtering function
def get_filters():
    """
    Asks the user to specify a city, month and day. It takes no arguments and it returns
    the following:
        the name of the city to analyze
        either the name of the month selected by the user or "all" if all months are selected
        either the name of the day selected by the user or "all" if all days are selected
    """
    print('Welcome! Check out some interesting bikeshare data from 3 cities in the USA!')
    #Initializing an empty city variable to store city choice from user
    city = ''
    #Running this loop to ensure that the user entered the correct input
    while city not in CITY_DATA.keys():
        print("\nWhich city's data would you like to explore?")
        print("\n1. Chicago 2. New York City 3. Washington")
        print("\nPlease, type the city below:")
        #Taking user's input and converting into lower to standardize them
        city = input().lower()

        if city not in CITY_DATA.keys():
            print("\nPlease, select one of the afformentioned cities.")
            print("\nInitializing...")

    print(f"\nLet\'s see some bikeshare data for {city.title()}.")

    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month, between January to June, that is of your interest:")
        print("\n(If you would like to see data for all months, please type 'all'.)")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("\nPlease select one of the afformentioned months.")
            print("\nInitializing...")

    print(f"\nData for {month.title()} are loaded.")

    #Creating a dictionary to store all the days including the 'all' option
    DAY_DATA = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7, 'all': 8}
    day = ''
    while day not in DAY_DATA.keys():
        print("\nPlease, enter a day of the week or type 'all' to see data for the whole month:")
        day = input().lower()

        if day not in DAY_DATA.keys():
            print("\nPlease select a day of the week.")
            print("\nInitializing...")

    print(f"\nBikeshare data for {day.title()} in {month.title()} in {city.title()} are loaded.")
    print('-'*80)
    #Returning the city, month and day that the user selected
    return city, month, day

#Function to load data from .csv files
def load_data(city, month, day):
    """
    Loads data for the selected city and filters by month and day. Take as arguments the city, the month and the day and
    returns a dataframe wontaing the the data for the selected city, month and day.
    """
    #Loading data for the selected city
    print("\nPlease wait, magic in progress...")
    df = pd.read_csv(CITY_DATA[city])

    #Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Extracting month and day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day

    #Filtering by month if the user selected a specific month
    if month != 'all':
        #Using the index of the months list to get the corresponding integer for month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Creating the new dataframe
        df = df[df['month'] == month]

    #Filtering by day if the user selected a specific day
    if day != 'all':
        #Using the index of the days list to get the corresponding integer for day
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        
        #Creating the new dataframe
        df = df[df['day_of_week'] == day]

    #Returns the dataframe that was created, with the relevant columns
    return df

#Function to calculate time-related stats for the selected data
def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nWhen do people bikeshare the most?\n')
    start_time = time.time()

    #Mode method to find the most popular month
    popular_month = df['month'].mode()[0]

    print(f"The most popular month is: {popular_month}. (1 = January,...,6 = June)")

    #Mode method to find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nThe most popular day is: {popular_day}")

    #Creating an column for the hour
    df['hour'] = df['Start Time'].dt.hour

    #Mode method to find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print(f"\nThe most popular starting hour of the day is: {popular_hour}")

    #Printing the time needed to perform the calculation
    print('-'*100)
    print(f"\nThis magic happened in just round({(time.time() - start_time)}, 2) seconds!")
    print('*'*100)

#Function to calculate station related stats
def station_stats(df):
    """Displays statistics on the most popular stations and trip. Takes as argument the dataframe that we will work with and
    returns nothing.
    """

    print('\nWhich are the most used Stations and Trips?\n')
    start_time = time.time()

    #Mode method to find the most common start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station is: {common_start_station}")

    #Mode method to find the most common end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station is: {common_end_station}")

    #Combining two columns in the dataframe with str.cat
    #Assigning the result to a column named 'Start To End'
    #Finding out the most common combination of start and end stations by using mode method on the new column
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print('-'*100)
    print(f"\nThis magic happened in just {(time.time() - start_time)} seconds.")
    print('*'*100)

#Function for trip duration related stats
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration. Takes as argument the dataframe that we will work with and
    returns nothing.
    """

    print('\nHow much do the trips take?\n')
    start_time = time.time()

    #Sum method to calculate the total trip duration
    total_duration = df['Trip Duration'].sum()
    #Finding out the duration in minutes and seconds
    minute, second = divmod(total_duration, 60)
    #Finding out the duration in hour and minutes
    hour, minute = divmod(minute, 60)
    print(f"The total duration of the trips is {hour} hours, {minute} minutes and {second} seconds.")

    #Calculating the average trip duration using mean method
    average_duration = round(df['Trip Duration'].mean())
    #Finding the average duration in minutes and seconds
    mins, sec = divmod(average_duration, 60)
    #Printing the time in hours, minutes, seconds format if the minutes are over 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average duration of a trip is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average duration of a trip is {mins} minutes and {sec} seconds.")
    
    print('-'*100)
    print(f"\nThis magic happened in just {(time.time() - start_time)} seconds.")
    print('*'*100)

#Function to calculate user stats
def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None.
    """

    print('\nBelow you can see some data regarding the users of bikesharing.\n')
    start_time = time.time()

    #Counting the total users using value_counts method
    #Then they are displayed by their type
    user_type = df['User Type'].value_counts()

    print(f"Subscribers vs Customers:\n\n{user_type}")

    #Displaying the number of users by Gender, if there is a gender column in the dataframe, by using the try clause
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe gender of the users:\n\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

    #Similarly, for birth years
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe oldest users were born in year {earliest}\n\nThe youngest users were born in year {recent}\n\nThe year in which most users were born was {common_year}")
    except:
        print("There are no birth year details in this file.")
    
    print('-'*100)
    print(f"\nThis magic happened in {(time.time() - start_time)} seconds.")
    print('*'*100)

#Function to display the data frame if the user selects to
def display_data(df):
    """Displays 5 rows of data from the csv file for the selected city. Takes as argument the respective dataframe
    and returns nothing.
    """
    BIN_RESPONSE_LIST = ['yes', 'no']
    rdata = ''
    #counter variable is initialized as a tag to ensure only details from
    #a particular point is displayed
    counter = 0
    while rdata not in BIN_RESPONSE_LIST:
        print("\nWould you like to view some of the data?")
        print("\nType Yes or No, below:")
        rdata = input().lower()
        #the raw data from the df is displayed if user opts for it
        if rdata == "yes":
            print(df.head())
        elif rdata not in BIN_RESPONSE_LIST:
            print("\nPlease check your input.")
            print("You should type Yes or No.")
            print("\nInitializing...\n")

    #A while loop to ask the user if they want more data
    while rdata == 'yes':
        print("Would you like some more data?")
        counter += 5
        rdata = input().lower()
        #If user opts in, they get 5 more rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

    print('-'*100)

#Main function to restart the process
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Type yes or no, below:\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
