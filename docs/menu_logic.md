# Menu 0:
>Welcome to Weather Scraper App!<br>
There are following year(s) weather data in the database:<br>
[1996,1997,1998…2020]<br>

>What do you want to do?<br>
1.Fetch all new data from the website.<br>
2.Update data between today and the latest date in the database.<br>
3.Generate a plot.<br>
4.Exit<br>
Please input the number of the options[1,2,3]:__

# Menu 0.1:
>Are you sure you want to fetch all new data from the website?<br>
>It will take several minutes [Y/N] : __

# Menu 0.1.1:
>Fetching all new data from the website. It will take several minutes...<br>
Scraping data of year: 2020, month: 1...<br>
Scraping data of year: 2020, month: 2...<br>
Scraping data of year: 2020, month: 2...<br>
...<br>
Purging all the data from the database...<br>
Database is updating...<br>
Database is updated.<br>
> 
{Go back to Menu 0}

# Menu 0.2:
>The last day in the database is:<br>
[2020-12-01]<br>
Fetching the missing data from the website...<br>
Scraping data of year: 2020, month: 12...<br>
Database is updating...<br>
Database is updated.<br>

{Go back to Menu 0}

# Menu 0.3:
>What the kind of plots you want?<br>
1.Generate a BOX PLOT between a year range.<br>
2.Generate a LINE PLOT for an assigned month.<br>
3.Return to main menu.<br>
4.Exit<br>
> Please input the number of the options[1,2,3,4]:__

# Menu 0.3.1
>You are trying to generate a BOX PLOT between a year range:<br>
Enter the start year[between 1996-2020]:_2020_<br>
Enter the end year[between 1996-2020]:_2015_<br>

If **end year** is less that **start year**, they are switched automatically.

>Error: Sorry, your input is not validated, please try again.<br>

>Generate a BOX PLOT between years [2015-2020]...<br>
 
{Go back to Menu 0.3}

# Menu 0.3.2
>You are trying to generate a LINE PLOT for an assigned month:<br>
Enter the year[between 1996-2020]:_2020_<br>
Enter the month[between 1-12]:_12_<br>

>Error: Sorry, your input is not validated, please try again.<br>
Error: Sorry, there in no weather data in the database for [year:1996, month:1]<br>

>Generate a LINE PLOT [year:2020, month:12]...<br>

{Go back to Menu 0.3}<br>
