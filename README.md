Instructions to connect to DB
* Run `./cloud_sql_proxy -instances=uwenca:us-central1:energyhacks-2020=tcp:3306`
* If the above command doesn't work in Google Cloud SDK Shell, use: `"cloud_sql_proxy.exe" -instances=uwenca:us-central1:energyhacks-2020=tcp:3306`
* On your prefered SQL Studio, connect to localhost:3306 and use password.


Run tests
* `python -m pytest` 
* unning tests not working on GitHub, please run locally!)
