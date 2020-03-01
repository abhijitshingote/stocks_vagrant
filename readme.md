STEPS

1.sudo apt install virtualbox

2.sudo apt update

3.sudo apt install vagrant

4.git clone https://github.com/abhijitshingote/stocks.git

5.cd stocks

6.rm -r .vagrant

7.vagrant up

8.Connect to powerbi - select postgresql get sources

9.server 172.168.33.10 db stockdb

10.connection will throw certificate error

11.Follow below steps and reconnect

Its not best way but worked for me since if u dont need encryption for security reason.

Go to Postgres config file on your DB server and go from

ssl = true

to

ssl = false

Then open your power bi desktop File-> Options and settings -> Data source settings -> then in global you will have saved your connection press Edit Permissions and uncheck "ENCRYPT CONNECTIONS"

Then it will work

WARNING: THIS IS NOT RECOMMENDED IF YOUR DB IS OPEN TO PUBLIC.