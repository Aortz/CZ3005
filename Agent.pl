 %% Demo coming from http://clwww.essex.ac.uk/course/LG519/2-facts/index_18.html
%%
%% Please load this file into SWI-Prolog
%%
%% Sam's likes and dislikes in food
%%
%% Considering the following will give some practice
%% in thinking about backtracking.
%%
%% You can also run this demo online at
%% http://swish.swi-prolog.org/?code=https://github.com/SWI-Prolog/swipl-devel/raw/master/demo/likes.pl&q=likes(sam,Food).

/** <examples>
?- likes(sam,dahl).
?- likes(sam,chop_suey).
?- likes(sam,pizza).
?- likes(sam,chips).
?- likes(sam,curry).
*/

%------------------------------------------------------------------------------
% Declaring dynamic methods

:- dynamic ([
             wall/2,tingle/2,visited/2,move/2,stench/2,current/3,glitter/2, hasarrow/0,reborn/0,reposition/1,turn/1,gold/2,init/1,wumpus/2,sameDirection/2,
       confundus/2,start/1,safe/2,explored/3	    ]).


%------------------------------------------------------------------------------



% DEFINING THE PERCEPTORS

% Helper predicate to check if cell position given is valid in the board.

validposition([X,Y]) :-
    X > -1,
    X < 5,
    Y > -1,
    Y < 4.


% Generate adjacent positions of a given position.
adjacent(X,Y,Xa,Ya):- (Left is Xa-1),X=Left, Y=Ya.
adjacent(X,Y,Xa,Ya):- Right is Xa+1, X=Right, Y=Ya.
adjacent(X,Y,Xa,Ya):- Above is Ya+1, X=Xa, Y=Above.
adjacent(X,Y,Xa,Ya):- Below is Ya-1, X=Xa, Y=Below.


%% TAKING THE ACTIONS

explore(L) :-
   (
    current(X,Y,D),
    \+recurExplore(L,X,Y,D),
    \+glitter(_,_)->
    (
       retractall(explored(_,_,_)),
       assertz(explored(X,Y,D)),
       returnToOrigin(L,X,Y,D)
     ));
    (
       (
        current(X,Y,_),
        glitter(X,Y))->
        L=[pickup]
    );
    (
       (
        current(X,Y,D),
       \+glitter(X,Y),
         (
            possible(_,_)
        )->
       (
          retractall(explored(_,_,_)),
          assertz(explored(X,Y,D)),
          recurExplore(L,X,Y,D)
       )
       )
     ).

possible(A,B) :-
    safe(A,B),
    \+visited(A,B),
    \+current(A,B,_),
    \+wall(A,B).


recurExplore([],X,Y,_) :-
    \+visited(X,Y).

recurExplore(L,X,Y,D) :-
    [H|Tail] = L,
    (H=moveforward;H=turnleft;H=turnright),
    ((H=moveforward->D1=D, forward(X,Y,D,X1,Y1));
    (H=turnleft->X1=X, Y1=Y, turnleft(D, D1));
    (H=turnright->X1=X, Y1=Y, turnright(D, D1))),
    safe(X1,Y1),
    \+explored(X1,Y1,D1),
    assertz(explored(X,Y,D)),
    recurExplore(Tail,X1,Y1,D1).


returnToOrigin(L,0,0,_) :-
    L=[].


returnToOrigin(L,X,Y,D) :-
    [H|Tail] = L,
    (H=turnleft;H=turnright;H=moveforward),
    ((H=turnleft->X1 is X, Y1 is Y, turnleft(D, D1));
    (H=turnright->X1 is X, Y1 is Y, turnright(D, D1));
    (H=moveforward->D1=D, forward(X,Y,D,X1,Y1))),
    visited(X1,Y1),
    \+explored(X1,Y1,D1),
    assertz(explored(X,Y,D)),
    returnToOrigin(Tail,X1,Y1,D1).


