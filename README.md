# Melee Framedata Database

The [Melee Database](https://meleeframedata.com) is a web application inspired by [Ultimate Frame Data](https://ultimateframedata.com/) to give players easy and convenient access to gameplay data that is otherwise not readily avaliable. The database utilizes Flask as the webframe for the main Python program, which uses SQLAlchemy to store the data for each character

![](static/images/logo.png)

## To Do
* Most characters still have blank data fields that need to be filled

* Add general info icon on home page, explaining terminology used on the website and give credit to all who datamined the game to obtain the frame data

* Add character stats such as dash duration, rankings for misc info (if you have any suggestions feel free to direct message me on [Twitter](https://twitter.com/SandTFGC))

* Find missing character animation GIFs, such as all of Pichu's animations and most character's throws

* Clean up the "Attacks" data table by seperating attacks among ground normals, aerials, grounded specials, and aerial specials

* Toggle some more information off if it does not apply to that character/specific move (such as how multi jabs are by default not shown unless inserted in the data table) 

* Add search bar on homepage for characters, potentially search bar on character pages for attacks

* Find a way to not have to prompt the user to select mobile/desktop version

* Add more comments to the main python program to improve readability

* Possible CSS stylistic changes
