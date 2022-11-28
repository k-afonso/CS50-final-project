# iShare
#### Video Demo:  https://youtu.be/RrgRXqMzYM8
#### Description:


## **Final Project CS50**

First and foremost, I wanted to thank the CS50 team for this amazing course. I started this course as an absolute beginner with no previous experience in any programming language.

This course helped starting thinking like a programmer and see Computer Science as beautiful field.

<br/><br/>

## **Introduction**

For my final project, I really wanted to do something that integrates most of what I've learned in CS50. I decided to create a web application because it includes **HTML, CSS, Python, SQL, and more**.

I had multiple ideas for this project but I finally settled on creating a website where people can share their unused items with people who need them for a short time. 

<br/>

### **- Why this project?**

This idea has always been in the back of my mind because I like doing small projects and I often find myself forced to buy tools that I only needed for a project and are now just collecting dust. I am sure that I am not the only one in this situation. 

**Would it be possible to borrow a drill machine for 30 minutes just to put up that shelf? Or a car jack for 2 hours to change the car oil? A sewing machine just to fix a tear in the jeans?** This would make life so much easier for a lot of people.

I decided to create **iShare**, a platform where people can share their collecting dust items with people that actually need them for a small period of time. 

<br/>

### **- Action Plan**

After deciding on the subject of my project, it was time to create a blueprint of what I wanted the web application to look like.

I quickly realized that this application was going to be harder than I initially thought and I would need a practical plan of attack, otherwise I would feel overwhelmed in no time.

I created 3 initial steps: 
1. **Create the app on paper:** I just wanted visual support to see what the app should look like, the pages needed, integrations, SQL tables, routes, etc. 
2. **Make the structure of the app:** Here I will just focus on having a web app that works. The goal here is the write the Python code, connect to the Database and create the HTML pages. 
3. **Styling:** with a working web app, I can focus on making the website prettier with CSS, and images. 

<br/><br/>

## **Creating the web application**

### **- Structure**
** **

The first goal here is to have a working web application.

Being a web application, I started with the folders and files: **static, templates, requirements.txt, and app.py**.

Inside the templates folder, I added a **layout.html** file that would become the layout for most (*if not all*) of the HTML pages.

<br/>

#### **Index page**

<br/>

The first page to be created was the index page.

I started by creating **index.html** and adding some code to it. The page was simple at this stage. I used `Django` to get the basic page layout from layout.html and I added a header and a paragraph with a welcome message. 

Then comes the python code (`@app.route("/")`).

The backend code here was not too complicated. I used the `@app.route` decorator to connect the URL to the function `index()`. This function makes a SQL query to get all the items listed (*more about this in later paragraphs*) and renders the index.html page passing the list of items.

I then updated the index.html page to display these items using `Jinja and Django`, I added a banner for aesthetic reasons.
With that done, I have a page that briefly introduces the web app and shows the list of items available.

**PS**: Unlike other pages, the index route does not require the user to be logged in. This allows everyone to be able to see the page and have an idea of what the web app is about before registering.

<br/>

#### **Register page**

<br/>

To do most of the things in the web application the user will need to be logged in. It is only logical to create a registration page. 

I created **register.html**, made it an extension of layout.html, and added a form to collect the registration information:
- Input of type text for the username
- Input of type password for the password and password confirmation
- Submit button

The form is sent to the URL "/register" using a "POST" method to keep the user's information safe.

We can now create the python backend. Again, I used `@app.route` to connect the URL "/register" to the function `register()`. But unlike the index route, here we will support both "GET" and "POST" request methods.

If the request method is "GET", the function will render the register.html page. 

