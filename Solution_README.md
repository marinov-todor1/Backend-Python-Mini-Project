# Tenyks Backend Take-Home Mini-Project 🦾


Dear Tenyksians, 

Below I am describing the structure of my submission and the process it took to have it done to this stage.

Note: Install requirements.txt before running

The SDK call samples are in the Processor.py

## Overview
The overall design is inteded to split the code into four logical pieces:
1. Load & Process - A loader /Load.py/ to deal with the reading of images/annotations from the file system and
a processor /Processor.py/ to generate the internal representation for datasets, models and images.
The processor is constructed to load all dataset data in bulk.


2. DataObjects.py defines the internal representation which should be used for processing and reading/writing from the DB.
Reader.py and Writer.py were meant for communication with the DB, where the Writer could potentially utilze the Singleton
pattern if the DB does not have auto-lock feature. Both are not implemented, due to the DB itself is missing.


3. Test.py contains some lightweight tests. At the very end pytest started throwing some strange error 
(cannot detect the imported modules), which I couldn't fix. The tests are working, but pytest isn't...


4. The Database itself, I couldn't finish. I had to choose between sending an improvised implementation of it or research
proper scaling structures and send only an ERG diagram. I choose the latter.
   1. My idea is to use horizontal partitioning per dataset, in order to search only through relevant pictures. 
   Also, the implementation could (and probably should) be done with only one instance of Models and Training_Datasets, 
   if Model data is uniform for all datasets.
   2. Further vertical segmentation could be utilized, if image columns are not always requested in bulk.

![ERD](ERD.jpg)


## The Process

After I took the first look at the README.md I was "Wow, that's big and probably challenging!".
And I was right :).... but I was also right that with enough reading it is manageable.

First I started with the readily available advices and went into researching design patterns and interfaces,
this was my first encounter with the topic. All was understood, but I still couldn't imagine where to expect
specific problems in order to apply the respective designs in advance.. hence, I decided to come back to this later, if I have time.

Next, I decided to just start writing and take baby steps, first let's load all the necessary data into the program memory.

Having that done I decide to focus on the pre-processing and started with the internal representation.

Later, something, which I should  have probably done earlier, I started thinking about the whole "System design".
From my studies I knew only the MVC structure and this was my starting point. I modified it a little to reflect the specifics
of the homework.

Time for tests, great, but that was my first encounter with this topic as well. So I had to do some proper research before
I write anything.

With no time left, I decided to research scalable database design instead of sending just any DB. The simplest optimizations
I came up with (for relational DB) were horizontal and vertical partitioning. Which, I believe, will bring significant 
benefits at scale (not much in the beginning).

As you can see, I've learned a lot, and ultimately I'm very grateful for that challenge! :) 

I'm sure my delivery is far from perfect, and I would highly appreciate your constructive feedback 
(e.g. as in the Basic Example)

Cheers,
Todor