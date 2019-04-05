import copy
<<<<<<< HEAD
from CSP import *
=======
>>>>>>> 219b55a7d9cac93bd9a641f598d876a0786b24a1

def backtrackingSearch(csp):
	return recursiveBackTrackingSearch({}, csp.variables, csp.domains, csp.constraints)

def recursiveBackTrackingSearch(assignment, variables, domains, constraints):

	if assignmentComplete(assignment, variables):
		return assignment

	next_var = chooseVariable(assignment, variables)

	for domainList in domains[next_var]:
		#could do an argmax here to make the best possible assignment/ q-learning here
		for next_val in domainList:
			assignment[next_var] = next_val
			old_domains = copy.deepcopy(domains)
			if validAssignment(assignment, constraints):
				print("validAssignment")
				print("next_val{}".format(next_val))
				updateDomains(assignment, variables, domains, next_val)
				if noEmptyDomain(domains):
					print("here")
					result = recursiveBackTrackingSearch(assignment, variables, domains, constraints)
					if result is not None:
						return result
			del assignment[next_var]
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
	print("********domains{}".format(domains))
	var_for_domain_update = chooseVariable(assignment, variables)
	if var_for_domain_update == None:
		return
	#print("********var_for_domain_update{}".format(var_for_domain_update))
	#print("********next_val{}".format(next_val))
	domainMapVal = domains[var_for_domain_update]
	newDomainMapVal = []
	for domainList in domainMapVal:
		print("********domainList{}".format(domainList))
		if domainList[0][0] == next_val[1]:
			newDomainMapVal.append(domainList)

	domains[var_for_domain_update] = newDomainMapVal
	return

def noEmptyDomain(domains):
	print(domains)
	for key in domains:
		if len(domains[key]) == 0:
			#print("returning False")
			return False
	return True


csp = CSP(5, 0)
print(csp.domains)
print(backtrackingSearch(csp))







