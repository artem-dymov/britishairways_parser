
## britishairways_parser

### Installation
Runtime: python3.10+

1. Clone repo, go to project folder, create new python venv:
```
python3.10 -m venv venv
```

2. Install dependencies:

```
python3.10 -m pip install -r requirements.txt
```

3. Run the following command to start program with API interface:
```
uvicorn api.app:app
```

4. Check the following local website to get docs and testing tools for API:
```
http://localhost:8000/docs
```

5. Wait until all started processes print 'STARTUP STUFF SUCCESSFUL'
Wait up to 1 minute for single process.

Note: there are 2 lendings on britishairways website: orange and blue.
It takes +30sec to load startup stuff for blue lending.

6. Make API requests.


