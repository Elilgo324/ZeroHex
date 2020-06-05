# zeroHex 
Human players prefer training with human opponents over agents as the latter are distinctively different in level and style than humans. 
Agents designed for human-agent play are capable of adjusting their level, however their style is not aligned with that of human players. 
In this work, we implement approach for designing such agents.

## Basic Agent
Our agents (agent1 folder) are based on https://github.com/gwylim/hexnet.

## Doc
Read doc of significant part of our work here https://docs.google.com/document/d/10GZNeofaPGmkTV7eE-QRveydXXX6NEnmbwWA05Aiho0/edit.

## Data
We found lists of ELO ranked players and their games (board size 11X11) at http://www.littlegolem.net/jsp/info/player_list.jsp?gtvar=hex_HEX11&countryid=&filter=&Send=submit.

### Original Format
The original format of the games was as the following:
```
(;FF[4]EV[hex.mc.2010.oct.1.11]PB[Maciej Celuch]PW[pensando]SZ[13]RE[B]GC[ game #1254910]SO[http://www.littlegolem.com];W[mf];B[gg];W[de];B[df];W[ji];B[if];W[ld];B[jg];W[jf];B[ig];W[kg];B[kc];W[mb];B[ma];W[lb];B[la];W[kb];B[ka];W[jb];B[ja];W[hc];B[hb];W[fd];B[fc];W[ib];B[ia];W[gc];B[gb];W[cd];B[da];W[eb];B[dd];W[ce];B[dc];W[cc];B[db];W[bb];B[le];W[kf];B[ke];W[je];B[il];W[jj];B[kk];W[hk];B[resign])
```
This was needed to be parsed and arranged. 

### More Sources
Check the also the site http://hex.kosmanor.com/hex-bin/board/.
There is a potential to mine from it more games. 

### Our Datasets
We produced, among the rest, the following datasets:
- Files of all the players according their rank (for instance, the file 1234.txt belongs to a player with rank 1234)
Clearly, the rank function isn't one to one, and thus there can be multiple players with the same rank.
- Files of all the players according their rank, when the name of the player is at the first line.
- The files used to train the humanized agents, separated.
- The original bunch from littlegolem.
- The records of the games between our agent and wolve.

## Work Components
Our work contains, among the rest, the following components:
- The code of the modified and the original agents.
It contains the original files to create and train the original agent.
The file compare.py can be run by `compare.py model1 model2` to compare the models.
The file learning.py can be run by `learning.py` to train the agent to fit the rank of a banch of games.
- Inside the agent folder there are also files that used to run our agents against the agent wolve.
It can be run by `vs_wolve.py`. Modify the hard coded paths inside.
Some integration details (commands, parameters and more) can be founded inside `wolve_integration.py`.
- The convertor contains scripts to handle and arrange the original games records.
- The evaluation tool can be used to evaluate the accuracy of predicting the next move given a board state. 
It can be run by `eval.py`. Notice that the paths and games are hard coded inside (and can easily be modified).
- The gui that can be used by human to play against the agents.
The original application had some bugs in it, that we fixed in this version.

## Rivals
Find more agents to test against here https://github.com/cgao3/benzene-vanilla-cmake.

## Gui
Playing against the agent can be done by using https://github.com/DebuggerOR/hexgui.

## About Us
The work done by Avshalom , Ori and Shlomo as undergraduates' final project at Bar Ilan University.

## Some Theory
At the beginning of the work, some of theoretic material was needed to be caught up.

### The DNN
Note that the focus in humanizing the agent was in adjusting the search tree's parameters and not the nn's. 

### Reinforcement Learning
Reinforcement learning differs from the supervised learning in a way that in supervised learning the training data has the answer key with it so the model is trained with the correct answer itself whereas in reinforcement learning, there is no answer but the reinforcement agent decides what to do to perform the given task. In the absence of training dataset, it is bound to learn from its experience.

### MCTS
Creation of mcts consists four stages:
#### 1. Selection
    Used for nodes we've seen before.
    Pick according to UCB.
#### 2. Expansion
    Used when we reach the frontier.
    Add one node per playout.
#### 3. Simulation
    Used beyond the search frontier.
    Don't bother with UCB, just play randomly.
#### 4. Backpropagation
    After reaching a terminal node.
    Update value and visits for states expanded in selection and expansion.

### Read & Watch more
https://www.biostat.wisc.edu/~craven/cs760/lectures/AlphaZero.pdf.

https://www.youtube.com/watch?v=MgowR4pq3e8&t=492s.

http://u.cs.biu.ac.il/~sarit/advai2018/MCTS.pdf.

https://medium.com/oracledevs/lessons-from-implementing-alphazero-7e36e9054191 and more at medium.com.

https://notes.jasonljin.com/projects/2018/05/20/Training-AlphaZero-To-Play-Hex.html.
