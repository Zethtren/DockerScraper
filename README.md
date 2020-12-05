# DockerScraper

## Overview: 
This project creates a docker app which will launch (3) containers for scraping data from CoinBase Pro tickers in real-time and inserting it into a SQL Server 2019 Developer instance.

The data in the SQL server will be stored into a database named 'ticks' ( I am working on making this customizable )

Each scraper will create its own table named after the market in which it is scraping data from.

If you run the docker-compose file without modification:
- Your server will be hosted at localhost,1433
- Your username will be 'sa'
- Your password will be 'custompassword1234!'
- You will have 3 tables in your 'ticks' database ('BTC-USD', 'ETH-USD', 'ETH-BTC')

I have tested connecting to this from both Azure Data Studio as well SSMS without any issues.


This project has been tested running on windows and mac as low as 4 cpu cores without any error or missed data over the course of 24 hours. I have even tested it while running apps that display 100% CPU and GPU usage. There was no failure in any of the insertions.

The containers will automatically spin up again if they fail out. Any data commited to the container will be saved. If the container is deleted completely and rebuilt then there will be no stored data. 

Any data missed while the containers are down is missed. You will have to recollect this data some other way. Because of this I recommend running two separate instances in two separate locations.

## Instructions:

If you do not have docker-compose you will need to download it [here](https://docs.docker.com/compose/install/)

Once you have docker compose you simply need to create a folder with the name you want for your app and move into this folder:
In bash this looks like <br>
<code>$ mkdir \<your-app-name\></code><br>
<code>$ cd \<your-app-name\></code><r><br>
<code>$</code> represents the start of your terminal line. The line to copy starts after the first white-space.

After you have the directory you will need to clone or recreate the docker-compose.yml inside of this directory. <br>
If you have git installed this can be done quickly by cloning the repo:<br>
<code>$ git clone https://github.com/Zethtren/DockerScraper.git</code>
If you have wget installed you can grab just the docker-compose file and it will work perfectly fine: <br>
<code>$ wget https://raw.githubusercontent.com/Zethtren/DockerScraper/master/docker-compose.yml</code>

Alternatively, You can copy and paste the contents of docker-compose.yml into a new file named docker-compose.yml in the folder you just created.

Once you have the docker-compose.yml inside of the folder you want simply run:<br>
<code>$ docker-compose up -d</code>

This will start the application. It takes ~1 minute to run once the images are downloaded. You will see the image downloads followed by indicators that each component successfully launched.
After this is done you can view these logs using regular docker CLI tools, which you can read about [here](https://docs.docker.com/engine/reference/commandline/cli/) or Docker Desktop, which you can read about [here](https://www.docker.com/products/docker-desktop)

## Notes 
Without modification to the set-up you can expect <~25GB of data to be collected over the course of an entire year. Each market I have tested pulls about 160,000 unique trades per day. Each additional market you add can expect to add 7-8GB on your yearly data usage following these estimates.

## Future plans:
I intend to work on integrating this into kubernetes so I can create a ML workflow based on this data. I will also be working to create an automated trading platform based on the ML suggeestions were custom models can be passed to make trades with. 
This will likely be separated from the this project and run on a separate network to maintain data integrity and security as well as failover.
