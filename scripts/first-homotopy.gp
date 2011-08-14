/* Given a vector a returns i where i is the
   smallest index with a[i] minimal among the entries of a. */
smallest(a) =
{
local(n, f, i, j);
n = length(a);
f = a[1];
i = 1;
j = 2;
while(j <= n,
	if(a[j] < f, f = a[j]; i = j);
	j = j + 1
);
return(i)
}

/* Given a vector a and an index i returns j where
j > i is the smallest index with a[j] = a[i], if such an index does
not exist j is the smallest index such that a[j] > a[i] is minimal among
the entries if a bigger than a[i]. */
next_smallest(a, i) =
{
local(n, f, j, g, k);
n = length(a);
f = a[i];
j = i + 1;
while(j <= n,
	if(a[j] == f, return(j));
	j = j + 1
);
j = 1;
g = f - 1;
while(j <= n,
	if(a[j] > f, if((a[j] < g) || (g < f), g = a[j]; k = j));
	j = j + 1
);
return(k)
}

/* Given a vector a makes the unique permutation s such that
	a[s[1]] <= a[s[2]] <= ... <= a[s[n]]
   and
   	a[s[i]] = a[s[i + 1]] implies s[i] < s[i + 1]. */
make_sigma(a) =
{
local(n, b, t, i);
n = length(a);
b = vector(n);
t = smallest(a);
b[1] = t;
i = 2;
while(i <= n,
	t = next_smallest(a, t);
	b[i] = t;
	i = i + 1
);
return(b)
}

/* Given a permutation s of length n and 1 <= a <= n makes the
   unique permutation sa such that
	sa[i] = s[i] for 1 <= i < a, and
	sa[a] < sa[a + 1] < ... < sa[n].
   Of course this implies that sa[j] for j >= a omits the values
   s[i] (i < a) which have already been mapped to. */
make_sigma_a(s, a) =
{
local(n, sa, i, j, k);
n = length(s);
sa = vector(n);
i = 1;
while(i < a,
	sa[i] = s[i];
	i = i + 1;
);
i = 1;
j = a;
while((i <= n) && (j <= n),
	k = 1;
	while(k < a,
		if(s[k] == i, i = i + 1; k = 0);
		k = k + 1
	);
	sa[j] = i;
	j = j + 1;
	i = i + 1
);
return(sa)
}

/* Computes the sign of a permutation. */
sign_perm(s) =
{
local(n, i, j, t);
n = length(s);
t = 1;
i = 1;
while(i < n,
	j = i + 1;
	while(j <= n,
		if(s[i] > s[j], t = -t);
		j = j + 1
	);
	i = i + 1
);
return(t)
}

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

/* Given a vector a of length n which we think of as a multi-index
	a[1]...a[n]
   we compute a list
   	[[l1, [a1], ..., [ln, [an]]
   where li is an integer and ai is a multi-index of length n - 1 such that
	h(s)_a = \sum li s_ai
   in the cech complex, where h is the homotopy of Equation
   \ref{equation-first-homotopy} comparing Cech cochain with
   semi-alternating cochains in the proof of
   	Cohomology, Lemma \ref{cohomology-lemma-alternating-usual}. */
h_single(m) =
{
local(n, uit, s, e, t, a, sa, ea, i);
n = length(m);
uit = vector(n);
s = make_sigma(m);
e = sign_perm(s);
t = vector(n + 1);
a = 1;
while(a <= n,
	sa = make_sigma_a(s, a);
	ea = sign_perm(sa);
	i = 1;
	while(i <= a,
		t[i] = m[s[i]];
		i = i + 1
	);
	i = a;
	while(i <= n,
		t[i + 1] = m[sa[i]];
		i = i + 1
	);
	uit[a] = [(-1)^(a - 1)*ea, t];
	a = a + 1
);
return(uit)
}

/* Given a list
   	lijst = [[l1, [a1], ..., [ln, [an]]
   compute a list
   	[[ll', [a1'], ..., [lm', [am']]
   such that
   	sum li h(s)_ai = sum li' s_{ai'}
   in the Cech complex. */
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

/* The outcome should be [] in order for formula
	Cohomology, Equation \ref{cohomology-equation-homotopy}
   to be correct. */
test(m) =
{
local(n, s, ms, i, lijst);
n = length(m);
s = make_sigma(m);
ms = vector(n);
i = 1;
while(i <= n,
	ms[i] = m[s[i]];
	i = i + 1
);
lijst = [[-1, m], [sign_perm(s), ms]];
return(reduce(concat(lijst, concat(h(diff_single(m)), diff(h_single(m))))))
}

/* Does 1000 random tests with multi-indices having d entries. */
test_random(d) =
{
local(m, i, j);
m = vector(d);
i = 1;
while(i <= 1000,
	j = 1;
	while(j <= d,
		m[j] = random(d);
		j = j + 1
	);
	if(test(m) <> [], print("Error for m = ", m,"."));
	i = i + 1
)
}
