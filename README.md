# Facebook-Group-Crawler

An example project that crawl all the posts and comments in facebook public group page

## Getting Started

### Prerequisites

* Linux or Unix-like system

* Redis Database

* Python 3.7 environment

* Docker (optional)

### Installing

```bash
# local machine
pip install -r requirements.txt

# or install as a package
pip install .
```

## Executing

Crawler use redis as a job queue, you should start redis-server before crawler execution, if you don't have redis in local machine, refer to "Docker" section

Program will stop until all of the posts and comments be collected, or press "Ctrl + c" to stop manually

GROUP_ID "xxx" is a target facebook group id show in URL, for example 1260448967306807 in https://facebook.com/groups/1260448967306807

Data will be save as json file into "data" folder

Notice that the group must be public

```bash
cd src

# create envrionment variable
export GROUP_ID=xxx

# start the program
python -m fb_group.run

# if install as a package, there is a shell command
fb_group_crawler
```

GROUP_ID could also passed by command line argument

```bash
cd src

python -m fb_group.run GROUP_ID=xxx

fb_group_crawler GROUP_ID=xxx
```

## Docker

```bash
# build docker image
docker-compose build

# start redis-server and crawler
export GROUP_ID=xxx
docker-compose up
```

## Running the tests

Run all of the test scripts in ./tests folder

```bash
make test
```

## Deployment


## License

This project is licensed under the MIT License

## Acknowledgments

