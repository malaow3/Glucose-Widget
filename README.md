# Glucose-Widget
Continuous Glucose Monitor iOS 14 Widget setup using Python and JS

As per Scriptable docs, "the widget will refresh periodically and the rate at which the widget refreshes is largely determined by the operating system". My experience has been the widget will update within a new glucose reading (~5 minute window), but will not update as frequently with low power mode active.

# Setup 
* Install Scriptable on iOS 14 device (https://scriptable.app)
* Copy repository to local machine
* Sign up for Repl.it account (https://repl.it/) for webhosting
* Create a new Repl with python
* Copy contents of main.py and keep_alive.py to repl
* Add .env file containing username and password –– format should be:
```python
   username="myusername"
   password="mypassword"
```
* Run repl and copy link of webpage that is set up
* _Optional:_ set up account on uptimerobot (http://uptimerobot.com) to ping repl site to ensure it is constantly active
* Copy contents of Bggraph.js and Bggraph2.js to scriptable and modify the appropriate urls
* Add widget to home screen

Note: Repl.it web hosting is optional, this can be hosted anywhere that supports python and Flask —— I chose Repl since it is free

# Widget
<img src="https://i.imgur.com/EhpGp2M.jpeg" width=250>
