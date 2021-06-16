# Server_client

What we did til now 

In our code, there are three thread which works in parallelly..

1). The job of the First thread  is to accept TCP multi client connection (one client or more than one client)

2.) The job of the second thread is to try to establish a connection with the TCP server (Because we tried to implement the code in such a way that it works in parallel as a TCP server-client) 

3.) The task of the third thread is to check that the file has been received or not and, if received, to forward it to the adjacent nodei.e to forward it to the adjacent client and server)
