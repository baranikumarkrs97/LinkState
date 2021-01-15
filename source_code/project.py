
import csv
import sys
import os

# Python version : 2.7
# Author : Barani Kumar Kalangal Ramasamy Soundararajan (A20434813)
# CS-542 Project 


# intializing global variable 
# this holds the matrix with routers and link costs between them
global G
G = []
global Path
Path = []
# this holds link cost of from each and every router to other routers
Router_list = []
# if 0 matrix is not yet set , if 1 matrix already been set from the input file 

# list holds the number of routers eg : [1,2,3,4,5]
routers = []
# holds the total distance cost from one router to another 
link_cost = {}
# nodes which not incorporated in the algorithm
nodesTobe = {}
# previous node
previous = {}
# nodes which are added in the set , incorprated in the algorithm
nodesAdded = {}
# holds the next hop from the source to destination
nextHop = {}
# holds the path from one router to another 
route = []
# source router 
src = 0
#destination router
dest = 0

src_select = 0

flag = 0

## -----------------------------------------------------Fuctions Definitions----------------------------------------------------------

# Function to print the choices when program starts.

def Menu():

    print "\n---------------------Link State Routing Simulator-----------------------\n"
    print "|                          1->Create Network                               |"
    print "|                    2->Build a Connection Table                           |"
    print "|               3->Shortest route from source to destination               |"
    print "|                          4->Delete a router                              |"
    print "|                            5->Add a router                               |"
    print "|                            6->Best Router                                |"
    print "|                                7->Exit                                   |"
    print "\n--------------------------------------------------------------------------\n"
    pass


def printRouterMatrix(Router_list):

    # Function to print the network matrix.

    line =0
    while line<len(Router_list):
        for c in Router_list[line]:
            print c,
        print 
        line += 1


# Function to store the distances in dictionary format.


def costInitialization(R_list):


    global link_cost
    global routers
    global graph
    graph = {}
    link_cost = {}
    routers = []

    # setting the cost between one to another 

    i=0
    while i < len(R_list):
        tempdict = {}
        j=0
        while j < len(R_list):
            if i!=j and R_list[i][j]!=-1:
                tempdict[j+1] = R_list[i][j]
            j += 1 
        link_cost[i+1] = tempdict
        # appending all the routers in the in routers dictionary
        routers.append(i+1)
        i += 1
    
    graph=link_cost
    return graph


def createMatrix(fname):

    # function processes the input file and stores as a matrix
    
    global matrix_set
    global Router_list
    matrix_set = 0
    Router_list = []

    with open(fname) as fhandle:
        Router_list=[list(map(int,line.split(" "))) for line in fhandle]      # Data from input file is stored in a two dimensional list(array).
    matrix_set = matrix_set + 1 

    G=Router_list

    print "\n-----------Original topology matrix-------------\n"
    printRouterMatrix(Router_list)
    costInitialization(Router_list) 
    print "Total number of routers :",len(routers)
    
def linkState(src):

    # implementation of dijkstra's algorithm

    global link_cost
    global routers
    global nodesTobe
    global previous
    global nodesAdded
    global nextHop

    tempList = []
    

    # flushing out all the old values ( for delete router )

    nodesTobe.clear()
    previous.clear()
    nextHop.clear()
    nodesAdded.clear() 

    # intializing the variables to none 

    for i in routers:
        nodesTobe[i]=None
        previous[i]=None 
        nextHop[i]=None 
        nodesAdded[i]=None 
    
    # setting the cost for source node as zero
    
    nodesTobe[src] = 0         
    
    # loop will run for all the routers 

    node = src
    node_cost = 0
    
    while True:
        for nxt_node, cost in link_cost[node].items():

            if nxt_node not in nodesTobe: 
                continue
            tempCost = node_cost + cost

    # setting the shortest distance from source to all the adjacent nodes

    #searching the router which are not added in the route 
           
            if nodesTobe[nxt_node] > tempCost or not nodesTobe[nxt_node] :
                nodesTobe[nxt_node] = tempCost
                previous[nxt_node] = node

    # updating the next router from the source for connection table
                if not nextHop[node]:
                    nextHop[nxt_node] = nxt_node
                else: 
                    nextHop[nxt_node] = nextHop[node]
                    
        nodesAdded[node] = node_cost
        del nodesTobe[node]
        
        check = 1
        # print "nodesTobe=",nodesTobe 
        for x in nodesTobe:
            if nodesTobe[x]:
                check = 0
                break

        if check or not nodesTobe:
            break


        # sets only the nodes which has finite distance to the router
        for n in nodesTobe.items():
            if n[1]!= None :
                tempList.append(n)

        # seleting the router with minimum distance from source router 

        tempList.sort(key = lambda x: x[1])
        node, node_cost = tempList[0]
        tempList = []


def deleteRouter(fname,r):   
    
## function to delete router
    
    ##removing values from matrix
    
    Router_list.pop(r)                 
    for i in range(len(Router_list)):
            Router_list[i].pop(r)

    print "\n Modofied topology matrix:\n"

    printRouterMatrix(Router_list)

    # setting the cost for each router

    costInitialization(Router_list)

    return Router_list

