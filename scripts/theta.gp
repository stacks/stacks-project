p = 3

/*
We will use z and l as the variables, where l corresponds to what
is called lambda in the text; then we have
	xi = z^p - l
in this notation.
*/

/*
This computes z^i xi^[n]
*/
monomial(t) =
{
local(i, n);
i = t[1];
n = t[2];
return( z^i * (z^p - l)^n * (n!)^(-1))
}

/*
This finds the "leading coefficient" c in the expansion
	f = sum c_{i, n} z^i xi^[n]
*/
leading(f) =
{
local(d, c, i, n);
if(f == 0, return([0, 0, 0]));
d = poldegree(f, z);
c = polcoeff(f, d, z);
i = d % p;
n = (d - i)/p;
c = c * (n!);
return([i, n, c])
}

/*
This function associates to a polynomial f in z and l
the coefficients c_{i, n} such that
	f = sum c_{i, n} z^i xi^[n]
*/
decompose(f) =
{
local(t, u);
t = leading(f);
u = [t];
while(t[1] + t[2] > 0,
	f = f - t[3]*monomial(t);
	t = leading(f);
	u = concat(u, [t]);
);
return(u)
}

/*
This puts a sequence of coefficients c_{i, n}
back into a polynomial in z and l.
*/
putback(u) =
{
local(f, j);
f = 0;
j = 1;
while(j <= length(u),
	f = f + u[j][3]*monomial(u[j]);
	j = j + 1
);
return(f)
}

/*
Is each of the coefficients c_{i, n} p-adically integral?
*/
is_integral(u) =
{
local(j, c);
j = 1;
while(j <= length(u),
	c = u[j][3];
	if(valuation(c, p) < 0, return(0));
	j = j + 1
);
return(1)
}

/*
Our choice of theta. Have to use capitalized theta as
theta already exits in pari/gp.
*/
Theta_monomial(t) =
{
local(j, m);
j = t[1];
m = t[2];
if(j >= p, error("Power z too high."));
if(m == 0, return([[j + 1, 0, p*t[3]/(j + 1)], [0, 0, 0]]));
if(j == p - 1, return([[0, m + 1, t[3]], [0, 0, 0]]));
return(
[[j + 1, m, p*t[3]/(j + 1 + p*m)], [j, m - 1, - t[3]*p*l/(j + 1 + p*m)]]
)
}

Theta(u) =
{
local(v, i, t, tt);
v = [];
i = 1;
while(i <= length(u),
	t = u[i];
	tt = Theta_monomial(t);
	while(tt[2][3],
		v = concat(v, [tt[1]]);
		t = tt[2];
		tt = Theta_monomial(t)
	);
	v = concat(v, [tt[1]]);
	i = i + 1
);
return(v)
}

/*
Tests decompose and putback
*/
test_decompose_putback(m) =
{
local(i, j);
i = 0;
while(i <= p*m,
	if(z^i - putback(decompose(z^i)), error("Problem with code!"));
	i = i + 1
);
i = 0;
while(i <= p - 1,
	j = 0;
	while(j <= m,
		if(z^i * (z^p - l)^j/(j!) - putback([[i, j, 1]]),
			error("Problem with code!"));
		j = j + 1
	);
	i = i + 1
)
}

/*
Tests that theta indeed is an right inverse to differentiation
with respect to z.
*/
test_theta(m) =
{
local(i, j, u, n, c, k);
i = 0;
while(i <= p - 1,
	j = 0;
	while(j <= m,
		if(p*putback([[i, j, 1]]) -
				deriv(putback(Theta([[i, j, 1]])), z),
			error("Problem with code!"));
		/* Test formula for theta in paper. */
		if((i < p - 1) && (j > 0),
			u = Theta([[i, j, 1]]);
			n = 1;
			while(n <= length(u),
				if(u[n][1] <> i + 1,
					error("Problem with code!"));
				if(u[n][2] <> j - n + 1,
					error("Problem with code!"));
				c = (-1)^(n + 1)*l^(n - 1)*p^n;
				c = c/prod(k = 1, n, i + 1 + p*(j - k + 1));
				if(u[n][3] <> c,
					error("Problem with code!"));
				n = n + 1
			)
		);
		j = j + 1
	);
	i = i + 1
)
}

/*
Tests that theta indeed is an right inverse to differentiation
with respect to z.
*/
test_integrality(m) =
{
local(i, j);
i = 0;
while(i <= p - 1,
	j = 0;
	while(j <= m,
		u = decompose(Theta(putback([[i, j, 1]])));
		if(is_integral(u),,
			print("Not integral for [i, j] = [", i, "," j,"]");
			print(u);
		);
		j = j + 1
	);
	i = i + 1
)
}


/*
Print nonzero values of p - theta o partial_z on basis elements
*/
test_factor(m) =
{
local(i, j, t, f, g, u, v, h);
i = 0;
while(i <= p - 1,
	j = 0;
	while(j <= m,
		t = [i, j, 1];
		f = p * putback([t]);
		g = putback([t]);
		h = deriv(g, z);
		u = decompose(h);
		v = Theta(u);
		h = putback(v);
		if(f - h,
			print(t);
			print(f - h)
		);
		j = j + 1
	);
	i = i + 1
)
}


/*
Print nonzero values o
	(theta tensor 1) o d_1 - d_1 o theta
on basis elements
*/
test_horizontal(m) =
{
local(i, j, t, f, g, u, v, h);
i = 0;
while(i <= p - 1,
	j = 0;
	while(j <= m,
		t = [i, j, 1];
		f = putback([t]);
		g = deriv(f, l);
		u = decompose(g);
		v = Theta(u);
		h = putback(v);
		u = Theta([t]);
		f = putback(u);
		g = deriv(f, l);
		if(g - h,
			print(t);
			print(h - g)
		);
		j = j + 1
	);
	i = i + 1
)
}

