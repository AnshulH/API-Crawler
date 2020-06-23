# Basic Public APIs List Crawler

This is an api crawler that fetches public apis data from [POSTMAN](https://documenter.getpostman.com/view/4796420/SzmZczsh?version=latest). Support for rate limiting and pagination. 

More reference - Public APIs github repo (https://github.com/public-apis/public-apis) is a collective list of free APIs for use in software and web development. 


### Steps to run the code

- To fetch all api data to database ``` python3 main.py```   in source file
    - All data should be fetched by this command to database files  
- To run queries on data base simply run ``` python3 queryDB.py```    



### Database Schema

[DB Schema](https://drive.google.com/file/d/1qwK9msB8ZlnIQVgs0HgEg5_S3OP2bYmm/view?usp=sharing)


### Points Achieved

- [x] Your code should follow concept of OOPS
- [x] Support for Authentication & token expiration
- [x] Support for Pagination to get all data
- [x] Support for Rate limiting
- [x] Crawled all API entries for all categories and stored it in a database

### Things to Improve with time / TODO List

- Database is not scalable for more large number of entries. Use another Scalable Db framework.
- Need to implement checks while writing to db to avoid copies.
- A few unnecessary token calls are bring made and can be avoided.
- Implement better async code to speed up processing.
- Use docker to run the code.
- Improve async implementation

