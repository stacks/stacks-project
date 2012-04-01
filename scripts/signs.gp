/* epsilon = a*N*M + b*N*P + c*N*R + d*M*P + e*M*R + f*P*R */
epsilon = 0*N*M + 1*N*P + 1*N*R + 0*M*P + 0*M*R + 1*P*R + R
/* + g*N + h*M + i*P + j*R */

fill(aa, bb, cc, dd) =
{
local(AA);
AA = subst(subst(subst(subst(epsilon, N, aa), M, bb), P, cc), R, dd);
return(AA)
}


/* Cup product is a map of complexes */

test1() =
{
local(AA, BB);
AA = p + 1 + fill(n, m, p + 1, r);
BB = fill(n + 1, m, p + 1, r) + r;
return(AA - BB)
}

test2() =
{
local(AA, BB);
AA = p + 1 + fill(n, m, p + 1, r) + n - r;
BB = n + fill(n, m + 1, p + 1, r) + p + 1 - r;
return(AA - BB)
}

test3() =
{
local(AA, BB);
AA = fill(n + 1, m, p + 1, r) + r;
BB = 1 + n + fill(n, m + 1, p + 1, r - 1);
return(AA - BB)
}

test4() =
{
local(AA, BB);
AA = fill(n, m, p, r);
BB = n + fill(n, m + 1, p + 1, r) - r;
return(AA - BB)
}

test5() =
{
local(AA, BB);
AA = fill(n, m, p, r - 1);
BB = fill(n + 1, m, p + 1, r);
return(AA - BB)
}

test1
test2
test3
test4
test5


/* The associativity of cup product */

associative() =
{
local(AA, BB, CC, DD);
AA = fill(a + b, c, p, r);
BB = fill(a, b, r, s);
CC = fill(a, b + c, p, s);
DD = fill(b, c, p - s, r - s);
return(AA + BB - CC - DD)
}

associative


/* The graded commutativity of cup product */

chi(t) =
{
return (t*(t + 1)/2)
}

commutative() =
{
local(AA, BB, CC, DD);
AA = fill(n, m, p, r) + (n - r)*(m - (p - r));
BB = n*m + chi(p) + fill(m, n, p, p - r) + chi(r) + chi(p -r);
return(AA - BB)
}

commutative
