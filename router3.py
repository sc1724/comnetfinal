from socket import socket, AF_INET, SOCK_DGRAM
from packet import *
from threading import Thread
from textwrap import wrap

#Creates new router
class udprouter():

    # For sake of assignment I am letting each router know eachothers rt
    def __init__(self, id, port, ip):
        self.port = port
        self.id = id
        self.ip = ip
        self.rt = { 'routes': [{'id': 101, 'ip': '192.168.1.1', 'gateway': '192.168.1.2', 'port':8880},
        {'id': 202, 'ip': '10.0.1.1', 'gateway': '10.0.1.0', 'port':8882}] }
        self.graph = {} # {'id' : {'id': costs,...}}
    # Using the dst received in packet finds the corresponding dst address
    def search_dst_addr(self, dst):
        for x in range(len(self.rt['routes'])):
                if self.rt['routes'][x]['id'] == dst:
                        return (self.rt['routes'][x]['ip'], self.rt['routes'][x]['port'])
        return (self.ip, self.port)

    # Sends packet to dst address
    def handle_sending(self, packet, server):
        s = socket(AF_INET, SOCK_DGRAM)
        s.sendto( packet, server )
        print('Sending To: ', server)
        s.close()
        return 0

    # Waits to receive a packet anxd if the correct type starts new thread to sent that packet
    def handle_packets(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        while True:
            packet, addr = s.recvfrom(1024)
            print("Received From: ", addr)
            pkttype = read_header(packet)
            if pkttype == 0:
                pkttype, seq, ttl, src = read_hello(packet)
                if len(self.graph[self.id]) == 0 : # Populate graph with immediate neighbors
                    self.graph[self.id].append({src : '1'})
            elif pkttype == 1: #Populate graph with the rest of the routers
                pkttype, seq, ttl, src, ls = read_update(packet)
                update = wrap(ls,24)
                for i in range(len(update)):
                     x = wrap(update[i],8)
                     if len(self.graph[x[2]]) == 0:
                         self.graph[x[2]].append({x[0] : x[1]})
            elif pkttype == 2:
                pkttype, seq, pktlen, src, kval, dst1, dst2, dst3, nval, kremain = read_datapacket(packet)
                data=read_data(packet)
                dst = 0
                if dst2 == None & dst3 == None:
                    server = self.search_dst_addr(dst1)
                    thread = Thread(target=self.handle_sending(packet,server))
                    thread.start()
                elif dst2 != None and dst3 == None:
                    path1, distance1 = self.dijkstra(self.graph,src,dst1)
                    path2, distance2 = self.dijkstra(self.graph,src,dst2)
                    distancek1 = min(distance1, distance2)
                    if distancek1 == distance1:
                        dst = dst1
                    else:
                        dst = dst2
                    if kval == 1:
                        server = self.search_dst_addr(dst)
                        thread = Thread(target=self.handle_sending(packet,server))
                        thread.start()
                    else:
                        if path1[1] == path2[1]:
                            server = self.search_dst_addr(dst1)
                            thread = Thread(target=self.handle_sending(packet,server))
                            thread.start()
                        else:
                            server1 = self.search_dst_addr(dst1)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst1, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()
                            server2 = self.search_dst_addr(dst2)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst2, nval = 3, kremain = kremain, data = data)
                            thread2 = Thread(target=self.handle_sending(packet,server2))
                            thread2.start()
                else:
                    path1, distance1 = self.dijkstra(self.graph,src,dst1)
                    path2, distance2 = self.dijkstra(self.graph,src,dst2)
                    path3, distance3 = self.dijkstra(self.graph,src,dst3)
                    distancek1 = min(distance1, distance2, distance3)
                    if distancek1 == distance1:
                        dst = dst1
                    elif distancek1 == distance2:
                        dst = dst2
                    else:
                        dst = dst3
                    if kval == 1:
                        server = self.search_dst_addr(dst)
                        thread = Thread(target=self.handle_sending(packet,server))
                        thread.start()
                    elif kval == 2:
                        if path1[1] == path2[1]:
                            server = self.search_dst_addr(dst1)
                            thread = Thread(target=self.handle_sending(packet,server))
                            thread.start()
                        elif path1[1] == path3[1]:
                            server = self.search_dst_addr(dst1)
                            thread = Thread(target=self.handle_sending(packet,server))
                            thread.start()
                        elif path2[1] == path3[1]:
                            server = self.search_dst_addr(dst2)
                            thread = Thread(target=self.handle_sending(packet,server))
                            thread.start()
                        else:
                            sortdis = [distance1, distance2, distance3].sort()
                            if sortdis[0] == distance1:
                                dst = dst1
                            elif sortdis[0] == distance2:
                                dst = dst2
                            else:
                                dst = dst3
                            server1 = self.search_dst_addr(dst)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()

                            if sortdis[1] == distance1:
                                dst = dst1
                            elif sortdis[1] == distance2:
                                dst = dst2
                            else:
                                dst = dst3
                            server2 = self.search_dst_addr(dst)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst, nval = 3, kremain = kremain, data = data)
                            thread2 = Thread(target=self.handle_sending(packet,server2))
                            thread2.start()
                    else:
                        if path1[1] == path2[1] and path1[1] == path3[1]:
                            server = self.search_dst_addr(dst)
                            thread = Thread(target=self.handle_sending(packet,server))
                            thread.start()
                        elif path1[1] == path2[1]:
                            server1 = self.search_dst_addr(dst1)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 2, dst1 = dst1, dst2 = dst2, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()

                            server3 = self.search_dst_addr(dst3)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst3, nval = 3, kremain = kremain, data = data)
                            thread3 = Thread(target=self.handle_sending(packet,server3))
                            thread3.start()
                        elif path1[1] == path3[1]:
                            server1 = self.search_dst_addr(dst1)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 2, dst1 = dst1, dst2 = dst3, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()

                            server2 = self.search_dst_addr(dst2)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst2, nval = 3, kremain = kremain, data = data)
                            thread2 = Thread(target=self.handle_sending(packet,server2))
                            thread2.start()
                        elif path2[1] == path3[1]:
                            server2 = self.search_dst_addr(dst2)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 2, dst1 = dst2, dst2 = dst3, nval = 3, kremain = kremain, data = data)
                            thread2 = Thread(target=self.handle_sending(packet,server2))
                            thread2.start()

                            server1 = self.search_dst_addr(dst1)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst1, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()
                        else:
                            server1 = self.search_dst_addr(dst1)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst1, nval = 3, kremain = kremain, data = data)
                            thread1 = Thread(target=self.handle_sending(packet,server1))
                            thread1.start()

                            server2 = self.search_dst_addr(dst2)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst2, nval = 3, kremain = kremain, data = data)
                            thread2 = Thread(target=self.handle_sending(packet,server2))
                            thread2.start()

                            server3 = self.search_dst_addr(dst3)
                            packet = create_data(pkttype = pkttype, seq = seq, src = src, kval = 1, dst1 = dst3, nval = 3, kremain = kremain, data = data)
                            thread3 = Thread(target=self.handle_sending(packet,server3))
                            thread3.start()

            else:
                pkttype, seq, src, dst = read_dataack(packet)
                server = self.search_dst_addr(dst)
                thread = Thread(target=self.handle_sending(packet,server))
                thread.start()
        s.close()
        return 0

    def dijkstra(self,graph,src,dest,visited=[],distances=[],predecessors=[]):
        if src not in graph:
            raise TypeError('The root of the shortest path tree cannot be found')
        if dest not in graph:
            raise TypeError('The target of the shortest path cannot be found')
            # ending condition
        if src == dest:
            # We build the shortest path and display it
            path=[]
            pred=dest
            while pred != None:
                path.append(pred)
                pred=predecessors.get(pred,None)
            # reverses the array, to display the path nicely
            readable=path[0]
            for index in range(1,len(path)): readable = path[index]+'--->'+readable
            #prints it

            return path[::-1], distances[dest]
            print('shortest path - array: '+str(path))
            print("path: "+readable+",   cost="+str(distances[dest]))
        else :
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src]=0
            # visit the neighbors
            for neighbor in graph[src] :
                if neighbor not in visited:
                    new_distance = distances[src] + graph[src][neighbor]
                    if new_distance < distances.get(neighbor,float('inf')):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = src
            # mark as visited
            visited.append(src)
            # now that all neighbors have been visited: recurse
            # select the non visited node with lowest distance 'x'
            # run Dijskstra with src='x'
            unvisited={}
            for k in graph:
                if k not in visited:
                    unvisited[k] = distances.get(k,float('inf'))
            x=min(unvisited, key=unvisited.get)
            self.dijkstra(graph,x,dest,visited,distances,predecessors)


if __name__ == '__main__':
        print("Router Started...")
        udp_router = udprouter(id=203, port=8883)
        udp_router.handle_packets()
