# Facebook-Group-Crawler

An example project that crawl all the posts and comments in facebook public group page

## Getting Started

### Prerequisites

Linux or Unix-like system

Redis Database

Python 3.7 environment

### Installing

```bash
# local machine
pip install -r requirements.txt
```

## Executing

Program will stop until all of the posts and comments be collected, or press "Ctrl + c" to stop manually

Argument group_id "xxx" is a target facebook group id show in URL, for example 1260448967306807 in https://facebook.com/groups/1260448967306807

Notice that the group must be public

```bash
# local machine
export GROUP_ID=xxx
python src/run.py

# local machine with argument
python src/run.py group_id=xxx
```

Data will be save into "data" folder

## Running the tests

Run all of the test scripts in ./tests folder

```bash
make test
```

## Deployment


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

