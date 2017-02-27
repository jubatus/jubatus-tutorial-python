Jubatus Tutorial in Python
==========================

* Jubatus Python Client is required for this tutorial (`pip install jubatus`).
* For details, see [Quick Start](http://jubat.us/en/quickstart.html) and [Tutorial](http://jubat.us/en/tutorial/).

Brief Usage
-----------

```
$ wget http://qwone.com/~jason/20Newsgroups/20news-bydate.tar.gz
$ tar -xvzf 20news-bydate.tar.gz

$ jubaclassifier --name tutorial --configpath config.json
$ python tutorial.py
```

Note
----

If you encounter following problem,

```
socket.error: [Errno 99] Cannot assign requested address
```

try this:

```
$ sudo /sbin/sysctl -w net.ipv4.tcp_tw_recycle=1
```
