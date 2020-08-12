# Melee Framedata Database

The [Melee Database](http://meleeframedata.com) is a web application inspired by [Ultimate Frame Data](https://ultimateframedata.com/) to give players easy and convenient access to gameplay data that is otherwise not readily available. The database utilizes Flask as the webframe for the main Python program, which uses SQLAlchemy to store the data for each character

![](static/images/logo.png)


## Instructions for Deploying Locally

Run the command `python3 __init__.py` from inside the scope of meleeWebProject 

**Packages used** include Flask and SQL_Alchemy

To view from web browser, enter `http://0.0.0.0:5000`. View on mobile/other devices by connecting to the same network as the host and replacing 0.0.0.0 with the host's IP

(I've only ran this on Linux, so if you run into problems on Windows or Mac let me know)

## To Do

* Fill in current missing character data as I come across it, as well as cross check data that came from < 2 sources

* Make GIF Frame by Frame viewer more consistent, either through finding a consistent resource of all GIFs recorded in the same way, or editing each GIF individually

* Keep an eye on frame-by-frame viewer, fix any bugs associated

* Adding in data for +/- on shields

* Looking to add other data in the future, some possibilities include ledge, tech, and hitstun frame data

* Update admin security

* Find missing character animation GIFs, such as most Pichu's animations and most character's throws

* Add more comments to the main python program to improve readability

* Upload ER Diagram of the Database

* Possible CSS stylistic changes

* Add Toggleable Dark Mode


