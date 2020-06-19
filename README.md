# Melee Framedata Database

The [Melee Database](http://meleeframedata.com) is a web application inspired by [Ultimate Frame Data](https://ultimateframedata.com/) to give players easy and convenient access to gameplay data that is otherwise not readily avaliable. The database utilizes Flask as the webframe for the main Python program, which uses SQLAlchemy to store the data for each character

![](static/images/logo.png)

## To Do
* Site is insecure, need to work on admin security

* Some character data is still missing, need to find a way to extract that info

* Some character data may be inaccurate, need to do cross-checking (ICs, young link have already been brought up)

* Throw data is inaccurate, throw's total frames are based on the weight of the character they are throwing, a note needs to made of [that](https://smashboards.com/threads/detailed-throws-techs-and-getups-frame-data.206469/)

* Add Dr. Mario/Mario? up b cancel stats [here](https://smashboards.com/threads/up-b-cancel-frame-and-hitbox-data-complete-with-gifs-and-now-oos-data.378468/)

* Add character stats such as dash duration, rankings for misc info (if you have any suggestions feel free to direct message me on [Twitter](https://twitter.com/SandTFGC))

* Find missing character animation GIFs, such as most Pichu's animations and most character's throws

* Give user the option to go "frame-by-frame" on character GIFs

* Clean up the info page

* Clean up the "Attacks" data table by seperating attacks among ground normals, aerials, grounded specials, and aerial specials 

* Add search bar on homepage for characters, potentially search bar on character pages for attacks

* Add more comments to the main python program to improve readability

* Upload ER Diagram of the Database

* Possible CSS stylistic changes

* Add Toggelable Dark Mode
