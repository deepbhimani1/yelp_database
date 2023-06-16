Deep Bhimani (301468915) - CMPT 354 Assignment 7

Requirements:
1) Python 3.x
2) pymssql library
3) Tkinter library

Overview of the program:
Yelp database application 
This python application has a login page, two options of either searching a business or a user with filters wih options of making a friend and writing a review

How to Use:
1) gather all the required things
2) run the main.py file by typing "python main.py" in the terminal (after make sure it is connected to the database)
3) have a valid login_id from the database (an example id is given in the code's comments)
4) click on either search business or search user buttons
5) either apply any filter or simply click search where the results will apear
6) if you wish, you could make a friend or leave a review by double clicking on it
7) once done you can always head to the back page with the back button or exit by clicking the exit key on the top right of the window

Functionality pages (GUI):
1) login page:
    - have a valid user_id from the database to log in
    - a appropriate textbox message will apear if you fail or succeed
    - once succeeded it will take you to the second page

2) Second page
    - text on top of the page will say "you have logged in"
    - total of 3 buttons search business, search users, back all three will redirect you to appropriate pages

3) Search business page:
    - it will have 3 filters: (name and city as textbox) and (stars with a dropdown menu with either min or max stars)
    - filters are optional and filters are not case sensitive
    - a search button is provided, once clicked the results table with appropriate columns will aprear with a scroll menu
    - a text saying "you can double click to make a review" will aprear as well
    - once double clicked if wanted, a text box asking for rating will apear.
    - the rating textbox will show error if values are not between 1-5 or not given, will show success otherwise
    - at the bottom of the page back button is present which will take the user to the second page

4) Search user page:
    - it will have 4 filters: (name as textbox) and (funny,cool,and useful with a dropdown menu with either yes or no)
    - filters are optional and filters are not case sensitive
    - a search button is provided, once clicked the results table with appropriate columns will aprear with a scroll menu
    - a text saying "you can double click to make a friend" will aprear as well
    - once double clicked on a user if wanted, then a textbox conforming it would apear likewise
    - at the bottom of the page back button is present which will take the user to the second page