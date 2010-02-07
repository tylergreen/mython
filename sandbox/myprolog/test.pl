length([],0)
length([H|T],N) :- length(T,Nt), N is Nt+1

length([a,b,c],X)?	