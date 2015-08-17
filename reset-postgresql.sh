# reset postgresql

rm -rf var/databases/postgres
./bin/initdb -U chromaway -W var/databases/postgres/
./bin/postgres -N 500 -i -p 17520 -D var/databases/postgres
