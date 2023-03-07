/* 
CS 3210 - Principles of Programming Languages - Spring 2020
Author(s): Evan Birt
*/

begin :- 
  intro,
  undo,
  check(Bourbon), 
  solution(Bourbon), nl,
  write('To try again, just type begin.').

intro :-
  write('Welcome to this ES about Bourbon!'), nl,
  write('I am going to ask questions about Bourbon characteristics.'), nl,
  write('Please answer yes. or no.'), nl,
  ready(ready).

/* dynamic yes and no facts */
:- dynamic yes/1,no/1.

/* checks preexisting dynamic facts or/then creates new */
is_true(S) :- 
    (yes(S) -> true ;
    (no(S) -> fail ; 
    ask(S))).

/* creates new facts based on user input if they don't exist */
ask(Question) :- 
  question(Question),
  read(Response), nl, 
  ((Response == yes ; Response == y) -> 
  assert(yes(Question))) ; 
  (assert(no(Question)), fail).

/* Confirm if user wants to start or not with appropriate message */
ready(Question) :- 
    question(Question), 
    read(Response),   
    ((Response == yes ; Response == y) -> 
    writeln('Does this Whiskey have the following attributes: ')) ; 
    (writeln('Bye!'), fail).

/* Confirm if system guessed correctly/ provided correct information */
ending(Question) :- 
    question(Question), 
    read(Response),   
    ((Response == yes ; Response == y) -> 
    write('Nice!')) ; 
    (write('Not my fault! My designer did not give me enough information about Bourbons')).

/* undoes all asserts */
undo :- retract(yes(_)),fail.
undo :- retract(no(_)),fail. 
undo. 

/* start checking all types with KB */
check(Bourbon) :-
  bourbon(Bourbon), !.

/* Kowledge Base (KB). Could expand on this lots given the time or maybe add categories. */
bourbon(knob_creek) :-
  is_true(q1),
  is_true(q2),
	is_true(q3),
  is_true(q4),
  is_true(q5),
  is_true(smooth),
  is_true(spice).
bourbon(evan_williams) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
  is_true(q4),
  is_true(q5),
  is_true(smooth),
  is_true(cheap).
bourbon(traditional) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
  is_true(q4),
  is_true(q5),
  is_true(smooth).

bourbon(four_roses) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(spice),
  is_true(dry),
  is_true(single_barrel).
bourbon(woodford) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(spice),
  is_true(dry).
bourbon(rye) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(spice).

bourbon(rebel_yell) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(nutty),
  is_true(smooth).
bourbon(makers) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(nutty),
  is_true(cheap).
bourbon(wheat) :- 
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
  is_true(q5),
  is_true(nutty).

/* specific bourbons above here */
bourbon(bourbon) :-
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4),
	is_true(q5).

/* none as in not bourbons but can easily expand on other whiskey options here */
bourbon(none1) :-
  is_true(q2),
	is_true(q3),
	is_true(q4),
	is_true(q5).
bourbon(none2) :-
  is_true(q1),
	is_true(q3),
	is_true(q4),
	is_true(q5).
bourbon(none3) :-
  is_true(q1),
  is_true(q2),
	is_true(q4),
	is_true(q5).
bourbon(none4) :-
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q5).
bourbon(none5) :-
  is_true(q1),
  is_true(q2),
	is_true(q3),
	is_true(q4).

bourbon(unknown). /* last case None-Found */

/* questions asked */
question(ready) :- 
  write('ready? '), nl.
question(q1) :- 
  write('Made in the US? '), nl.
question(q2) :- 
  write('NO additives besides water? '), nl.
question(q3) :- 
  write('Over 80 proof? '), nl.
question(q4) :- 
  write('Aged 2 years minimum? '), nl.
question(q5) :- 
  write('%51-%80 corn content? '), nl.
question(spice) :- 
  write('Spicier flavors? '), nl.
question(smooth) :- 
  write('Extra smooth? '), nl.
question(nutty) :- 
  write('Nuttier flavors? '), nl.
question(cheap) :- 
  write('Very afforable? '), nl.
question(single_barrel) :- 
  write('Single Barrel whiskey? '), nl.
question(dry) :- 
  write('More dry? '), nl.
question(correctness) :- 
  write('Did I get it right? '), nl.


/* Endings possible. Is it correct? aka (ending(correctness)) question is only on most relevent solutions */
solution(unknown) :-
  write('Hmmm, I could not figure this one out...').
solution(bourbon) :-
  write('You have a bourbon but not sure which one!').

solution(knob_creek) :-
  write('This traditional bourbon is Knob Creek'), nl, ending(correctness).
solution(evan_williams) :-
  write('This traditional bourbon is Evan Williams'), nl, ending(correctness).
solution(traditional) :-
  write('This traditional bourbon is not in stock').

solution(four_roses) :-
  write('This high-rye bourbon is Four Roses'), nl, ending(correctness).
solution(woodford) :-
  write('This high-rye bourbon is Wordford Reserve'), nl, ending(correctness).
solution(rye) :-
  write('This high-rye bourbon is not in stock').

solution(rebel_yell) :-
  write('This high-wheat bourbon is Rebel Yell'), nl, ending(correctness).
solution(makers) :-
  write('This high-wheat bourbon is Makers Mark'), nl, ending(correctness).
solution(wheat) :-
  write('This high-wheat bourbon is not in stock').

solution(none1) :-
  write('Not a bourbon and it may be called whisky not whiskey with an e!'), nl, ending(correctness).
solution(none2) :-
  write('Not a bourbon but it could be Jack Daniels!'), nl, ending(correctness).
solution(none3) :-
  write('Nota bourbon and weak whiskey!'), nl, ending(correctness).
solution(none4) :-
  write('Not a bourbon this cannot be called straight whiskey having been so young!'), nl, ending(correctness).
solution(none5) :-
  write('Not a bourbon but still taisty whiskey!'), nl, ending(correctness).

