.. _design:

Design Decisions
################

Why not compile template in crutch.py?

Open Issues
###########

* How best should the unified search box work? Right now it is not using anything more than
  a simple case-insensitive search of everything (or just projects/sections). I was using a
  regex search but that became a pain. What about starting on word boundaries, start of string,
  etc?
