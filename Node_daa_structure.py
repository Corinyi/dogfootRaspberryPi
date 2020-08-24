# Node and Route information data structure

class markerNode:
    """
    Save marker data
    Floor : current floor
    Id : id of the marker
    northConnectedNode : connected node which located in north
    southConnectedNode : connected node which located in south
    westConnectedNode : connected node which located in west
    eastConnectedNode : connected node which located in east
    nextNode : next node for the route

    1. Destination Node
        For elevator, toilet, exit etc
        Use Id from 1~50
    2. Marker Node
        For the way point
        Use Id from over 50
    """
    def __init__(self, name, floor, id, north = None, south = None, west = None, east = None):
        self.name = name
        self.floor = floor
        self.id = id
        self.northConnectedNode = north
        self.southConnectedNode = south
        self.westConnectedNode = west
        self.eastConnectedNode = east
        self.next = None

    def update(self, north = None, south = None, west = None, east = None):
        self.northConnectedNode = north
        self.southConnectedNode = south
        self.westConnectedNode = west
        self.eastConnectedNode = east
        self.next = None

class markerGraph:
    """
    Fixed map graph for Seolleung station
    Not made yet
    """
    def __init__(self):
        self.size = 1000

class routeData:
    """
    Stack the ordered route information
    """
    def __init__(self, markerNode = None):
        self.head = markerNode
        self.routeLength = 1

    def insertFirstNode(self, firstNode):
        new_node = firstNode
        temp_node = self.head
        self.head = new_node
        self.head.next = temp_node
        self.routeLength += 1

    def insertLast(self, insertNode):
        node = self.head
        while True:
            if node.next == None:
                break
            node = node.next

        new_node = insertNode
        node.next = new_node
        self.routeLength += 1

    def selectNode(self, num):
        if self.routeLength < num:
            print("Overflow")
            return
        node = self.head
        count = 0
        while count < num:
            node = node.next
            count += 1
        return node

    def deleteHead(self):
        node = self.head
        self.head = node.next
        del node
        self.routeLength -= 1

    def length(self):
        return str(self.routeLength)

def createB2mapInSeooleung():
    """
    Seolleung station marker nodes in B2 Floor
    :return: way points in Seolleung station B2
    """
    #railWay marker
    global railWay_7_4_Seolleung_B2
    global railWay_8_1_Seolleung_B2, railWay_8_2_Seolleung_B2, railWay_8_3_Seolleung_B2, railWay_8_4_Seolleung_B2
    global railWay_9_1_Seolleung_B2
    # blockWay marker
    global blockWay_51_Seolleung_B2, blockWay_52_Seolleung_B2
    # elevator marker
    global elevator_2_Seolleung_B2

    # railWay marker
    railWay_7_4_Seolleung_B2 = markerNode("Seolleung_7_4_B2", 2, 1)
    railWay_8_1_Seolleung_B2 = markerNode("Seolleung_8_1_B2", 2, 2)
    railWay_8_2_Seolleung_B2 = markerNode("Seolleung_8_2_B2", 2, 2)
    railWay_8_3_Seolleung_B2 = markerNode("Seolleung_8_3_B2", 2, 2)
    railWay_8_4_Seolleung_B2 = markerNode("Seolleung_8_4_B2", 2, 2)
    railWay_9_1_Seolleung_B2 = markerNode("Seolleung_9_4_B2", 2, 2)

    # blockWay marke
    blockWay_51_Seolleung_B2 = markerNode("Seolleung_51_B2", 2, 51)
    blockWay_52_Seolleung_B2 = markerNode("Seolleung_52_B2", 2, 52)

    # elevator marker
    elevator_2_Seolleung_B2 = markerNode("Seolleung_EV_2_B2", 2, 3)

    #update
    railWay_7_4_Seolleung_B2.update(north = blockWay_51_Seolleung_B2, east = railWay_8_1_Seolleung_B2)
    railWay_8_1_Seolleung_B2.update(west = railWay_7_4_Seolleung_B2, east = railWay_8_2_Seolleung_B2)
    railWay_8_2_Seolleung_B2.update(west = railWay_8_1_Seolleung_B2, east = railWay_8_3_Seolleung_B2)
    railWay_8_3_Seolleung_B2.update(west = railWay_8_2_Seolleung_B2, east = railWay_8_4_Seolleung_B2)
    railWay_8_4_Seolleung_B2.update(west = railWay_8_3_Seolleung_B2, east = railWay_9_1_Seolleung_B2)
    railWay_9_1_Seolleung_B2.update(west = railWay_8_4_Seolleung_B2)

    blockWay_51_Seolleung_B2.update(north = blockWay_52_Seolleung_B2, west = railWay_7_4_Seolleung_B2)
    blockWay_52_Seolleung_B2.update(south = blockWay_51_Seolleung_B2, east = elevator_2_Seolleung_B2)

    elevator_2_Seolleung_B2.update(west = blockWay_52_Seolleung_B2)


