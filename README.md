# Board-Games
For Quest.


### Q-Learning Description

(from [ML Final Project Description in Canvas](https://nuevaschool.instructure.com/courses/677/assignments/10299))

#### What was the goal?

   To create a Q-Learning agent to play tic tac toe that is generic enough to also be adaptable (with ease) to other, more complicated games. It should be good enough that it beats a random agent and holds up against humans.

#### What algorithms/techniques did you try?

   At first, I tried to create a neural network that would input the state of the board and output coordinates for movement and round them (although coordinates are discrete, they are near each other so that shoul make it easier to train). I then switched to a Q-Learning approach and had the network output a classification list, where it would predict the probability of each player winning (the Board works for an indefinite number of players, and ties are usually treated as player 0). This proved to be very difficult, so I tried starting Q-learning from the beginning to help my comprehension and code. I used a Q learning algorithm in which the Q-function was a dictionary with keys `(state, move)`. This algorithm had paramaters for randomness, learning rate, and discount rate. I used these to choose actions and update the Q function. Reward was given at the end of the game and I only updated a Q-value when the agent preformed that move (as I saw was common practice online).

#### What was the outcome (if you have a working project) or where are you in the process (for works in progress)?

   Because of the nature of the algorithm, it takes a somewhat long time to train. It had many fatal flaws that I fixed. Currently, it stops my winning moves %70 of the time, but I need to do further testing. I'm pretty proud of it, but I'd have to continue training and testing.

#### If you were continuing this, what would your next steps be?

   I would clean up the code and make nicer and more thorough tests. I should save the data after training so I don't have to constantly retrain. I could do this by saving a text file of the Q-vals and later parsing it, but hopefully there's a better way. Furthermore, I should implen=ment a possible reward for every move (for other games), as well as create a neural network model for larger games that would have an obscene amount of possible states or actions. Right now, I am going to train it more and have it tie or win against humans. Maybe I should train on more intelligent algorithms (not random ones). I should also experiment with different levels of randomness, discount rates, and learning rates.








### Notes on using neural nets (old):

* Could use evolutionary nets - randomly generate them and then make new generations based on the best preforming ones. Works for all models (neural nets aren't really great for this)

* Could train on examples of humans playing based on whether or not they won (and negatively gradient if its an example of a loss!)

* Could train on examples of whether or not a random model won or lost.

* Needs Q-Learning probs. Should make Q-Learning (all of the above are pretty iffy and not bueno)


~~Let's discuss the use of git for this.~~
