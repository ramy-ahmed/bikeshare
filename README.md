## Bike Share Data

## The Datasets

Randomly selected data for the first six months of 2017 are provided for all three cities. All three of the data files contain the same core six (6) columns:

- Start Time (e.g., 2017-01-01 00:07:57)
- End Time (e.g., 2017-01-01 00:20:53)
- Trip Duration (in seconds - e.g., 776)
- Start Station (e.g., Broadway & Barry Ave)
- End Station (e.g., Sedgwick St & North Ave)
- User Type (Subscriber or Customer)

The Chicago and New York City files also have the following two columns:

- Gender
- Birth Year

## Statistics Computed

You will learn about bike share use in Chicago, New York City, and Washington by computing a variety of descriptive statistics. In this project, you'll write code to provide the following information:

### 1 Popular times of travel (i.e., occurs most often in the start time)

- most common month
- most common day of week
- most common hour of day

### 2 Popular stations and trip

- most common start station
- most common end station
- most common trip from start to end (i.e., most frequent combination of start station and end station)

### 3 Trip duration

- total travel time
- average travel time

### 4 User info

- counts of each user type
- counts of each gender (only available for NYC and Chicago)
- earliest, most recent, most common year of birth (only available for NYC and Chicago)

## How to run this project?

You will need to have csv data files called (chicago.csv,
new_york_city.csv,
washington.csv)

This project is depending on conda, you have to have a [conda installed](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) 

```
conda env create --file bikeshare_env.yml
```

```
conda activate bikeshare_env
```

```
python bikeshare.py
```