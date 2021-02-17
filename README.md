# Life Dashboard
A dashboard to display useful analytics about your life

# Database design
The following data sources are included in the database design:
- Up Banking
- Google Calendar
- Strava
- Trello

- Database design:
https://app.sqldbm.com/MySQL/Edit/p152946/#



The following have not been included in the database design:

- Google Maps
Unsure of how to utilize google maps currently as the API does not support a personal google account timeline, so cannot display historical trends etc over movements

- Spotify
The main functionality required for this is to display the top songs and artists being listened to, Spotify's API has this built in as a feature, and considering it will be changing as I listen to things and has the ability to select different timeframes, a database is not necessary

- Google Keep
Notes by definition probably don't need to be displayed on a dashboard, instead we will be using the Trello "This Week" cards section to display a to-do list

- Gmail
Unsure what functionality I was after here, but there doesn't seem to be a need to display emails on the dashboard, add a ticket for future functionality where it will display urgent unread emails

## Notes
- Further research into the specifics of table construction is required, including how to structure the database with multiple tables, and the utilisation of Primary Keys, Alternative Keys and Foreign Keys


# Infrastructure design

Design document: https://drive.google.com/file/d/1cpWIr5uYrzPKb2ywaftCqYkVY4dCIocc/view?usp=sharing

|Resource   |Size   |Monthly Price   |
|---|---|---|
|API Gateway   |NA   |$1   |
|Webhook Lambda   |NA   |$0   |
|Request Lambda   |NA   |$0   |
|MySQL Instance   |db.t3.micro   |$16   |
|Quicksight   |Basic   |$5   |
|Elastic Beanstalk   |   |   |
|VPC| NA| ?|
|NAT Instance| t2.micro| $10|
|Codepipeline |NA |$0|


# Infrastructure as Code

- All infrastructure to be provisioned through Cloudformation
- Codepipeline source to be found in a separate repository (life-app)
- Codepipeline infra still setup with CF script from life-infra

