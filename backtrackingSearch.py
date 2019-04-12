import copy
from CSP import *
from random import shuffle
from graphics import *
from featureExtractor import *
from regression import *

import time
start = time.time()
"the code you want to test stays here"

weights = normalEquations(featureMatrix('Database.txt'),targetMatrix('Database.txt'))
print(weights)

def backtrackingSearch(csp):
    return recursiveBackTrackingSearch({}, csp.variables, csp.domains, csp.constraints)


def recursiveBackTrackingSearch(assignment, variables, domains, constraints):
    if assignmentComplete(assignment, variables):
        return assignment
    next_var = chooseVariable(assignment, variables)
	#best approach probably to merge items in each domain list.
    for domainList in domains[next_var]:
        #could do an argmax here to make the best possible assignment/ q-learning here
        """Some sort of regression choosing should go here"""
        """*************************************"""
        hypothesis = evaluate(weights, FeatureExtractorUtil().extractFeatures(assignment))
        """*************************************"""
        #can also randomize values picked here, as well as the domainList picked.
        shuffle(domainList)
        for next_val in domainList:
            assignment[next_var] = next_val
            print("****************next_val********************")
            print(next_val)
            old_domains = createDeepCopy(domains)
            if validAssignment(assignment, constraints):
                print("*********validAssignment next_val{}".format(next_val))
                #print("next_val{}".format(next_val))
                updateDomains(assignment, variables, domains, next_val)
                if noEmptyDomain(domains):
                    result = recursiveBackTrackingSearch(assignment, variables, domains, constraints)
                    if result is not None:
                        return result
            del assignment[next_var]
            print("****backtracked next_val{}, next_var{}".format(next_val, next_var))

            domains = old_domains
    return None

def assignmentComplete(assignment, variables):
    for var in variables:
        if var not in assignment:
            return False
    return True


def chooseVariable(assignment, variables):
    for var in variables:
        if var not in assignment:
            return var
    return None


def validAssignment(assignment, constraints):
    return constraints(assignment)


def updateDomains(assignment, variables, domains, next_val):
    #print("********domains{}".format(domains))
    var_for_domain_update = chooseVariable(assignment, variables)
    if var_for_domain_update == None:
        return
    # print("********var_for_domain_update{}".format(var_for_domain_update))
    # print("********next_val{}".format(next_val))
    domainMapVal = domains[var_for_domain_update]
    newDomainMapVal = []
    for domainList in domainMapVal:

        if domainList[0][0] == next_val[1]:
            newDomainMapVal.append(domainList)

    domains[var_for_domain_update] = newDomainMapVal
    return

def noEmptyDomain(domains):
    #print(domains)
    for key in domains:
        if len(domains[key]) == 0:
            # print("returning False")
            return False
    return True

def createDeepCopy(domains):
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


csp = CSP(4, 0)
#print(csp.domains)

#assignment = backtrackingSearch(csp)
#print(assignment)
#StructureVisual().drawStructure(assignment)

