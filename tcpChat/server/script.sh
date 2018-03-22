#!/bin/bash
sudo apt-get update
sudo apt-get install debconf-utils

sudo debconf-set-selections <<< 'mysql-server mysql-server/root-pass password Rfv753'
sudo debconf-set-selections <<< 'mysql-server mysql-server/re-root-pass password Rfv753'
DEBIAN_FRONTEND=noninteractive sudo -E apt-get -q -y install mysql-server

sudo mysql -u root << EOS
CREATE DATABASE IF NOT EXISTS tcpChat;
GRANT ALL ON tcpChat.* TO 'chat'@'%' IDENTIFIED BY 'Rfv753';
FLUSH PRIVILEGES;
EOS

mysql -u chat -pRfv753 tcpChat << EOS
CREATE TABLE IF NOT EXISTS users (login VARCHAR(50), password VARCHAR(40));
CREATE TABLE IF NOT EXISTS log (time VARCHAR(50), sender VARCHAR(50), receiver VARCHAR(50), message VARCHAR(255));
EOS

sudo sed -i 's/bind-address\t\t= 127.0.0.1/bind-address\t\t= 0.0.0.0/g' /etc/mysql/mysql.conf.d/mysqld.cnf
sudo service mysql restart

