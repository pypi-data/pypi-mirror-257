"""
eastats is a collection of helpful statistical tools.
"""

import arviz as az
import numpy as np
import pandas as pd
from scipy.stats import gamma, norm, t
from scipy.optimize import minimize


def ci_int(ser, distr="norm", breakdown="levels", conf_lvl=0.95):
    """Calculate the confidence interval for a given series.

    Args:
        ser (pd.Series): The input series for which the confidence interval is calculated.
        distr (str, optional): The distribution to assume for the calculation ("norm" or "bin"). Defaults to "norm".
        breakdown (str, optional): The type of breakdown for the confidence interval ("levels" or "elements"). Defaults to "levels".
        conf_lvl (float, optional): The confidence level for the interval. Defaults to 0.95.

    Returns:
        tuple: If breakdown=="elements":
            A tuple containing the mean, interval, length, and standard deviation of the series,
               or the interval for the specified breakdown type.
            If breakdown=="levels":
                A tuple containing the low and high boundaries of the confidence interval
    """
    ser = ser.astype(float)
    alpha = (1 - conf_lvl) / 2
    if distr=="bin":
        z_value = norm.isf(alpha)
        num_trials = len(ser)
        mean_success = np.mean(ser)
        intv = z_value * np.sqrt((mean_success * (1 - mean_success)) / num_trials)
    elif distr=="norm":
        t_value = t.ppf(1 - alpha, df=len(ser)-1)
        intv = t_value * np.std(ser) / np.sqrt(len(ser))
    if breakdown == "elements":
        return round(np.mean(ser), 3), round(intv, 3), len(ser), ser.std()
    elif breakdown == "levels":
        if distr=="bin":
            return max(0.0, np.mean(ser) - intv), min(1.0, np.mean(ser) + intv)
        else:
            return np.mean(ser) - intv, np.mean(ser) + intv


def population_adj_weights(df, pop_col="CountyDSC", adj_cols=["SexDSC", "RaceEthnicity", "AgeBucket"]):
    """Calculate the population adjustment weights to use for rate adjustments.

    Args:
        df (pd.DataFrame): Dataframe to calculate sample population weights for adjusted target rate.
        pop_col (str, optional): Level of sample population to aggregate. Defaults to "CountyDSC".
        adj_cols (list, optional): Variables to control for in adjustment. Defaults to ["SexDSC", "RaceEthnicity", "AgeBucket"].

    Returns:
        pd.DataFrame: Desired population weights to use for adjustments.
    """
    gcols = [pop_col] + adj_cols
    df_weights = df\
        [["PatientID"] + gcols]\
        .groupby(gcols, as_index=False)\
        .agg({"PatientID": "nunique"})\
        .rename(columns = {"PatientID":"n"})

    df_weights = pd.merge(
        df_weights,
        df_weights.groupby(pop_col, as_index=False).agg({"n": "sum"}).rename(columns={"n": "N"}),
        on = pop_col,
        how = "inner"
    )

    df_weights["weight"] = df_weights["n"] / df_weights["N"]

    return df_weights


