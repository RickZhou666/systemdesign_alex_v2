# 26. Real Time Gaming Leaderboard

<br><br><br>

## Step 1 - Understand the problem
- display top 10 or all?
    - each page top 10 and user can check their pos
- DAU?
    - 5 million, 25 million Monthly Active Users(MAU)
    - 10 matches for each user per day
- same score?
- real time?
    - not a batch story

<br><br>

### functional requirements
1. display top 10 players on the leaderboard
2. show a users specific rank
3. display players who are 4 places above and below the desired user

### non-functional requirements
1. real time update on scores
2. score update is reflected on the leaderboard in real-time
3. general scalability, availability and reliability requirements

### back-of-the-envelope estimation
1. 5 million DAU -> 5*10^6 / 10^5 seconds = ~50 active users per second
    - but people mostly like play during the night, we assume the peak is 5 times more than 250 users per second
2. QPS for users scoring a point: if a user play 10 games per day, QPS = 50 * 10 = ~500; for the peak QPS = 250 * 10 = ~2500
3. QPS for fetching the top 10 leaderboard: assume a user opens a game once a day and top 10 leaderboard is loaded only when a user first opens the game.


<br><br><br>

## Step 2 - Propose high-level design and get buy-in

### 2.1 API design

<br><br>

### 2.2 High-level architecture

<br><br>

### 2.3 data models

<br><br><br>

## Step 3 - Design Deep Dive

<br><br><br>

## Step 4 - Wrap up