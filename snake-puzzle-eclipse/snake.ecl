% Vietnam snake
% http://www.theguardian.com/science/alexs-adventures-in-numberland/2015/may/20/can-you-do-the-maths-puzzle-for-vietnamese-eight-year-olds-that-has-stumped-parents-and-teachers
%
% ECLiPSe 6.1 #199 - http://www.eclipseclp.org/
% Usage:
% eclipse -b electrifying.ecl -e main

:- lib(ic).
puzzle(A + 13 * B / C +
    D + 12 * E - F - 11 +
    G * H / I - 10 #= 66).
snake(Puzzle) :-
    term_variables(Puzzle, Vars),
    [A,B,C,D,E,F,G,H,I] = Vars,
    Vars :: 1..9,
    alldifferent(Vars),
    call(Puzzle),
    labeling(Vars).
main :-
    puzzle(Puzzle),
    findall(_, (
            snake(Puzzle),
            writeln(Puzzle)
        ), _).
