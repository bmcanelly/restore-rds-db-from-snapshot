# Restore RDS DB from Snapshot 
Interactive Python script to restore RDS databases from snapshots 


### Requirements ###

- Python 3.x 
- Install dependencies: ```pip install -r requirements.txt```


### Linting ###
```./run_linter.zsh```

### Testing ###
```./run_tests.zsh```


### Example Command usage and output ###

```
# from root of this repo
# example switching of regions and displaying databases
# then create a database called test-5 from one of the
# test1 snapshots
python main.py
Default region: us-east-1
---------------------------------------------
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
2
    test
    test2
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
1
Please select one of the following:
1. af-south-1
2. ap-east-1
3. ap-northeast-1
4. ap-northeast-2
5. ap-northeast-3
6. ap-south-1
7. ap-south-2
8. ap-southeast-1
9. ap-southeast-2
10. ap-southeast-3
11. ap-southeast-4
12. ap-southeast-5
13. ca-central-1
14. ca-west-1
15. eu-central-1
16. eu-central-2
17. eu-north-1
18. eu-south-1
19. eu-south-2
20. eu-west-1
21. eu-west-2
22. eu-west-3
23. il-central-1
24. me-central-1
25. me-south-1
26. sa-east-1
27. us-east-1
28. us-east-2
29. us-west-1
30. us-west-2
26
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
2
    test3
    test4
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
1
Please select one of the following:
1. af-south-1
2. ap-east-1
3. ap-northeast-1
4. ap-northeast-2
5. ap-northeast-3
6. ap-south-1
7. ap-south-2
8. ap-southeast-1
9. ap-southeast-2
10. ap-southeast-3
11. ap-southeast-4
12. ap-southeast-5
13. ca-central-1
14. ca-west-1
15. eu-central-1
16. eu-central-2
17. eu-north-1
18. eu-south-1
19. eu-south-2
20. eu-west-1
21. eu-west-2
22. eu-west-3
23. il-central-1
24. me-central-1
25. me-south-1
26. sa-east-1
27. us-east-1
28. us-east-2
29. us-west-1
30. us-west-2
27
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
2
    test1
    test2
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
3
Please select one of the following:
1. test1
2. test2
2
Please select one of the following:
1. rds:test1-2024-10-04-05-05
2. rds:test1-2024-10-05-05-05
3. rds:test1-2024-10-06-05-07
4. rds:test1-2024-10-07-05-05
5. rds:test1-2024-10-08-05-06
6. rds:test1-2024-10-09-05-05
7. rds:test1-2024-10-10-05-05
8. rds:test1-2024-10-11-05-05
6
Enter a name for the new database: test5
---------------------------------------------
You've chosen:
source  : test1
snapshot: rds:test1-2024-10-09-05-05
target  : test5
---------------------------------------------
Proceed with restore (y/n)? : y
Create test-5: request sent!
Please select one of the following:
1. Change region
2. List databases
3. Create database from snapshot
4. Quit
4
Bye

```