def addRouter(fname,new_list):
   
    # appending the new cost list to the existing router matrix
    j = 0 
    new_list.reverse()
    for i in range(len(Router_list)):
        while j < len(new_list):
            k = new_list[j]
            Router_list[i].append(k)
            j = j + 1
            break

    new_list.reverse()
    # setting the cost between same router as 0
    v = 0
    new_list.append(v)
    Router_list.append(new_list)

    # printing the modified matrix

    print "\n...........Updated Topology matrix............."
    printRouterMatrix(Router_list)
    costInitialization(Router_list)

    return Router_list

def minimumCost_path(source, destination):
    # shortest route from source to destination    
    global route
    route = []

    # appending the destination to the path
    route.append(destination)
    while True :
        if destination == source:
            break
        route.append(previous[destination])
        destination = previous[destination]
    # reversing bring the destination from start to end of the list
    route.reverse()
    return route


def connectionTable(nextHop):
    print "\nRouting Table"
    print "\nDestination\tNext Hop"
    for key in nextHop:
        print key,"\t\t", nextHop[key]

def print_path(route_1):
    print "\nThe shortest route from router %s to router %s : " %(src, dest),
    for i in range(len(route_1)):
        print route_1[i]," ",
    cost = 0
    if nodesAdded[dest]:
        cost = nodesAdded[dest]
    print "\nThe total cost between router %s to router %s : %s" %(src, dest,cost)



##----------------------------------------------------------------------------Program Begins----------------------------------------------------------------
while True :
    Menu()
    try:
        user_input = (int(raw_input("Selection:")))
    except :
        print "Please Enter a valid input"
        continue

    if user_input > 7 or user_input < 1 :

        print "Please enter a valid selection"
        continue
    
    if user_input == 1:

        # Creating the network matrix 
        
            input_file = raw_input("\nEnter the Input topology file name with (.txt) : ")

            if os.path.isfile(input_file):
                createMatrix(input_file)
                src = 0
                dest = 0
                flag = 1 
                
            else:
                print "\nNo such file in the directory"
                break

    

    elif user_input == 2:

        # Printing connection table

        if flag ==1 :

            src = int(raw_input("\nSelect a source router : "))
            src_select=1

            if src > 0 and src <= len(Router_list):
                linkState(src)
                connectionTable(nextHop)
            else:
                src = 0
                print "\nPlease enter a valid source router."
        else:
            print "\nNo network topology updated"
            break
            
    elif user_input == 3:

        # shortest path and cost 
    
        if flag == 1 :
            

            dest = int(raw_input("\nSelect a destination router : "))
            
            if src == dest:
                print "source router == destination router ,Please do try again with different router"
                continue
                
            if dest > 0 and dest <= len(Router_list):
                if src_select != 1:
                    src =1
                    linkState(src)
                Path=minimumCost_path(src,dest)
                print_path(Path)
                
            else:
                print "\nPlease enter a valid destination router."

        else :
            print "\nNo network topology updated"
            continue 

    elif user_input == 4:

        # deleting a router 
        
        d=int(raw_input("Enter the router to be deleted:"))
        
        if d == dest or d == src:
            d=d-1
            G=deleteRouter(input_file,d)
            linkState(src)
            connectionTable(nextHop)
            print "\nRouter ",d+1," is down"
        
        else :
            d=d-1
            G=deleteRouter(input_file,d)
            linkState(src)
            connectionTable(nextHop)
            
            if not previous[dest] :
                print "\nThere does not exist any route from Source : %s to Destination : %s. \nPlease select a different destination router. "  %(src, dest)
            else:
                Path=minimumCost_path(src,dest)
                print_path(Path)
            



    
    elif user_input == 5:

        # adding router
        
        global new_matrix
        new_matrix = []
        print "Total number of routers",len(routers)
        c=str(raw_input("Enter the cost from new router to existing routers with (,) : "))
        new_matrix = list(map(int,c.split(",")))
        G=addRouter(input_file,new_matrix)
        linkState(src)
        connectionTable(nextHop)
        if not previous[dest] :
            print "\nThere does not exist any path , Enter different destination  "  %(src, dest)
        else:
            Path=minimumCost_path(src,dest) 
            print_path(Path)

    elif user_input == 6 :

        #displying the optimal router

        tempDict ={}
        router=[]
        print "Total sum of distances for all the routers:"
        for v in routers:
            sum = 0
            linkState(v)
            ## calculating the sum of all the routers as start router
            for i in nodesAdded:    
                sum = sum + nodesAdded[i]
            router.append(sum)      
            tempDict[sum] = v     
        router.sort()   
                           
        ##sorting bring the minium value as first

        print tempDict
        print "The Best Router is :", tempDict[router[0]]


    elif user_input == 7 :
        print "\nExiting the application\n"
        quit()

##-------------------------------------------------------------------------------------------------------------------------------------------------------



