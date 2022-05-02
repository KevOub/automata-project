REFERENCE:
https://github.com/rohaquinlop/automathon
https://www.usna.edu/Users/cs/wcbrown/courses/F18SI340/lec/l18/lec.html
https://medium.com/swlh/visualizing-thompsons-construction-algorithm-for-nfas-step-by-step-f92ef378581b

## ALGORITHM FOR VALIDATION

create queue - reverse list
add initial state

1) Check if index is equal to the length of input string
   1) If so, check if in final state
2) Check if the string at index is accepted by the language
3) Check if the state is in the transition table (delta)
   1) For each possible transition, check if `d` == string
      1) IF matched add all transition states to the queue
      2) Each state will be dequeued and tested for validity against above
4) If the string reached a final state (index == length of string && state == final state) or the queue is empty, fin