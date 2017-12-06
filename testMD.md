> This file is to test whether [github-mathjax](https://github.com/orsharir/github-mathjax) chrome extension works.

The sparse target distribution $p$ is defined as:

$$
\begin{align*}
p_i = 
\begin{cases} 
1-\left(y-\lfloor y\rfloor\right), \ &i=\lfloor y\rfloor \\\\
y-\lfloor y\rfloor,    &i=\lfloor y\rfloor+1\\\\
0    &\mbox{otherwise }
\end{cases}
\end{align*}
$$

for $1\leq i\leq K$. For example, if $K=5$ and $y=3.6$, $p=[0, 0, 0.4, 0.6, 0]$. See [this paper](http://arxiv.org/pdf/1503.00075.pdf).

$$
C_{i}=\sum_{\substack{j=1\\\\j\neq i}}^n\sum_{\substack{k=1\\\\k>j}}^nb_{jk}(i)
$$

A special symbol $\odot$.

$$
\underset{\theta}{\operatorname {argmax}}\ f(\theta)
$$

$$ 
(\gamma^,\phi^)=\underset{\gamma,\phi}{\operatorname{argmin}} D_{\mathrm{KL}}(q(\theta,z|\gamma,\phi)|p(\theta,z|w,\alpha,\beta)) 
$$
