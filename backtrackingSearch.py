import copy

def backtrackingSearch(csp):
	return recursiveBackTrackingSearch({}, csp.variables, csp.domains, csp.constraints)


def recursiveBackTrackingSearch(assignment, variables, domains, constraints):

	if assignmentComplete(assignment, variables):
		return assignment

	next_var = chooseVariable(variables)

	for domainList in domains[next_var]:
		for next_val in domainList:
			assignment[next_var] = next_val
			old_domains = copy.deepcopy(domains)
			if validAssignment(assignment, constraints):
				domains = updateDomains(assignment, variables, domains, constraints)
				if noEmptyDomain(domains):
					result = recursiveBackTrackingSearch(assignment, variables, domains, constraints)
					if result is not None:
						return result
			del assignment[next_var]
			domains = old_domains
	return None