def population_adjusted_rates(df, target, multiplier=100, 
                              pop_col="CountyDSC", sample_col="CensusTractGEOID", 
                              adj_cols=["SexDSC", "RaceEthnicity", "AgeBucket"],
                              includeCI=False, distr="norm"):
    """Calculate population adjusted rates.

    Args:
        df (pd.DataFrame): DataFrame to perform adjusted rate calculation.
        target (string): Column name of metric to perform adjusted rate for.
        multiplier (int, optional): Rate multiplier; change for scaling requirements. (Defaults to 100)
        pop_col (str, optional): Level of population to calculate reference population weights from. (Defaults to "CountyDSC")
        sample_col (str, optional): Level of population to apply population weights. (Defaults to "CensusTractGEOID")
        adj_cols (list, optional): Variables to control for in adjustment. (Defaults to ["SexDSC", "RaceEthnicity", "AgeBucket"])
        includeCI (bool, optional): Include 95% confidence interval in resulting DataFrame. (Defaults to False)
        distr (str, optional): Specify distribution to use for confidence interval. Options are: ["bin", "norm"] (Defaults to "norm")

    Returns:
        pd.DataFrame: Dataframe of adjusted rates.
    """

    cols = ["PatientID", pop_col, sample_col, target] + adj_cols
    df = df[cols]

    # calculate base stats of target population
    df_adj = df\
        .groupby([sample_col] + adj_cols)\
        .agg({pop_col: "max", "PatientID": "nunique", target: "sum"})
    
    # rename and reset
    df_adj.columns = [pop_col, "N", "n"]
    df_adj["p"] = df_adj["n"] / df_adj["N"]
    df_adj = df_adj.reset_index()

    # calculate group CIs
    df_ci = df\
        .groupby([sample_col] + adj_cols)\
        [target].apply(lambda x: ci_int(x, distr=distr))\
        .apply(pd.Series)\
        .reset_index()\
        .rename(columns={0: "lwr", 1: "upr"})

    df_adj = pd.merge(df_adj, df_ci, on=[sample_col] + adj_cols, how="inner")

    # generate base population weights
    df_weights = population_adj_weights(df, pop_col=pop_col, adj_cols=adj_cols)

    df_adj = pd.merge(
        df_adj,
        df_weights.drop(columns=["n", "N"]),
        on = [pop_col] + adj_cols,
        how = "inner"
    )

    # apply weights
    df_adj["weighted_p"] = df_adj[f"p"] * df_adj["weight"]
    df_adj["weighted_lwr"] = df_adj[f"lwr"] * df_adj["weight"]
    df_adj["weighted_upr"] = df_adj[f"upr"] * df_adj["weight"]
    
    # sum weighted rates
    df_adj_rate = df_adj\
        .groupby(sample_col)\
        .agg({"weighted_p": "sum", "weighted_lwr": "sum", "weighted_upr": "sum"})\
        .rename(columns={"weighted_p": f"{target}_adj_p", "weighted_lwr": f"{target}_adj_lwr", "weighted_upr": f"{target}_adj_upr"})

    df_adj_rate = df_adj_rate * multiplier
    df_adj_rate = df_adj_rate.reset_index()

    if includeCI:
        pass
    else:
        df_adj_rate = df_adj_rate.drop(columns=[f"{target}_adj_lwr", f"{target}_adj_upr"])

    return df_adj_rate


def mean_t_test(ser, comp_mean):
    """Calculate 1-sample mean t-test.

    Args:
        ser (pd.Series): Series of data to compare mean to known comp_mean
        comp_mean (float): comparison mean that series mean is compared to

    Returns:
        float: p-value for null hypothesis that the series mean is the same as the comp_mean.
        A value of 0.05 is interpreted as a 95% probability of rejecting the null hypothesis.
        This is often seen evidence that the series mean is significantly different than the comp_mean.
    """
    if (len(ser) > 1) and (comp_mean not in [None, np.nan]):
        return t.sf(
            abs(
                (ser.mean() - comp_mean) /
                (ser.std() / np.sqrt(len(ser)))
            ), 
            df=len(ser)
        ) * 2
    else:
        return np.nan

def geo_mean(ser, include_zeros=True):
    """Calculate Geometric Mean of series

    Args:
        ser (series): Series of data
        include_zeros (bool): If you include zeros and there is a zero value, the geo mean will always be 0. 
            Excluding zeros may skew the result is done inappropriately

    Returns:
        float: Geometric mean of series
    """
    if not include_zeros:
        ser = ser[ser != 0]
    return np.exp(np.log(ser).mean())

