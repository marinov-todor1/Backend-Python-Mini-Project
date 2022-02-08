# Backend Python Mini-Project 🦾

## Overview
The overall design is inteded to split the code into four logical pieces:
1. Load & Process - A loader /Load.py/ to deal with the reading of images/annotations from the file system and
a processor /Processor.py/ to generate the internal representation for datasets, models and images.
The processor is constructed to load all dataset data in bulk.


2. DataObjects.py defines the internal representation which should be used for processing and reading/writing from the DB.
Reader.py and Writer.py are meant for communication with the DB. Both are in progress


3. Test.py contains some lightweight tests. Pytest is misbehaving and will be debugged at the end.

4. For the DB the idea is to use horizontal partitioning per dataset and mode, in order to maintain the performance at scale. 
Each new dataset processed with any given model or old dataset processed with new model will be recorded in
new separate table. Further vertical segmentation could be utilized, if image columns are not always requested in bulk.

![ERD](DB_ERD.jpg)