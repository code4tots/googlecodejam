'''
Problem A. Ticket Swapping
This contest is open for practice. You can try every problem as many times as you like, though we won't keep track of which problems you solve. Read the Quick-Start Guide to get started.
Small input
8 points	
Solve A-small
Judge's response for last submission: Correct.
Large input
11 points	
Solve A-large
Judge's response for last submission: Correct.
Problem

The city has built its first subway line, with a grand total of N stations, and introduced a new way of paying for travel. Instead of just paying for one ticket and making an arbitrary journey, the price you pay is now based on entry cards.

When entering the subway, each passenger collects an entry card, which specifies the station the passenger entered at. When leaving the subway, the passenger has to give up the entry card, and is charged depending on the distance (in stations traveled) between the entry station specified on the entry card, and the exit station on which the entry card is surrendered. The payment depends on the distance between these stations as follows:

if they are the same station, you don't pay;
if they are adjacent stations, you pay N pounds;
if the distance is two stations, you pay 2N - 1: a charge N for the first stop and N - 1 for the second;
the third station costs N-2 (so you pay 3N - 3 for a three-station-long trip), the fourth stop N-3, and the ith stop N + 1-i;
thus, if you travel from one end of the subway to the other (a distance of N-1 stations), you pay 2 pounds for the last station traveled, and a grand total of (N2 + N - 2) / 2 in total.
After introducing this system the city noticed their gains are not as big as they expected. They figured out this might be due to people swapping their entry cards — so, for instance, if one person enters at station A, travels two stations to B and exits, while another person enters at B, travels three stations to C and exits, they would normally pay (in total) 2N - 1 + 3N - 3 = 5N - 4. But if the two people swapped their entry cards at station B, then the first one would travel for free (as he would surrender an entry card specifying the station B while exiting a station B, and so register a distance of zero); while the second person will exit at station C and surrender an entry card specifying station A, which is 5 stations away, and pays 5N - 10, at a net loss of six pounds to the city!

The city now wants to learn how much they can possibly lose if this practice becomes widespread. We will consider only one direction (from station 1 to station N, passing through all the stations in order) of the subway, and only one train on this line. We assume a passenger travelling from o to e obtains an entry card at o, can swap her entry card any number of times with any other passengers anywhere between o and e, including swapping with people who leave at o or those who enter at e, and then exit the train at e with some entry card (it is necessary to surrender some entry card to exit the subway). We also assume the passenger will not exit the train in the meantime (that is, will not surrender the currently held card and obtain a new one).

You are given a map of traffic (specifying how many passengers travel this train from which station to which), and you should calculate the city's financial loss, assuming passengers swap their cards to maximize this loss.

Input

The first line of the input gives the number of test cases, T. T test cases follow. Each test case contains the number N of stops (the stops are numbered 1 to N), and the number M of origin-endpoint pairs given. The next M lines contain three numbers each: the origin stop oi, the end stop ei and pi: the number of passengers that make this journey.

Output

For each test case, output one line containing "Case #x: y", where x is the case number (starting from 1) and y is the total loss the city can observe due to ticket swapping, modulo 1000002013.

Limits

1 ≤ T ≤ 20.
1 ≤ oi < ei ≤ N

Small dataset

2 ≤ N ≤ 100.
1 ≤ M ≤ 100.
1 ≤ pi ≤ 100.
Large dataset

2 ≤ N ≤ 109.
1 ≤ M ≤ 1000.
1 ≤ pi ≤ 109.
Sample


Input 
 	
Output 
 
3
6 2
1 3 1
3 6 1
6 2
1 3 2
4 6 1
10 2
1 7 2
6 9 1
Case #1: 6
Case #2: 0
Case #3: 10

The first test case is the case described in the problem statement - two passengers meet at station 3 and swap tickets. In the second test case the two passengers don't meet at all, so they can't swap tickets (and so the city incurs no loss). In the third case, only one of the early passengers can swap tickets with the later passenger.


'''

def solve():
	'solves a single test case'

	def cost(o,e):
		'cost of a single ticket going from o to e'
		return (e-o) * N - (e-o) * (e-o-1) // 2
	
	from collections import defaultdict
	N, M = map(int,input().split())
	d = defaultdict(lambda : 0) # d[station] is net number of people leaving the train at given station
	
	owed = 0 # owed is how much people would pay total without ticket swapping
	for o, e, p in (map(int,input().split()) for _ in range(M)):
		d[o] -= p # they enter at o
		d[e] += p # they leave at e
		owed += p * cost(o,e)
	
	tickets = []
	paid = 0 # paid is how much people pay total with ticket swapping
	for station in sorted(d):
		if d[station] < 0:
			# net influx of people entering the train
			# simply collect their tickets
			tickets.append( (station,-d[station]) )
		
		else:
			# net influx of people leaving the train
			# pay for it with the most recent tickets
			# older tickets get better discounts for successive stations.
			while d[station]:
				last_station, ntickets = tickets.pop()
				
				tickets_used = min(ntickets,d[station])
				
				paid += cost(last_station,station) * tickets_used
				
				d[station] -= tickets_used
				ntickets -= tickets_used
				
				if ntickets:
					tickets.append((last_station,ntickets))
		
	return (owed - paid) % 1000002013

for t in range(1,int(input())+1):
	print('Case #%d: %d' % (t,solve()))

