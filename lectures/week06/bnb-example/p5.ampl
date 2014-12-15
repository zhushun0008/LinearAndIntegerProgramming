var x1  >= 0, <= 10;
var x2  >= 0, <= 0;
var x3  >= 3, <= 4;
var x4  >= 0, <= 10;
var x5  >= 0, <= 10;
var x6  >= 0, <= 10;

maximize obj: -x1 - 2* x2 -0.5 * x3 - 0.2* x4 - x5 +0.5* x6;

c1: x1 + 2 * x2 >= 1; # Alternatively: x1 + x2 >= 1
c2: x1 + x2 + 3* x6 >= 1;
c3: x1 + x2 + x6 >= 1;
c4: x3 - 3* x4  >= 1;
c5: x3 - 2* x4 -5* x5 >= 1;
c6: x4 + 3* x5 -4 *x6   >= 1;
c7: x2 + x5 + x6 >= 1;

solve;

display x1, x2,x3, x4, x5, x6;
printf 'Optimal Value: %f\n', -(x1 + 2* x2 +0.5 * x3+ 0.2* x4 + x5 -0.5* x6);

end;