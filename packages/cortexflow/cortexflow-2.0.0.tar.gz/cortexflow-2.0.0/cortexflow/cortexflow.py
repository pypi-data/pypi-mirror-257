class BayesianLinearRegression:
    def __init__(self):
        self.X = None
        self.y = None
        self.n = None
        self.d = None
        self.beta = None
        self.epsilon = 0.01
        self.target_acceptance_rate = 0.65
        self.mu = None
        self.M = None
        self.step_size_adaptation_factor = 0.01
        self.hbar = 0
        self.log_bar = 0
        self.gamma = 0.05
        self.t0 = 10
        self.kappa = 0.75
        self.delta = 0.6
        self.eta = 0.05
        self.epsilon_min = 0.001
        self.epsilon_max = 0.2
        self.epsilon_update_factor = 0.01
        self.M_inv = None

    def log_prior(self, beta):
        return stats.norm.logpdf(beta, loc=0, scale=10).sum()

    def log_likelihood(self, beta):
        mu = np.dot(self.X, beta)
        return stats.norm.logpdf(self.y, loc=mu, scale=1).sum()

    def log_posterior(self, beta):
        return self.log_prior(beta) + self.log_likelihood(beta)

    def grad_log_posterior(self, beta):
        return -np.dot(self.X.T, self.y - np.dot(self.X, beta)) + 10 * beta

    def potential_energy(self, beta):
        return -self.log_posterior(beta)

    def kinetic_energy(self, r):
        return 0.5 * np.dot(r, np.dot(self.M_inv, r))

    def hamiltonian(self, beta, r):
        return self.potential_energy(beta) + self.kinetic_energy(r)

    def leapfrog(self, beta, r, epsilon):
        r -= epsilon * 0.5 * self.grad_log_posterior(beta)
        beta += epsilon * np.dot(self.M_inv, r)
        r -= epsilon * 0.5 * self.grad_log_posterior(beta)
        return beta, r

    def find_reasonable_epsilon(self):
        r = np.random.multivariate_normal(self.mu, self.M)
        beta_init = self.beta
        _, r = self.leapfrog(beta_init, r, self.epsilon)
        new_beta, new_r = self.leapfrog(beta_init, r, self.epsilon)
        alpha = min(1, np.exp(self.hamiltonian(beta_init, r) - self.hamiltonian(new_beta, new_r)))
        return 0.5 * (self.target_acceptance_rate / alpha)

    def adapt_step_size(self, accept_prob):
        self.hbar = (1 - 1 / (self.t0 + self.log_bar)) * self.hbar + (1 / (self.t0 + self.log_bar)) * (self.target_acceptance_rate - accept_prob)
        self.log_bar += self.kappa * (self.delta - accept_prob)
        self.epsilon = np.exp(self.log_bar) * self.hbar / self.target_acceptance_rate
        self.epsilon = min(max(self.epsilon, self.epsilon_min), self.epsilon_max)

    def adapt_momentum_distribution(self, beta):
        self.M = (1 - self.gamma) * self.M + self.gamma * np.outer(beta - self.mu, beta - self.mu)
        self.M_inv = np.linalg.inv(self.M)

    def hamiltonian_monte_carlo(self, X, y, n_samples, L):
        self.X = np.hstack((np.ones((X.shape[0], 1)), X))
        self.y = y
        self.n, self.d = self.X.shape
        self.beta = np.zeros(self.d)
        self.mu = np.zeros(self.d)
        self.M = np.eye(self.d)
        self.M_inv = np.eye(self.d)
        samples = np.zeros((n_samples, self.d))
        accept_count = 0

        for t in range(n_samples):
            r = np.random.multivariate_normal(self.mu, self.M)
            beta_init = self.beta

            beta_proposed = beta_init
            r_proposed = r
            for _ in range(L):
                beta_proposed, r_proposed = self.leapfrog(beta_proposed, r_proposed, self.epsilon)

            log_prob_init = -self.hamiltonian(beta_init, r)
            log_prob_proposed = -self.hamiltonian(beta_proposed, r_proposed)
            accept_prob = min(1, np.exp(log_prob_init - log_prob_proposed))
            if np.random.rand() < accept_prob:
                self.beta = beta_proposed
                accept_count += 1
            samples[t] = self.beta

            if t % 100 == 0 and t > 0:
                accept_rate = accept_count / 100
                self.adapt_step_size(accept_rate)
                self.adapt_momentum_distribution(self.beta)
                accept_count = 0
        return samples

def hmcregression(X, y, n_samples, L):
    blr = BayesianLinearRegression()
    return blr.hamiltonian_monte_carlo(X, y, n_samples, L)

