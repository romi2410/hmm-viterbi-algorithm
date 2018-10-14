"""
Author - Romi Padam
"""

import sys

#-----------------------------------------------------------------------#
#--Viterbi algorithm - Computing probabilites of moving into each state-#
#-----------------------------------------------------------------------#
def viterbi(hotProb, coldProb, transitionProb, obsSeq):

    viterbisCold = []
    viterbisHot = []
    hotProbList = []
    coldProbList = []

    # Calculating viterbi values at first state
    viterbiCold = transitionProb[('start', 'cold')] * coldProb[(obsSeq[0], 'cold')]
    viterbiHot = transitionProb[('start', 'hot')] * hotProb[(obsSeq[0], 'hot')]

    viterbisHot.append((obsSeq[0], viterbiHot, 'hot'))
    viterbisCold.append((obsSeq[0], viterbiCold, 'cold'))

    hotProbList.append(viterbiHot)
    coldProbList.append(viterbiCold)

    # Calculating remianing viterbi values for the entire sequence
    for i in range(1, len(obsSeq)):
        hotGivenHot = transitionProb[('hot', 'hot')] * hotProb[(obsSeq[i], 'hot')] * hotProbList[i-1]

        hotGivenCold = transitionProb[('cold', 'hot')] * hotProb[(obsSeq[i], 'hot')] * coldProbList[i-1]

        coldGivenCold = transitionProb[('cold', 'cold')] * coldProb[(obsSeq[i], 'cold')] * coldProbList[i-1]

        coldGivenHot = transitionProb[('hot', 'cold')] * coldProb[(obsSeq[i], 'cold')] * hotProbList[i-1]

        if coldGivenCold > coldGivenHot:
            viterbisCold.append((obsSeq[i], coldGivenCold, 'cold'))
        else:
            viterbisCold.append((obsSeq[i], coldGivenHot, 'hot'))

        if hotGivenHot > hotGivenCold:
            viterbisHot.append((obsSeq[i], hotGivenHot, 'hot'))
        else:
            viterbisHot.append((obsSeq[i], hotGivenCold, 'cold'))

        hotProbList.append(max(hotGivenHot, hotGivenCold))
        coldProbList.append(max(coldGivenCold, coldGivenHot))

    return viterbisCold, viterbisHot

#-----------------------------------------------------------------------#
#Backtracing - finding the path which corresponds to highest probability#
#-----------------------------------------------------------------------#
def backtracing(viterbisCold, viterbisHot, obsSeq):
    stateSequence = []
    prob=[]

    if viterbisCold[-1][1] > viterbisHot[-1][1]:
        stateSequence.append('cold')
        prev = 'cold'
        prob = viterbisCold[-1][1]
        for i in range(len(obsSeq), 1, -1):
            if prev == 'cold':
                stateSequence.append(viterbisCold[i-1][2])
            else:
                stateSequence.append(viterbisHot[i-1][2])
                prev = 'hot'

    else:
        stateSequence.append('hot')
        prev = 'hot'
        prob = viterbisHot[-1][1]
        for i in range(len(obsSeq), 1, -1):
            if (prev == 'hot'):
                stateSequence.append(viterbisHot[i-1][2])
                prev = viterbisHot[i-1][2]
            else:
                stateSequence.append(viterbisCold[i-1][2])
                prev= viterbisCold[i-1][2]

    stateSequence.append('start')
    stateSequence.reverse()
    return stateSequence, prob

#-----------------------------------------------------------------------#
#---------------------------------Main----------------------------------#
#-----------------------------------------------------------------------#
if __name__ == '__main__':
    # Take first argument as input observation sequence
    obsSeq = sys.argv[1]
    print("Computing most likely weather sequence for " + obsSeq + " ...\n")

    # Porbability Matrix
    hotProb = {('1', 'hot') : 0.2, ('2', 'hot') : 0.4, ('3', 'hot') : 0.4}
    coldProb = {('1', 'cold') : 0.5, ('2', 'cold') : 0.4, ('3', 'cold') : 0.1}
    transitionProb = {('hot', 'hot') : 0.7, ('hot', 'cold') : 0.3, ('cold', 'cold') : 0.6, ('cold', 'hot') : 0.4, ('start', 'hot'): 0.8, ('start', 'cold'): 0.2}

    # Computing probabilities of moving into each state using viterbi algorithm
    viterbisCold, viterbisHot = viterbi(hotProb, coldProb, transitionProb, obsSeq)

    # Backtracing to reconstruct the correct state sequence
    stateSequence, prob = backtracing(viterbisCold, viterbisHot, obsSeq)

    print("Weather sequence with the probability of " + str(prob) + " is generated for the given input:")
    print(*stateSequence, sep=' -> ')
    print ("\nEnd of the program")
