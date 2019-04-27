import copy
from CSP import *
from random import shuffle
from graphics import *
from featureExtractor import *
from regression import *
import json
import csv
from util import *

import time
start = time.time()

class BacktrackingSearch:
    def __init__(self):
        with open('Weights.csv', 'r') as f:
            reader = csv.reader(f)
            weights = list(reader)
        weights = weights[0]
        for i in range(len(weights)):
            weights[i] = float(weights[i])
        self.weights = weights
        self.regression = Regression("Database.txt")
        self.featureExtractor = FeatureExtractorUtil()

    def backtrackingSearch(self, csp):
        return self.backTrackingSearchWithHeuristic({}, csp.variables, csp.domains, csp.constraints, 0)


    def recursiveBackTrackingSearch(self, assignment, variables, domains, constraints, nodesExpanded):
        if self.assignmentComplete(assignment, variables):
            return (assignment, nodesExpanded)
        next_var = self.chooseVariable(assignment, variables)
    	#best approach probably to merge items in each domain list.
        for domainList in domains[next_var]:
            #could do an argmax here to make the best possible assignment/ q-learning here
            """Some sort of regression choosing should go here"""
            """*************************************"""
           #a = json.dumps(assignment)
           #hypothesis = evaluate(weights, FeatureExtractorUtil().extractFeatures(a))
            """*************************************"""
            #can also randomize values picked here, as well as the domainList picked.
            domainList = list(domainList)
            shuffle(domainList)
            for next_val in domainList:
                nodesExpanded +=1
                assignment[next_var] = next_val
                #print("****************next_val********************")
                #print(next_val)
                old_domains = self.createDeepCopy(domains)
                if self.validAssignment(assignment, constraints):
                    #print("*********validAssignment next_val{}".format(next_val))
                    ##print("next_val{}".format(next_val))
                    self.updateDomains(assignment, variables, domains, next_val)
                    if self.noEmptyDomain(domains):
                        result = self.recursiveBackTrackingSearch(assignment, variables, domains, constraints, nodesExpanded)
                        if result is not None:
                            return (result[0], result[1])
                del assignment[next_var]
                #print("****backtracked next_val{}, next_var{}".format(next_val, next_var))

                domains = old_domains
        return None



    def backTrackingSearchWithHeuristic(self, assignment, variables, domains, constraints, nodesExpanded):
        if self.assignmentComplete(assignment, variables):
            return (assignment, nodesExpanded)
        next_var = self.chooseVariable(assignment, variables)
        domain = PriorityQueue()
        for domainList in domains[next_var]:
            for domain_val in domainList:
                assignment[next_var] = domain_val
                #print("assignment {}".format(assignment))
                features = self.featureExtractor.extractFeatures(assignment)
                hypothesis = self.regression.evaluate(self.weights, features) 
                #print("domain {}, hypothesis{}".format(domain_val, hypothesis))
                domain.push(domain_val, hypothesis)
                del assignment[next_var]


        while not domain.isEmpty():
            next_val = domain.pop()
            nodesExpanded +=1
            assignment[next_var] = next_val
            #print("****************next_val********************")
            #print(next_val)
            old_domains = self.createDeepCopy(domains)
            if self.validAssignment(assignment, constraints):
                #print("*********validAssignment next_val{}".format(next_val))
                ##print("next_val{}".format(next_val))
                self.updateDomains(assignment, variables, domains, next_val)
                if self.noEmptyDomain(domains):
                    result = self.backTrackingSearchWithHeuristic(assignment, variables, domains, constraints, nodesExpanded)
                    if result is not None:
                        return (result[0], result[1])
            del assignment[next_var]
            #print("****backtracked next_val{}, next_var{}".format(next_val, next_var))
            domains = old_domains
        return None

    def assignmentComplete(self, assignment, variables):
        for var in variables:
            if var not in assignment:
                return False
        return True


    def chooseVariable(self, assignment, variables):
        for var in variables:
            if var not in assignment:
                return var
        return None


    def validAssignment(self, assignment, constraints):
        return constraints(assignment)


    def updateDomains(self, assignment, variables, domains, next_val):
        ##print("********domains{}".format(domains))
        var_for_domain_update = self.chooseVariable(assignment, variables)
        if var_for_domain_update == None:
            return
        # #print("********var_for_domain_update{}".format(var_for_domain_update))
        # #print("********next_val{}".format(next_val))
        domainMapVal = domains[var_for_domain_update]
        newDomainMapVal = []
        for domainList in domainMapVal:

            if domainList[0][0] == next_val[1]:
                newDomainMapVal.append(domainList)

        domains[var_for_domain_update] = newDomainMapVal
        return

    def noEmptyDomain(self, domains):
        ##print(domains)
        for key in domains:
            if len(domains[key]) == 0:
                # #print("returning False")
                return False
        return True

    def createDeepCopy(self, domains):
        newDomain = {}
        for key in domains:
            newValue = []
            value = domains[key]
            for domainList in value:
                newDomainList = []
                for domain in domainList:
                    newDomainList.append(domain)
                newValue.append(newDomainList)
            newDomain[key] = newValue
        return newDomain
    

backTrackSearch =BacktrackingSearch()


csp = CSP(10, 0)
start = time.time()
result = backTrackSearch.backtrackingSearch(csp)
print(result)
print(time.time() - start)
StructureVisual().drawStructure(result[0])

# csp = CSP(10, 0)
# finalMap = {} 
# for i in range(50):
#     result = backTrackSearch.backtrackingSearch(csp)
#     finalMap[i] = result[1]
# print(finalMap)
# file = open('testData.txt', 'a')
# file.write(json.dumps(finalMap))
# file.close()



##print(csp.domains)

# assignment = backtrackingSearch(csp)
# #print("\n\n\n\n\n\n\n\n*******************************************")
# #print(assignment)
# if assignment is not None:
#     file = open('Database.txt', 'a')
#     file.write("\n")
#     file.write(json.dumps(assignment))
#     file.close()
#     StructureVisual().drawStructure(assignment)

