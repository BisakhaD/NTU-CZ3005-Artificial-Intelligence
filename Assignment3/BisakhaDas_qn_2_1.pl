offspring(prince, charles).
offspring(princess, ann).
offspring(prince, andrew).
offspring(prince, edward).

older(charles, ann).
older(ann, andrew).
older(andrew, edward).

male(A):- offspring(prince,A).
female(A):- offspring(princess,A).

is_older(X, Y):- older(X, Y).
is_older(A, B):- older(A, X),is_older(X, B).

in_order(X, Y) :- offspring(prince, X), offspring(princess, Y).
in_order(X, Y) :- offspring(A, X), offspring(A, Y), is_older(X, Y).

bubble_sort(List,Sorted):-b_sort(List,[],Sorted).
b_sort([],Acc,Acc).
b_sort([H|T],Acc,Sorted):-bubble(H,T,NT,Max),b_sort(NT,[Max|Acc],Sorted).

bubble(X,[Y|T],[X|NT],Max):-in_order(X, Y),bubble(Y,T,NT,Max).
bubble(X,[Y|T],[Y|NT],Max):- not(in_order(X, Y)),bubble(X,T,NT,Max).
bubble(X,[],[],X).

successionLine(X):- 
findall(Y,offspring(_,Y),OffspringList),bubble_sort(OffspringList,X).