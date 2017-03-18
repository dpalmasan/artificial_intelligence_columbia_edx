from copy import deepcopy
from CSP import *

class Queue:
    """
    Queue implementation
    """
    def __init__(self):
        self.queue = []

    def isEmpty(self):
        return len(self.queue) == 0

    def enqueue(self, e):
        self.queue.append(e)

    def dequeue(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)

class CSP:
    """
    This is an abstract class that defines the required methods to apply
    search algorithms as seen in class
    """
    def __init__(self, domain, binary_constraints, unassigned_vars):
        """
        A CSP problem must have the following attributes:
        - domain: For each variable, the values that can take (it is a dict, in which
        the key is the variable name, and the value is a list of possible values for that
        variable.
        - binary_constraints: A list of tuples, representing binary constraints.
        - unassigned_vars: A list of variable names that are unassigned.
        - empty: A symbol representing that a variable has not been assigned yet.
        """
        self.domain = domain
        self.binary_constraints = binary_constraints
        self.unassigned_vars
        self.empty

    def getNeighbors(self):
        raise NotImplementedError

    def getUnassignedVariables(self):
        raise NotImplementedError

    def assignVariable(self, var, value):
        raise NotImplementedError

    def checkConsistency(self):
        raise NotImplementedError

def AC3(csp):
    """
    Returns False if an inconsistency is found, True otherwise
    """

    queue = Queue()
    queue.queue = list(csp.binary_constraints)

    while not queue.isEmpty():
        (Xi, Xj) = queue.dequeue()
        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False
            for Xk in csp.getNeighbors(Xi, Xj):
                queue.enqueue((Xk, Xi))
           
    return True

def Revise(csp, Xi, Xj):
    """
    Returns True iff we revise the domain of Xi
    """
    revised = False
    for x in csp.domain[Xi]:
        canSatisfy = False
        for y in csp.domain[Xj]:
            if x != y:
                canSatisfy = True
                break
        if not canSatisfy:
            csp.domain[Xi].remove(x)
            revised = True
    return revised

def forwardChecking(csp, var, value):
    """
    Given an assignment, uses forward checking to make inferences about possible
    assignments for free variables. Returns True if no variable domain is empty,
    False otherwise
    """

    variables = list(csp.getUnassignedVariables())
    if var in variables:
        variables.remove(var)

    for v in variables:
        for val in list(csp.domain[v]):
            csp.assignVariable(v, val)
            if not csp.checkConsistency():
                csp.domain[v].remove(val)
            if len(csp.domain[v]) == 0:
                return False
        if len(csp.domain[v]) == 1:
            csp.assignVariable(v, csp.domain[v][0])
        else:
            csp.assignVariable(v, csp.empty)

    return True

def BacktrackingSearch(csp):
    """
    Returns a solution or failure
    """
    return Backtrack({}, csp)

# TODO: Add a method for selecting value order for variables.
def Backtrack(assignment, csp, inference=forwardChecking):

    # Get unassigned variables
    variables = list(csp.getUnassignedVariables())
    for key in assignment.keys():
        if key in variables:
            variables.remove(key)


    # Assignment Complete
    if len(variables) == 0:
        return assignment

    # Pick the next variable to be assigned using MRV heuristic
    maxDi = float('Inf')
    var = None
    for v in variables:
        if len(csp.domain[v]) < maxDi:
            maxDi = len(csp.domain[v])
            var = v

    # TODO: Implement a better ordering
    for value in csp.domain[var]:
        cspTemp = deepcopy(csp)
        cspTemp.assignVariable(var, value)
        cspTemp.unassigned_vars.remove(var)
        if cspTemp.checkConsistency():
            assignment[var] = value
            inferences = []
            if inference(cspTemp, var, value):
                for v in list(cspTemp.getUnassignedVariables()):
                    if len(cspTemp.domain[v]) == 1:
                        assignment[v] = cspTemp.domain[v][0]
                        inferences.append(v)

                result = Backtrack(assignment, cspTemp)
                if result != False:
                    return result

            # Remove var and inferences from assignment
            assignment.pop(var, None)
            for v in inferences:
                assignment.pop(v, None)

    return False