turnleft(D,D1) :-
    (D==rnorth->
        D1=rwest);
    (D==reast->
        D1=rnorth);
    (D==rsouth->
    D1=reast);
    (D==rwest->
        D1=rsouth).

turnright(D,D1) :-
    (D==rnorth->
        D1=reast);
    (D==reast->
        D1=rsouth);
    (D==rsouth->
        D1=rwest);
    (D==rwest->
        D1=rnorth).

forward(X,Y,D,X1,Y1) :-
    (D==rnorth->
        X1=X,Y1 is Y+1);
    (D==reast->
        X1 is X+1,Y1=Y);
    (D==rsouth->
        X1=X,Y1 is Y-1);
    (D==rwest->
        X1 is X-1,Y1=Y).

check_wumpus(Xa,Ya):-
    (
    stench(Xa,Ya),
    adjacent(X,Y,Xa,Ya),
    \+wumpus(X,Y),
    \+visited(X,Y))->(
    assert(wumpus(X,Y)),
    check_wumpus(Xa,Ya)
    ).

check_confundus(Xa,Ya) :-
    (
    tingle(Xa,Ya),
    adjacent(X,Y,Xa,Ya),
    \+confundus(X,Y),
    \+visited(X,Y))->(
    assert(confundus(X,Y)),
    check_confundus(Xa,Ya)
    ).

reborn :-
    retractall(turn(_)),
    assert(turn(1)),
    reposition([on,off,off,off,off,off]).

reposition(L) :-
    ((turn(1)
    )->
    (
    assert(hasarrow),
    retractall(current(_,_,_)),
    retractall(stench(_,_)),
    retractall(glitter(_,_)),
    retractall(visited(_,_)),
    retractall(tingle(_,_)),
    retractall(wumpus(_,_)),
    retractall(confundus(_,_)),
    retractall(gold(_,_)),
    retractall(wall(_,_)),
    retractall(explored(_,_,_)),
    assert(visited(0,0)),
    assert(current(0,0,rnorth)),
    L=L
    ));
    (
    retractall(current(_,_,_)),
    retractall(stench(_,_)),
    retractall(glitter(_,_)),
    retractall(visited(_,_)),
    retractall(tingle(_,_)),
    retractall(wumpus(_,_)),
    retractall(confundus(_,_)),
    retractall(gold(_,_)),
    retractall(wall(_,_)),
    retractall(explored(_,_,_)),
    assert(visited(0,0)),
    assert(current(0,0,rnorth))
    ).

gold(X,Y) :-
    glitter(X,Y),
    current(X,Y,_).

safe(X1,Y1):-
   (
    (
    visited(X,Y),
    \+wall(X,Y),
    X1=X,
    Y1=Y);
    (
    (visited(X,Y),
    \+wall(X,Y),
    adjacent(X1,Y1,X,Y),
    \+confundus(X1,Y1),
    \+wumpus(X1,Y1)),
    \+wall(X1,Y1))
    ).

isOn(X) :-
    X==on.

prevPos(X,Y,D) :-
    current(X0,Y0,D0),
    ((D0==rnorth->(X=X0,Y is Y0-1,D=D0));
    (D0==reast->(X is X0-1,Y=Y0,D=D0));
    (D0==rsouth->(X=X0,Y is Y0+1,D=D0));
    (D0==rwest->(X is X0+1,Y=Y0,D=D0))).

nextPos(X,Y,D) :-
    current(X0,Y0,D0),
    ((D0==rnorth->(X=X0,Y is Y0+1,D=D0));
    (D0==reast->(X is X0+1,Y=Y0,D=D0));
    (D0==rsouth->(X=X0,Y is Y0-1,D=D0));
    (D0==rwest->(X is X0-1,Y=Y0,D=D0))).


sameDirection(X1,Y1) :-
    current(X,Y,D),
    stench(X,Y),
    ((D==rnorth->(X1 is X,Y1 is Y+1));
    (D==reast->(X1 is X+1,Y1 is Y));
    (D==rsouth->(X1 is X,Y1 is Y-1));
    (D==rwest->(X1 is X-1,Y1 is Y))).

