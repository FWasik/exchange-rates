# Exchange Rates App

## Description
The application is designed to retrieve and store exchange rates for stored currencies. 

Two endpoints are available:
- currency/ (GET)
- currency/<base_currency>/<target_currency>/ (GET).

The first returns a list of currencies stored in the database. The second returns the latest exchange rate for the given currencies presented in the database.

To start application run command: `docker compose up`. Remember about .env file. In **exchange_rates** folder there is a env.example file which helps creating own .env file.

There are 4 default currencies (EUR, USD, PLN, JPY), they are added when the container is created and after migrations by the `default_currencies` command defined in **exchange_rates/rates/management/commands**. The `get_exchange_rates` command is then executed to retrieve the rates for all currencies. The app gets exchange rates from open version of [ExchangeRate-Api](https://www.exchangerate-api.com/docs/free). There can be only one rate for a given currency pair for each day.

If you want to have more currencies and exchange rates for them, you need to add a currency via the admin panel and then you must run the `get_exchange_rates` command. This can be done by recreating the container or in the container shell using the command: `python manage.py get_exchange_rates`.


The application also includes unittests for commands and endpoints. These can be run in the container shell with the `python manage.py test` command.
