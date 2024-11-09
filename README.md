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
1. awsbackup:job-78977ff2-c6d7-5d82-ff4a-8c58eb7cd2a7      01/01/23 00:17:52
2. awsbackup:job-dd8cad20-7503-81de-e3f3-f866e40e2017      01/01/24 00:27:52
3. rds:test1-2024-11-02-06-07                              11/02/24 06:07:48
4. awsbackup:job-ee17f8f3-3c04-78fa-b048-32f2e70114c9      11/03/24 00:18:53
5. rds:test1-2024-11-03-06-07                              11/03/24 06:07:21
6. awsbackup:job-767bf0ef-5879-fcbb-6c4c-da8d2daf679b      11/03/24 06:17:50
7. awsbackup:job-e673edaa-26ec-527e-7f57-4d662683c917      11/03/24 12:14:00
8. awsbackup:job-0eae94ea-9bad-4764-8915-7450c9d7b5f4      11/03/24 18:16:58
9. awsbackup:job-6fe71bc5-888f-4cf2-0b5c-67ee2c4e29e8      11/04/24 00:16:05
10. rds:test1-2024-11-04-06-07                              11/04/24 06:07:14
11. awsbackup:job-d3aa4c1f-cc93-a40f-f6e4-83d980f482ea      11/04/24 06:15:54
12. awsbackup:job-99e05ee0-c0a8-03c1-46f4-deb010f85e48      11/04/24 12:17:47
13. awsbackup:job-6f6b648f-b81b-45f2-37b0-9dc98b35e5d6      11/04/24 18:14:42
14. awsbackup:job-b0418e52-5b94-e19b-bea3-b9deada11d31      11/05/24 00:16:13
15. rds:test1-2024-11-05-06-08                              11/05/24 06:08:24
16. awsbackup:job-b8b35813-6b6c-a770-efa6-5040866aeb5c      11/05/24 07:07:14
17. awsbackup:job-7f0a3c00-ca58-230a-b91c-6542aa872fee      11/05/24 12:16:15
18. awsbackup:job-bcbb9a71-e3ab-7233-997b-e5501b877369      11/05/24 18:13:58
19. awsbackup:job-af437491-7704-cd7e-af1a-076ec08dd7aa      11/06/24 00:16:33
20. rds:test1-2024-11-06-06-08                              11/06/24 06:08:12
21. awsbackup:job-415c8ff4-fb81-3a3d-1081-1ee641a8e277      11/06/24 06:24:51
22. awsbackup:job-e40623b8-2b11-cc9f-3578-cc3137a7f5c5      11/06/24 12:16:37
23. awsbackup:job-a1c7c79b-500e-ad4a-4823-65fda90b72c9      11/06/24 18:14:55
24. awsbackup:job-f68ab550-83b4-ece4-1b2f-0431bc5b0ec2      11/07/24 00:15:28
25. rds:test1-2024-11-07-06-06                              11/07/24 06:06:40
26. awsbackup:job-3d384823-1ada-0adc-507b-7812f149c5fe      11/07/24 06:14:06
27. awsbackup:job-75ffeee6-a284-3665-8e9c-82199a29d472      11/07/24 12:18:03
28. awsbackup:job-1b4ff37e-8e56-1922-574a-b54b21df4d59      11/07/24 18:14:52
29. awsbackup:job-a4ce499d-ce39-649f-aac8-78a2ea7b7c14      11/08/24 00:14:56
30. rds:test1-2024-11-08-06-07                              11/08/24 06:07:56
31. awsbackup:job-9411b712-fde4-994a-d4a7-5191f45fc092      11/08/24 06:17:28
32. awsbackup:job-ddcb5612-7466-7bd3-4de8-f2eef6d6db43      11/08/24 12:16:20
33. awsbackup:job-390277d7-f922-7d99-73d7-0834ec018201      11/08/24 18:13:40
34. rds:test1-2024-11-08-21-02                              11/08/24 21:02:25
35. rds:test1-2024-11-08-22-27                              11/08/24 22:27:20
36. awsbackup:job-6997366e-c33b-6921-9b92-137eb69ba04f      11/09/24 00:17:40
37. rds:test1-2024-11-09-06-10                              11/09/24 06:10:45
38. awsbackup:job-37693f3e-bd75-9ed2-af65-79f98e978817      11/09/24 06:32:33
39. awsbackup:job-4ebe17e8-1cac-1f43-69dd-17a9de07481a      11/09/24 12:16:21
40. awsbackup:job-95effa17-11d3-543f-7881-876f839be3ef      11/09/24 18:15:28
5
Enter a name for the new database: test5
---------------------------------------------
You've chosen:
source  : test1
snapshot: rds:test1-2024-11-03-06-07
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
