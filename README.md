# SunopsisLogViewer
SLV - application to  fast revision for Sunopsis logs. 

Sunopsis is old, unsupported ETL application to move data from databases.
It's interface is written in java and dramatic slow. 
The log module select all logs from database and present on screen in tree-like view. 
Even if you are interesting only to see logs from one session, application download all unnecessary information witch consume lot of time. 

The purpose to create SunopsisLogViewer was to create a fast and easy way to see logs, filter them an analyse.

What do you need?
- Python 3.7
- Flask
- cx_oracle
- ...
