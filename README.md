# Cash Register

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pydantic](https://img.shields.io/badge/Pydantic-e92063?style=for-the-badge&logo=pydantic&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?style=for-the-badge&logo=astral&logoColor=white)

The idea here in this project is to focus in the business core and avoid overengineering just to impress stakeholders. 
I planned to keep the system simple, clean, modern, easy to maintain for internationalization and secure. I tried to 
follow some principles of clean architecture and DDD. Due to the size of the project and its simplicity not all the layers 
were implemented. These main ideas helped me to set the design principles for this system. 

## Workflow Status 

[![Lint & Format Code](https://github.com/DeployIsComing/CashRegister/actions/workflows/lint.yml/badge.svg)](https://github.com/DeployIsComing/CashRegister/actions/workflows/lint.yml)

## The use of AI 

As this is a challenge most part of the code I tried to envision and develop on my own. I have used AI to generate test 
cases and "plan" in all possible testing scenarios just to keep the system secure: The spec used to create the tests can be found in 
.claude folder. This approach takes more time than necessary, but I can present a little bit some of my skills (programming and 
analysis). 

## Development Environment 

- PyCharm 2026.2.1

## Requirement 

- Python 3.14 (or above)

## About Libs

- Added pydantic for better file management access and class support
- Added flake8 to keep the code neat i.e. "lint", only for dev

## Setup 

### Install uv 

If you do not have uv installed run the following command in your terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### Pin python version

```bash
uv python pin 3.14
```

### Start venv 

```bash
source .venv/bin/activate
```

### Install dependencies 

```bash
uv sync
```

### Run the project

```bash
uv run main.py
```

### Tests 

To test the domain layer entities and services 

```bash
uv run cashregister --test
```

### Prettify the code

```bash
# check for errors and fix
uv run ruff check --fix .

# lint the code automatically
uv run ruff format .
```

## Prompt usage 

Prompt options are beautifully formatted for end-users using the lib argparse. To invoke all
the options:

```bash
# help
uv run cashregister --help

# Running happy path 
uv run cashregister input_transactions.txt

# Simple basic tests just to test domain/entities (vo)
uv run cashregister input_transactions.txt --test

# Output to a file 
uv run cashregister input_transactions.txt -o output.txt

# read the file 
cat output.txt
```

ps: in case user wants to test different values, please add it to input_transactions.txt

## Architectural Decisions

I decided to keep the config folder outside the "app" folder because it is the core. So when decide for Euro/France currency
there is no need to touch the files under app folder.

Also with the "adapters" layer implemented in case stakeholders decide to create, in the future, an *API for HTTP* 
such as FastAPI, for transactions just add it as a new adapter, simply as that (ABC, 123). No need to change the rest of the code 
keeping the separation of concerns.

## BONUS

A few extra spicy.

### AI support 

Having in mind the future expansion of Cash Register to other countries, I developed an AI powered script to generate 
currency JSON files for any desired country. The scripts get the 3-digit country code informed in CLI and generates 
the JSON using Groq free AI API service.

```bash
# Running the script
uv run python scripts/generate_currency_json.py

# You will be prompted for the 3-digit code, please inform it such as BRL, EUR, CAD, etc.
```

ps: *Please, bear in mind you are required to create a free API key and inform inside the script at: https://console.groq.com*

### Github actions 

In addition, I have added a simple Github Actions workflow to prettify the code. 

### Claude

Created claude specs to generate pytest scenarios. 

## The Problem
Creative Cash Draw Solutions is a client who wants to provide something different for the cashiers who use their system. The function of the application is to tell the cashier how much change is owed, and what denominations should be used. In most cases the app should return the minimum amount of physical change, but the client would like to add a twist. If the "owed" amount is divisible by 3, the app should randomly generate the change denominations (but the math still needs to be right :))

Please write a program which accomplishes the clients goals. The program should:

1. Accept a flat file as input
	1. Each line will contain the amount owed and the amount paid separated by a comma (for example: 2.13,3.00)
	2. Expect that there will be multiple lines
2. Output the change the cashier should return to the customer
	1. The return string should look like: 1 dollar,2 quarters,1 nickel, etc ...
	2. Each new line in the input file should be a new line in the output file

## Sample Input
2.12,3.00

1.97,2.00

3.33,5.00

## Sample Output
3 quarters,1 dime,3 pennies

3 pennies

1 dollar,1 quarter,6 nickels,12 pennies

*Remember the last one is random

## The Fine Print
Please use whatever technology and techniques you feel are applicable to solve the problem. We suggest that you approach this exercise as if this code was part of a larger system. The end result should be representative of your abilities and style.

Please fork this repository. When you have completed your solution, please issue a pull request to notify us that you are ready.

Have fun.

## Things To Consider
Here are a couple of thoughts about the domain that could influence your response:

* What might happen if the client needs to change the random divisor?
* What might happen if the client needs to add another special case (like the random twist)?
* What might happen if sales closes a new client in France?