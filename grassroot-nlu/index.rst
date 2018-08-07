.. Grassroot-nlu documentation master file, created by
   sphinx-quickstart on Sun Aug  5 11:20:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Grassroot-NLU's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Grassroot-nlu is an nlu engine trained for parsing through common Grassroot user
input and extracting intent and entities from said text.

Getting Started with Grassroot-NLU
----------------------------------

There are multiple ways one could get the server up. A popular option is 
building a docker image from this current directories parent directory (which 
should contain a :file:`Dockerfile`). Open a terminal and run ::

   $ sudo docker build -t grassroot-nlu .

Please be aware of the '.' at the end of the above command. It is a necessary
part of the command.

Building a docker image will download necessary dependencies and behave 
predictably. Before running the image, make sure to have the necessary aws access
key id and aws secret key which should be passed as environment variables 
when running the image, like so ::

   $ sudo docker run -e AWS_ACCESS_KEY_ID='ACCESSKEYVALUE' -e AWS_SECRET_ACCESS_KEY='SECRETKEYVALUE' -p 5000:80 grassroot-nlu

This runs a docker container exposing port 80, mapped to port 5000.

Alternatively, if you prefer a docker free environment, then simply open a terminal
in the directory containing :file:`main.py` and run ::

   $ bash depends.sh

which will download and install all necessary dependencies and follow it up
with ::

   $ python3 main.py

.. warning::

   This alternative installation only works on Linux systems, preferably Ubuntu
   16.04 with Python 3


Demo Client
-----------

For your convenience and as an example a demo client is provided below ::

    import os
    import requests
    import json

    base_url = input('Enter base url: ')
    uid = None

    def emulate():
        global uid
        # SECTION 1
        # Request sent: call a vote
        print('\nSECTION 1')
        raw = requests.get('%s/parse?text=call a vote&uid=%s' % (base_url, uid)).content.decode('ascii')
        ret_val = json.loads(raw)
        print(ret_val)
        uid = (ret_val['uid'])
        # SECTION 2
        # Request sent: tomorrow
        # Tells the engine to look for text with certain uid
        # in this case that text is 'call a vote'.
        # once text is found the value added below, 'tomorrow' is appended
        # and the new text value is sent for parsing and returned.
        print('\nSECTION 2')
        raw = requests.get('%s/parse?text=tomorrow&uid=%s' % (base_url, uid)).content.decode('ascii')
        ret_val = json.loads(raw)
        print(ret_val)
        uid = (ret_val['uid'])    
        # SECTION 3
        # In this case though the uid passed to the api points to the text 'call a vote tomorrow' created
        # by the first two sections, the uid and its associated text are ignored.
        # This is thanks to process identifier that identifies what is to be done with
        # recieved text. In this case it would recognize the text below as a new entry
        # and disregard any uid recieved with request.
        print('\nSECTION 3')
        raw = requests.get('%s/parse?text=find me volunteers for a protest this friday&uid=%s' % (base_url, uid)).content.decode('ascii')
        ret_val = json.loads(raw)
        print(ret_val)
        uid = (ret_val['uid'])

    emulate()

copy and paste this code in a file which we will call :file:`demo_client.py`.
then run the file with ::

    $ python3 demo_client.py

This will prompt you to enter a base url. If you running Grassroot-NLU from a
docker conatiner and have used the above port mapping then enter :file:`http://localhost:5000`
This will also work where the engine is started from running :file:`python3 main.py` 

If you have hosted it online somewhere then enter the base domain and path to the engine prior
to :file:`/parse`.

The demo client will demonstate how to implement dynamic text construction as well as how 
to pass general queries to the engine.

Output
------

The basic output for a request like :file:`call a meeting tomorrow` is ::

    {
     "parsed": {
      "intent": {
       "name": "call_meeting",
       "confidence": 0.0
      },
      "entities": [
       {
        "entity": "datetime",
        "value": "YYYY-MM-DDTHH:MM",
        "start": 15,
        "end": 23
       }
      ],
      "text": "call a meeting tomorrow"
     },
     "uid": "8e8df664-32ab-xxxx-a896-0f650rtn92x0",
     "date": "2018-08-07 15:45:24.127244",
     "past_lives": []
    }
    
All output conforms to this basic structure with variable intents and entities.


Core Functions
--------------

.. automodule:: main
   :members:

.. automodule:: config
   :members: