import xmltodict
class Node:

	def __init__(self,name,price,cores):
		self.name=name
		self.price=price
		self.cores=cores
		self.nextNode=self
		self.multiplier=1
		self.count=0

def initialProcess(nodeList):
	for i in range(1,len(nodeList)):
		multiply = nodeList[i].cores//nodeList[i-1].cores
		result = multiply*nodeList[i-1].price
		if nodeList[i].price > result:
			nodeList[i].price = multiply*nodeList[i-1].price
			nodeList[i].nextNode = nodeList[i-1].nextNode
			nodeList[i].multiplier = multiply*nodeList[i-1].multiplier

def findCostForCores(nodeList,total_cores):
	nn = len(nodeList)-1
	while total_cores > 0 and nn >=0:
		if total_cores >= nodeList[nn].cores:
			total_cores = total_cores - nodeList[nn].cores
			nodeList[nn].nextNode.count = nodeList[nn].nextNode.count + nodeList[nn].multiplier
		else:
			nn = nn-1
	if total_cores > 0:  #if total_cores is less than minimum core available
		total_cores = total_cores - nodeList[0].cores
		nodeList[0].nextNode.count = nodeList[0].nextNode.count + nodeList[0].multiplier

def findCoresForCost(nodeList,total_cost):
	nn = len(nodeList)-1
	while total_cost > 0 and nn >=0 :
		if total_cost >= nodeList[nn].price:
			total_cost = total_cost - nodeList[nn].price
			nodeList[nn].nextNode.count = nodeList[nn].nextNode.count + nodeList[nn].multiplier
		else:
			nn = nn-1    	                

def parseDict(instances,zone_name):
        zone = instances[zone_name]
        nodeList = []
        mul = 1
        for j in ('large','xlarge','2xlarge','4xlarge','8xlarge','10xlarge'):
                result = zone.get(j,-1)
                if result != -1:
                        node = Node(j,result,mul)
                        nodeList.append(node)
                mul = mul * 2
	return nodeList

def multiplyCost(nodeList,hours):
	for node in nodeList:
		node.price = node.price * hours

def findTotalCost(nodeList):
	totalCost=0
	for node in nodeList:
		if node.count > 0:
			totalCost = totalCost + (node.price * node.count)
	return totalCost	
	
def get_costs(instances,hours,cpus,price):
	allNodes = []
	for zone in instances:
		nodeList = parseDict(instances,zone)
		initialProcess(nodeList)
		if cpus != 0 and price == 0:
			multiplyCost(nodeList,hours)
			findCostForCores(nodeList,cpus)
			totalCost=findTotalCost(nodeList)
		elif cpus == 0 and price != 0:
			multiplyCost(nodeList,hours)
			findCoresForCost(nodeList,price)
			totalCost=findTotalCost(nodeList)
		elif cpus !=0 and price !=0:
			multiplyCost(nodeList,hours)
			findCostForCores(nodeList,cpus)
			totalCost=findTotalCost(nodeList)
			#If minimum price is greater than given price, skip the zone 
			if totalCost>price:
				continue
		else:
			continue  #Invaid cpus and price	
		newNode = {}	
		newNode["region"]=zone
		newNode["total_cost"]="$"+"{0:.2f}".format(totalCost)
		newNode["servers"] = []
		for node in nodeList:
			if node.count > 0:
				tup = node.name, node.count
				newNode["servers"].append(tup)
		allNodes.append(newNode)
		allNodes.sort(key=lambda x: x["total_cost"])
	print allNodes

if __name__ == "__main__":
	tdict = input("Instances:")
	hours = input("Hours:")
	cores = input("Cores:")
	price = input("Price:")
	get_costs(tdict,hours,cores,price)
