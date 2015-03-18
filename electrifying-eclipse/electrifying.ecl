% ECLiPSe 6.1 #196 - http://www.eclipseclp.org/
% Usage:
% eclipse -b electrifying.ecl -e main

:- lib(ic).
:- lib(branch_and_bound).

solve(HouseXs, HouseYs, K, GenXs, GenYs, Cost) :-
    dim(HouseXs, [N]),
    MaxX #= max(HouseXs), MaxY #= max(HouseYs),
    dim(GenXs, [K]), dim(GenYs, [K]),
    GenXs :: 1..MaxX, GenYs :: 1..MaxY,
    ( for(I, 1, N), foreach(Di, Distances), param(HouseXs, HouseYs, GenXs, GenYs, K) do
        ( for(J, 1, K), fromto(1.0Inf, Dprev, Dcurr, Di), param(I, HouseXs, HouseYs, GenXs, GenYs) do
            Dcurr $= min(Dprev, sqrt(sqr(HouseXs[I] - GenXs[J]) + sqr(HouseYs[I] - GenYs[J])))
        )
    ),
    Cost $= sum(Distances),
    bb_min(search([](GenXs, GenYs), 0, most_constrained, indomain_middle, complete, []), Cost, bb_options{delta:0.1}).
%    bb_min(labeling([](GenXs, GenYs)), Cost, bb_options{delta:0.1}).

main :-
    HouseXs = [](2, 2, 3, 3, 4, 4,  5, 5, 5, 5, 6, 6, 7, 7, 8, 8, 8, 9, 9, 10),
    HouseYs = [](2, 5, 6, 8, 2, 10, 2, 3, 6, 8, 1, 5, 2, 8, 5, 7, 8, 4, 7, 3),
    solve(HouseXs, HouseYs, 3, GenXs, GenYs, Cost),
    ( foreacharg(X, GenXs), foreacharg(Y, GenYs) do
        LetterCode is 0'A + Y - 1,
        char_code(Letter, LetterCode),
        write(X), write(Letter), nl
    ).
