functions
{
    vector get_X_bar_flat(vector X_flat, int R, int N, array[] int K)
    {
        // NOTE: we are doing a column-wise average of X. If X_flat is stored
        // column-wise, to_matrix is useless
        
        array[R] int K_c = to_int(to_array_1d(to_vector(K) - 1));
        
        vector[sum(K_c)] X_bar_flat;
        
        for(r in 1:R)
        {
            matrix[N, K[r]] X = to_matrix(
                segment(X_flat, 1+N*sum(K[1:r-1]), N*K[r]),
                N, K[r], 0);
            
            vector[K_c[r]] X_bar;
            for(i in 2:K[r])
            {
                X_bar[i-1] = mean(X[, i]);
            }
            
            int begin = 1+sum(K_c[1:r-1]);
            X_bar_flat[begin:begin+K_c[r]-1] = X_bar;
        }
        
        return X_bar_flat;
    }
    
    vector get_X_c_flat(vector X_flat, int R, int N, array[] int K, vector X_bar_flat)
    {
        array[R] int K_c = to_int(to_array_1d(to_vector(K) - 1));
        
        vector[N*sum(K_c)] X_c_flat;
        
        for(r in 1:R)
        {
            matrix[N, K[r]] X = to_matrix(
                segment(X_flat, 1+N*sum(K[1:r-1]), N*K[r]),
                N, K[r], 0);
            
            vector[K_c[r]] X_bar = segment(X_bar_flat, 1+sum(K_c[1:r-1]), K_c[r]);
            matrix[N, K_c[r]] X_c;
            for(i in 2:K[r])
            {
                X_c[, i-1] = X[, i] - X_bar[i-1];
            }
            
            int begin = 1+N*sum(K_c[1:r-1]);
            X_c_flat[begin:begin+N*K_c[r]-1] = to_vector(X_c');
        }
        
        return X_c_flat;
    }
}

data
{
    // Number of univariate models
    int<lower=1> R;
    // Number of outcomes (the same for each response)
    int<lower=1> N; 
    // Number of predictors for each univariate model
    array[R] int<lower=1> K;
    
    // Outcomes, as column vectors
    matrix[N, R] y;
    // Flattened predictors. TODO: describe the flattening process
    vector[N*sum(K)] X_flat;
    
    // Location and scale of the intercept priors
    vector[R] mu_alpha, sigma_alpha;
    
    // Scale of the non-intercept priors (location is 0)
    vector<lower=0>[sum(K)-R] sigma_beta_flat;
    
    // Scale of the variance priors
    vector<lower=0>[R] lambda_sigma;
    
    // Shape of the correlation matrix prior
    real<lower=1> eta_L;
    
    // Number of new outcomes to predict
    int<lower=0> N_new;
    // New flattened predictors. TODO: describe the flattening process
    vector[N_new*sum(K)] X_new_flat;
    // Whether to generate data from prior or posterior distribution
    int use_prior;
}

transformed data
{
    array[R] int K_c = to_int(to_array_1d(to_vector(K) - 1));
    
    // Center the predictors
    vector[sum(K)-R] X_bar_flat = get_X_bar_flat(X_flat, R, N, K);
    vector[N*(sum(K)-R)] X_c_flat = get_X_c_flat(X_flat, R, N, K, X_bar_flat);
    
    // Center the new predictors, if given, around the *original* predictors
    vector[N_new*sum(K_c)] X_c_new_flat;
    if(N_new > 0)
    {
        X_c_new_flat = get_X_c_flat(X_new_flat, R, N_new, K, X_bar_flat);
    }
}
 
parameters
{
    vector[R] alpha_c;
    vector[sum(K_c)] beta_flat;
    vector<lower=0>[R] sigma;
    
    cholesky_factor_corr[R] L;
}

model
{
    alpha_c ~ student_t(3, mu_alpha, sigma_alpha);
    beta_flat ~ student_t(3, 0, sigma_beta_flat);
    sigma ~ exponential(lambda_sigma);
    
    L ~ lkj_corr_cholesky(eta_L);
    
    matrix[N, R] mu;
    for(r in 1:R)
    {
        matrix[N, K_c[r]] X_c = to_matrix(
            segment(X_c_flat, 1+N*sum(K_c[1:r-1]), N*K_c[r]),
            N, K_c[r], 0);
        vector[K_c[r]] beta = segment(beta_flat, 1+sum(K_c[1:r-1]), K_c[r]);
        
        mu[:, r] = alpha_c[r] + X_c*beta;
    }
    
    matrix[R, R] Sigma = diag_pre_multiply(sigma, L);
    
    for(n in 1:N)
    {
        y[n] ~ multi_normal_cholesky(mu[n], Sigma);
    }
}

generated quantities
{
    // Non-centered intercept
    vector[R] alpha;
    for(r in 1:R)
    {
        vector[K_c[r]] X_bar = segment(X_bar_flat, 1+sum(K_c[1:r-1]), K_c[r]);
        vector[K_c[r]] beta = segment(beta_flat, 1+sum(K_c[1:r-1]), K_c[r]);
        alpha[r] = alpha_c[r] - dot_product(X_bar, beta);
    }
    
    // Expected Value of the prior-or-posterior predictive distribution
    matrix[R, N_new] mu_rep;
    matrix[R, N_new] y_rep;
    if(N_new > 0)
    {
        for(r in 1:R)
        {
            real alpha_c_;
            vector[K_c[r]] beta_;
            real sigma_;
            
            if(use_prior == 1)
            {
                // WARNING: the RNG must match the prior
                alpha_c_ = student_t_rng(3, mu_alpha[r], sigma_alpha[r]);
                beta_ = to_vector(
                    student_t_rng(
                        3, 0,
                        segment(sigma_beta_flat, 1+sum(K_c[1:r-1]), K_c[r])));
                sigma_ = exponential_rng(lambda_sigma[r]);
            }
            else
            {
                alpha_c_ = alpha_c[r];
                beta_ = segment(beta_flat, 1+sum(K_c[1:r-1]), K_c[r]);
                sigma_ = sigma[r];
            }
            
            matrix[N_new, K_c[r]] X_c_new = to_matrix(
                segment(X_c_new_flat, 1+N_new*sum(K_c[1:r-1]), N_new*K_c[r]),
                N_new, K_c[r], 0);
            
            // FIXME: should L/Sigma play a role here?
            mu_rep[r, :] = (alpha_c_ + X_c_new*beta_)';
            y_rep[r, :] = (to_vector(normal_rng(mu_rep[r, :], sigma_)))';
        }
    }
    
    corr_matrix[R] Sigma = multiply_lower_tri_self_transpose(L);
}
