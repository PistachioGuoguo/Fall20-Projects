# King Othello: Othello with King pieces - Fall20-Projects

Author: Zizhou Sang ([zsang2@illinois.edu](mailto:zsang2@illinois.edu))

Presentation slides: [Google Drive link](https://drive.google.com/file/d/1ap3_Gis_JBwC4pjCGbQatRcWOkHf6F7K/view?usp=sharing)

## Introduction

Othello is a popular board game with simple rules but rich tactics. This semester in IS 597 DSO final project, one of the direction was to make some **original variation** of an existing board game. Othello, a game I first found on *Windows XP* 12 years ago (called *Internet Reversi* that time), came to my mind.

My original variation is to allowing 5 king pieces for each side, that can be placed anytime during a game. The specific rules are as follows:

1. A king can only be flipped when directly sandwiched by two opponent’s kings

    ♔ ⚫ ⚫ ♚ ⚫  x     -> (valid to place a white king at "x")   ->         ♔ ⚪ ⚪ ⚪ ⚪ ♔
    
    ♔ ⚪ ⚫ ⚫ ♚  x      (this time, it's invalid to place a white king at "x", as the **nearest** opponent piece of the Black king is a common white piece)  
2.  When flipped (captured), it becomes a common piece owned by opponent (see diagram above)
3. Each player have 5 king pieces in a game
4. The rest rules are all same with normal Othello


For more information, please see [my slides on Google Drive](https://drive.google.com/file/d/1ap3_Gis_JBwC4pjCGbQatRcWOkHf6F7K/view?usp=sharing), thanks.


## How to play

Currently the GUI is simple and only has one mode: human (Black) versus a minimax based AI (white).
1. Run ```GUI_king.py```

1. To put a common piece, just LEFT click where you want to put the piece on the screen

2. To put a king piece, RIGHT click where you want ot put on the screen

3. Each player only has 5 king pieces, but the program will not remind you how many king pieces you still have. If you run out of your King pieces, you have to go with your common pieces.

Please forgive the GUI is simple, because PyQt5 is really too colossal for me to pick up in a short time :( So I just implemented the most basic version

Also the AI is not that smart, but please feel free to change the settings in ```kingOthello.py```. Thanks.

Notice: There are also some normal Othello AI and functions in other files. Please see my slide for more information.
## Acknowledgments

Big thanks to instructor [Mr. Weible](https://ischool.illinois.edu/people/john-weible), as I really learned a lot and had great fun from IS 597 DSO this semester!


## Reference

1. Alpha-beta minimax algorithm, [Sebastian Lague - Youtube](https://www.youtube.com/watch?v=l-hh51ncgDI)

2. Reversi evaluation function, [DHConnelly](http://dhconnelly.com/paip-python/docs/paip/othello.html)

3. GUI Part, I learned some PyQt5 techniques from this [Gomoku Project - Github](https://github.com/ColinFred/GoBang#gobang)


