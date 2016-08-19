# grassroot-learning
Machine learning components (some WIP) of Grassroot platform
The core component is a natural language date/time parser, made with a custom-trained version of Stanford NLP's Named Entity Recognizer and Stanford NLP's SUTime. It is trained to recognize a wide variety of misspelled and malformed inputs. It converts the input into a Java 8 LocalDateTime object, which is sent as an ISO String via JSON.