def createB3mapInSeooleung():
    """
    Seolleung station marker nodes in B3 Floor
    :return: way points in Seolleung station B3
    """
    # railWay marker
    global railWay_2_4_Seolleung_B3
    # blockWay marker
    global blockWay_53_Seolleung_B3, blockWay_54_Seolleung_B3, blockWay_55_Seolleung_B3
    # elevator marker
    global elevator_2_Seolleung_B3

    # railWay marker
    railWay_2_4_Seolleung_B3 = markerNode("Seolleung_2_4_B3", 3, 4)

    # blockWay marker
    blockWay_53_Seolleung_B3 = markerNode("Seolleung_53_B3", 3, 53)
    blockWay_54_Seolleung_B3 = markerNode("Seolleung_54_B3", 3, 54)
    blockWay_55_Seolleung_B3 = markerNode("Seolleung_55_B3", 3, 55)

    # elevator marker
    elevator_2_Seolleung_B3 = markerNode("Seolleung_EV_2_B3", 3, 3)

    #update
    railWay_2_4_Seolleung_B3.update(east=blockWay_55_Seolleung_B3)

    blockWay_53_Seolleung_B3.update(west=blockWay_54_Seolleung_B3, south=elevator_2_Seolleung_B3)
    blockWay_54_Seolleung_B3.update(east=blockWay_53_Seolleung_B3, north=blockWay_55_Seolleung_B3)
    blockWay_55_Seolleung_B3.update(west=railWay_2_4_Seolleung_B3, south=blockWay_54_Seolleung_B3)

    elevator_2_Seolleung_B3.update(north = blockWay_53_Seolleung_B3)


def createB1mapInHanti():
    """
    Hanti station marker nodes in B4 Floor
    :return: way points in Hanti station B4
    """
    #railWay marker

    #blockWay marker
    global blockWay_59_Hanti_B1
    # elevator marker
    global elevator_1_Hanti_B1, elevator_2_Hanti_B1

    # blockWay marker
    blockWay_59_Hanti_B1 = markerNode("Hanti_59_B1", 1, 59)

    # elevator marker
    elevator_1_Hanti_B1 = markerNode("Hanti_EV_1_B1", 1, 7)
    elevator_2_Hanti_B1 = markerNode("Hanti_EV_2_B1", 1, 8)

    #update
    blockWay_59_Hanti_B1.update(south = elevator_2_Hanti_B1, east = elevator_1_Hanti_B1)

    elevator_1_Hanti_B1.update(west = blockWay_59_Hanti_B1)
    elevator_2_Hanti_B1.update(north = blockWay_59_Hanti_B1)


