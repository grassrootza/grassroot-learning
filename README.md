# grassroot-learning
Machine learning components (some WIP) of Grassroot platform
The core component is a natural language date/time parser, made with a custom-trained version of Stanford NLP's Named Entity Recognizer and Stanford NLP's SUTime. It's trained to recognize a wide variety of misspelled and malformed inputs. Output is a Java 8 LocalDateTime object, which is sent as an ISO String via JSON.


## Testing
The selo_test.py script requires some set-up before it will run correctly. You will need to install a couple python libraries, create a few directories and generate some files. 

Install libpq-dev, python-dev, and psycopg2 through your preferred method   

In the same directory as grassroot-learning, create a new directory named **grassroot-resources**. Inside of **grassroot-resources**, create a folder named **testing**. Put your *test_config.properties* file - which contains your auth token and database information - inside of **testing**. **testing** will also host two additional folders: **tmp** and **hist**. If this is your first time running the script, create an empty file titled *selo_errors_X.txt* inside of **hist**, where X corresponds to the numerical representation of last month (for example, if the current month is August, the file would be *selo_errors_7.txt*).  
