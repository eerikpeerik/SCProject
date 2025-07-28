# Cyber Security Base 2025 Course Project 1
This project is using the OWASP 2021 [top ten list](https://owasp.org/www-project-top-ten/) and CSRF

To run the project, install the [required dependencies](https://cybersecuritybase.mooc.fi/installation-guide) used in the course, clone the repository, and run the command:

```
python manage.py runserver
```
The website can be found at http://127.0.0.1:8000/ once the server is up and running

The website has a superuser, with username superuser and password superuser

However, there are also default users:
   | Username | Password |
   |:--------:|:--------:|
   | admin    | admin |
   | bob   | thebuilder |
   | alice | inwonderland |

## FLAW 1: [SQL Injection](https://owasp.org/Top10/A03_2021-Injection/)
Pin-pointed out the flaw ->
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L21-L24
An SQL injection is when a user injects malicious data into an unsafe and/or poorly written input field. The data entered in the input field contains an SQL query which alters the existing database. Depending on the SQL query, the user can modify, delete or even drop complete data tables. They might even find out other users’ passwords. How this site processes user added items is through an SQL query INSERT INTO, which is not properly set up. Any malicious user can use this input field to alter the existing database.

For example, Bob can alter Alice’s list by entering in:

```
'); UPDATE list_listitem SET item_text='Hacked!' WHERE user_id=3; --
```

To fix this vulnerability, you can use Django’s standard method of creating objects. 
Comment out these lines:
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L19-L25

And enable this line:
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L28C1-L28C74

### Screenshots
Before 1: Alice has a list of her favourite songs.

Before 2: Bob has typed in an SQL query that alters Alice’s list to say “Hacked!”.

Before 3: All items in Alice’s list have changed to “Hacked!”.
#
After 1: Bob has typed in the same query.

After 2: This time, it becomes added to the list instead of being compiled as an SQL query.

After 3: Thanks to the vulnerability patch, Alice’s list remains untouched.

## FLAW 2: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
Pin-pointed out the flaw ->

Missing CSRF token:
https://github.com/eerikpeerik/SCProject/blob/f4257178d0557540220e5c80201d78f04c5d2bc3/SCProject/list/templates/list/list.html#L20

Unnecessary CSRF exemption:
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L54C1-L54C61

GET requests instead of POST:
https://github.com/eerikpeerik/SCProject/blob/f4257178d0557540220e5c80201d78f04c5d2bc3/SCProject/list/templates/list/list.html#L19
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L62-L63

Cross-site request forgery (CSRF) is when an attacker sends requests to its target through another source (for example, another website) where the attacker has authentication. A typical CSRF attack follows a victim clicking on a link that sends them to a malicious website. This website contains is programmed to steal or alter the user’s data. This project has a dummy CSRF attack page (csrf_attack.html) which contains an HTML image. But instead of there being an actual image, there is an URL. When the website tries to load the image, it runs the malicious URL that is designed to alters the user’s password without their knowledge. The link to the CSRF attack can be found on Bob’s list. Copy and paste it into another tab and log out of Bob’s account and see how you are met with a login error as Bob’s password has been changed. The project handles password changing with a GET method instead of POST method, which is malpractice as GET skips the validation process.

To fix this vulnerability, we can add CSRF tokens where they are missing in the list.html file as well as removing @csrf_exempt in views.py. Plus, we can change how the password changing process processes requests; Instead of using GET, we switch to POST as POST needs a valid CSFR token to work ensuring great protection against CSRFs.

Add in {% csrf_token %}"}:
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/templates/list/list.html#L20

Remove @csrf_exempt:
https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L54

Change GET to POST method:
https://github.com/eerikpeerik/SCProject/blob/f4257178d0557540220e5c80201d78f04c5d2bc3/SCProject/list/templates/list/list.html#L19

https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L62-L63

### Screenshots
Before 1: Bob logs in as normal.

Before 2: Bob finds that an item advertising free iPhones has been added to his list. 

Before 3: Bob copies and pastes the link in his browser and is taken to a new webpage claiming that he has been hacked.

Before 4: Later, when Bob tried to log back in but is met with an error of his password being incorrect. His password has been changed without his permission thanks to this CSRF attack.
#
After 1: After the vulnerability has been fixed and Bob has recovered his account. He retakes steps in Before pictures 1-3, logs out and enters in his login details.

After 2: Bob successfully enters his personal list without any harm. The vulnerability is patched.

## FLAW 3: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
Pin-pointed out the flaw ->

Password changing handled with GET method: https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L62-L63
Missing @login_required: https://github.com/eerikpeerik/SCProject/blob/faecd5e4b5b8d7dbd9d64074e7ff3c26c5e0d866/SCProject/list/views.py#L55

Broken Access Control (BAC) is when the code that limits a user’s access is missing or not implemented correctly. Some data in the project is stored through a path variable, which can be altered to give the user access to data that they normally are not able to access. The project might not check for authorization making it so that any user (even the user with the lowest privilege) the ability to access admin features. But that is not the only thing covered by BAC, weak authentication such as weak password policies and lack of multi-factor authentication also falls under the umbrella of BAC. In this project, users can alter each other’s passwords while being both logged in and logged out. By opening this link: http://localhost:8000/list/changepassword/?user=bob&password=hacked123 Bob’s password will be changed to ”hacked123”.

In order to fix this vulnerability, we must change from GET to POST in order to hide the parameters in the URL, in list.html: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/templates/list/list.html#L19
And in views.py: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/views.py#L66
Furthermore, we must add a requirement to be logged in to be able to change one’s password. We do this by changing how we get the user, by using request.usr: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/views.py#L59
And by adding @login_required like in previous vulnerabilities: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/views.py#L55
As a consequence of switching from GET to POST, we need to add in CSRF tokens as they are required for POST methods: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/templates/list/list.html#L20
Then comment out or remove this line: https://github.com/eerikpeerik/SCProject/blob/b25ee41490127b31080512df98e044da7f1abed7/SCProject/list/views.py#L62
### Screenshots
Before 1: A malicious user has figured out how to change user’s password without needing to be logged in. They have entered the URL in their browser, ready to hit ENTER.

Before 2: After the malicious user has hit ENTER, they are redirected back to the login page. Bob tries to login to his page. Only to be met with an error saying that his login credentials are wrong.
#
After 1: After the malicious user has hit ENTER, instead of being redirected back to the login page, they are instead met with a 404 error as the website no longer changes passwords with GET methods.

## FLAW 4: [Logging](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)
Pin-pointed out the flaw ->

No logging implemented: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/SCProject/settings.py#L136

Logging is needed so that admins can see what activity is going on the website. For example, the admin needs to know when a password has been updated and without proper logging, they are left in the dark. It is important for the admin to know what’s going on in case an attacker change’s another user’s password.

To fix this vulnerability, we can use Django’s built-in logging which can help admin to see and alert for any suspicious activity, like the example mentioned above. First we must add in the built-in logging code in settings.py by uncommenting these lines of code: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/SCProject/settings.py#L137-L169
Then we need to add the actual loggers. We must import logging to views.py: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/list/views.py#L11
Then we must add the loggers that tell the admin what has been updated or changed. These can also be found in views.py: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/list/views.py#L12-L13
https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/list/views.py#L30
https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/list/views.py#L72C1-L72C79
# Screenshots
Before 1: Bob wants to change his password to “bob” to make it easier to remember.

Before 2: No direct logging saying that Bob has changed his password. Only changePassowrd’s change method being called is shown.
#
After 1: Now there is a clear log saying that Bob has changed their password.

After 2: In addition, new items are now also added to log so admins can see if any suspicious links or data is stored or if anyone tries to do an SQL injection.
## FLAW 5: [Security misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
Pin-pointed out the flaw ->

The SECRET_KEY is visible to everyone: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/SCProject/settings.py#L28
DEBUG is left on True: https://github.com/eerikpeerik/SCProject/blob/65ce5b984e75b4777c3c435b778b180178b03602/SCProject/SCProject/settings.py#L31
Security misconfiguration is when developers have overseen crucial configurations or left in errors. Security might not have been taken into consideration during configuration during set-up. This can lead to a vulnerable application, like this project, which opens the doors for hackers to access the project and its data and code more easily. 
In settings.py, you can find the SECRET_KEY which is currently visible for everyone. Django uses it for cryptographic signing of data, and it is unique, meaning it should be hidden. As obtaining it means that an attack can use it to generate false tokens and cookies. 
In addition, due to Debug being set to true, attackers can run the command 
```python manage.py check –deploy``` 
to see each vulnerability and even gain access to the program.
To fix this vulnerability, we can run the command while Debug is set to true to see what we should fix. Plus, it is important to hide to secret key. We do that by:
1.  We need to install a new dependency by running this command in the console: 
```pip install python-dotenv```
2. Create a new .env file in the base directory. In this project it is the same directory where manage.py is located in. https://github.com/eerikpeerik/SCProject/blob/main/SCProject/.env
3. We cannot have the .env in our public repositories, so we must update the .gitignore file to prevent the .env file from being added to potential commits and pushes by version control. https://github.com/eerikpeerik/SCProject/blob/fc75e782d726e25098eb3125b98838e5a4c52a9e/SCProject/.gitignore#L3
4. We must import dotenv library in our settings.py: https://github.com/eerikpeerik/SCProject/blob/fc75e782d726e25098eb3125b98838e5a4c52a9e/SCProject/SCProject/settings.py#L15 
and load in the key for usage: https://github.com/eerikpeerik/SCProject/blob/fc75e782d726e25098eb3125b98838e5a4c52a9e/SCProject/SCProject/settings.py#L25-L26
5. Finally, we must remove SECRET_KEY from settings.py: https://github.com/eerikpeerik/SCProject/blob/fc75e782d726e25098eb3125b98838e5a4c52a9e/SCProject/SCProject/settings.py#L28 
and switch Debug from true to false: https://github.com/eerikpeerik/SCProject/blob/fc75e782d726e25098eb3125b98838e5a4c52a9e/SCProject/SCProject/settings.py#L31
### Screenshots
This one is difficult to demonstrate so I instead decided to show how the code is changed.

Before 1: The SECRET_KEY is visible for everyone, and debug is set to true.
#
After 1: The SECRET_KEY is removed and instead being read in by dotenv. Plus, debug is set to false. 

After 2: The SECRET_KEY is hidden in its own .env file.
