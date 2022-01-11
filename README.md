# Common Phrase Detection
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This is an API python library which is developed for detecting stop phrases.


## Table of Contents

- [Background](#background)
- [Install](#install)
- [API](#api)
- [Maintainers](#maintainers)

## Background
NLP (Natural Language Processing) techniques is very helpful in various applications such as sentiment analysis, chatbots and other areas. For developing NLP models a need for a large & clean corpus for learning words relations is indisputable. One of the challanges in achieving a clean corpus is stop phrases. Stop phrases usually does not contain much information about the text and so must be identified and removed from the text.
<br>
This is the aim of this repo to provide a structure for processing HTML pages (which are a valuable source of text for all languages) and finding a certain number of possible combinations of words and using human input for identifying stop phrases.

## Install

1. Make sure you have `docker`,`docker-compose` and `python 3.8` and above installed.

2. create a `.env` file with desired values based on `.env.example` file.

3. After cloning the project, go to the project directory and run below command.
```bash
docker-compose -f docker-compose-dev.yml build
```

4. After the images are built successfully, run below command for starting the project.
```bash
docker-compose -f docker-compose-dev.yml up -d
```

5. We need to create a database and collection in mongo in order to use the API. First run mongo bash.
```
docker exec -it db bash
```
6. Authenticate in mongo container.
```
mongo -u ${MONGO_INITDB_ROOT_USERNAME} -p ${MONGO_INITDB_ROOT_PASSWORD} -- authenticationDatabase admin
```
7. Create the database and collection based on `MONGO_PHRASE_DB` and `MONGO_PHRASE_COL` names you provided in step `2`.
```
use phrasedb;  # Database creation
db.createCollection("common_phrase");  # Collection creation
```
8. Now you're ready yo use the API section.

## API

This API has three endpoints. <br>

### Document Process

Here you can pass a HTML text in request body to process it.

The process stages are:

* Fetching all H1-H6 and p tags

* Cleaning text
* Finding bags (from 1 to 5 bags of word)
* Counting the number of occurences in text
* Integrating results in database
(Updating count field of the phrase if already exists, otherwise inserting a
new record)

### Status Updater

Updates statuses. <br>

Changing the status of a phrase to either **stop** or **highlight**.

### Data Fetcher

Fetching data from database based on the statuses.
Here you can fetch phrases based on 4 different situation for statuses:

* Stop phrases

* Highlight phrases

* Phrases that have status (either stop or highlight)

* Phrases which statuses are not yet determined

### API details

* API Base URL 
```
127.0.0.1:8000
```
* API Swagger UI
```
127.0.0.1:8000/docs
```
For futher details and how to make request to each endpoint refer to the swagger of the API.

## Maintainers
[Maani Beygi](https://github.com/MaaniBeigy)<br>
[Reza Shabrang](https://github.com/rezashabrang)

