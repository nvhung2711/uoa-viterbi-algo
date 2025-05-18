Robot localization is the process of determining where a mobile robot is located con-
cerning its environment. Robot localization provides an answer to the question: Where
is the robot now ? A reliable solution to the localization is one of the most fundamental
competencies required by an autonomous robot as the knowledge of the robot’s own
location is an essential precursor to making decisions about future actions.
In a typical robot localization scenario, a map of the environment is available and the
robot is equipped with sensors that observe the environment as well as monitor its own
motion. The localization problem then becomes one of estimating the robot’s position
within the map using information gathered from these sensors. The following shows an
example of a 2D map drawn using ASCII characters:
0 0 0 0 X 0 0 0 0 X
X X 0 0 X 0 X X 0 X
X 0 0 0 X 0 X X 0 0
0 0 X 0 0 0 X 0 0 0
The character ‘X’ denotes an obstacle (the path cannot be traversed), while the
character ‘0’ (Zero) represents a traversable positions. Any position within the map is
indicated by the coordinates (k, j), where k is the row number (ordered top to bottom)
and j is the column number (ordered left to right), starting from 1. For example, the
top left position is (1, 1) and the bottom right is (4, 10).
A robot moves in the map and gathers information along the way. In this version,
the robot has a single non-deterministic Move action and its sensors reports whether
or not obstacles lay immediately to the north, south, east, and west. A sequence of
Semester 1 2023 Page 1
sensor readings observed is the set of possible blocked directions. The following shows
the example of the observed sensor readings at each time step; which means e.g., at time
1, the north (N), south (S) and west (W) of the robot have obstacles:
Time Steps 1 2 3 4
Blocked direcition(s) NSW NS N NE
1.1 Problem formulation
• The state variable Xt represents the location of the robot on the discrete grid; the
domain of this variable is the set of traversable points illustrated as ‘0’ points in
the map.
• Let NEIGHBORS(i) be the set of traversable points that are adjacent to and let
N (i) be the size of that set. Then the transition model for the Move action is
defined as follows, which means the robot has equal probability to move to each
of its neighbours.
P (Xt+1 = j|Xt = i) =
(
1/N (i) if j ∈ NEIGHBORS(i)
0 otherwise
We don’t know where the robot starts, so we will assume a uniform distribution
over all the sates; that is, P (X0 = i) = 1/K, where K is the number of ‘0’ points
in the map.
• The sensor variable Et has 16 possible values, each a four-bit sequence giving the
presence or absence of an obstacle in each of the compass directions (North, East,
South and West). NSWE is the way of specifying the four-bit sequence and your
program must expand each direction in this order. For example, a four-bit
sequence 1010 represents that the sensors report an obstacle on its north and south
west positions, while the east and westsouth positions do not have obstacles.
• The sensors’ error rate is ε and that errors occur independently for the four sensors.
In that case, the probability of getting all four bits right is (1 − ε)4, and the
probability of getting them all wrong is ε4. Furthermore, if dit denotes the number
of directions are reporting erroneous values, then the probability that a robot at
position i would receive a sensor reading et (i.e., the observation/emission model)
is:
Semester 1 2023 Page 2
P (Et = et|Xt = i) = (1 − ε)4−dit εdit
Using the above problem formulation, you are requested to use the Viterbi forward
algorithm provided below to find the Trellis matrix. A trellis matrix gives us the prob-
ability of each state (path in this case) given each observation made by the robot’s
sensors. For the path(s) which cannot be traversed, the probability is 0 (Zero) in the
trellis matrix. Therefore, the trellis matrix could reflect the possible positions of the
robot.
Algorithm 1 Viterbi forward algorithm
1: input: O, observation space O = {o1, o2,...,oN }.
S, state space S = {s1,s2,...,sK } // Here, K refers to the traversable positions.Q, array of initial probabilities Q = (π1,π2,...,πK ) // Here, π1 = π2 =, ..., πK .
Y, a sequence of observations Y = (y1,y2,...,yT ).
Tm, transition matrix of size K x K.
Em, emission matrix of size K x N.
2: output: Trellis matrix
3: for each position i = 1, 2, ..., K do
4: trellis[i,1] ← πi * Emiy1
5: end for
6: for each observation j = 2, 3, ...T do
7: for each state i = 1, 2, ...K do
8: trellis[i,j] ← max
k (trellis[k, j - 1] * T mki ∗ Emiyj ) // Here, k is the most likely
prior positions and yj is the observation at time j.
9: end for
10: end for
11: return trellis
