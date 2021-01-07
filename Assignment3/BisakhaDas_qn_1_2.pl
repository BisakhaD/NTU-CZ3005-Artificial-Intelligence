company(sumSum).
company(appy).
smartPhoneTech(galacticaS3).
boss(stevey).
competitor(sumsum,appy).
develop(sumsum, galacticaS3).
stole(stevey,galacticaS3).
rival(X) :- competitor(X,appy);competitor(appy,X).
business(X) :- smartPhoneTech(X).
unethical(X):- boss(X), stole(X,Y), business(Y), develop(Z,Y), rival(Z).