/*
    H is X1-X,
    V is Y1-Y,
    (H=:=1,V=:=0,D==reast);
    (H=:=0,V=:=1,D==rnorth);
    (H=:=(-1),V=:=0,D==rwest);
    (H=:=0,V=:=(-1),D==rsouth).*/

move(moveforward,L) :-
    (
    nth1(1,L,Confounded),
    isOn(Confounded)->
    reposition(L));
    (
        turn(K),
        nth1(2,L,Stench),
        current(X,Y,D),
        nextPos(X1,Y1,D),
        isOn(Stench)->
        assert(visited(X1,Y1)),
        assert(stench(X1,Y1)),
        retract(current(X,Y,D)),
        assert(current(X1,Y1,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N)),
        check_wumpus(X1,Y1)
    );
    (
        turn(K),
        nth1(3,L,Tingle),
        current(X,Y,D),
        nextPos(X1,Y1,D),
        isOn(Tingle)->
        assert(visited(X1,Y1)),
        assert(tingle(X1,Y1)),
        retract(current(X,Y,D)),
        assert(current(X1,Y1,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N)),
        check_confundus(X1,Y1)

    );
    (
        turn(K),
        nth1(4,L,Glitter),
        current(X,Y,D),
        nextPos(X1,Y1,D),
        isOn(Glitter)->
        assert(glitter(X1,Y1)),
        retract(current(X,Y,D)),
        assert(current(X1,Y1,D)),
        assert(visited(X1,Y1)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (
        turn(K),
        nth1(5,L,Bump),
        nextPos(X1,Y1,_),
        (
            isOn(Bump)->
            assert(wall(X1,Y1)),
            assert(visited(X1,Y1)),
            N is K+1,
            retract(turn(K)),
            assert(turn(N))

    ));
    (
        turn(K),
        current(X,Y,D),
        nextPos(X1,Y1,D),
        nth1(1,L,Confounded),
        nth1(2,L,Stench),
        nth1(3,L,Tingle),
        nth1(5,L,Bump),
        \+isOn(Confounded),\+isOn(Stench),\+isOn(Bump),\+isOn(Tingle)
        ->
        retract(current(X,Y,D)),
        assert(current(X1,Y1,D)),
        assert(visited(X1,Y1)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))
    ).

move(turnleft,_) :-
    current(X,Y,D),turn(K),
    (
    (D==rnorth->
        assert(current(X,Y,rwest)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==reast->
        assert(current(X,Y,rnorth)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==rsouth->
        assert(current(X,Y,reast)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==rwest->
        assert(current(X,Y,rsouth)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    )
    ).

move(turnright,_) :-
    current(X,Y,D),turn(K),
    (
    (D==rnorth->
        assert(current(X,Y,reast)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==reast->
        assert(current(X,Y,rsouth)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==rsouth->
        assert(current(X,Y,rwest)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    );
    (D==rwest->
        assert(current(X,Y,rnorth)),
        retract(current(X,Y,D)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))

    )
    ).

move(pickup,_) :-
    (current(X,Y,_),glitter(X,Y),turn(K)->(
    retractall(glitter(X,Y)),
    retractall(gold(_,_)),
    N is K+1,
    retract(turn(K)),
    assert(turn(N)))).


move(shoot,L) :-
    (
    retract(hasarrow),
    (
    turn(K),
    (
        nth1(6,L,Scream)),
        isOn(Scream))->
    (
        retractall(stench(_,_)),
        retractall(wumpus(_,_)),
        N is K+1,
        retract(turn(K)),
        assert(turn(N))
    ));
    (
        turn(K),
        (
        sameDirection(X1,Y1),
        nth1(6,L,Scream),
        \+isOn(Scream))->(
            retract(wumpus(X1,Y1)),
            N is K+1,
            retract(turn(K)),
            assert(turn(N))
        )
    ).


