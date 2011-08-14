/* Given a vector a and an index i returns the vector which
   omits the value a[i]. */
hati(a, i) =
{
local(n, j, b);
n = length(a);
b = vector(n - 1);
j = 1;
while(j <= n - 1,
	if(j < i, b[j] = a[j]);
	if(i <= j, b[j] = a[j + 1]);
	j = j + 1
);
return(b)
}

/* Given a vector a and an index i returns the vector which
   doubles the value a[i]. */
doublei(a, i) =
{
local(n, j, b);
n = length(a);
b = vector(n + 1);
j = 1;
while(j <= n + 1,
	if(j <= i, b[j] = a[j]);
	if(i < j, b[j] = a[j - 1]);
	j = j + 1
);
return(b)
}

/* Given a vector a of length n which we think of as a multi-index
	a[1]...a[n]
   we compute a list
   	[[l1, [a1], ..., [ln, [an]]
   where li is an integer and ai is a multi-index of length n - 1 such that
	d(s)_a = \sum li s_ai
   in the cech complex. */
diff_single(a) =
{
local(n, i, uit);
n = length(a);
uit = vector(n);
i = 1;
while(i <= n,
	uit[i] = [(-1)^(i - 1), hati(a, i)];
	i = i + 1
);
return(uit)
}

/* Given a list
   	lijst = [[l1, [a1], ..., [ln, [an]]
   compute a list
   	[[ll', [a1'], ..., [lm', [am']]
   such that
   	sum li d(s)_ai = sum li' s_{ai'}
   in the Cech complex. */
diff(lijst) =
{
local(n, uit, i, t, m, j);
n = length(lijst);
uit = [];
i = 1;
while(i <= n,
	t = diff_single(lijst[i][2]);
	m = length(t);
	j = 1;
	while(j <= m,
		t[j][1] = lijst[i][1]*t[j][1];
		j = j + 1
	);
	uit = concat(uit, t);
	i = i + 1
);
return(uit)
}

/* Computes the number of equal entries of the vector m starting at index i. */
nrequal(m, a) =
{
local(n, nr, i);
n = length(m);
nr = 1;
i = a + 1;
while((i <= n) && (m[i] == m[a]), i = i + 1; nr = nr + 1);
return(nr)
}

/* Given a vector a of length n which we think of as a multi-index
	a[1]...a[n]
   we compute a list
   	[[l1, [a1], ..., [ln, [an]]
   where li is an integer and ai is a multi-index of length n - 1 such that
	h(s)_a = \sum li s_ai
   in the cech complex, where h is the homotopy of Equation
   \ref{equation-second-homotopy} comparing semi-orderd Cech cochains with
   ordered cochains in the proof of
   	Cohomology, Lemma \ref{cohomology-lemma-alternating-usual}. */
h_single(m) =
{
local(n, uit, s, a, t);
n = length(m);
uit = [];
s = 0;
a = 1;
while(a <= n,
	if(((a == 1) || (m[a - 1] < m[a])) && (nrequal(m, a) > 1),
		if(s == 0,
			t = doublei(m, a);
			uit = concat(uit, [[(-1)^(a - 1), t]])
		);
		s = s + 1
	);
	a = a + 1
);
return(uit)
}

h(lijst) =
{
local(n, uit, i, t, m, j);
n = length(lijst);
uit = [];
i = 1;
while(i <= n,
	t = h_single(lijst[i][2]);
	m = length(t);
	j = 1;
	while(j <= m,
		t[j][1] = lijst[i][1]*t[j][1];
		j = j + 1
	);
	uit = concat(uit, t);
	i = i + 1
);
return(uit)
}

/* Given a list
   	lijst = [[l1, [a1], ..., [ln, [an]]
   compute a list
   	[[ll', [a1'], ..., [lm', [am']]
   such that
   	sum li s_ai = sum li' s_{ai'}
   in the Cech complex and such that the new list has no repeats. */
reduce(lijst) =
{
local(n, uit, i, j);
n = length(lijst);
uit = [];
i = 1;
while(i <= n,
	j = i + 1;
	while(j <= n,
		if(lijst[i][2] == lijst[j][2],
			lijst[i][1] = lijst[i][1] + lijst[j][1];
			lijst[j][1] = 0
		);
		j = j + 1
	);
	if(lijst[i][1] <> 0, uit = concat(uit, [lijst[i]]));
	i = i + 1
);
return(uit)
}

test(m) =
{
local(n, e, i, lijst);
n = length(m);
e = 1;
i = 1;
while(i < n,
	if(m[i] == m[i + 1], e = 0);
	i = i + 1
);
if(e == 0, lijst = [[-1, m]], lijst = []);
return(reduce(concat(lijst, concat(h(diff_single(m)), diff(h_single(m))))))
}

/* Does all tests with multi-indices having d entries. */
test_all(d) =
{
local(m, bits, i, j);
m = vector(d);
m[1] = 0;
bits = vector(d - 1);
i = 1;
while(i,
	j = 2;
	while(j <= d,
		m[j] = m[j - 1] + bits[d - j + 1];
		j = j + 1
	);
	if(test(m) <> [], error("Did not work for m = ", m));
	j = 1;
	while((j <= d - 1) && (bits[j] == 1), j = j + 1);
	if(j == d, print("Succes!"); return);
	bits[j] = 1;
	j = j - 1;
	while(j >= 1, bits[j] = 0; j = j - 1);
)
}
