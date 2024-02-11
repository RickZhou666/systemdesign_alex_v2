# 06. Design consistent hashing
https://bytebytego.com/courses/system-design-interview/design-consistent-hashing


## Rehashing problems

<br><br><br>

## Consistent hashing
1.  a change in the number of array slots causes nearly all keys to be remapped

<br><br>

## Hash spece and hash ring
1. SHA-1 as hashfunction. x0 -> 0, xn -> 2^160 - 1. all other hash fall between 0 and 2^160-1

## Hash servers

## Hash keys
1. there is no modular operation

## server lookup

## add a server
1. adding a new server will only require redistribution of a fraction of keys


## remove a server
1. only fraction of keys will be redistributed

##  two issues in the basic approach
1. consistent hashing basic steps:
    - map servers and keys on to the ring using a uniformly distributed hash function
    - find out which server a key is mapped to, go clockwise until meet first server

2. two problems
    - it is impossible to keep the same size of partitions
    - it is possible to have a non-uniform keys distribution on the ring


## virtual nodes
1. a virtual node refers to the real node, reach server is represented by multiple virtual nodes
    - in real world, the number of virtual nodes is much larger
2. as the number of virtual nodes increases, the distribution of keys becomes more balanced

## find affected keys