def createB4mapInHanti():
    """
    Hanti station marker nodes in B4 Floor
    :return: way points in Hanti station B4
    """
    #railWay marker
    global railWay_2_4_Hanti_B4
    global railWay_3_1_Hanti_B4, railWay_3_2_Hanti_B4
    # blockWay marker
    global blockWay_56_Hanti_B4, blockWay_57_Hanti_B4, blockWay_58_Hanti_B4
    # elevator marker
    global elevator_1_Hanti_B4

    # railWay marker
    railWay_2_4_Hanti_B4 = markerNode("Hanti_2_4_B4", 4, 4)
    railWay_3_1_Hanti_B4 = markerNode("Hanti_3_1_B4", 4, 5)
    railWay_3_2_Hanti_B4 = markerNode("Hanti_3_2_B4", 4, 6)

    #blockWay marker
    blockWay_56_Hanti_B4 = markerNode("Hanti_56_B4", 4, 56)
    blockWay_57_Hanti_B4 = markerNode("Hanti_57_B4", 4, 57)
    blockWay_58_Hanti_B4 = markerNode("Hanti_58_B4", 4, 58)

    # elevator marker
    elevator_1_Hanti_B4 = markerNode("Hanti_EV_1_B4", 4, 7)

    #update
    railWay_2_4_Hanti_B4.update(west = railWay_3_1_Hanti_B4)
    railWay_3_1_Hanti_B4.update(west = railWay_3_2_Hanti_B4, east = railWay_2_4_Hanti_B4)
    railWay_3_2_Hanti_B4.update(north = blockWay_56_Hanti_B4, east = railWay_3_1_Hanti_B4)

    blockWay_56_Hanti_B4.update(south = railWay_3_2_Hanti_B4, west = blockWay_57_Hanti_B4)
    blockWay_57_Hanti_B4.update(north = blockWay_58_Hanti_B4, east = blockWay_56_Hanti_B4)
    blockWay_58_Hanti_B4.update(south = blockWay_57_Hanti_B4, west = elevator_1_Hanti_B4)

    elevator_1_Hanti_B4.update(east = blockWay_58_Hanti_B4)


def createRouteForTransfer():
    # Seolleung station B2 way point
    global routeDataList
    routeDataList = routeData(railWay_9_1_Seolleung_B2)
    routeDataList.insertLast(railWay_8_4_Seolleung_B2)
    routeDataList.insertLast(railWay_8_3_Seolleung_B2)
    routeDataList.insertLast(railWay_8_2_Seolleung_B2)
    routeDataList.insertLast(railWay_8_1_Seolleung_B2)
    routeDataList.insertLast(railWay_7_4_Seolleung_B2)
    routeDataList.insertLast(blockWay_51_Seolleung_B2)
    routeDataList.insertLast(blockWay_52_Seolleung_B2)
    routeDataList.insertLast(elevator_2_Seolleung_B2)
    routeDataList.insertLast(elevator_2_Seolleung_B3)
    routeDataList.insertLast(blockWay_53_Seolleung_B3)
    routeDataList.insertLast(blockWay_54_Seolleung_B3)
    routeDataList.insertLast(blockWay_55_Seolleung_B3)
    routeDataList.insertLast(railWay_2_4_Seolleung_B3)
    routeDataList.insertLast(railWay_2_4_Hanti_B4)
    routeDataList.insertLast(railWay_3_1_Hanti_B4)
    routeDataList.insertLast(railWay_3_2_Hanti_B4)
    routeDataList.insertLast(blockWay_56_Hanti_B4)
    routeDataList.insertLast(blockWay_57_Hanti_B4)
    routeDataList.insertLast(blockWay_58_Hanti_B4)
    routeDataList.insertLast(elevator_1_Hanti_B4)
    routeDataList.insertLast(elevator_1_Hanti_B1)
    routeDataList.insertLast(blockWay_59_Hanti_B1)
    routeDataList.insertLast(elevator_2_Hanti_B1)

class currentLocation:
    def __init__(self, floor, prev = None, cur = None, next = None):
        self.floor = floor
        self.prev = prev
        self.cur = cur
        self.next = next

    def updateFloor(self, floor):
        self.floor = floor

    def updateLocation(self, next):
        self.prev = self.cur
        self.cur = self.next
        self.next = next

