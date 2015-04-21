% http://puzzlor.com/2015-02_Coins.html
%
% ECLiPSe 6.1 #196 - http://www.eclipseclp.org/
% Usage:
% eclipse -b coins.ecl -e main

:- lib(ic).
:- lib(ic_global).
main :-
    dim(Coins, [3, 3]),
    Coins :: [1, 5, 10],
    occurrences(1, Coins, 3),
    occurrences(5, Coins, 3),
    occurrences(10, Coins, 3),
    sum(Coins[1, 1..3]) #= 11,
    sum(Coins[2, 1..3]) #= 12,
    sum(Coins[3, 1..3]) #= 25,
    sum(Coins[1..3, 1]) #= 21,
    sum(Coins[1..3, 2]) #= 16,
    sum(Coins[1..3, 3]) #= 11,
    labeling(Coins),
    ( foreacharg(Row, Coins) do
        array_list(Row, List),
        join_string(List, "\t", Line),
        writeln(Line)
    ).
