

Requirements and installations:
1. Download nodejs:
   https://nodejs.org/en/download/
2. install node through visual studio code terminal:
   npm install -g @angular/cli
3. From the zip file present:
   unzip and upload complete folder to VS Code
4. Now download sqlite extension in VS CODE. Then ctrl+shift+p opens a search bar, Then open "opensqlite database".
5. In files section, this oepns SQLITE EXPLORER at the bottom: where all tables can be seen.
4. Run these commands in VS Code terminal: ng serve
   on running this command a local host url is popped up, copy the url and paste it in the browser. 
5. Open a new terminal and run python3 app.py ( this is the backend code running ).
6. Now go the browser and in local host url we can see the app running: 
   Options:
    step1: register the user, provide details. These details are added to users table which can be seen in SQLITE EXPLORER.
    step2: Login with the details provided during registration.
    step3: New page has two options 1. To add review and view menu item details. ( select restaurant, select menu item and add review)
                                          (Added reviews are stored in reviews table and sentiment column will be null)
                                    2. To view ratings ( select menu item, provides top restaurants in order where thismenu item is rated highly).

Backend steps to run the model and update ratings in the table:

1. Reviews table has all the training data and testing data.
2. Run logistic_model.py, this takes data from reviews table for training and predict sentiment on new reviews added through frontend.
3. Then run update_ratings.py, this fill newly calculated ratings in restaurant and menu_item tables.
4. Now tables are ready and ratings(new restaurant recommendations) for second option gets pulled from these tables.Refer code for more details.