def findMarkerLocation(findId):
    node = routeDataList.head
    while True:
        if node.id == findId:
            return node
        node = node.next
        if node.next == None:
            print("Not found")
            return

def dataForNextNode(currentLoc, mode):
    """
    get the data to go to next node

    :param node: Get the current node data
    :param mode:
    0 : Nothing, just go forward
    1 : Riding elevator, change to E.V. sign
    2 : Riding subway, change to wait sign
    3 : Etc, depending on the situation

    :return: string list data which will be sent to web
    """
    prev  = currentLoc.prev
    cur = currentLoc.cur
    next = currentLoc.next
    stringList = []

    if mode == 0:
        if cur.northConnectedNode == next:
            if cur.southConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.eastConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.westConnectedNode == next:
            if cur.eastConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.northConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.southConnectedNode == next:
            if cur.northConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.westConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        elif cur.eastConnectedNode == next:
            if cur.westConnectedNode == prev:
                stringList.append("F")
                stringList.append("Go_Straight")
            elif cur.southConnectedNode == prev:
                stringList.append("R")
                stringList.append("Turn_Right")
            else:
                stringList.append("L")
                stringList.append("Turn_Left")
        stringList.append("F")

    elif mode == 1:
        if next == None:
            stringList.append("E")
            stringList.append("FINISH")
            stringList.append("E")
            return stringList

        stringList.append("E")
        stringList.append("Go_to_B" + str(next.floor) + "_floor")
        stringList.append("E")

    elif mode == 2:
        stringList.append("S")
        stringList.append("Get_off_at_" + str(next.name) + "_platform")
        stringList.append("S")

    elif mode == 3:
        if cur == railWay_9_1_Seolleung_B2:
            stringList.append("L")
            stringList.append("Turn_Left")
            stringList.append("F")
        elif cur == railWay_7_4_Seolleung_B2:
            stringList.append("R")
            stringList.append("Turn_Right_Go_Straight_Turn_Right")
            stringList.append("F")
        elif cur == elevator_2_Seolleung_B3:
            stringList.append("F")
            stringList.append("Get_off_EV_Go_Straight")
            stringList.append("F")
        elif cur == railWay_2_4_Hanti_B4:
            stringList.append("L")
            stringList.append("Get_off_Subway_Turn_Left")
            stringList.append("F")
        elif cur == elevator_1_Hanti_B1:
            stringList.append("L")
            stringList.append("Get_off_EV_Turn_Left")
            stringList.append("F")

    return stringList


#main function
if __name__ == '__main__':
    createB2mapInSeooleung()
    createB3mapInSeooleung()
    createB1mapInHanti()
    createB4mapInHanti()
    createRouteForTransfer()

    IdList = [2, 2, 2, 2, 2, 1, 51, 52, 3, 3, 53, 54, 55, 4, 4, 5, 6, 56, 57, 58, 7, 7, 59, 8]
    modeList = [3, 0, 0, 0, 0, 3, 0, 0, 1, 3, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 1, 3, 0, 1]

    i = 0
    currentNode = routeDataList.head
    currentLocation = currentLocation(currentNode.floor, cur = currentNode, next = currentNode.next)
    routeDataList.deleteHead()
    stringList = dataForNextNode(currentLocation, 3)
    print("step " + str(i))
    print(stringList)
    #print("ID : " + str(currentNode.id))

    while True:
        if routeDataList.routeLength == 0:
            print("The end")
            break

        i += 1

        tempNode = findMarkerLocation(IdList[i])
        mode = modeList[i]

        if tempNode.floor != currentNode.floor:
            currentLocation.updateFloor(tempNode.floor)

        currentLocation.updateLocation(tempNode.next)

        stringList = dataForNextNode(currentLocation, mode)
        print("step " + str(i))
        print(stringList)

        currentNode = tempNode

        routeDataList.deleteHead()

        #print("ID : " + str(currentNode.id))
        #print("length")
        #print(routeDataList.routeLength)