# TASKS:
1)	create fixture which will return the array of all people
2)	create test which checks length of array of all people with "count" field in response of simple get /people request
3)	create test which checks that names of all people are unique
4)	create a few tests for validation that search for people is case insensitive
5)	create test which will validate that there is no page with number 0 for people request 
6)	create parametrized test which will check that there are 3 Skywalker's, 1 Vader, 2 Darth's (using ?search)
7)	create fixture which will return schema of people object
8)	create test which will validate that all people objects contain required schema fields
9)	* screate factory fixture which will return search people results
10)	* create test which will check that search for any char in English alphabet or any number from 0 to 9 will return number of results >0 except cases of search by 6, 9 and 0. It is not allowed to use loops inside the test body.
11)	* try to suggest and implement any other meaningful and suitable tests for "get /people" request
12)	** try to suggest (and implement if possible) any meaningful and suitable tests for "get /people" requests with parameter ?format=wookiee 
13)	** There is some bug with implementation of Wookiee format. It would be great if you can find that and say a few words with your thoughts what is the root cause.