If the request method is "POST", the function will:
- Get information submitted
- Run a SQL query to see if the username is already taken and if it is, it will return an apology message saying that the username is taken.
- It will compare the password and the password confirmation to make sure they match (*if not, apology message*), and if they do, it will use `generate_password_hash` to generate a password hash (for security reasons, we are not going to save the user's passwords).
- And finally, it will save the username and the respective password into the "users" table inside our database. 

The function will then redirect the user to "/login" to make the first login.

Now might be a good moment to introduce the first table in our database. 

<br/>

##### **Users table**

The "users" table will be used to save the login information for each new user.
It has 3 columns:
- **id**: A unique id assigned to each new user
- **username**: the username chosen by the user
- **hash**: the unique hash generated by the user's password

This table is created only once using the syntax `CREATE TABLE IF NOT EXISTS users` that I learned from a website called w3schools.

<br/>

#### **Login page**
<br/>

With an account created on the registration page, the user is prompted to log in for the first time.

To achieve that, I created **login.html**. On this page, the user can enter his/her username and password in order to log in. I used a form that submits the information via the "POST" method so that sensitive information doesn't show up in the URL.

I then created the /login route that again supports 2 request methods: **GET and POST**.

When the user submits the username and password via "POST", the backend function `login()` checks:
- **If the username and password fields were filled out** (*I could also use the required attribute for the input tags but I decided to add more complexity*).
- **If the username exists in the database**: To check for this, we run a SQL query to get all the information for the matching username. If the query returns nothing, this means that the username does not exist. An apology message will be rendered in this case.
- **If the username exists**, we check if the password submitted will generate the same hash as the hash we have on file. If it does, then we successfully confirmed the user's identity, and we use "session" from Flask to save the session information. If the hash does not match, we render an apology message.

<br/>

##### **Logout**

While on the subject, after registration and login, the only thing missing is a logout option.

This is achieved by creating a /logout route and using `session.clear()` to clean the session information saved during login.

<br/>

#### **Lend Page**

<br/>

In order to borrow a product, someone has to be willing to lend it. Let's then create a page that allows users to list the items that they don't use and are willing to lend to other people for a short period of time.

I started by creating **lend.html** inside the **"templates"** folder (*all HTML pages must be inside this folder in order for the web app to work properly*). Inside this page, I had a simple form that asked the user for a title and description for the item. The for then submitted to "/lend" URL via "POST" method. 

Then I added the backend code to app.py. 

Similar to the other pages, this route supported both GET and POST (for more details, please check the index and registration sections). 

If the request method is "GET", the `lend()` function renders the lend.html file. 

If the request method is "POST" (*the user submitted the form*), `lend()`  collects the information about the item and stores it on our database, inside a table called "**listing**".
On another table called "**transactions**" we make a record of this new item added.

<br/>

##### **Listing table**
The **listing table** will be used to save the information about each new item added by any user.
It has 3 columns:
- **product_id**: A unique id assigned to each new item
- **user_id**: The id of the user that listed the item
- **title**: The title of the item    - description: The description of the item

This table is also created only once using a similat syntax to the previous table (*please check app.py for query to create this table*).

<br/>

##### **Transactions table**

The transactions table will keep a record of all the listing and borrowing done by the users.

This table has 4 columns:
- **transaction_id**: A unique id assigned for each new transaction
- **user_id**: The id of the user who has listed or borrowed an item
- **type**: The type of the transaction (Listed or Borrow)
- **product_id**: The id of the item in listed or borrowed
- **title**: The title of the item in listed or borrowed

This table was created the same way as the other ones.

<br/>

##### **Updates**

With the page working and the item's information being properly stored in our database, I decided to make the lend page more interesting.
 
I started by adding a few fields inside the form:
- **label element**: I added labels to all fields using `<lable>`
- **Available date**: I used `<input>` of `type="date"` to allow the user to choose when the item will be available.
- **Images**:  Using `<input>` of `type="file"` that accepts images, the user can now upload photos of the items. 

To finish this set up, I have to then modify the listing table to include these new fields. 

I later thought that it would be cool if the user could see a list of item he/she has already listed. So, I made a second update.

I started by modifying the code to make a query to our database and collect all the items listed by the current user. This is possible because we have the user id stored in session. 

The list of items is store inside the variable "listing" which is then passed to the lend.html page. 

Then, using `Django and Jinja`, I created a table that displays all the items the user has listed before. (*The table only created if the listing variable is not empty*) 

For the third update, I wanted the user to be able to mark products as returned (*once a borrower has returned the item*) or unavailable (*if the owner will need the item and therefore can not borrow it at the moment*). 

To achieve this, I created a form with hidden input fields and a submit button. The purpose of this form is to submit the product id so that the item can be marked as returned or unavailable. 

On the backend, if the request method is "POST" and we get a `product_id` field, it means that we either want to mark this item as returned (*available = yes*) or mark it as unavailable (*available = no*).

Finally, I added an "available" column to the listing table with the default value "**yes**". Once an item is list, it is automatically marked as available.

I then run a few tests to make sure the page is performing as expected.

<br/>

#### **Borrow Page**

<br/>

We have some listed items. We can now borrow them.

Similar to the other pages, I started by creating the borrow.html file. This page is going to display all items available for the current user to borrow. Again, `Django and Jinja` were used to render this page. 

When the user finds an item to borrow, he/she clicks the "Borrow" button which submits the items id via "POST" to the "/product-page" URL (*more about that later*). 

On the backend, if the request method is "GET" we make a query to get all the items on the listing table that were NOT listed by the current user (the user can't borrow an item he/she owns) and store this list in a variable called listing. 

Here is the line of code used:

 `listing = db.execute("SELECT * FROM listing WHERE user_id <> (?)", session[" user_id "])`

The variable "listing" is then passed to borrow.html when rendering. This allows the page to display all the items automatically, as well as add each item's id for the next step. 

If the request method is "POST", we update the listing table to mark the product as unavailable (*available = no*) and we also make an insertion into the transactions table. 

The user is then redirected to the main page ("/"). 

<br/>

#### **Product Page**

<br/>

The goal for the product page was to have a page that showed the item's image, title and description, and then allowed the user to borrow the item with the click of a bottom. 

The idea is that once the user chooses to borrow, both the lender and the borrower will receive emails in order to arrange the pick up of the item.


Inside the templates folder I created **product_page.html** and added `<img>` for the item's image, `<h3>` tag for the title and `<p>` for the description. I then added a form with a `<input>` of `type="hidden"` with the item's id, as well as a submit button.

And here is why on the borrow page we submitted to this page via POST. Using the items id we can make a query to get all the information about the current item from the listing table and use `Django and Jinja` to render this page. The result is a page that automatically changes depending on the item being viewed. 

<br/>

##### **Updates**

I wanted to divide that page horizontaly so I created a class for that (*more about that later*). 

I also wanted the page to behave a little bit different **IF the item being seen was not available**: 
- I added a red warning message 
- I added a "notify me bottom". The idea is for the user to receive an email once the item has been marked as returned.

Now, when the item is available we have one page and when it is not we have a slightly different page.

<br/>

#### **History Page**

<br/>

I wanted a page in which the user could see the items borrowed and listed.

I used `Django and Jinja` for the **history.html** page and it displays all the items (*listed or borrowed*) inside a table with 3 columns:
- **Item**: Shows the title of each item
- **Action**: Shows if the item was "Borrow" or "Listed"
- **See Item Page**: A button the user uses if he/she wants to see the product page.

On the backend, we make a query to get all the information from the transactions table associated with the current user's id and store this information inside a variable called (listing). Here is the line of code used:

`listing = db.execute("SELECT type, product_id, title FROM transactions WHERE user_id = (?)", session[" user_id "])`

The listing variable is than passed to the history.html page. 

<br/>

#### **Profile Page**

<br/>

The profile.html page is very simple:  
- It has a link to the history page 
- And another link to the lend page

The backend is also very simple. It renders te profile.html page.

<br/>

### **- Styling**
** **

<br/>

With the structure of the website done and everything working properly, we can move on to the styling of the website.

<br/>

#### **Index Styling**

For the main page, I wanted a page that quickly conveys what the website is about right from the get-go. 

I created a banner that sets the mood for the website and I added it to the page using an image tag. I then added two paragraphs describing the website. 

Right below the paragraphs, there are 3 bottoms:
- **Borrow**: This button takes the user to /borrow
- **Lend**: This button takes the user to /lend
- **Donate**: The idea for this button is to allow users to make donations to the website

Each of the three buttons is inside a div element, and all 3 divs are inside a div of class "flex-container". The flex-container class uses the property `display: flex;`, among others, which allows the 3 divs to be side-by-side. I also added an inline CSS to each div to set the width at 33.3%. 

I used bootstrap for the buttons. The class used was `btn btn-primary`. 

Finally, it would be really cool to see some of the items available without having to go to the /borrow page. 

I added the products using `Django and Jinja`, and I created a few classes inside style.css to allow the products to stay by side-by-side using flex, I edited the way the images are displayed and so on.

<br/>

#### **Lend Styling**

For this page, I divided the input section horizontally and vertically using Flex and I added a bootstrap class to the button. 

I edited the sizes of the input fields for aesthetic reasons and I centralized everything by setting the left and right margins to `auto`.

For the table, I decided to use an element selector for the tags `<table>`, `<th>`, and `<td>` inside the **style.css** file. 

The last thing to be added were bootstrap classes for both the unavailable button (`class="btn btn-danger"`) and the retuned button (`class="btn btn-success"`)

<br/>

#### **Borrow Styling**

For this page, I started by adding a title and changing the background. 

I then used some of the classes used in the index page to maintain a similar aesthetics. 

<br/>

#### **History Styling**

Because we have already used an element selector for table, th and td, the history page did not need any extra styling.

I simply added a bootstrap class to the "View Item" button.


Other pages like login, register, etc., don't have too much styling added to them.