def posterior_simulation(observed_data, prior_params, num_samples=1000, distr="gamma"):
    """Perform posterior simulation sampling for a gamma distribution.

    Parameters:
    - observed_data (numpy.ndarray): Observed data.
    - prior_a (float): Shape parameter of the prior gamma distribution.
    - prior_b (float): Scale parameter of the prior gamma distribution.
    - num_samples (int): Number of samples to generate from the posterior.

    Returns:
    - numpy.ndarray: Samples from the posterior gamma distribution.
    """

    prior_a, prior_b = prior_params
    if distr == "gamma":
        # Define likelihood function (gamma distribution)
        def likelihood(params):
            shape, scale = params
            return -np.sum(gamma.logpdf(observed_data, a=shape, scale=scale))

        # Define prior function (gamma distribution)
        def prior(params):
            shape, scale = params
            return -gamma.logpdf(shape, a=prior_a, scale=prior_b) - gamma.logpdf(scale, a=prior_a, scale=prior_b)

        # Combine likelihood and prior to get the posterior
        def posterior(params):
            return likelihood(params) + prior(params)

        # Initial guess for the parameters
        initial_params = [1.0, 1.0]

        # Optimize to find the parameters that maximize the posterior
        result = minimize(posterior, initial_params, method='L-BFGS-B')

        # Extract the posterior parameters
        posterior_a, posterior_b = result.x

        # Generate samples from the posterior gamma distribution
        posterior_samples = np.random.gamma(posterior_a, posterior_b, num_samples)
    elif distr == "norm":
        # Define likelihood function (normal distribution)
        def likelihood(params):
            mean, std = params
            return -np.sum(norm.logpdf(observed_data, loc=mean, scale=std))

        # Define prior function (normal distribution)
        def prior(params):
            mean, std = params
            return -norm.logpdf(mean, loc=prior_a, scale=prior_b) - norm.logpdf(std, loc=prior_b, scale=prior_b)

        # Combine likelihood and prior to get the posterior
        def posterior(params):
            return likelihood(params) + prior(params)

        # Initial guess for the parameters
        initial_params = [1.0, 1.0]

        # Optimize to find the parameters that maximize the posterior
        result = minimize(posterior, initial_params, method='L-BFGS-B')

        # Extract the posterior parameters
        posterior_a, posterior_b = result.x

        # Generate samples from the posterior normal distribution
        posterior_samples = np.random.normal(loc=posterior_a, scale=posterior_b, size=num_samples)
    elif distr == "bin":
        num_successes = np.sum(observed_data)
        posterior_a = num_successes + prior_a
        posterior_b = len(observed_data) - num_successes + prior_b
        posterior_samples = np.random.beta(
            posterior_a,
            posterior_b,
            num_samples
        )

    return posterior_samples, posterior_a, posterior_b

def get_credible_diff(df, y, treatment, distr="gamma", prior_params=(2,1), num_samples=10000, credibility_lvl=0.9):
    """Calculate the credible interval for the difference between treatment and control groups.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        y (str): The column name for the outcome variable.
        treatment (str): The column name indicating the treatment group (binary: 0 or 1).
        distr (str, optional): The assumed distribution for the posterior simulation. Defaults to "gamma".
        prior_shape (int, optional): The shape parameter for the prior distribution. Defaults to 2.
        prior_scale (int, optional): The scale parameter for the prior distribution. Defaults to 1.
        num_samples (int, optional): The number of samples for the posterior simulation. Defaults to 10000.
        credibility_lvl (float, optional): The desired credibility level for the interval. Defaults to 0.9.

    Returns:
        tuple: A tuple containing the lower and upper bounds of the credible interval.
    """
    no_treat_gp = df.loc[(df[treatment]==0), y]
    treat_gp = df.loc[(df[treatment]==1), y]
    posterior_samples_no_treat_gp, shape_no_treat_gp, scale_no_treat_gp = posterior_simulation(np.array(no_treat_gp), prior_params, num_samples, distr)
    posterior_samples_treat_gp, shape_treat_gp, scale_treat_gp = posterior_simulation(np.array(treat_gp), prior_params, num_samples, distr)
    d = posterior_samples_treat_gp - posterior_samples_no_treat_gp

    return az.hdi(np.array(d), hdi_prob=credibility_lvl)

def smape(act, pred):
    """Calculate the Symmetric Mean Absolute Percentage Error (SMAPE) between actual and predicted values.

    Args:
        act (array-like): The actual values.
        pred (array-like): The predicted values.

    Returns:
        float: The SMAPE value.
    """
    return np.sum(np.abs((act - pred)) / (np.abs(act) + np.abs(pred))) / len(act)
