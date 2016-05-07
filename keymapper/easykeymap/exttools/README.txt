Developer Notes:

The exttools directory is the location where Easy AVR keeps its "batteries
included" AVR loader tools.  The exttools directory should not commit .exe
files to the source repository, but if a developer places exe files in this
location on their local copy then the py2exe script will include them in
the distribution.

Users of the source distribution may also place loader tools in this location
if they don't want to install them or modify their PATHs.
