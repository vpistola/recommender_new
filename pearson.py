from db import *
from math import sqrt
import pprint

# The hardcoded PREFS is for debugging purposes
#PREFS = {2: {5: 1, 6: 1, 7: 0, 8: 1, 9: 0, 10: 1, 120: 1, 490: 0, 576: 0, 605: 0, 610: 0, 618: 0, 671: 1, 718: 0, 735: 1, 906: 0, 2284: 1}, 8: {5: 1, 6: 0, 7: 0, 8: 1, 9: 0, 10: 1, 120: 0, 490: 0, 576: 0, 605: 0, 610: 0, 618: 0, 671: 1, 718: 0, 735: 1, 906: 0, 2153: 0, 2306: 0}, 10: {47: 0, 48: 0, 67: 0, 219: 0, 2243: 0, 2306: 0, 2337: 0}, 15: {482: 1, 538: 0, 824: 1}}
#PREFS = getUserHistoryDict()
#print(PREFS)

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item]=1
    
    # Find the number of elements
    n=len(si)

    # if they are no ratings in common, return 0
    if n==0: return 0
    
    # Add up all the preferences
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    
    # Sum up the squares
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    
    # Sum up the products
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    
    # Calculate Pearson score
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0
    
    r=num/den
    
    return r


# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores=[(similarity(prefs, person, other), other) for other in prefs if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other==person: continue
        sim = similarity(prefs, person, other)
        #print(f'person is {other} and similarity is {sim}')
        #ignore scores of zero or lower
        if sim<=0: continue
        for item in prefs[other]: 
            #only score movies i haven't seen yet
            if item not in prefs[person]: #or prefs[person][item]==0:
                #similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item]*sim
                #sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim
    
    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items( )]
    
    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings


#print(topMatches(PREFS, 8, n=3))
#print(sim_pearson(PREFS, 8, 2))
#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(getRecommendations(PREFS, 8))