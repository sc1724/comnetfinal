To test multicast program run in the order below and on the corresponding nodes. All starting from mininet@mininet-vm

1. sudo python topo7.py
2. In mininet --> xterm s d1 d2 d3 r1 r2 r3 r4 r5 r6 r7
3. In d1 terminal --> python3.5 server1.py
4. In d2 terminal --> python3.5 server2.py
5. In d3 terminal --> python3.5 server3.py
6. In r1 terminal --> python3.5 router1.py
7. In r2 terminal --> python3.5 router2.py
8. In r3 terminal --> python3.5 router3.py
6. In r4 terminal --> python3.5 router4.py
7. In r5 terminal --> python3.5 router5.py
8. In r6 terminal --> python3.5 router6.py
9. In r6 terminal --> python3.5 router7.py
10. In s terminal --> python3.5 udpclient.py

To change the k value and data value go to line 16 and 17 respectively in the udpclient.py file.
