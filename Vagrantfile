# -*- mode: ruby -*-
# vi: set ft=ruby :
$script = <<SCRIPT

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python-pip -y
sudo pip install --upgrade pip
apt-get install -y postgresql
sudo sed -i "s/#listen_address.*/listen_addresses '*'/" /etc/postgresql/9.5/main/postgresql.conf
sudo cat << EOF >> /etc/postgresql/9.5/main/pg_hba.conf 
# Accept all IPv4 connections - FOR DEVELOPMENT ONLY!!!
host    all         all         172.168.33.1/32             md5
EOF
sudo -u postgres psql -c "CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD 'vagrant';"
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O vagrant stockdb"
sudo service postgresql restart
sudo su - postgres -c "pg_restore -d stockdb /vagrant/populate_stockinfotable_from_local.sql"
# new
sudo su - postgres -c "psql stockdb < /vagrant/populate_stock_price_history_dev.sql"
sudo su - postgres -c "psql stockdb < /vagrant/other_scripts.sql"
# end new
sudo pip install virtualenv
virtualenv myenv --python=python3.6
source myenv/bin/activate
# pip install pandas
# pip install sqlalchemy
# pip install requests
# pip install yfinance
# pip install psycopg2-binary
# pip install lxml
pip install django==2.1.2
pip install django-mathfilters
pip install psycopg2-binary
touch /home/vagrant/webserverlog
sudo chmod 777 /home/vagrant/webserverlog
sudo /home/vagrant/myenv//bin/python  /vagrant/webapp/manage.py runserver 0.0.0.0:80 > /home/vagrant/webserverlog

sudo rm /etc/localtime
sudo ln -s /usr/share/zoneinfo/US/Eastern /etc/localtime
sudo service cron restart

# /home/vagrant/myenv/bin/python /vagrant/query_yfinance.py
sudo su postgres -c "psql -d stockdb -a -f /vagrant/removeduplicates_from_stockpricehistory.sql"
touch /home/vagrant/autofile
sudo chmod 777 /home/vagrant/autofile
# echo "30 16 * * 1-5 /home/vagrant/myenv/bin/python /vagrant/query_yfinance.py  >> /vagrant/cronlogfile.log" >> mycron
# echo '30 17 * * 1-5 sudo su postgres -c "psql - stockdb -a -f /vagrant/removeduplicates_from_stockpricehistory.sql" ' >> mycron
# sudo su - vagrant -c "crontab mycron"
# rm mycron

date
SCRIPT

Vagrant.configure("2") do |config|
  
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.provider "virtualbox" do |v|
    v.name = "dev_vm"
  end

  config.vm.network "private_network", ip: "172.168.33.21"
  config.vm.network "forwarded_port", guest: 5432, host: 5421
  config.vm.network "forwarded_port", guest: 80, host: 8081
  config.vm.provision "shell", inline: $script
end
