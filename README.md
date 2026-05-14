# Restore RDS DB from Snapshot
Interactive Python script to restore RDS databases from snapshots


### Requirements ###

- Python 3.13+

### Setup ###
```
make install
```


### Linting ###
```
make lint
```

### Testing ###
```
make test
```


### Example usage ###

```
python main.py
Default region: us-east-1
---------------------------------------------
? What would you like to do?
> Change region
  List databases
  Create database from snapshot
  Quit
```

Selecting **List databases**:
```
    test1
    test2
```

Selecting **Change region** opens an arrow-key menu of all available RDS source regions.

Selecting **Create database from snapshot** walks through:
1. Choose source database
2. Choose snapshot (displayed newest-first with timestamp)
3. Enter a name for the new database
4. Review summary and confirm

```
---------------------------------------------
You've chosen:

source  : test1
snapshot: rds:test1-2024-11-03-06-07
target  : test5
---------------------------------------------
? Proceed with restore? (Y/n)
Create test5: request sent!
```
