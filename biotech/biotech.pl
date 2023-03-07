/* 
CS 3210 - Principles of Programming Languages - Spring 2020
Author(s): Evan Birt
Answer: Joel is interested in biotech companies 
*/

:- use_module(library(clpfd)).

sol([City, Investment, Tie, Name, Area, Age]) :-

/* each target variable can be seen as a list of variables themselves*/
City        = [Atlanta, Los_Angeles, Miami,      New_York, San_Francisco],
Investment  = [One,     Two,         Three,      Four,     Five         ],
Tie         = [Black,   Blue,        Green,      Purple,   Red          ],
Name        = [Adam,    Dave,        Joe,        Matt,     Pierre       ],
Area        = [Biotech, Clean_Tech,  Healthcare, Internet, Software     ],
Age         = [Thirty, Thirty_Five, Forty, Forty_Five,     Fifty        ],

/* the values in each list are exclusive*/
all_different(City),
all_different(Investment),
all_different(Tie),
all_different(Name),
all_different(Area),
all_different(Age),

/* values in 1..5*/
City       ins 1..5,
Investment ins 1..5,
Tie        ins 1..5,
Name       ins 1..5,
Area       ins 1..5,
Age        ins 1..5,

/* hint #1 - the investor who lives in San Francisco is somewhere between the investor who invested $5 millions last month and the investor who lives in Los Angeles, in that order;*/
(San_Francisco #> Five #/\ San_Francisco #< Los_Angeles),

/* hint #2 - at the fourth position is the investor interested in Healthcare companies;*/
Healthcare #= 4,

/* hint #3 - the investor who invested $3 millions last month is somewhere between the investor wearing the Red tie and the investor who invested $2 millions last month, in that order;*/
(Three #> Red #/\ Three #< Two),

/* hint #4 - at the fifth position is the investor interested in Internet companies;*/
Internet #= 5,

/* hint #5 - the investor wearing the Red tie is somewhere to the left of the investor interested in Healthcare companies;*/
Red #< Healthcare,

/* hint #6 - the investor that lives in Miami is next to the investor interested in Clean tech companies;*/
(Miami #= Clean_Tech - 1 ; Miami #= Clean_Tech + 1),

/* hint #7 - the investor wearing the Red tie is somewhere between the investor who invested $5 millions last month and the investor wearing the Black tie, in that order;*/
(Red #> Five #/\ Red #< Black),

/* hint #8 - at one of the ends is the investor who did a $4 millions investment last month;*/
(Four #= 1 ; Four #= 5),

/* hint #9 - Matt is next to the 45 years old man;*/
(Matt #= Forty_Five - 1 ; Matt #= Forty_Five + 1),

/* hint #10 - Pierre is somewhere to the right of the investor wearing the Blue tie;*/
Pierre #> Blue,

/* hint #11 - the 40 years old man is next to the investor interested in Healthcare companies;*/
(Forty #= Healthcare - 1 ; Forty #= Healthcare + 1),

/* hint #12 - the man wearing the Red tie is somewhere between the man wearing the Green tie and the youngest man, in that order;*/
(Red #> Green #/\ Red #< Thirty),

/* hint #13 - the investor wearing the Red tie is next to the investor who lives in Atlanta;*/
(Red #= Atlanta - 1 ; Red #= Atlanta + 1),

/* hint #14 - Dave is exactly to the left of the 30 years old man;*/
(Dave #= Thirty - 1),

/* hint #15 - the investor interested in Biotech companies is next to the investor who lives in Atlanta;*/
(Biotech #= Atlanta - 1 ; Biotech #= Atlanta + 1),

/* hint #16 - the 35 years old man is somewhere between Adam and the investor interested in Software companies, in that order;*/
(Thirty_Five #> Adam #/\ Thirty_Five #< Software),

/* hint #17 - the 45 years old investor is exactly to the right of the investor that invested $2 millions last month;*/
(Forty_Five #= Two + 1),

/* hint #18 - the investor wearing the blue tie is interested in Software companies;*/
Blue #= Software,

/* hint #19 - the 40 years old man is next to the man wearing the Purple tie; and*/
(Forty #= Purple - 1 ; Forty #= Purple + 1),

/* hint #20 - at the first position is the investor who lives in New York.*/
New_York #= 1,

/* show the solution using numbers 1..5 */
flatten([City, Investment, Tie, Name, Area, Age], List), label(List).
