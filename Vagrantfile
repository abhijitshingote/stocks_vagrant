# -*- mode: ruby -*-
# vi: set ft=ruby :
$script = <<SCRIPT

sudo apt-get install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python-pip -y
sudo apt-get install nginx -y
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
sudo pip install virtualenv
virtualenv myenv --python=python3.6
source myenv/bin/activate
# pip install pandas
# pip install sqlalchemy
# pip install requests
# pip install yfinance
# pip install psycopg2-binary==2.7.7
# pip install lxml
# pip install django==2.1.2
# pip install django-mathfilters
# pip install psycopg2-binary
# pip install gunicorn
pip install -r /vagrant/requirements.txt

sudo rm /etc/localtime
sudo ln -s /usr/share/zoneinfo/US/Eastern /etc/localtime
sudo service cron restart

sudo su - postgres -c "psql stockdb < /vagrant/sql_files/populate_stockinfotable_from_local_insert.sql"
sudo su - postgres -c "psql stockdb < /vagrant/sql_files/cleanup_stockinfotable.sql"
# /home/vagrant/myenv/bin/python /vagrant/query_yfinance.py
sudo su - postgres -c "gunzip -c /vagrant/sql_files/compressed_stock_price_history.gz | psql stockdb "
sudo su postgres -c "psql -d stockdb -a -f /vagrant/sql_files/removeduplicates_from_stockpricehistory.sql"
sudo su - postgres -c "psql stockdb < /vagrant/sql_files/other_scripts.sql"
touch /home/vagrant/autofile
sudo chmod 777 /home/vagrant/autofile

#### DAILY JOB BELOW
echo "30 16 * * 1-5 /home/vagrant/myenv/bin/python /vagrant/query_yfinance.py  >> /vagrant/cronlogfile.log" >> mycron
echo '30 17 * * 1-5 sudo su postgres -c "psql -d stockdb -a -f /vagrant/sql_files/removeduplicates_from_stockpricehistory.sql" ' >> mycron
echo '40 17 * * 1-5 sudo su - postgres -c "psql stockdb < /vagrant/sql_files/other_scripts.sql" ' >> mycron

sudo su - vagrant -c "crontab mycron"
rm mycron

date
sudo cp /vagrant/stockdash_nginx_conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
cd /vagrant/webapp/
sudo /home/vagrant/myenv/bin/gunicorn --bind 0.0.0.0:8888 --workers 3  webapp.wsgi


SCRIPT

Vagrant.configure("2") do |config|
  
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.provider "virtualbox" do |v|
    v.name = "dev_vm"
  end

  config.vm.network "private_network", ip: "172.168.33.10"
  config.vm.network "forwarded_port", guest: 5432, host: 5421
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.provision "shell", inline: $script
end
