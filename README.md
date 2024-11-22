# Keysight_ML
Keysight ML Take Home Project for ML/AI Engineer

# Task

Design an URL Shortener API with following features:
## A) Functional requirements:
    a. Generate a unique short URL for a given long URL
    b. Redirect the user to the original URL when the short URL is accessed
    c. Support link expiration where URLs are no longer accessible after a certain period.

## B) Operational requirement:
    a. Think of how you can maintain high availability and scalability

# Running the Code

Assuming there is a local python enviroment

Run 

    pip install -r requirements.txt 

Once installed, to run the program , navigate into your src directory (cd src) and execute

    flask run

Go to your browser to 
    http://127.0.0.1:5000/ to generate a unique short URL

# Explanation
## Generate a unique short URL for a given long URL

Any long URL will be shorted to a 8 digit hash.

8 digit has is randomly generated and includes  62 characters in total.
This provides 62^8 possible combinations of hash.

If there is a collision, the program will try to find a new hash.

If we need to support more URLs we can increase the length

##  Redirect the user to the original URL when the short URL is accessed

So to acesss the URL, you need to go to http://127.0.0.1:5000/url/<hash>

When a user access the short URL, using the hashed value we can lookup the database for the long URL
hash is the primary key in a relational database to lookup the long URL

### Not implemented/Risks
At the moment, I have not included any user_id concept, this means that someone can hack our system to create URLs in a loop.

One proposed solution is to have user id as part of the table and limit how much short URLs one user can create

## Support link expiration where URLs are no longer accessible after a certain period.

if no expiration date is provided, the link expires after 1 year
If expiration date is provided, the expiration date is updated in the table

We can periodically run delete_expired_urls() to delete expired URLs
Also if the user access an expired URL, we will send a message back to the user and delete that URL entry

## Think of how you can maintain high availability and scalability
This system is designed as an API call.

To handle 1000s of requests at the same time, we can use a load balancer

We have 62^8 available random combinations that are difficult to guest and readily available

We can cached some of the most frequented URLs 

## Testing

Functional Testing - Done



https://github.com/user-attachments/assets/b29b4f5f-69fb-49e9-8213-ebb2c21c0fe1



Pytests for functions - Not complated
