# How it works and file breakdown
genUsers.py, when pointed at an elasticsearch instance/endpoint, 
  creates a random graph where nodes represent users and
  edges represent connections between users.
  This is based on the Graph class in genNodes.py.
  
Connections.py makes 2 classes available, a User and a simple GraphApi.
  User stores and searches for its connections, up to the 3rd degree.
    (if A is connected to B and B is connected to C and C is connected to D,
      then A's 1st degree connection is B, 2nd degree connection is C, and 3rd degree connection is D)
  GraphApi is the primary workhorse for User's requests. 
    It builds and sends requests, then parses the response to be understood by User.
    If incorporated into a larger API scheme, it would be recommended to rename the class and methods.
    But for the scope of this project, it should be clear enough.
 
connectionsES.py is a RESTful API that calls on the logic in Connections.py to deliver data and results.
