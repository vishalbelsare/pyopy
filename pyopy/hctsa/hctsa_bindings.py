# coding=utf-8
from pyopy.base import MatlabSequence
from pyopy.hctsa.hctsa_bindings_gen import HCTSASuper


class CO_AddNoise(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyzes changes in the automutual information function with the addition of
    % noise to the input time series.
    % Adds Gaussian-distributed noise to the time series with increasing standard
    % deviation, eta, across the range eta = 0, 0.1, ..., 2, and measures the
    % mutual information at each point using histograms with
    % nbins bins (implemented using CO_HistogramAMI).
    % 
    % The output is a set of statistics on the resulting set of automutual
    % information estimates, including a fit to an exponential decay, since the
    % automutual information decreases with the added white noise.
    % 
    % Can calculate these statistics for time delays 'tau', and for a number 'nbins'
    % bins.
    % 
    % This algorithm is quite different, but was based on the idea of 'noise
    % titration' presented in: "Titration of chaos with added noise", Chi-Sang Poon
    % and Mauricio Barahona P. Natl. Acad. Sci. USA, 98(13) 7107 (2001)
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (13,)

    TAGS = ('AMI', 'correlation', 'entropy', 'stochastic')

    def __init__(self, tau=1.0, meth='quantiles', nbins=20.0):
        super(CO_AddNoise, self).__init__()
        self.tau = tau
        self.meth = meth
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_AddNoise', x, )
        elif self.meth is None:
            return eng.run_function(1, 'CO_AddNoise', x, self.tau)
        elif self.nbins is None:
            return eng.run_function(1, 'CO_AddNoise', x, self.tau, self.meth)
        return eng.run_function(1, 'CO_AddNoise', x, self.tau, self.meth, self.nbins)


class CO_AutoCorr(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the autocorrelation of an input time series, y, at a time-lag, tau
    % 
    %---INPUTS:
    % y, a scalar time series column vector.
    % tau, the time-delay. If tau is a scalar, returns autocorrelation for y at that
    %       lag. If tau is a vector, returns autocorrelations for y at that set of
    %       lags.
    % whatMethod, the method of computing the autocorrelation: 'Fourier',
    %             'TimeDomainStat', or 'TimeDomain'.
    %       
    %---OUTPUT: the autocorrelation at the given time-lag.
    %
    %---HISTORY:
    % Ben Fulcher, 2014-10-28. Added a version of the 'TimeDomain' method that can
    % tolerate NaN values in the time series, for a specific application for Simonne
    % Cohen.
    % 
    % Ben Fulcher, 2014-03-24. Added multiple definitions for computing the
    %       autocorrelation Computing mean/std across the full time series makes a
    %       significant difference for short time series, but can produce values
    %       outside [-1,+1]. The filtering-based method used by Matlab's autocorr,
    %       is probably the best for short time series, and is now implemented here.
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('autocorrelation', 'correlation')

    def __init__(self, tau=32.0, whatMethod='Fourier'):
        super(CO_AutoCorr, self).__init__()
        self.tau = tau
        self.whatMethod = whatMethod

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_AutoCorr', x, )
        elif self.whatMethod is None:
            return eng.run_function(1, 'CO_AutoCorr', x, self.tau)
        return eng.run_function(1, 'CO_AutoCorr', x, self.tau, self.whatMethod)


class CO_AutoCorrShape(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Outputs a set of statistics summarizing how the autocorrelation function
    % changes with the time lag, tau.
    % 
    % Outputs include the number of peaks, and autocorrelation in the
    % autocorrelation function itself.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (27,)

    TAGS = ('correlation',)

    def __init__(self):
        super(CO_AutoCorrShape, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'CO_AutoCorrShape', x, )


class CO_CompareMinAMI(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Finds the first minimum of the automutual information by various different
    % estimation methods, and sees how this varies over different coarse-grainings
    % of the time series.
    % 
    % The function returns a set of statistics on the set of first minimums of the
    % automutual information function obtained over a range of the number of bins
    % used in the histogram estimation, when specifying 'nbins' as a vector
    % 
    % INPUTS:
    % y, the input time series
    % 
    % meth, the method for estimating mutual information (input to CO_HistogramAMI)
    % 
    % nbins, the number of bins for the AMI estimation to compare over (can be a
    %           scalar or vector)
    % 
    % Outputs include the minimum, maximum, range, number of unique values, and the
    % position and periodicity of peaks in the set of automutual information
    % minimums.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (13,)

    TAGS = ('AMI', 'correlation')

    def __init__(self, meth='std2', nbins=(MatlabSequence('2:80'))):
        super(CO_CompareMinAMI, self).__init__()
        self.meth = meth
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.meth is None:
            return eng.run_function(1, 'CO_CompareMinAMI', x, )
        elif self.nbins is None:
            return eng.run_function(1, 'CO_CompareMinAMI', x, self.meth)
        return eng.run_function(1, 'CO_CompareMinAMI', x, self.meth, self.nbins)


class CO_Embed2(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Embeds the z-scored time series in a two-dimensional time-delay
    % embedding space with a given time-delay, tau, and outputs a set of
    % statistics about the structure in this space, including angular 
    % distribution, etc.
    % 
    %---INPUTS:
    % y, the column-vector time series
    % tau, the time-delay (can be 'tau' for first zero-crossing of ACF)
    % 
    %---OUTPUTS: include the distribution of angles between successive points in the
    % space, stationarity of this angular distribution, euclidean distances from the
    % origin, and statistics on outliers.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (30,)

    TAGS = ('correlation', 'embedding')

    def __init__(self, tau='tau'):
        super(CO_Embed2, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_Embed2', x, )
        return eng.run_function(1, 'CO_Embed2', x, self.tau)


class CO_Embed2_AngleTau(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Investigates how the autocorrelation of angles between successive points in
    % the two-dimensional time-series embedding change as tau varies from
    % tau = 1, 2, ..., maxtau.
    % 
    %---INPUTS:
    % y, a column vector time series
    % maxtau, the maximum time lag to consider
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (14,)

    TAGS = ('correlation', 'embedding')

    def __init__(self, maxtau=50.0):
        super(CO_Embed2_AngleTau, self).__init__()
        self.maxtau = maxtau

    def _eval_hook(self, eng, x):
        if self.maxtau is None:
            return eng.run_function(1, 'CO_Embed2_AngleTau', x, )
        return eng.run_function(1, 'CO_Embed2_AngleTau', x, self.maxtau)


class CO_Embed2_Basic(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Obtains a set of measures of point density in a plot of y_i against y_{i-tau}.
    %
    % INPUTS:
    % y, the input time series
    % 
    % tau, the time lag (can be set to 'tau' to set the time lag the first zero
    %                       crossing of the autocorrelation function)
    % 
    % Outputs include the number of points near the diagonal, and similarly, the
    % number of points that are close to certain geometric shapes in the y_{i-tau}, 
    % y_{tau} plot, including parabolas, rings, and circles.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (29,)

    TAGS = ('correlation',)

    def __init__(self, tau=1.0):
        super(CO_Embed2_Basic, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_Embed2_Basic', x, )
        return eng.run_function(1, 'CO_Embed2_Basic', x, self.tau)


class CO_Embed2_Dist(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns statistics on the sequence of successive Euclidean distances between
    % points in a two-dimensional time-delay embedding space with a given
    % time-delay, tau.
    % 
    % Outputs include the autocorrelation of distances, the mean distance, the
    % spread of distances, and statistics from an exponential fit to the
    % distribution of distances.
    % 
    %---INPUTS:
    % y, a z-scored column vector representing the input time series
    % tau, the time delay.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (13,)

    TAGS = ('correlation', 'embedding')

    def __init__(self, tau='tau'):
        super(CO_Embed2_Dist, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_Embed2_Dist', x, )
        return eng.run_function(1, 'CO_Embed2_Dist', x, self.tau)


class CO_Embed2_Shapes(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Takes a shape and places it on each point in the two-dimensional time-delay
    % embedding space sequentially. This function counts the points inside this shape
    % as a function of time, and returns statistics on this extracted time series.
    % 
    % INPUTS:
    % y, the input time-series as a (z-scored) column vector
    % tau, the time-delay
    % shape, has to be 'circle' for now...
    % r, the radius of the circle
    % 
    % Outputs are of the constructed time series of the number of nearby points, and
    % include the autocorrelation, maximum, median, mode, a Poisson fit to the
    % distribution, histogram entropy, and stationarity over fifths of the time
    % series.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (16,)

    TAGS = ('correlation', 'embedding')

    def __init__(self, tau='tau', shape='circle', r=1.0):
        super(CO_Embed2_Shapes, self).__init__()
        self.tau = tau
        self.shape = shape
        self.r = r

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_Embed2_Shapes', x, )
        elif self.shape is None:
            return eng.run_function(1, 'CO_Embed2_Shapes', x, self.tau)
        elif self.r is None:
            return eng.run_function(1, 'CO_Embed2_Shapes', x, self.tau, self.shape)
        return eng.run_function(1, 'CO_Embed2_Shapes', x, self.tau, self.shape, self.r)


class CO_FirstMin(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the time at which the first minimum in a given correlation function
    % occurs.
    % 
    %---INPUTS:
    % y, the input time series
    % MinWhat, the type of correlation to minimize: either 'ac' for autocorrelation,
    %           or 'mi' for automutual information
    % 
    % Note that selecting 'ac' is unusual operation: standard operations are the
    % first zero-crossing of the autocorrelation (as in CO_FirstZero), or the first
    % minimum of the mutual information function ('mi').
    %
    % The 'mi' option uses Rudy Moddemeijer's RM_information.m code that may or may
    % not be great...
    % 
    %---HISTORY
    % Ben Fulcher, 2008
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('AMI', 'autocorrelation', 'correlation', 'tau')

    def __init__(self, MinWhat='mi'):
        super(CO_FirstMin, self).__init__()
        self.MinWhat = MinWhat

    def _eval_hook(self, eng, x):
        if self.MinWhat is None:
            return eng.run_function(1, 'CO_FirstMin', x, )
        return eng.run_function(1, 'CO_FirstMin', x, self.MinWhat)


class CO_FirstZero(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the first zero-crossing of a given autocorrelation function.
    % 
    % y, the input time series
    % corrfn, the self-correlation function to measure:
    %         (i) 'ac': normal linear autocorrelation function. Uses CO_AutoCorr to
    %                   calculate autocorrelations.
    % maxtau, a maximum time-delay to search up to
    % 
    % In future, could add an option to return the point at which the function
    % crosses the axis, rather than the first integer lag at which it has already
    % crossed (what is currently implemented)
    % 
    %---HISTORY:
    % Ben Fulcher, 2008
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('autocorrelation', 'correlation', 'tau')

    def __init__(self, corrfn='ac', maxtau=None):
        super(CO_FirstZero, self).__init__()
        self.corrfn = corrfn
        self.maxtau = maxtau

    def _eval_hook(self, eng, x):
        if self.corrfn is None:
            return eng.run_function(1, 'CO_FirstZero', x, )
        elif self.maxtau is None:
            return eng.run_function(1, 'CO_FirstZero', x, self.corrfn)
        return eng.run_function(1, 'CO_FirstZero', x, self.corrfn, self.maxtau)


class CO_HistogramAMI(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the automutual information using histograms, using a given approach
    % to binning the data.
    % 
    % Uses hist2.m function (renamed NK_hist2.m here) by Nedialko Krouchev, obtained
    % from Matlab Central,
    % http://www.mathworks.com/matlabcentral/fileexchange/12346-hist2-for-the-people
    % [[hist2 for the people by Nedialko Krouchev, 20 Sep 2006 (Updated 21 Sep 2006)]]
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % tau, the time-lag (1 by default)
    % 
    % meth, the method of computing automutual information:
    %           (i) 'even': evenly-spaced bins through the range of the time series,
    %           (ii) 'std1', 'std2': bins that extend only up to a multiple of the
    %                                standard deviation from the mean of the time
    %                                series to exclude outliers,
    %           (iii) 'quantiles': equiprobable bins chosen using quantiles.
    % 
    % nbins, the number of bins, required by some methods, meth (see above)
    % 
    %---OUTPUT: the automutual information calculated in this way.
    %
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('AMI', 'correlation', 'information')

    def __init__(self, tau=2.0, meth='std2', nbins=10.0):
        super(CO_HistogramAMI, self).__init__()
        self.tau = tau
        self.meth = meth
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_HistogramAMI', x, )
        elif self.meth is None:
            return eng.run_function(1, 'CO_HistogramAMI', x, self.tau)
        elif self.nbins is None:
            return eng.run_function(1, 'CO_HistogramAMI', x, self.tau, self.meth)
        return eng.run_function(1, 'CO_HistogramAMI', x, self.tau, self.meth, self.nbins)


class CO_NonlinearAutocorr(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes autocorrelations of the input time series of the form
    % <x_i x_{i-\tau_1} x{i-\tau_2}...>
    % The usual two-point autocorrelations are
    % <x_i.x_{i-\tau}>
    % 
    % Assumes that all the taus are much less than the length of the time
    % series, N, so that the means can be approximated as the sample means and the
    % standard deviations approximated as the sample standard deviations and so
    % the z-scored time series can simply be used straight-up.
    % 
    %---INPUTS:
    % y  -- should be the z-scored time series (Nx1 vector)
    % taus -- should be a vector of the time delays as above (mx1 vector)
    %   e.g., [2] computes <x_i x_{i-2}>
    %   e.g., [1,2] computes <x_i x_{i-1} x{i-2}>
    %   e.g., [1,1,3] computes <x_i x_{i-1}^2 x{i-3}>
    % doabs [opt] -- a boolean (0,1) -- if one, takes an absolute value before
    %                taking the final mean -- useful for an odd number of
    %                contributions to the sum. Default is to do this for odd
    %                numbers anyway, if not specified.
    %
    % Note: for odd numbers of regressions (i.e., even number length
    %         taus vectors) the result will be near zero due to fluctuations
    %         below the mean; even for highly-correlated signals. (doabs)
    % Note: doabs = 1 is really a different operation that can't be compared with
    %         the values obtained from taking doabs = 0 (i.e., for odd lengths
    %         of taus)
    % Note: It can be helpful to look at nlac at each iteration.
    % 
    %---HISTORY
    % Ben Fulcher, 8/6/09
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('autocorrelation', 'correlation', 'nonlinearautocorr')

    def __init__(self, taus=(0.0, 4.0, 5.0), doabs=None):
        super(CO_NonlinearAutocorr, self).__init__()
        self.taus = taus
        self.doabs = doabs

    def _eval_hook(self, eng, x):
        if self.taus is None:
            return eng.run_function(1, 'CO_NonlinearAutocorr', x, )
        elif self.doabs is None:
            return eng.run_function(1, 'CO_NonlinearAutocorr', x, self.taus)
        return eng.run_function(1, 'CO_NonlinearAutocorr', x, self.taus, self.doabs)


class CO_RM_AMInformation(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Wrapper for Rudy Moddemeijer's information code to calculate automutual
    % information.
    % 
    % INPUTS:
    % y, the input time series
    % tau, the time lag at which to calculate the automutual information
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('AMI', 'correlation', 'information')

    def __init__(self, tau=10.0):
        super(CO_RM_AMInformation, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_RM_AMInformation', x, )
        return eng.run_function(1, 'CO_RM_AMInformation', x, self.tau)


class CO_StickAngles(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyzes line-of-sight angles between time-series points where each
    % time-series value is treated as a stick protruding from an opaque baseline
    % level. Statistics are returned on the raw time series, where sticks protrude
    % from the zero-level, and the z-scored time series, where sticks
    % protrude from the mean level of the time series.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    %---OUTPUTS: are returned on the obtained sequence of angles, theta, reflecting the
    % maximum deviation a stick can rotate before hitting a stick representing
    % another time point. Statistics include the mean and spread of theta,
    % the different between positive and negative angles, measures of symmetry of
    % the angles, stationarity, autocorrelation, and measures of the distribution of
    % these stick angles.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (65,)

    TAGS = ('correlation', 'locdep', 'raw', 'spreaddep')

    def __init__(self):
        super(CO_StickAngles, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'CO_StickAngles', x, )


class CO_TSTL_AutoCorrMethod(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates the autocorrelation function using a fast Fourier Transform method
    % implemented in TSTOOL and returns the mean square discrepancy between the
    % autocorrelation coefficients obtained in this way from those obtained in the
    % time domain using CO_AutoCorr.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    % No real rationale behind this, other than the difference in autocorrelations
    % computed by the two methods may somehow be informative of something about the
    % time series...
    % 
    %---INPUTS:
    % y, the input time series
    % maxlag, the maximum time lag to compute up to -- will compare autocorrelations
    %         up to this value
    % 
    %---HISTORY:
    % Ben Fulcher, October 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('correlation',)

    def __init__(self, maxlag=None):
        super(CO_TSTL_AutoCorrMethod, self).__init__()
        self.maxlag = maxlag

    def _eval_hook(self, eng, x):
        if self.maxlag is None:
            return eng.run_function(1, 'CO_TSTL_AutoCorrMethod', x, )
        return eng.run_function(1, 'CO_TSTL_AutoCorrMethod', x, self.maxlag)


class CO_TSTL_amutual(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses amutual code from TSTOOL, which uses a
    % histogram method with n bins to estimate the mutual information of a
    % time series across a range of time-delays, tau.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    %
    %---INPUTS:
    % 
    % y, the time series
    % 
    % maxtau, the maximum lag for which to calculate the auto mutual information
    % 
    % nbins, the number of bins for histogram calculation
    % 
    %---OUTPUTS:
    % A number of statistics of the function over the range of tau, including the
    % mean mutual information, its standard deviation, first minimum, proportion of
    % extrema, and measures of periodicity in the positions of local maxima.
    % 
    %---HISTORY:
    % Ben Fulcher, October 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (28,)

    TAGS = ('AMI', 'entropy', 'lengthdep', 'tstool')

    def __init__(self, maxtau=20.0, nbins=10.0):
        super(CO_TSTL_amutual, self).__init__()
        self.maxtau = maxtau
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.maxtau is None:
            return eng.run_function(1, 'CO_TSTL_amutual', x, )
        elif self.nbins is None:
            return eng.run_function(1, 'CO_TSTL_amutual', x, self.maxtau)
        return eng.run_function(1, 'CO_TSTL_amutual', x, self.maxtau, self.nbins)


class CO_TSTL_amutual2(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses amutual2 code from TSTOOL to compute the mutual information up to a given
    % maximum time-delay.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, column vector of time series data
    % maxtau, maximal lag
    % 
    %---OUTPUTS: Statistics on the output of amutual2 over this range, as for
    % CO_TSTL_amutual.
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (65,)

    TAGS = ('AMI', 'entropy', 'tstool')

    def __init__(self, maxtau=50.0):
        super(CO_TSTL_amutual2, self).__init__()
        self.maxtau = maxtau

    def _eval_hook(self, eng, x):
        if self.maxtau is None:
            return eng.run_function(1, 'CO_TSTL_amutual2', x, )
        return eng.run_function(1, 'CO_TSTL_amutual2', x, self.maxtau)


class CO_TranslateShape(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns statistics on the number of data points that reside inside a given
    % geometric shape that is moved around the time series. Inputs specify a shape
    % and its size, and a method for moving this shape through the time domain.
    % 
    % This is usually more informative in an embedding space (CO_Embed2_...), but
    % here we do it just in the temporal domain (_t_).
    % 
    % In the future, could perform a similar analysis with a soft boundary, some
    % decaying force function V(r), or perhaps truncated...?
    %
    % INPUTS:
    % 
    % y, the input time series
    % 
    % shape, the shape to move about the time-domain ('circle')
    % 
    % d, a parameter specifying the size of the shape (e.g., d = 2)
    % 
    % howtomove, a method specifying how to move the shape about, e.g., 'pts'
    %               places the shape on each point in the time series
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (20, 18, 17, 15, 13)

    TAGS = ('correlation',)

    def __init__(self, shape='circle', d=2.5, howtomove='pts'):
        super(CO_TranslateShape, self).__init__()
        self.shape = shape
        self.d = d
        self.howtomove = howtomove

    def _eval_hook(self, eng, x):
        if self.shape is None:
            return eng.run_function(1, 'CO_TranslateShape', x, )
        elif self.d is None:
            return eng.run_function(1, 'CO_TranslateShape', x, self.shape)
        elif self.howtomove is None:
            return eng.run_function(1, 'CO_TranslateShape', x, self.shape, self.d)
        return eng.run_function(1, 'CO_TranslateShape', x, self.shape, self.d, self.howtomove)


class CO_f1ecac(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Finds where autocorrelation function first crosses 1/e, the 1/e correlation
    % length
    % 
    %---INPUTS:
    % y, the input time series
    % 
    %---HISTORY:
    % Ben Fulcher, 2008
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('autocorrelation', 'correlation', 'tau')

    def __init__(self):
        super(CO_f1ecac, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'CO_f1ecac', x, )


class CO_fzcglscf(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the first zero-crossing of the generalized self-correlation function
    % introduced in Duarte Queiros and Moyano in Physica A, Vol. 383, pp. 10--15
    % (2007) in the paper "Yet on statistical properties of traded volume:
    % Correlation and mutual information at different value magnitudes"
    % Uses CO_glscf to calculate the generalized self-correlations.
    % Keeps calculating until the function finds a minimum, and returns this lag.
    % 
    %---INPUTS:
    % y, the input time series
    % alpha, the parameter alpha
    % beta, the parameter beta
    % maxtau [opt], a maximum time delay to search up to (default is the time-series
    %                length)
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('correlation', 'glscf', 'tau')

    def __init__(self, alpha=5.0, beta=10.0, maxtau=None):
        super(CO_fzcglscf, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.maxtau = maxtau

    def _eval_hook(self, eng, x):
        if self.alpha is None:
            return eng.run_function(1, 'CO_fzcglscf', x, )
        elif self.beta is None:
            return eng.run_function(1, 'CO_fzcglscf', x, self.alpha)
        elif self.maxtau is None:
            return eng.run_function(1, 'CO_fzcglscf', x, self.alpha, self.beta)
        return eng.run_function(1, 'CO_fzcglscf', x, self.alpha, self.beta, self.maxtau)


class CO_glscf(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the generalized linear self-correlation function of a time series.
    % This function was introduced in Queiros and Moyano in Physica A, Vol. 383, pp.
    % 10--15 (2007) in the paper "Yet on statistical properties of traded volume: 
    % Correlation and mutual information at different value magnitudes"
    % 
    % The function considers magnitude correlations:
    %---INPUTS:
    % y, the input time series
    % alpha and beta are real and nonzero parameters
    % tau is the time-delay (can also be 'tau' to set to first zero-crossing of the ACF)
    % 
    % When alpha = beta estimates how values of the same order of magnitude are
    % related in time
    % When alpha ~= beta, estimates correlations between different magnitudes of the
    % time series.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('correlation', 'glscf')

    def __init__(self, alpha=2.0, beta=5.0, tau=2.0):
        super(CO_glscf, self).__init__()
        self.alpha = alpha
        self.beta = beta
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.alpha is None:
            return eng.run_function(1, 'CO_glscf', x, )
        elif self.beta is None:
            return eng.run_function(1, 'CO_glscf', x, self.alpha)
        elif self.tau is None:
            return eng.run_function(1, 'CO_glscf', x, self.alpha, self.beta)
        return eng.run_function(1, 'CO_glscf', x, self.alpha, self.beta, self.tau)


class CO_tc3(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    %
    % Computes the tc3 function, a normalized nonlinear autocorrelation, at a
    % given time-delay, tau.
    % Outputs are the raw tc3 expression, its magnitude, the numerator and its magnitude, and
    % the denominator.
    % 
    %---INPUTS:
    % y, input time series
    % tau, time lag
    % 
    % See documentation of the TSTOOL package (http://www.physik3.gwdg.de/tstool/)
    % for further details about this function.
    %
    %---HISTORY:
    % Ben Fulcher, 15/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('autocorrelation', 'correlation', 'nonlinear')

    def __init__(self, tau=1.0):
        super(CO_tc3, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_tc3', x, )
        return eng.run_function(1, 'CO_tc3', x, self.tau)


class CO_trev(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the trev function, a normalized nonlinear autocorrelation,
    % mentioned in the documentation of the TSTOOL nonlinear time-series analysis
    % package (available here: http://www.physik3.gwdg.de/tstool/).
    % 
    % The quantity is often used as a nonlinearity statistic in surrogate data
    % analysis, cf. "Surrogate time series", T. Schreiber and A. Schmitz, Physica D,
    % 142(3-4) 346 (2000).
    % 
    %---INPUTS:
    % 
    % y, time series
    % 
    % tau, time lag (can be 'ac' or 'mi' to set as the first zero-crossing of the
    %       autocorrelation function, or the first minimum of the automutual
    %       information function, respectively)
    % 
    %---OUTPUTS: the raw trev expression, its magnitude, the numerator and its
    % magnitude, and the denominator.
    % 
    %---HISTORY:
    % Ben Fulcher, 15/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('autocorrelation', 'correlation', 'nonlinear')

    def __init__(self, tau='ac'):
        super(CO_trev, self).__init__()
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'CO_trev', x, )
        return eng.run_function(1, 'CO_trev', x, self.tau)


class CP_ML_StepDetect(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Gives information about discrete steps in the signal, using the function
    % l1pwc from Max A. Little's step detection toolkit.
    % 
    % cf.,
    % "Sparse Bayesian Step-Filtering for High-Throughput Analysis of Molecular
    % Machine Dynamics", Max A. Little, and Nick S. Jones, Proc. ICASSP (2010)
    % 
    % "Steps and bumps: precision extraction of discrete states of molecular machines"
    % M. A. Little, B. C. Steel, F. Bai, Y. Sowa, T. Bilyard, D. M. Mueller,
    % R. M. Berry, N. S. Jones. Biophysical Journal, 101(2):477-485 (2011)
    % 
    % Software available at: http://www.maxlittle.net/software/index.php
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % method, the step-detection method:
    %           (i) 'kv': Kalafut-Visscher
    %                 cf. The algorithm described in:
    %                 Kalafut, Visscher, "An objective, model-independent method for
    %                 detection of non-uniform steps in noisy signals", Comp. Phys.
    %                 Comm., 179(2008), 716-723.
    %                 
    %           (ii) 'l1pwc': L1 method
    %                 This code is based on code originally written by Kim et al.:
    %                 "l_1 Trend Filtering", S.-J. Kim et al., SIAM Review 51, 339
    %                 (2009).
    % 
    % params, the parameters for the given method used:
    %           (i) 'kv': (no parameters required)
    %           (ii) 'l1pwc': params = lambda
    % 
    %---OUTPUTS:
    % Statistics on the output of the step-detection method, including the intervals
    % between change points, the proportion of constant segments, the reduction in
    % variance from removing the piece-wise constants, and stationarity in the
    % occurrence of change points.
    % 
    %---HISTORY:
    % Ben Fulcher, 2014-10-08 Commented out Chung-Kennedy.
    % Ben Fulcher, 12/4/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (15,)

    TAGS = ('l1pwc', 'lengthdep', 'stepdetection')

    def __init__(self, method='l1pwc', params=0.2):
        super(CP_ML_StepDetect, self).__init__()
        self.method = method
        self.params = params

    def _eval_hook(self, eng, x):
        if self.method is None:
            return eng.run_function(1, 'CP_ML_StepDetect', x, )
        elif self.params is None:
            return eng.run_function(1, 'CP_ML_StepDetect', x, self.method)
        return eng.run_function(1, 'CP_ML_StepDetect', x, self.method, self.params)


class CP_l1pwc_sweep_lambda(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Gives information about discrete steps in the signal across a range of
    % regularization parameters lambda, using the function l1pwc from Max Little's
    % step detection toolkit.
    % 
    % cf.,
    % "Sparse Bayesian Step-Filtering for High-Throughput Analysis of Molecular
    % Machine Dynamics", Max A. Little, and Nick S. Jones, Proc. ICASSP (2010)
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % lambdar, a vector specifying the lambda parameters to use
    % 
    %---OUTPUTS:
    % At each iteration, the CP_ML_StepDetect code was run with a given
    % lambda, and the number of segments, and reduction in root mean square error
    % from removing the piecewise constants was recorded. Outputs summarize how the
    % these quantities vary with lambda.
    % 
    %---HISTORY:
    % Ben Fulcher, 2010-04-13
    % Ben Fulcher, 2014-02-24. Fixed a problem with no matches giving an error
    % instead of a NaN.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (8,)

    TAGS = ('l1pwc', 'stepdetection')

    def __init__(self, lambdar=MatlabSequence('0:0.05:0.95')):
        super(CP_l1pwc_sweep_lambda, self).__init__()
        self.lambdar = lambdar

    def _eval_hook(self, eng, x):
        if self.lambdar is None:
            return eng.run_function(1, 'CP_l1pwc_sweep_lambda', x, )
        return eng.run_function(1, 'CP_l1pwc_sweep_lambda', x, self.lambdar)


class CP_wavelet_varchg(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Finds variance change points using functions from Matlab's Wavelet Toolbox,
    % including the primary function wvarchg, which estimates the change points in
    % the time series.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % wname, the name of the mother wavelet to analyze the data with: e.g., 'db3',
    %           'sym2', cf. Wavelet Toolbox Documentation for details
    % 
    % level, the level of wavelet decomposition
    % 
    % maxnchpts, the maximum number of change points
    % 
    % mindelay, the minimum delay between consecutive change points (can be
    %           specified as a proportion of the time-series length, e.g., 0.02
    %           ensures that change points are separated by at least 2% of the
    %           time-series length)
    % 
    % 
    %---OUTPUT: 
    % The optimal number of change points.
    % 
    %---HISTORY:
    % Ben Fulcher, 23/1/2010
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('varchg', 'wavelet', 'waveletTB')

    def __init__(self, wname='db3', level=3.0, maxnchpts=10.0, mindelay=0.01):
        super(CP_wavelet_varchg, self).__init__()
        self.wname = wname
        self.level = level
        self.maxnchpts = maxnchpts
        self.mindelay = mindelay

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'CP_wavelet_varchg', x, )
        elif self.level is None:
            return eng.run_function(1, 'CP_wavelet_varchg', x, self.wname)
        elif self.maxnchpts is None:
            return eng.run_function(1, 'CP_wavelet_varchg', x, self.wname, self.level)
        elif self.mindelay is None:
            return eng.run_function(1, 'CP_wavelet_varchg', x, self.wname, self.level, self.maxnchpts)
        return eng.run_function(1, 'CP_wavelet_varchg', x, self.wname, self.level, self.maxnchpts, self.mindelay)


class DN_Burstiness(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the 'burstiness' statistic from:
    % 
    % Goh and Barabasi, 'Burstiness and memory in complex systems' Europhys. Lett.
    % 81, 48002 (2008)
    % 
    %---INPUT:
    % y, the input time series
    % 
    %---OUTPUT:
    % The burstiness statistic, B.
    % 
    %---HISTORY:
    % Ben Fulcher, 2008
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('burstiness', 'locdep', 'raw')

    def __init__(self):
        super(DN_Burstiness, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'DN_Burstiness', x, )


class DN_CompareKSFit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns simple statistics on the discrepancy between the
    % kernel-smoothed distribution of the time-series values, and the distribution
    % fitted to it by some model: Gaussian (using normfifit from Matlab's
    % Statistics Toolbox), Extreme Value (evfifit), Uniform (unififit), Beta
    % (betafifit), Rayleigh (raylfifit), Exponential (expfifit), Gamma (gamfit),
    % LogNormal (lognfifit), and Weibull (wblfifit).
    % 
    %---INPUTS:
    % x, the input time series
    % whatDistn, the type of distribution to fit to the data:
    %           'norm' (normal), 'ev' (extreme value), 'uni' (uniform),
    %           'beta' (Beta), 'rayleigh' (Rayleigh), 'exp' (exponential),
    %           'gamma' (Gamma), 'logn' (Log-Normal), 'wbl' (Weibull).
    % 
    %---OUTPUTS: include the absolute area between the two distributions, the peak
    % separation, overlap integral, and relative entropy.
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('adiff', 'beta', 'distribution', 'ev', 'exp', 'gamma', 'ksdensity', 'locdep', 'lognormal'
            'norm', 'olapint', 'peaksepx', 'peaksepy', 'raw', 'rayleigh', 'relent', 'spreaddep', 'uni', 'weibull')

    def __init__(self, whatDistn='norm'):
        super(DN_CompareKSFit, self).__init__()
        self.whatDistn = whatDistn

    def _eval_hook(self, eng, x):
        if self.whatDistn is None:
            return eng.run_function(1, 'DN_CompareKSFit', x, )
        return eng.run_function(1, 'DN_CompareKSFit', x, self.whatDistn)


class DN_Compare_zscore(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Compares the distribution of a time series to a z-scored version of it
    % 
    %---INPUT:
    % x, a (not z-scored) time series
    % 
    %---OUTPUTS: ratios of features between the original and z-scored time series,
    % including the number of peaks, the maximum, and the distributional entropy.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (3,)

    TAGS = ('compare', 'distribution', 'entropy', 'ksdensity', 'max', 'numpeaks', 'raw', 'spreaddep')

    def __init__(self):
        super(DN_Compare_zscore, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'DN_Compare_zscore', x, )


class DN_Cumulants(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Very simple function that uses the skewness and kurtosis functions in 
    % Matlab's Statistics Toolbox to calculate these higher order moments of input time series, y
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % whatcum, the type of higher order moment:
    %           (i) 'skew1', skewness
    %           (ii) 'skew2', skewness correcting for bias
    %           (iii) 'kurt1', kurtosis
    %           (iv) 'kurt2', kurtosis correcting for bias
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self, whatcum=None):
        super(DN_Cumulants, self).__init__()
        self.whatcum = whatcum

    def _eval_hook(self, eng, x):
        if self.whatcum is None:
            return eng.run_function(1, 'DN_Cumulants', x, )
        return eng.run_function(1, 'DN_Cumulants', x, self.whatcum)


class DN_CustomSkewness(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates custom skewness measures, the Pearson and Bowley skewnesses.
    % 
    % INPUTS:
    % y, the input time series
    % 
    % whichskew, the skewness measure to calculate, either 'pearson' or 'bowley'
    % 
    % The Bowley skewness uses the quantile function from Matlab's Statistics
    % Toolbox.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'locdep', 'moment', 'raw', 'shape')

    def __init__(self, whichskew='pearson'):
        super(DN_CustomSkewness, self).__init__()
        self.whichskew = whichskew

    def _eval_hook(self, eng, x):
        if self.whichskew is None:
            return eng.run_function(1, 'DN_CustomSkewness', x, )
        return eng.run_function(1, 'DN_CustomSkewness', x, self.whichskew)


class DN_FitKernelSmooth(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a kernel-smoothed distribution to the data using the ksdensity function
    % from Matlab's Statistics Toolbox and returns a set of simple statistics.
    % 
    %---INPUTS:
    % x, the input time series
    % <can also produce additional outputs with the following optional settings>
    % [opt] 'numcross': number of times the distribution crosses the given threshold
    %           e.g., usage: DN_FitKernelSmooth(x,'numcross',[0.5,0.7]) for
    %                        thresholds of 0.5 and 0.7
    % [opt] 'area': area under where the distribution crosses the given thresholds.
    %               Usage as for 'numcross' above
    % [opt] 'arclength': arclength between where the distribution passes given
    %       thresholds. Usage as above.
    % 
    %---EXAMPLE USAGE:                  
    % DN_FitKernelSmooth(x,'numcross',[0.05,0.1],'area',[0.1,0.2,0.4],'arclength',[0.5,1,2])
    % returns all the basic outputs, plus those for numcross, area, and arclength
    % for the thresholds given
    % 
    %---OUTPUTS: a set of statistics summarizing the obtained distribution, including
    % the number of peaks, the distributional entropy, the number of times the curve
    % crosses fifixed probability thresholds, the area under the curve for fifixed
    % probability thresholds, the arc length, and the symmetry of probability
    % density above and below the mean.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (21, 2)

    TAGS = ('arclength', 'area', 'areaconst', 'crossconst', 'distribution', 'entropy', 'ksdensity'
            'numpeaks', 'peakmax', 'raw', 'spreaddep', 'symmetry')

    def __init__(self, varargin='numcross'):
        super(DN_FitKernelSmooth, self).__init__()
        self.varargin = varargin

    def _eval_hook(self, eng, x):
        if self.varargin is None:
            return eng.run_function(1, 'DN_FitKernelSmooth', x, )
        return eng.run_function(1, 'DN_FitKernelSmooth', x, self.varargin)


class DN_Fit_mle(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits either a Gaussian, Uniform, or Geometric distribution to the data using
    % maximum likelihood estimation via the Matlab function mle
    % from the Statistics Toolbox.
    % 
    %---INPUTS:
    % y, the time series
    % fitwhat, the type of fit to do: 'gaussian', 'uniform', or 'geometric'.
    % 
    %---OUTPUTS: parameters from the fit.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1, 2)

    TAGS = ('distribution', 'fit', 'location', 'locdep', 'raw', 'spread', 'spreaddep')

    def __init__(self, fitwhat='geometric'):
        super(DN_Fit_mle, self).__init__()
        self.fitwhat = fitwhat

    def _eval_hook(self, eng, x):
        if self.fitwhat is None:
            return eng.run_function(1, 'DN_Fit_mle', x, )
        return eng.run_function(1, 'DN_Fit_mle', x, self.fitwhat)


class DN_HighLowMu(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates a statistic related to the mean of the time series data that
    % is above the (global) time-series mean compared to the mean of the data that
    % is below the global time-series mean.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'locdep', 'raw', 'skewness', 'spreaddep')

    def __init__(self):
        super(DN_HighLowMu, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'DN_HighLowMu', x, )


class DN_HistogramMode(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the mode of the time series using histograms a given numbers
    % of bins.
    % 
    %---INPUTS:
    % 
    % y, the input time series.
    % 
    % nbins, the number of bins to use in the histogram.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('location',)

    def __init__(self, nbins=10.0):
        super(DN_HistogramMode, self).__init__()
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.nbins is None:
            return eng.run_function(1, 'DN_HistogramMode', x, )
        return eng.run_function(1, 'DN_HistogramMode', x, self.nbins)


class DN_Mean(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures a given type of 'mean', or measure of location of the time series.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % meantype, (i) 'norm' or 'arithmetic', arithmetic mean
    %           (ii) 'median', median
    %           (iii) 'geom', geometric mean
    %           (iv) 'harm', harmonic mean
    %           (v) 'rms', root-mean-square
    %           (vi) 'iqm', interquartile mean
    %           (vii) 'midhinge', midhinge
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('location', 'locdep', 'raw', 'spreaddep')

    def __init__(self, meantype='median'):
        super(DN_Mean, self).__init__()
        self.meantype = meantype

    def _eval_hook(self, eng, x):
        if self.meantype is None:
            return eng.run_function(1, 'DN_Mean', x, )
        return eng.run_function(1, 'DN_Mean', x, self.meantype)


class DN_MinMax(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the maximum and minimum values of the input time series.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % minormax, either 'min' or 'max' to return either the minimum or maximum of y
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'misc')

    def __init__(self, minormax='max'):
        super(DN_MinMax, self).__init__()
        self.minormax = minormax

    def _eval_hook(self, eng, x):
        if self.minormax is None:
            return eng.run_function(1, 'DN_MinMax', x, )
        return eng.run_function(1, 'DN_MinMax', x, self.minormax)


class DN_Moments(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Output is the moment of the distribution of the input time series.
    % Normalizes by the standard deviation
    % Uses the moment function from Matlab's Statistics Toolbox
    % 
    %---INPUTS:
    % y, the input time series
    % n, the moment to calculate (a scalar)
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'moment', 'raw', 'shape', 'spreaddep')

    def __init__(self, n=3.0):
        super(DN_Moments, self).__init__()
        self.n = n

    def _eval_hook(self, eng, x):
        if self.n is None:
            return eng.run_function(1, 'DN_Moments', x, )
        return eng.run_function(1, 'DN_Moments', x, self.n)


class DN_OutlierInclude(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures a range of different statistics about the time series as more and
    % more outliers are included in the calculation according to a specified rule:
    % 
    % (i) 'abs': outliers are furthest from the mean,
    % (ii) 'p': outliers are the greatest positive deviations from the mean, or
    % (iii) 'n': outliers are the greatest negative deviations from the mean.
    % 
    % The threshold for including time-series data points in the analysis increases
    % from zero to the maximum deviation, in increments of 0.01*sigma (by default),
    % where sigma is the standard deviation of the time series.
    % 
    % At each threshold, the mean, standard error, proportion of time series points
    % included, median, and standard deviation are calculated, and outputs from the
    % algorithm measure how these statistical quantities change as more extreme
    % points are included in the calculation.
    % 
    %---INPUTS:
    % y, the input time series (ideally z-scored)
    % 
    % howth, the method of how to determine outliers: 'abs', 'p', or 'n' (see above
    %           for descriptions)
    % 
    % inc, the increment to move through (fraction of std if input time series is
    %       z-scored)
    % 
    % Most of the outputs measure either exponential, i.e., f(x) = Aexp(Bx)+C, or
    % linear, i.e., f(x) = Ax + B, fits to the sequence of statistics obtained in
    % this way.
    % 
    % [future: could compare differences in outputs obtained with 'p', 'n', and
    %               'abs' -- could give an idea as to asymmetries/nonstationarities??]
    %               
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (36,)

    TAGS = ('distribution', 'outliers', 'stochastic')

    def __init__(self, howth='abs', inc=None):
        super(DN_OutlierInclude, self).__init__()
        self.howth = howth
        self.inc = inc

    def _eval_hook(self, eng, x):
        if self.howth is None:
            return eng.run_function(1, 'DN_OutlierInclude', x, )
        elif self.inc is None:
            return eng.run_function(1, 'DN_OutlierInclude', x, self.howth)
        return eng.run_function(1, 'DN_OutlierInclude', x, self.howth, self.inc)


class DN_OutlierTest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Removes the p% of highest and lowest values in the time series (i.e., 2*p%
    % removed from the time series in total) and returns the ratio of either the
    % mean or the standard deviation of the time series, before and after this
    % transformation.
    % 
    %---INPUTS:
    % y, the input time series
    % p, the percentage of values to remove beyond upper and lower percentiles
    % justme [opt], just returns a number:
    %               (i) 'mean' -- returns the mean of the middle portion of the data
    %               (ii) 'std' -- returns the std of the middle portion of the data
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (2,)

    TAGS = ('distribution', 'outliers', 'spread')

    def __init__(self, p=2.0, justme=None):
        super(DN_OutlierTest, self).__init__()
        self.p = p
        self.justme = justme

    def _eval_hook(self, eng, x):
        if self.p is None:
            return eng.run_function(1, 'DN_OutlierTest', x, )
        elif self.justme is None:
            return eng.run_function(1, 'DN_OutlierTest', x, self.p)
        return eng.run_function(1, 'DN_OutlierTest', x, self.p, self.justme)


class DN_ProportionValues(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns statistics on the values of the raw time series: the proportion
    % of zeros in the raw time series, the proportion of positive values, and the
    % proportion of values greater than or equal to zero.
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % propwhat, the proportion of a given type of value in the time series:
    %           (i) 'zeros': values that equal zero
    %           (ii) 'positive': values that are strictly positive
    %           (iii) 'geq0': values that are greater than or equal to zero
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('locdep', 'raw')

    def __init__(self, propwhat='positive'):
        super(DN_ProportionValues, self).__init__()
        self.propwhat = propwhat

    def _eval_hook(self, eng, x):
        if self.propwhat is None:
            return eng.run_function(1, 'DN_ProportionValues', x, )
        return eng.run_function(1, 'DN_ProportionValues', x, self.propwhat)


class DN_Quantile(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the quantile value at a specified proportion p using the Statistics
    % Toolbox function, quantile.
    % 
    % INPUTS:
    % y, the input time series
    % p, the quantile proportion
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution',)

    def __init__(self, p=0.6):
        super(DN_Quantile, self).__init__()
        self.p = p

    def _eval_hook(self, eng, x):
        if self.p is None:
            return eng.run_function(1, 'DN_Quantile', x, )
        return eng.run_function(1, 'DN_Quantile', x, self.p)


class DN_RemovePoints(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyze how some time-series properties function changes as points are removed
    % from a time series.
    % 
    % A proportion, p, of points are removed from the time series according to some
    % rule, and a set of statistics are computed before and after the change.
    % 
    % INPUTS:
    % y, the input time series
    % howtorem, how to remove points from the time series:
    %               (i) 'absclose': those that are the closest to the mean,
    %               (ii) 'absfar': those that are the furthest from the mean,
    %               (iii) 'min': the lowest values,
    %               (iv) 'max': the highest values,
    %               (v) 'random': at random.
    %               
    % p, the proportion of points to remove
    % 
    % Output statistics include the change in autocorrelation, time scales, mean,
    % spread, and skewness.
    % 
    % Note that this is a similar idea to that implemented in DN_OutlierInclude.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('correlation', 'distribution', 'outliers')

    def __init__(self, howtorem='absclose', p=0.1):
        super(DN_RemovePoints, self).__init__()
        self.howtorem = howtorem
        self.p = p

    def _eval_hook(self, eng, x):
        if self.howtorem is None:
            return eng.run_function(1, 'DN_RemovePoints', x, )
        elif self.p is None:
            return eng.run_function(1, 'DN_RemovePoints', x, self.howtorem)
        return eng.run_function(1, 'DN_RemovePoints', x, self.howtorem, self.p)


class DN_SimpleFit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits different distributions or simple time-series models to the time series
    % using 'fit' function from Matlab's Curve Fitting Toolbox.
    % 
    % The distribution of time-series values is estimated using either a
    % kernel-smoothed density via the Matlab function ksdensity with the default
    % width parameter, or by a histogram with a specified number of bins, nbins.
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % dmodel, the model to fit:
    %       (I) distribution models:
    %           (i) 'gauss1'
    %           (ii) 'gauss2'
    %           (iii) 'exp1'
    %           (iv) 'power1'
    %       (II) simple time-series models:
    %           (i) 'sin1'
    %           (ii) 'sin2'
    %           (iii) 'sin3'
    %           (iv) 'fourier1'
    %           (v) 'fourier2'
    %           (vi) 'fourier3'
    % 
    % nbins, the number of bins for a histogram-estimate of the distribution of
    %       time-series values. If nbins = 0, uses ksdensity instead of histogram.
    % 
    % 
    %---OUTPUTS: the goodness of fifit, R^2, rootmean square error, the
    % autocorrelation of the residuals, and a runs test on the residuals.
    % 
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (6,)

    TAGS = ('adjr2', 'distribution', 'exp1', 'fourier1', 'gauss1', 'gauss2', 'gof', 'model'
            'power1', 'r2', 'resAC1', 'resAC2', 'resruns', 'rmse', 'sin1', 'sin2', 'sin3')

    def __init__(self, dmodel='exp1', nbins=0.0):
        super(DN_SimpleFit, self).__init__()
        self.dmodel = dmodel
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.dmodel is None:
            return eng.run_function(1, 'DN_SimpleFit', x, )
        elif self.nbins is None:
            return eng.run_function(1, 'DN_SimpleFit', x, self.dmodel)
        return eng.run_function(1, 'DN_SimpleFit', x, self.dmodel, self.nbins)


class DN_Spread(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns the spread of the raw time series, as the standard deviation,
    % inter-quartile range, mean absolute deviation, or median absolute deviation.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % SpreadMeasure, the spead measure:
    %               (i) 'std': standard deviation
    %               (ii) 'iqr': interquartile range
    %               (iii) 'mad': mean absolute deviation
    %               (iv) 'mead': median absolute deviation
    % 
    %---HISTORY:
    % Ben Fulcher, 2008
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('diff', 'raw', 'spread', 'spreaddep')

    def __init__(self, SpreadMeasure='std'):
        super(DN_Spread, self).__init__()
        self.SpreadMeasure = SpreadMeasure

    def _eval_hook(self, eng, x):
        if self.SpreadMeasure is None:
            return eng.run_function(1, 'DN_Spread', x, )
        return eng.run_function(1, 'DN_Spread', x, self.SpreadMeasure)


class DN_TrimmedMean(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Outputs the mean of the trimmed time series using the Matlab function
    % trimmean.
    % 
    %---INPUTS:
    % y, the input time series
    % n, the percent of highest and lowest values in y to exclude from the mean
    %     calculation
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('location', 'locdep', 'raw')

    def __init__(self, n=2.0):
        super(DN_TrimmedMean, self).__init__()
        self.n = n

    def _eval_hook(self, eng, x):
        if self.n is None:
            return eng.run_function(1, 'DN_TrimmedMean', x, )
        return eng.run_function(1, 'DN_TrimmedMean', x, self.n)


class DN_Withinp(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the proportion of the time-series data points that lie within
    % p standard deviations of its mean.
    % 
    %---INPUTS:
    % x, the input time series
    % p, the number (proportion) of standard deviations.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'spread')

    def __init__(self, p=3.0):
        super(DN_Withinp, self).__init__()
        self.p = p

    def _eval_hook(self, eng, x):
        if self.p is None:
            return eng.run_function(1, 'DN_Withinp', x, )
        return eng.run_function(1, 'DN_Withinp', x, self.p)


class DN_cv(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the coefficient of variation, sigma^k / mu^k, of order k.
    % 
    %---INPUTS:
    % 
    % x, the input time series
    % 
    % k, the order of coefficient of variation (k = 1 is usual)
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('cv', 'locdep', 'raw', 'spread', 'spreaddep')

    def __init__(self, k=4.0):
        super(DN_cv, self).__init__()
        self.k = k

    def _eval_hook(self, eng, x):
        if self.k is None:
            return eng.run_function(1, 'DN_cv', x, )
        return eng.run_function(1, 'DN_cv', x, self.k)


class DN_nlogL_norm(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a Gaussian distribution to the data using the normfit function in
    % Matlab's Statistics Toolbox and returns the negative log likelihood of the
    % data coming from a Gaussian distribution using the normlike function.
    % 
    %---INPUT:
    % y, the time series.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'gof', 'lengthdep')

    def __init__(self):
        super(DN_nlogL_norm, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'DN_nlogL_norm', x, )


class DN_pleft(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the maximum distance from the mean at which a given fixed proportion,
    % p, of the time-series data points are further.
    % Normalizes by the standard deviation of the time series
    % (could generalize to separate positive and negative deviations in future)
    % Uses the quantile function from Matlab's Statistics Toolbox
    %
    %---INPUTS:
    % y, the input time series
    % th, the proportion of data further than p from the mean
    %           (output p, normalized by standard deviation)
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'spread')

    def __init__(self, th=0.1):
        super(DN_pleft, self).__init__()
        self.th = th

    def _eval_hook(self, eng, x):
        if self.th is None:
            return eng.run_function(1, 'DN_pleft', x, )
        return eng.run_function(1, 'DN_pleft', x, self.th)


class DT_IsSeasonal(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % A simple test of seasonality by fitting a 'sin1' model to the time series
    % using fit function from the Curve Fitting Toolbox. The output is binary: 1 if
    % the goodness of fit, R^2, exceeds 0.3 and the amplitude of the fitted periodic
    % component exceeds 0.5, and 0 otherwise.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    %---OUTPUT: Binary: 1 (= seasonal), 0 (= non-seasonal)
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('periodicity',)

    def __init__(self):
        super(DT_IsSeasonal, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'DT_IsSeasonal', x, )


class EN_ApEn(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates the Approximate Entropy of the time series, ApEn(m,r).
    % 
    % cf. S. M. Pincus, "Approximate entropy as a measure of system complexity",
    % P. Natl. Acad. Sci. USA, 88(6) 2297 (1991)
    %
    % For more information, cf. http://physionet.org/physiotools/ApEn/
    % 
    %--INPUTS:
    % y, the input time series
    % mnom, the embedding dimension
    % rth, the threshold for judging closeness/similarity
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy',)

    def __init__(self, mnom=1.0, rth=0.2):
        super(EN_ApEn, self).__init__()
        self.mnom = mnom
        self.rth = rth

    def _eval_hook(self, eng, x):
        if self.mnom is None:
            return eng.run_function(1, 'EN_ApEn', x, )
        elif self.rth is None:
            return eng.run_function(1, 'EN_ApEn', x, self.mnom)
        return eng.run_function(1, 'EN_ApEn', x, self.mnom, self.rth)


class EN_DistributionEntropy(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates of entropy from the static distribution of the time series. The
    % distribution is estimated either using a histogram with nbins bins, or as a
    % kernel-smoothed distribution, using the ksdensity function from Matlab's
    % Statistics Toolbox with width parameter, w (specified as the iunput nbins).
    % 
    % An optional additional parameter can be used to remove a proportion of the
    % most extreme positive and negative deviations from the mean as an initial
    % pre-processing.
    % 
    %---INPUTS:
    % y, the input time series
    % HistorKS: 'hist' for histogram, or 'ks' for ksdensity
    % nbins: (*) (for 'hist'): an integer, uses a histogram with that many bins (for 'hist')
    %        (*) (for 'ks'): a positive real number, for the width parameter for ksdensity
    %                        (can also be empty for default width parameter, optimum for Gaussian)
    % olremp [opt]: the proportion of outliers at both extremes to remove
    %               (e.g., if olremp = 0.01; keeps only the middle 98% of data; 0 keeps all data.
    %               This parameter ought to be less than 0.5, which keeps none of the data)
    %
    %---HISTORY:
    % Ben Fulcher, August 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy', 'raw', 'spreaddep')

    def __init__(self, HistorKS='ks', nbins=(), olremp=0.1):
        super(EN_DistributionEntropy, self).__init__()
        self.HistorKS = HistorKS
        self.nbins = nbins
        self.olremp = olremp

    def _eval_hook(self, eng, x):
        if self.HistorKS is None:
            return eng.run_function(1, 'EN_DistributionEntropy', x, )
        elif self.nbins is None:
            return eng.run_function(1, 'EN_DistributionEntropy', x, self.HistorKS)
        elif self.olremp is None:
            return eng.run_function(1, 'EN_DistributionEntropy', x, self.HistorKS, self.nbins)
        return eng.run_function(1, 'EN_DistributionEntropy', x, self.HistorKS, self.nbins, self.olremp)


class EN_MS_shannon(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the approximate Shannon entropy of a time series using an
    % nbin-bin encoding and depth-symbol sequences.
    % Uniform population binning is used, and the implementation uses Michael Small's code
    % MS_shannon.m (renamed from the original, simply shannon.m)
    % 
    % cf. M. Small, Applied Nonlinear Time Series Analysis: Applications in Physics,
    % Physiology, and Finance (book) World Scientific, Nonlinear Science Series A,
    % Vol. 52 (2005)
    % Michael Small's code is available at available at http://small.eie.polyu.edu.hk/matlab/
    % 
    % In this wrapper function, you can evaluate the code at a given n and d, and
    % also across a range of depth and nbin to return statistics on how the obtained
    % entropies change.
    % 
    % INPUTS:
    % y, the input time series
    % nbin, the number of bins to discretize the time series into (i.e., alphabet size)
    % depth, the length of strings to analyze
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1, 5)

    TAGS = ('MichaelSmall', 'entropy', 'mex', 'shannon')

    def __init__(self, nbin=2.0, depth=2.0):
        super(EN_MS_shannon, self).__init__()
        self.nbin = nbin
        self.depth = depth

    def _eval_hook(self, eng, x):
        if self.nbin is None:
            return eng.run_function(1, 'EN_MS_shannon', x, )
        elif self.depth is None:
            return eng.run_function(1, 'EN_MS_shannon', x, self.nbin)
        return eng.run_function(1, 'EN_MS_shannon', x, self.nbin, self.depth)


class EN_PermEn(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the permutation entropy of order, ord, of a time series.
    % This is wrapper code for a Land and Elias implementation.
    % 
    % "Permutation Entropy: A Natural Complexity Measure for Time Series"
    % C. Bandt and B. Pompe, Phys. Rev. Lett. 88(17) 174102 (2002)
    % 
    % Code is adapted from logisticPE.m code obtained from
    % http://people.ece.cornell.edu/land/PROJECTS/Complexity/
    % http://people.ece.cornell.edu/land/PROJECTS/Complexity/logisticPE.m
    % 
    %---INPUTS:
    % y, a time series
    % ord, the order of permutation entropy
    % 
    %---OUTPUT:
    % out is the permutation entropy, using Land and Elias code
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy',)

    def __init__(self, ordd=3.0):
        super(EN_PermEn, self).__init__()
        self.ordd = ordd

    def _eval_hook(self, eng, x):
        if self.ordd is None:
            return eng.run_function(1, 'EN_PermEn', x, )
        return eng.run_function(1, 'EN_PermEn', x, self.ordd)


class EN_RM_entropy(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the entropy of the time series using a function by Rudy Moddemeijer
    % 
    % Original code, now RM_entropy, was obtained from:
    % http://www.cs.rug.nl/~rudy/matlab/
    % 
    % The above website has code and documentation for the function.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy',)

    def __init__(self):
        super(EN_RM_entropy, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'EN_RM_entropy', x, )


class EN_Randomize(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Progressively randomizes the input time series according to some randomization
    % scheme, and returns measures of how the properties of the time series change
    % with this process.
    % 
    % The procedure is repeated 2N times, where N is the length of the time series.
    % 
    %---INPUTS:
    % y, the input (z-scored) time series
    % randomizeHow, specifies the randomization scheme for each iteration:
    %      (i) 'statdist' -- substitutes a random element of the time series with
    %                           one from the original time-series distribution
    %      (ii) 'dyndist' -- overwrites a random element of the time
    %                       series with another random element
    %      (iii) 'permute' -- permutes pairs of elements of the time
    %                       series randomly
    % 
    %---OUTPUTS: summarize how the properties change as one of these
    % randomization procedures is iterated, including the cross correlation with the
    % original time series, the autocorrelation of the randomized time series, its
    % entropy, and stationarity.
    % 
    % These statistics are calculated every N/10 iterations, and thus 20 times
    % throughout the process in total.
    % 
    % Most statistics measure how these properties decay with randomization, by
    % fitting a function f(x) = Aexp(Bx).
    % 
    %---HISTORY:
    % Ben Fulcher, October 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (73,)

    TAGS = ('entropy', 'lengthdep', 'slow', 'stochastic')

    def __init__(self, randomizeHow='statdist'):
        super(EN_Randomize, self).__init__()
        self.randomizeHow = randomizeHow

    def _eval_hook(self, eng, x):
        if self.randomizeHow is None:
            return eng.run_function(1, 'EN_Randomize', x, )
        return eng.run_function(1, 'EN_Randomize', x, self.randomizeHow)


class EN_SampEn(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates the Sample Entropy of the time series, SampEn(m,r), by referencing
    % code from PhysioNet.
    % 
    % The publicly-available PhysioNet code, sampenc (renamed here to RN_sampenc) is
    % available from:
    % http://www.physionet.org/physiotools/sampen/matlab/1.1/sampenc.m
    %
    % cf. "Physiological time-series analysis using approximate entropy and sample
    % entropy", J. S. Richman and J. R. Moorman, Am. J. Physiol. Heart Circ.
    % Physiol., 278(6) H2039 (2000)
    % 
    % This function can also calculate the SampEn of successive increments of time
    % series, i.e., we using an incremental differencing pre-processing, as
    % used in the so-called Control Entropy quantity:
    % 
    % "Control Entropy: A complexity measure for nonstationary signals"
    % E. M. Bollt and J. Skufca, Math. Biosci. Eng., 6(1) 1 (2009)
    % 
    %---INPUTS:
    % y, the input time series
    % M, the embedding dimension
    % r, the threshold
    % preprocess [opt], (i) 'diff1', incremental difference preprocessing.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (10,)

    TAGS = ('controlen', 'entropy', 'sampen')

    def __init__(self, M=4.0, r=0.1, preprocess=None):
        super(EN_SampEn, self).__init__()
        self.M = M
        self.r = r
        self.preprocess = preprocess

    def _eval_hook(self, eng, x):
        if self.M is None:
            return eng.run_function(1, 'EN_SampEn', x, )
        elif self.r is None:
            return eng.run_function(1, 'EN_SampEn', x, self.M)
        elif self.preprocess is None:
            return eng.run_function(1, 'EN_SampEn', x, self.M, self.r)
        return eng.run_function(1, 'EN_SampEn', x, self.M, self.r, self.preprocess)


class EN_Shannonpdf(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates the (log_2) Shannon entropy from the probability distribution of the time
    % series.
    % 
    %---INPUT:
    % y, the input time series
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy', 'shannonpdf')

    def __init__(self):
        super(EN_Shannonpdf, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'EN_Shannonpdf', x, )


class EN_wentropy(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses the wentropy function from Matlab's Wavelet toolbox to
    % estimate the entropy of the input time series.
    % 
    %--INPUTS:
    % y, the input time series
    % whaten, the entropy type:
    %               'shannon',
    %               'logenergy',
    %               'threshold' (with a given threshold),
    %               'sure' (with a given parameter).
    %               (see the wentropy documentaiton for information)
    % p, the additional parameter needed for threshold and sure entropies
    % 
    % Author's cautionary note: it seems likely that this implementation of wentropy
    % is nonsense.
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy', 'logenergy', 'shannon', 'sure', 'threshold')

    def __init__(self, whaten='threshold', p=1.0):
        super(EN_wentropy, self).__init__()
        self.whaten = whaten
        self.p = p

    def _eval_hook(self, eng, x):
        if self.whaten is None:
            return eng.run_function(1, 'EN_wentropy', x, )
        elif self.p is None:
            return eng.run_function(1, 'EN_wentropy', x, self.whaten)
        return eng.run_function(1, 'EN_wentropy', x, self.whaten, self.p)


class EX_MovingThreshold(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % A measure based on a moving threshold model for extreme events. Inspired by an
    % idea contained in the following paper:
    % "Reactions to extreme events: Moving threshold model"
    % Altmann et al., Physica A 364, 435--444 (2006)
    % 
    % This algorithm is based on this idea: it uses the occurrence of extreme events
    % to modify a hypothetical 'barrier' that classes new points as 'extreme' or not.
    % The barrier begins at sigma, and if the absolute value of the next data point
    % is greater than the barrier, the barrier is increased by a proportion 'a',
    % otherwise the position of the barrier is decreased by a proportion 'b'.
    % 
    %---INPUTS:
    % y, the input (z-scored) time series
    % a, the barrier jump parameter (in extreme event)
    % b, the barrier decay proportion (in absence of extreme event)
    % 
    %---OUTPUTS: the mean, spread, maximum, and minimum of the time series for the
    % barrier, the mean of the difference between the barrier and the time series
    % values, and statistics on the occurrence of 'kicks' (times at which the
    % threshold is modified), and by how much the threshold changes on average.
    % 
    % In future could make a variant operation that optimizes a and b to minimize the
    % quantity meanqover/pkick (hugged the shape as close as possible with the
    % minimum number of kicks), and returns a and b...?
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('outliers',)

    def __init__(self, a=1.0, b=0.02):
        super(EX_MovingThreshold, self).__init__()
        self.a = a
        self.b = b

    def _eval_hook(self, eng, x):
        if self.a is None:
            return eng.run_function(1, 'EX_MovingThreshold', x, )
        elif self.b is None:
            return eng.run_function(1, 'EX_MovingThreshold', x, self.a)
        return eng.run_function(1, 'EX_MovingThreshold', x, self.a, self.b)


class FC_LocalSimple(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Does local forecasting using very simple predictors using the past l values
    % of the time series to predict its next value.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % fmeth, the forecasting method:
    %          (i) 'mean': local mean prediction using the past ltrain time-series
    %                       values,
    %          (ii) 'median': local median prediction using the past ltrain
    %                         time-series values
    %          (iii) 'lfit': local linear prediction using the past ltrain
    %                         time-series values.
    % 
    % ltrain, the number of time-series values to use to forecast the next value
    % 
    %---OUTPUTS: the mean error, stationarity of residuals, Gaussianity of
    % residuals, and their autocorrelation structure.
    % 
    %---HISTORY:
    % Ben Fulcher, Nov 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('forecasting',)

    def __init__(self, fmeth='mean', ltrain=3.0):
        super(FC_LocalSimple, self).__init__()
        self.fmeth = fmeth
        self.ltrain = ltrain

    def _eval_hook(self, eng, x):
        if self.fmeth is None:
            return eng.run_function(1, 'FC_LocalSimple', x, )
        elif self.ltrain is None:
            return eng.run_function(1, 'FC_LocalSimple', x, self.fmeth)
        return eng.run_function(1, 'FC_LocalSimple', x, self.fmeth, self.ltrain)


class FC_LoopLocalSimple(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyzes the outputs of FC_LocalSimple for a range of local window lengths, l.
    % Loops over the length of the data to use for FC_LocalSimple prediction
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % fmeth, the prediction method:
    %            (i) 'mean', local mean prediction
    %            (ii) 'median', local median prediction
    % 
    %---OUTPUTS: statistics including whether the mean square error increases or
    % decreases, testing for peaks, variability, autocorrelation, stationarity, and
    % a fit of exponential decay, f(x) = A*exp(Bx) + C, to the variation.
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (22,)

    TAGS = ('forecasting',)

    def __init__(self, fmeth='mean'):
        super(FC_LoopLocalSimple, self).__init__()
        self.fmeth = fmeth

    def _eval_hook(self, eng, x):
        if self.fmeth is None:
            return eng.run_function(1, 'FC_LoopLocalSimple', x, )
        return eng.run_function(1, 'FC_LoopLocalSimple', x, self.fmeth)


class FC_Surprise(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % How surprised you might be by the next recorded data points given the data
    % recorded in recent memory.
    % 
    % Coarse-grains the time series, turning it into a sequence of symbols of a
    % given alphabet size, ng, and quantifies measures of surprise of a
    % process with local memory of the past memory values of the symbolic string.
    % 
    % We then consider a memory length, memory, of the time series, and
    % use the data in the proceeding memory samples to inform our expectations of
    % the following sample.
    % 
    % The 'information gained', log(1/p), at each sample using expectations
    % calculated from the previous memory samples, is estimated.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % whatinf, the type of information to store in memory:
    %           (i) 'dist': the values of the time series in the previous memory
    %                       samples,
    %           (ii) 'T1': the one-point transition probabilities in the previous
    %                       memory samples, and
    %           (iii) 'T2': the two-point transition probabilities in the previous
    %                       memory samples.
    %                       
    % memory, the memory length (either number of samples, or a proportion of the
    %           time-series length, if between 0 and 1)
    %           
    % ng, the number of groups to coarse-grain the time series into
    % 
    % cgmeth, the coarse-graining, or symbolization method:
    %          (i) 'quantile': an equiprobable alphabet by the value of each
    %                          time-series datapoint,
    %          (ii) 'updown': an equiprobable alphabet by the value of incremental
    %                         changes in the time-series values, and
    %          (iii) 'embed2quadrants': by the quadrant each data point resides in
    %                          in a two-dimensional embedding space.
    % 
    % nits, the number of iterations to repeat the procedure for.
    % 
    %---OUTPUTS: summaries of this series of information gains, including the
    %            minimum, maximum, mean, median, lower and upper quartiles, and
    %            standard deviation.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (8, 7)

    TAGS = ('information', 'stochastic', 'symbolic')

    def __init__(self, whatinf='dist', memory=50.0, ng=3.0, cgmeth='quantile', nits=None):
        super(FC_Surprise, self).__init__()
        self.whatinf = whatinf
        self.memory = memory
        self.ng = ng
        self.cgmeth = cgmeth
        self.nits = nits

    def _eval_hook(self, eng, x):
        if self.whatinf is None:
            return eng.run_function(1, 'FC_Surprise', x, )
        elif self.memory is None:
            return eng.run_function(1, 'FC_Surprise', x, self.whatinf)
        elif self.ng is None:
            return eng.run_function(1, 'FC_Surprise', x, self.whatinf, self.memory)
        elif self.cgmeth is None:
            return eng.run_function(1, 'FC_Surprise', x, self.whatinf, self.memory, self.ng)
        elif self.nits is None:
            return eng.run_function(1, 'FC_Surprise', x, self.whatinf, self.memory, self.ng, self.cgmeth)
        return eng.run_function(1, 'FC_Surprise', x, self.whatinf, self.memory, self.ng, self.cgmeth, self.nits)


class HT_DistributionTest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a distribution to the data and then performs an appropriate hypothesis
    % test to quantify the difference between the two distributions. We fit
    % Gaussian, Extreme Value, Uniform, Beta, Rayleigh, Exponential, Gamma,
    % Log-Normal, and Weibull distributions, using code described for
    % DN_M_kscomp.
    % 
    %---INPUTS:
    % x, the input time series
    % thetest, the hypothesis test to perform:
    %           (i) 'chi2gof': chi^2 goodness of fit test
    %           (ii) 'ks': Kolmogorov-Smirnov test
    %           (iii) 'lillie': Lilliefors test
    % 
    % thedistn, the distribution to fit:
    %           (i) 'norm' (Normal)
    %           (ii) 'ev' (Extreme value)
    %           (iii) 'uni' (Uniform)
    %           (iv) 'beta' (Beta)
    %           (v) 'rayleigh' (Rayleigh)
    %           (vi) 'exp' (Exponential)
    %           (vii) 'gamma' (Gamma)
    %           (viii) 'logn' (Log-normal)
    %           (ix) 'wbl' (Weibull)
    % 
    % nbins, the number of bins to use for the chi2 goodness of fit test
    % 
    % All of these functions for hypothesis testing are implemented in Matlab's
    % Statistics Toolbox.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('chi2gof', 'distribution', 'hypothesistest', 'ks', 'lillie', 'locdep', 'raw')

    def __init__(self, thetest='ks', thedistn='beta', nbins=None):
        super(HT_DistributionTest, self).__init__()
        self.thetest = thetest
        self.thedistn = thedistn
        self.nbins = nbins

    def _eval_hook(self, eng, x):
        if self.thetest is None:
            return eng.run_function(1, 'HT_DistributionTest', x, )
        elif self.thedistn is None:
            return eng.run_function(1, 'HT_DistributionTest', x, self.thetest)
        elif self.nbins is None:
            return eng.run_function(1, 'HT_DistributionTest', x, self.thetest, self.thedistn)
        return eng.run_function(1, 'HT_DistributionTest', x, self.thetest, self.thedistn, self.nbins)


class HT_HypothesisTest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Outputs the p-value from a statistical hypothesis test applied to the
    % time series.
    % 
    % Tests are implemented as functions in Matlab's Statistics Toolbox.
    % (except Ljung-Box Q-test, which uses the Econometrics Toolbox)
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % theTest, the hypothesis test to perform:
    %           (i) sign test ('signtest'),
    %           (ii) runs test ('runstest'),
    %           (iii) variance test ('vartest'),
    %           (iv) Z-test ('ztest'),
    %           (v) Wilcoxon signed rank test for a zero median ('signrank'),
    %           (vi) Jarque-Bera test of composite normality ('jbtest').
    %           (vii) Ljung-Box Q-test for residual autocorrelation ('lbq')
    %           
    %---OUTPUT:
    % the p-value from the statistical test
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('econometricstoolbox', 'hypothesistest', 'jbtest', 'lbq', 'randomness', 'raw', 'runstest'
            'signrank', 'signtest', 'ztest')

    def __init__(self, theTest='runstest'):
        super(HT_HypothesisTest, self).__init__()
        self.theTest = theTest

    def _eval_hook(self, eng, x):
        if self.theTest is None:
            return eng.run_function(1, 'HT_HypothesisTest', x, )
        return eng.run_function(1, 'HT_HypothesisTest', x, self.theTest)


class MD_hrv_classic(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Packages up a bunch of classic heart rate variability (HRV) statistics and
    % applies them to the input time series.
    % 
    % Assumes an NN/RR time series in units of seconds.
    % 
    %---INPUTS:
    % y, the input time series.
    % 
    % Includes:
    %  (i) pNNx
    %  cf. "The pNNx files: re-examining a widely used heart rate variability
    %           measure", J.E. Mietus et al., Heart 88(4) 378 (2002)
    % 
    %  (ii) Power spectral density ratios in different frequency ranges
    %   cf. "Heart rate variability: Standards of measurement, physiological
    %       interpretation, and clinical use",
    %       M. Malik et al., Eur. Heart J. 17(3) 354 (1996)
    % 
    %  (iii) Triangular histogram index, and
    %  
    %  (iv) Poincare plot measures
    %  cf. "Do existing measures of Poincare plot geometry reflect nonlinear
    %       features of heart rate variability?"
    %       M. Brennan, et al., IEEE T. Bio.-Med. Eng. 48(11) 1342 (2001)
    %  
    % Code is heavily derived from that provided by Max A. Little:
    % http://www.maxlittle.net/
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (12,)

    TAGS = ('maxlittle', 'medical')

    def __init__(self):
        super(MD_hrv_classic, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'MD_hrv_classic', x, )


class MD_pNN(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Applies pNNx measures to time series assumed to represent sequences of
    % consecutive RR intervals measured in milliseconds.
    % 
    % cf. "The pNNx files: re-examining a widely used heart rate variability
    %           measure", J.E. Mietus et al., Heart 88(4) 378 (2002)
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % This code is derived from MD_hrv_classic.m becuase it doesn't make medical
    % sense to do PNN on a z-scored time series.
    % 
    % But now PSD doesn't make too much sense, so we just evaluate the pNN measures.
    % 
    % Code is heavily derived from that provided by Max A. Little:
    % http://www.maxlittle.net/
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('maxlittle', 'medical', 'raw', 'spreaddep')

    def __init__(self):
        super(MD_pNN, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'MD_pNN', x, )


class MD_polvar(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the POLVARd measure for a time series.
    % The first mention may be in Wessel et al., PRE (2000), called Plvar
    % cf. "Short-term forecasting of life-threatening cardiac arrhythmias based on
    % symbolic dynamics and finite-time growth rates",
    %       N. Wessel et al., Phys. Rev. E 61(1) 733 (2000)
    % 
    % The output from this function is the probability of obtaining a sequence of
    % consecutive ones or zeros.
    % 
    % Although the original measure used raw thresholds, d, on RR interval sequences
    % (measured in milliseconds), this code can be applied to general z-scored time
    % series. So now d is not the time difference in milliseconds, but in units of
    % std.
    % 
    % The measure was originally applied to sequences of RR intervals and this code
    % is heavily derived from that provided by Max A. Little, January 2009.
    % cf. http://www.maxlittle.net/
    % 
    %---INPUTS:
    % x, the input time series
    % d, the symbolic coding (amplitude) difference,
    % D, the word length (classically words of length 6).
    % 
    %---OUPUT:
    % p - probability of obtaining a sequence of consecutive ones/zeros
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('maxlittle', 'medical', 'symbolic')

    def __init__(self, d=0.1, D=3.0):
        super(MD_polvar, self).__init__()
        self.d = d
        self.D = D

    def _eval_hook(self, eng, x):
        if self.d is None:
            return eng.run_function(1, 'MD_polvar', x, )
        elif self.D is None:
            return eng.run_function(1, 'MD_polvar', x, self.d)
        return eng.run_function(1, 'MD_polvar', x, self.d, self.D)


class MD_rawHRVmeas(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Evaluates the triangular histogram index and Poincare plot measures to a time
    % series assumed to measure sequences of consecutive RR intervals measured in
    % milliseconds. Doesn't make much sense for other time series
    % 
    % cf. "Do existing measures of Poincare plot geometry reflect nonlinear
    %      features of heart rate variability?"
    %      M. Brennan, et al., IEEE T. Bio.-Med. Eng. 48(11) 1342 (2001)
    % 
    % Note that pNNx is not done here, but in MD_pNN.m
    % 
    % This code is heavily derived from Max Little's hrv_classic.m code
    % Max Little: http://www.maxlittle.net/
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('maxlittle', 'medical', 'raw', 'spreaddep')

    def __init__(self):
        super(MD_rawHRVmeas, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'MD_rawHRVmeas', x, )


class MF_ARMA_orders(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Given a set of AR orders, p, and a set of MA orders, q, this operation fits
    % ARMA(p,q) models to the time series and evaluates the goodness of fit from all
    % combinations (p,q).
    % 
    % Uses functions iddata, armax, and aic from Matlab's System Identification toolbox
    % 
    %---INPUTS:
    % y, the input time series
    % pr, a vector specifying the range of AR model orders to analyze
    % qr, a vector specifying the range of MA model orders to analyze
    % 
    %---OUTPUTS: statistics on the appropriateness of different types of models,
    % including the goodness of fit from the best model, and the optimal orders of
    % fitted ARMA(p,q) models.
    % 
    % ** Future improvements **
    % (1) May want to quantify where a particular order starts to stand out, i.e.,
    % may be quite sensitive to wanting p > 2, but may be quite indiscriminate
    % when it comes to the MA order.
    % (2) May want to do some prediction and get more statistics on quality of
    % model rather than just in-sample FPE/AIC...
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (7,)

    TAGS = ('arma', 'model', 'systemidentificationtoolbox')

    def __init__(self, pr=MatlabSequence('1:6'), qr=MatlabSequence('1:4')):
        super(MF_ARMA_orders, self).__init__()
        self.pr = pr
        self.qr = qr

    def _eval_hook(self, eng, x):
        if self.pr is None:
            return eng.run_function(1, 'MF_ARMA_orders', x, )
        elif self.qr is None:
            return eng.run_function(1, 'MF_ARMA_orders', x, self.pr)
        return eng.run_function(1, 'MF_ARMA_orders', x, self.pr, self.qr)


class MF_AR_arcov(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits an AR model of a given order, p, using arcov code from Matlab's Signal
    % Processing Toolbox.
    % 
    %---INPUTS:
    % y, the input time series
    % p, the AR model order
    % 
    %---OUTPUTS: include the parameters of the fitted model, the variance estimate of a
    % white noise input to the AR model, the root-mean-square (RMS) error of a
    % reconstructed time series, and the autocorrelation of residuals.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11, 10, 9, 8, 6)

    TAGS = ('AR', 'fit', 'gof', 'model', 'var')

    def __init__(self, p=3.0):
        super(MF_AR_arcov, self).__init__()
        self.p = p

    def _eval_hook(self, eng, x):
        if self.p is None:
            return eng.run_function(1, 'MF_AR_arcov', x, )
        return eng.run_function(1, 'MF_AR_arcov', x, self.p)


class MF_CompareAR(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Compares fits of AR models of various orders to the input time series.
    % 
    % Uses functions from Matlab's System Identification Toolbox: iddata, arxstruc,
    % and selstruc
    % 
    %---INPUTS:
    % y, vector of equally-spaced time series data
    % orders, a vector of possible model orders
    % howtotest, specify a fraction, or provide a string 'all' to train and test on
    %            all the data
    % 
    %---OUTPUTS: statistics on the loss at each model order, which are obtained by
    % applying the model trained on the training data to the testing data.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (18,)

    TAGS = ('ar', 'model', 'systemidentificationtoolbox')

    def __init__(self, orders=MatlabSequence('1:10'), howtotest='all'):
        super(MF_CompareAR, self).__init__()
        self.orders = orders
        self.howtotest = howtotest

    def _eval_hook(self, eng, x):
        if self.orders is None:
            return eng.run_function(1, 'MF_CompareAR', x, )
        elif self.howtotest is None:
            return eng.run_function(1, 'MF_CompareAR', x, self.orders)
        return eng.run_function(1, 'MF_CompareAR', x, self.orders, self.howtotest)


class MF_CompareTestSets(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Looks at robustness of test set goodness of fit over different samples in
    % the time series from fitting a given time-series model.
    % 
    % Similar to MF_FitSubsegments, except fits the model on the full time
    % series and compares how well it predicts time series in different local
    % time-series segments.
    % 
    % Says something of stationarity in spread of values, and something of the
    % suitability of model in level of values.
    % 
    % Uses function iddata and predict from Matlab's System Identification Toolbox,
    % as well as either ar, n4sid, or armax from Matlab's System Identification
    % Toolbox to fit the models, depending on the specified model to fit to the data.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % model, the type of time-series model to fit:
    %           (i) 'ar', fits an AR model
    %           (ii) 'ss', first a state-space model
    %           (iii) 'arma', first an ARMA model
    %
    % ord, the order of the specified model to fit
    %
    % howtosubset, how to select random subsets of the time series to fit:
    %           (i) 'rand', select at random
    %           (ii) 'uniform', uniformly distributed segments throughout the time
    %                   series
    %                   
    % samplep, a two-vector specifying the sampling parameters
    %           e.g., [20, 0.1] repeats 20 times for segments 10% the length of the
    %                           time series
    % 
    % steps, the number of steps ahead to do the predictions.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (20,)

    TAGS = ('ar', 'arfit', 'model', 'prediction', 'statespace', 'stochastic', 'systemidentificationtoolbox')

    def __init__(self, model='ar', ordd='best', howtosubset='uniform',
                 samplep=(25.0, 0.10000000000000001), steps=1.0):
        super(MF_CompareTestSets, self).__init__()
        self.model = model
        self.ordd = ordd
        self.howtosubset = howtosubset
        self.samplep = samplep
        self.steps = steps

    def _eval_hook(self, eng, x):
        if self.model is None:
            return eng.run_function(1, 'MF_CompareTestSets', x, )
        elif self.ordd is None:
            return eng.run_function(1, 'MF_CompareTestSets', x, self.model)
        elif self.howtosubset is None:
            return eng.run_function(1, 'MF_CompareTestSets', x, self.model, self.ordd)
        elif self.samplep is None:
            return eng.run_function(1, 'MF_CompareTestSets', x, self.model, self.ordd, self.howtosubset)
        elif self.steps is None:
            return eng.run_function(1, 'MF_CompareTestSets', x, self.model, self.ordd, self.howtosubset, self.samplep)
        return eng.run_function(1, 'MF_CompareTestSets', x, self.model, self.ordd, self.howtosubset,
                                self.samplep, self.steps)


class MF_ExpSmoothing(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits an exponential smoothing model to the time series using a training set to
    % fit the optimal smoothing parameter, alpha, and then applies the result to the
    % try to predict the rest of the time series.
    % 
    % cf. "The Analysis of Time Series", C. Chatfield, CRC Press LLC (2004)
    % 
    % Code is adapted from original code provided by Siddharth Arora:
    % Siddharth.Arora@sbs.ox.ac.uk
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % ntrain, the number of samples to use for training (can be a proportion of the
    %           time-series length)
    %           
    % alpha, the exponential smoothing parameter
    % 
    %---OUTPUTS: include the fitted alpha, and statistics on the residuals from the
    % prediction phase.
    % 
    % Future alteration could take a number of training sets and average to some
    % optimal alpha, for example, rather than just fitting it in an initial portion
    % of the time series.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (32,)

    TAGS = ('expsmoothing', 'model', 'siddarth')

    def __init__(self, ntrain=0.5, alpha='best'):
        super(MF_ExpSmoothing, self).__init__()
        self.ntrain = ntrain
        self.alpha = alpha

    def _eval_hook(self, eng, x):
        if self.ntrain is None:
            return eng.run_function(1, 'MF_ExpSmoothing', x, )
        elif self.alpha is None:
            return eng.run_function(1, 'MF_ExpSmoothing', x, self.ntrain)
        return eng.run_function(1, 'MF_ExpSmoothing', x, self.ntrain, self.alpha)


class MF_FitSubsegments(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Looks at the robustness of fitted parameters from a model applied to different
    % segments of the time series.
    % 
    % The spread of parameters obtained (including in-sample goodness of fit
    % statistics) provide some indication of stationarity.
    % 
    % Values of goodness of fit provide some indication of model suitability.
    % 
    % N.B., this code inherits strongly from this MF_CompareTestSets
    % 
    %---INPUTS:
    % y, the input time series.
    % 
    % model, the model to fit in each segments of the time series:
    %           'arsbc': fits an AR model using the ARfit package. Outputs
    %                       statistics are on how the optimal order, p_{opt}, and
    %                       the goodness of fit varies in different parts of the
    %                       time series.
    %           'ar': fits an AR model of a specified order using the code
    %                   ar from Matlab's System Identification Toolbox. Outputs are
    %                   on how Akaike's Final Prediction Error (FPE), and the fitted
    %                   AR parameters vary across the different segments of time
    %                   series.
    %           'ss': fits a state space model of a given order using the code
    %                   n4sid from Matlab's System Identification Toolbox. Outputs
    %                   are on how the FPE varies.
    %           'arma': fits an ARMA model using armax code from Matlab's System
    %                   Identification Toolbox. Outputs are statistics on the FPE,
    %                   and fitted AR and MA parameters.
    %                   
    % howtosubset, how to choose segments from the time series, either 'uniform'
    %               (uniformly) or 'rand' (at random).
    %               
    % samplep, a two-vector specifying how many segments to take and of what length.
    %           Of the form [nsamples, length], where length can be a proportion of
    %           the time-series length. e.g., [20,0.1] takes 20 segments of 10% the
    %           time-series length.
    % 
    %---OUTPUTS: depend on the model, as described above.
    % 
    %---HISTORY: Ben Fulcher, 12/2/2010
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (13, 5, 21, 11)

    TAGS = ('ar', 'arfit', 'arma', 'model', 'prediction', 'statespace', 'stochastic', 'systemidentificationtoolbox')

    def __init__(self, model='ar', order=2.0, howtosubset='uniform', samplep=(25.0, 0.10000000000000001)):
        super(MF_FitSubsegments, self).__init__()
        self.model = model
        self.order = order
        self.howtosubset = howtosubset
        self.samplep = samplep

    def _eval_hook(self, eng, x):
        if self.model is None:
            return eng.run_function(1, 'MF_FitSubsegments', x, )
        elif self.order is None:
            return eng.run_function(1, 'MF_FitSubsegments', x, self.model)
        elif self.howtosubset is None:
            return eng.run_function(1, 'MF_FitSubsegments', x, self.model, self.order)
        elif self.samplep is None:
            return eng.run_function(1, 'MF_FitSubsegments', x, self.model, self.order, self.howtosubset)
        return eng.run_function(1, 'MF_FitSubsegments', x, self.model, self.order, self.howtosubset, self.samplep)


class MF_GARCHcompare(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This code fits a set of GARCH(p,q) models to the time series and
    % returns statistics on the goodness of fits across a range of p and
    % q parameters.
    % 
    % Uses the following functions from Matlab's Econometrics Toolbox: archtest,
    % lbqtest, autocorr, parcorr, garchset, garchfit, garchcount, aicbic
    % 
    %---INPUTS:
    % y, the input time series
    % preproc, a preprocessing to apply:
    %           (i) 'none': no preprocessing is performed
    %           (ii) 'ar': performs a preprocessing that maximizes AR(2) whiteness,
    %           
    % pr, a vector of model orders, p, to compare
    % 
    % qr, a vector of model orders, q, to compare
    % 
    % Compares all combinations of p and q and output statistics are on the models
    % with the best fit.
    % 
    % This operation focuses on the GARCH/variance component, and therefore
    % attempts to pre-whiten and assumes a constant mean process.
    % 
    %---OUTPUTS: include log-likelihoods, Bayesian Information  Criteria (BIC),
    % Akaike's Information Criteria (AIC), outputs from Engle's ARCH test and the
    % Ljung-Box Q-test, and estimates of optimal model orders.
    % 
    %---HISTORY:
    % Ben Fulcher 26/2/2010
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (30,)

    TAGS = ('aic', 'bic', 'econometricstoolbox', 'garch', 'model')

    def __init__(self, preproc='ar', pr=MatlabSequence('1:3'), qr=MatlabSequence('1:3')):
        super(MF_GARCHcompare, self).__init__()
        self.preproc = preproc
        self.pr = pr
        self.qr = qr

    def _eval_hook(self, eng, x):
        if self.preproc is None:
            return eng.run_function(1, 'MF_GARCHcompare', x, )
        elif self.pr is None:
            return eng.run_function(1, 'MF_GARCHcompare', x, self.preproc)
        elif self.qr is None:
            return eng.run_function(1, 'MF_GARCHcompare', x, self.preproc, self.pr)
        return eng.run_function(1, 'MF_GARCHcompare', x, self.preproc, self.pr, self.qr)


class MF_GARCHfit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Simulates a procedure for fitting Generalized Autoregressive Conditional
    % Heteroskedasticity (GARCH) models to a time series, namely:
    % 
    % (1) Preprocessing the data to remove strong trends,
    % (2) Pre-estimation to calculate initial correlation properties of the time
    %       series and motivate a GARCH model,
    % (3) Fitting a GARCH model, returning goodness of fit statistics and parameters
    %           of the fitted model, and
    % (4) Post-estimation, involves calculating statistics on residuals and
    %           standardized residuals.
    % 
    % The idea is that all of these stages can be pre-specified or skipped using
    % arguments to the function.
    % 
    % Uses functions from Matlab's Econometrics Toolbox: archtest, lbqtest,
    % autocorr, parcorr, garchset, garchfit, garchcount, aicbic
    % 
    % All methods implemented are from Matlab's Econometrics Toolbox, including
    % Engle's ARCH test (archtest), the Ljung-Box Q-test (lbqtest), estimating the
    % partial autocorrelation function (parcorr), as well as specifying (garchset)
    % and fitting (garchfit) the GARCH model to the time series.
    % 
    % As part of this code, a very basic automatic pre-processing routine,
    % PP_ModelFit, is implemented, that applies a range of pre-processings and
    % returns the preprocessing of the time series that shows the worst fit to an
    % AR(2) model.
    % 
    % In the case that no simple transformations of the time series are
    % significantly more stationary/less trivially correlated than the original time
    % series (by more than 5%), the original time series is simply used without
    % transformation.
    % 
    % Where r and m are the autoregressive and moving average orders of the model,
    % respectively, and p and q control the conditional variance parameters.
    % 
    %---INPUTS:
    % y, the input time series
    % preproc, the preprocessing to apply, can be 'ar' or 'none'
    % params, the parameters of the GARCH model to fit, can be:
    %           (i) 'default', fits the default model
    %           (ii) 'auto', automated routine to select parameters for this time series
    %           (iii) e.g., params = '''R'',2,''M'',1,''P'',2,''Q'',1', sets r = 2,
    %                                   m = 1, p = 2, q = 1
    % 
    % 
    % ***In future this code should be revised by an expert in GARCH model fitting.***
    % 
    %---HISTORY:
    % Ben Fulcher, 25/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (62, 60)

    TAGS = ('aic', 'bic', 'econometricstoolbox', 'garch', 'model', 'stochastic')

    def __init__(self, preproc='ar', P=1.0, Q=1.0):
        super(MF_GARCHfit, self).__init__()
        self.preproc = preproc
        self.P = P
        self.Q = Q

    def _eval_hook(self, eng, x):
        if self.preproc is None:
            return eng.run_function(1, 'MF_GARCHfit', x, )
        elif self.P is None:
            return eng.run_function(1, 'MF_GARCHfit', x, self.preproc)
        elif self.Q is None:
            return eng.run_function(1, 'MF_GARCHfit', x, self.preproc, self.P)
        return eng.run_function(1, 'MF_GARCHfit', x, self.preproc, self.P, self.Q)


class MF_GP_FitAcross(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Trains a Gaussian Process model on equally-spaced points throughout the time
    % series and uses the model to predict its intermediate values.
    % 
    % Uses GP fitting code from the gpml toolbox, which is available here:
    % http://gaussianprocess.org/gpml/code.
    % 
    %---INPUTS:
    % y, the input time series
    % covFunc, the covariance function (structured in the standard way for the gpml toolbox)
    % npoints, the number of points through the time series to fit the GP model to
    % 
    %---OUTPUTS: summarize the error and fitted hyperparameters.
    % 
    % In future could do a better job of the sampling of points -- perhaps to take
    % into account the autocorrelation of the time series.
    % 
    %---HISTORY:
    % Ben Fulcher, 22/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (10,)

    TAGS = ('gaussianprocess',)

    def __init__(self, covFunc=('covSum', ('covSEiso', 'covNoise')), npoints=20.0):
        super(MF_GP_FitAcross, self).__init__()
        self.covFunc = covFunc
        self.npoints = npoints

    def _eval_hook(self, eng, x):
        if self.covFunc is None:
            return eng.run_function(1, 'MF_GP_FitAcross', x, )
        elif self.npoints is None:
            return eng.run_function(1, 'MF_GP_FitAcross', x, self.covFunc)
        return eng.run_function(1, 'MF_GP_FitAcross', x, self.covFunc, self.npoints)


class MF_GP_LearnHyperp(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Function used by main Gaussian Process model fitting operations that learns
    % Gaussian Process hyperparameters for the time series.
    % 
    % References code 'minimize' from the GAUSSIAN PROCESS REGRESSION AND
    % CLASSIFICATION Toolbox version 3.2, which is avilable at:
    % http://gaussianprocess.org/gpml/code
    % 
    %---INPUTS:
    % 
    % covFunc,       the covariance function, formated as gpml likes it
    % nfevals,       the number of function evaluations
    % t,             time
    % y,             data
    % init_loghyper, inital values for hyperparameters
    % 
    %---HISTORY:
    % Ben Fulcher, 2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self, y=None, covFunc=None, meanFunc=None, likFunc=None,
                 infAlg=None, nfevals=None, hyp=None):
        super(MF_GP_LearnHyperp, self).__init__()
        self.y = y
        self.covFunc = covFunc
        self.meanFunc = meanFunc
        self.likFunc = likFunc
        self.infAlg = infAlg
        self.nfevals = nfevals
        self.hyp = hyp

    def _eval_hook(self, eng, x):
        if self.y is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, )
        elif self.covFunc is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y)
        elif self.meanFunc is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc)
        elif self.likFunc is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc, self.meanFunc)
        elif self.infAlg is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc, self.meanFunc, self.likFunc)
        elif self.nfevals is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc, self.meanFunc,
                                    self.likFunc, self.infAlg)
        elif self.hyp is None:
            return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc, self.meanFunc,
                                    self.likFunc, self.infAlg, self.nfevals)
        return eng.run_function(1, 'MF_GP_LearnHyperp', x, self.y, self.covFunc, self.meanFunc,
                                self.likFunc, self.infAlg, self.nfevals, self.hyp)


class MF_GP_LocalPrediction(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a given Gaussian Process model to a section of the time series and uses
    % it to predict to the subsequent datapoint.
    % 
    % % Uses GP fitting code from the gpml toolbox, which is available here:
    % http://gaussianprocess.org/gpml/code.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % covFunc, covariance function in the standard form for the gpml package.
    %           E.g., covFunc = {'covSum', {'covSEiso','covNoise'}} combines squared 
    %           exponential and noise terms
    %           
    % ntrain, the number of training samples (for each iteration)
    % 
    % ntest, the number of testing samples (for each interation)
    % 
    % npreds, the number of predictions to make
    % 
    % pmode, the prediction mode:
    %       (i) 'beforeafter': predicts the preceding time series values by training
    %                           on the following values,
    %       (ii) 'frombefore': predicts the following values of the time series by
    %                    training on preceding values, and
    %       (iii) 'randomgap': predicts random values within a segment of time
    %                    series by training on the other values in that segment.
    % 
    % 
    %---OUTPUTS: summaries of the quality of predictions made, the mean and
    % spread of obtained hyperparameter values, and marginal likelihoods.
    % 
    % ---HISTORY
    % Ben Fulcher, 20/1/2010
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (24,)

    TAGS = ('gaussianprocess', 'stochastic')

    def __init__(self, covFunc=('covSum', ('covSEiso', 'covNoise')),
                 ntrain=10.0, ntest=3.0, npreds=20.0, pmode='frombefore'):
        super(MF_GP_LocalPrediction, self).__init__()
        self.covFunc = covFunc
        self.ntrain = ntrain
        self.ntest = ntest
        self.npreds = npreds
        self.pmode = pmode

    def _eval_hook(self, eng, x):
        if self.covFunc is None:
            return eng.run_function(1, 'MF_GP_LocalPrediction', x, )
        elif self.ntrain is None:
            return eng.run_function(1, 'MF_GP_LocalPrediction', x, self.covFunc)
        elif self.ntest is None:
            return eng.run_function(1, 'MF_GP_LocalPrediction', x, self.covFunc, self.ntrain)
        elif self.npreds is None:
            return eng.run_function(1, 'MF_GP_LocalPrediction', x, self.covFunc, self.ntrain, self.ntest)
        elif self.pmode is None:
            return eng.run_function(1, 'MF_GP_LocalPrediction', x, self.covFunc, self.ntrain, self.ntest, self.npreds)
        return eng.run_function(1, 'MF_GP_LocalPrediction', x, self.covFunc, self.ntrain, self.ntest,
                                self.npreds, self.pmode)


class MF_GP_hyperparameters(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a Gaussian Process model to a portion of the time series and returns the
    % fitted hyperparameters, as well as statistics describing the goodness of fit
    % of the model.
    % 
    % Uses GP fitting code from the gpml toolbox, which is available here:
    % http://gaussianprocess.org/gpml/code.
    % 
    % The code can accomodate a range of covariance functions, e.g.:
    % (i) a sum of squared exponential and noise terms, and
    % (ii) a sum of squared exponential, periodic, and noise terms.
    % 
    % The model is fitted to <> samples from the time series, which are
    % chosen by:
    % (i) resampling the time series down to this many data points,
    % (ii) taking the first 200 samples from the time series, or
    % (iii) taking random samples from the time series.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % covFunc, the covariance function, in the standard form of the gmpl package
    % 
    % squishorsquash, whether to squash onto the unit interval, or spread across 1:N
    % 
    % maxN, the maximum length of time series to consider -- inputs greater than
    %           this length are resampled down to maxN
    %           
    % methds, specifies the method of how to resample time series longer than maxN
    % 
    %---HISTORY:
    % Ben Fulcher, 19/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (18, 14)

    TAGS = ('gaussianprocess', 'stochastic')

    def __init__(self, covFunc=('covSum', ('covSEiso', 'covNoise')),
                 squishorsquash=1.0, maxN=200.0, methds='first'):
        super(MF_GP_hyperparameters, self).__init__()
        self.covFunc = covFunc
        self.squishorsquash = squishorsquash
        self.maxN = maxN
        self.methds = methds

    def _eval_hook(self, eng, x):
        if self.covFunc is None:
            return eng.run_function(1, 'MF_GP_hyperparameters', x, )
        elif self.squishorsquash is None:
            return eng.run_function(1, 'MF_GP_hyperparameters', x, self.covFunc)
        elif self.maxN is None:
            return eng.run_function(1, 'MF_GP_hyperparameters', x, self.covFunc, self.squishorsquash)
        elif self.methds is None:
            return eng.run_function(1, 'MF_GP_hyperparameters', x, self.covFunc, self.squishorsquash, self.maxN)
        return eng.run_function(1, 'MF_GP_hyperparameters', x, self.covFunc, self.squishorsquash,
                                self.maxN, self.methds)


class MF_ResidualAnalysis(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Given an input residual time series residuals, e, this function exports a
    % structure with fields corresponding to structural tests on the residuals.
    % These are motivated by a general expectation of model residuals to be
    % uncorrelated.
    %
    %---INPUT:
    % e, should be raw residuals as prediction minus data (e = yp - y) as a column
    %       vector. Will take absolute values / even powers of e as necessary.
    % 
    %---HISTORY:
    % Ben Fulcher, 10/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self):
        super(MF_ResidualAnalysis, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'MF_ResidualAnalysis', x, )


class MF_StateSpaceCompOrder(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits state space models using n4sid (from Matlab's System Identification
    % Toolbox) of orders 1, 2, ..., maxorder and returns statistics on how the
    % goodness of fit changes across this range.
    % 
    % c.f., MF_CompareAR -- does a similar thing for AR models
    % Uses the functions iddata, n4sid, and aic from Matlab's System Identification
    % Toolbox
    % 
    %---INPUTS:
    % y, the input time series
    % maxorder, the maximum model order to consider.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('model', 'statespace', 'systemidentificationtoolbox')

    def __init__(self, maxorder=8.0):
        super(MF_StateSpaceCompOrder, self).__init__()
        self.maxorder = maxorder

    def _eval_hook(self, eng, x):
        if self.maxorder is None:
            return eng.run_function(1, 'MF_StateSpaceCompOrder', x, )
        return eng.run_function(1, 'MF_StateSpaceCompOrder', x, self.maxorder)


class MF_StateSpace_n4sid(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a state space model of given order to the time series using the n4sid
    % function in Matlab's System Identification Toolbox.
    % 
    % First fits the model to the whole time series, then trains it on the first
    % portion and tries to predict the rest.
    % 
    % In the second portion of this code, the state space model is fitted to the
    % first p*N samples of the time series, where p is a given proportion and N is
    % the length of the time series.
    % 
    % This model is then used to predict the latter portion of the time
    % series (i.e., the subsequent (1-p)*N samples).
    % 
    % Uses the functions iddata, n4sid, aic, and predict from Matlab's System Identification Toolbox
    % 
    %---INPUTS:
    % y, the input time series
    % ord, the order of state-space model to implement (can also be the string 'best')
    % ptrain, the proportion of the time series to use for training
    % steps, the number of steps ahead to predict
    % 
    %---OUTPUTS: parameters from the model fitted to the entire time series, and
    % goodness of fit and residual analysis from n4sid prediction.
    % 
    %---HISTORY:
    % Ben Fulcher, 1/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (49, 42, 37)

    TAGS = ('model', 'statespace', 'systemidentificationtoolbox')

    def __init__(self, ordd=3.0, ptrain=0.5, steps=1.0):
        super(MF_StateSpace_n4sid, self).__init__()
        self.ordd = ordd
        self.ptrain = ptrain
        self.steps = steps

    def _eval_hook(self, eng, x):
        if self.ordd is None:
            return eng.run_function(1, 'MF_StateSpace_n4sid', x, )
        elif self.ptrain is None:
            return eng.run_function(1, 'MF_StateSpace_n4sid', x, self.ordd)
        elif self.steps is None:
            return eng.run_function(1, 'MF_StateSpace_n4sid', x, self.ordd, self.ptrain)
        return eng.run_function(1, 'MF_StateSpace_n4sid', x, self.ordd, self.ptrain, self.steps)


class MF_arfit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fit an AR model to the time series then returns statistics about it.
    % 
    % Uses various functions implemented in the ARfit package, which is
    % freely-available at http://www.gps.caltech.edu/~tapio/arfit/
    % 
    % cf. "Estimation of parameters and eigenmodes of multivariate autoregressive
    %       models", A. Neumaier and T. Schneider, ACM Trans. Math. Softw. 27, 27 (2001)
    % 
    % cf. "Algorithm 808: ARFIT---a Matlab package for the estimation of parameters
    %      and eigenmodes of multivariate autoregressive models",
    %      T. Schneider and A. Neumaier, ACM Trans. Math. Softw. 27, 58 (2001)
    % 
    % Autoregressive (AR) models are fitted with orders p = pmin, pmin + 1, ..., pmax.
    % 
    % The optimal model order is selected using Schwartz's Bayesian Criterion (SBC).
    % 
    %---INPUTS:
    % y, the input time series
    % pmin, the minimum AR model order to fit
    % pmax, the maximum AR model order to fit
    % selector, crierion to select optimal time-series model order (e.g., 'sbc', cf.
    %           ARFIT package documentation)
    % 
    %---OUTPUTS: include the model coefficients obtained, the SBCs at each model order,
    % various tests on residuals, and statistics from an eigendecomposition of the
    % time series using the estimated AR model.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (61,)

    TAGS = ('arfit', 'modelfit')

    def __init__(self, pmin=1.0, pmax=8.0, selector='sbc'):
        super(MF_arfit, self).__init__()
        self.pmin = pmin
        self.pmax = pmax
        self.selector = selector

    def _eval_hook(self, eng, x):
        if self.pmin is None:
            return eng.run_function(1, 'MF_arfit', x, )
        elif self.pmax is None:
            return eng.run_function(1, 'MF_arfit', x, self.pmin)
        elif self.selector is None:
            return eng.run_function(1, 'MF_arfit', x, self.pmin, self.pmax)
        return eng.run_function(1, 'MF_arfit', x, self.pmin, self.pmax, self.selector)


class MF_armax(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits an ARMA(p,q) model to the time series and returns various statistics on
    % the result.
    % 
    % Uses the functions iddata, armax, aic, and predict from Matlab's System
    % Identification Toolbox
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % orders, a two-vector for p and q, the AR and MA components of the model,
    %           respectively,
    % 
    % ptrain, the proportion of data to train the model on (the remainder is used
    %           for testing),
    % 
    % nsteps, number of steps to predict into the future for testing the model.
    % 
    % 
    %---OUTPUTS: include the fitted AR and MA coefficients, the goodness of fit in
    % the training data, and statistics on the residuals from using the fitted model
    % to predict the testing data.
    % 
    %---HISTORY:
    % Ben Fulcher, 1/2/2010
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (39, 39, 37)

    TAGS = ('arma', 'model', 'systemidentificationtoolbox')

    def __init__(self, orders=(2.0, 2.0), ptrain=0.5, nsteps=1.0):
        super(MF_armax, self).__init__()
        self.orders = orders
        self.ptrain = ptrain
        self.nsteps = nsteps

    def _eval_hook(self, eng, x):
        if self.orders is None:
            return eng.run_function(1, 'MF_armax', x, )
        elif self.ptrain is None:
            return eng.run_function(1, 'MF_armax', x, self.orders)
        elif self.nsteps is None:
            return eng.run_function(1, 'MF_armax', x, self.orders, self.ptrain)
        return eng.run_function(1, 'MF_armax', x, self.orders, self.ptrain, self.nsteps)


class MF_hmm_CompareNStates(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits HMMs with different numbers of states, and compares the resulting
    % test-set likelihoods.
    % 
    % The code relies on Zoubin Gharamani's implementation of HMMs for real-valued
    % Gassian-distributed observations, including the hmm and hmm_cl routines (
    % renamed ZG_hmm and ZG_hmm_cl here).
    % Implementation of HMMs for real-valued Gaussian observations:
    % http://www.gatsby.ucl.ac.uk/~zoubin/software.html
    % or, specifically:
    % http://www.gatsby.ucl.ac.uk/~zoubin/software/hmm.tar.gz
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % trainp, the initial proportion of the time series to train the model on
    % 
    % nstater, the vector of state numbers to compare. E.g., (2:4) compares a number
    %               of states 2, 3, and 4.
    % 
    %---OUTPUTS: statistics on how the log likelihood of the test data changes with
    % the number of states n_{states}$. We implement the code for p_{train} = 0.6$
    % as n_{states}$ varies across the range n_{states} = 2, 3, 4$.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (9,)

    TAGS = ('gharamani', 'hmm', 'model')

    def __init__(self, trainp=0.6, nstater=MatlabSequence('2:4')):
        super(MF_hmm_CompareNStates, self).__init__()
        self.trainp = trainp
        self.nstater = nstater

    def _eval_hook(self, eng, x):
        if self.trainp is None:
            return eng.run_function(1, 'MF_hmm_CompareNStates', x, )
        elif self.nstater is None:
            return eng.run_function(1, 'MF_hmm_CompareNStates', x, self.trainp)
        return eng.run_function(1, 'MF_hmm_CompareNStates', x, self.trainp, self.nstater)


class MF_hmm_fit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses Zoubin Gharamani's implementation of HMMs for real-valued Gaussian
    % observations:
    % http://www.gatsby.ucl.ac.uk/~zoubin/software.html
    % or, specifically:
    % http://www.gatsby.ucl.ac.uk/~zoubin/software/hmm.tar.gz
    % 
    % Uses ZG_hmm (renamed from hmm) and ZG_hmm_cl (renamed from hmm_cl)
    % 
    %---INPUTS:
    % y, the input time series
    % trainp, the proportion of data to train on, 0 < trainp < 1
    % numStates, the number of states in the HMM
    % 
    %---HISTORY:
    % Ben Fulcher 9/4/2010
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (14, 13)

    TAGS = ('gharamani', 'hmm', 'model')

    def __init__(self, trainp=0.7, numStates=3.0):
        super(MF_hmm_fit, self).__init__()
        self.trainp = trainp
        self.numStates = numStates

    def _eval_hook(self, eng, x):
        if self.trainp is None:
            return eng.run_function(1, 'MF_hmm_fit', x, )
        elif self.numStates is None:
            return eng.run_function(1, 'MF_hmm_fit', x, self.trainp)
        return eng.run_function(1, 'MF_hmm_fit', x, self.trainp, self.numStates)


class MF_steps_ahead(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Given a model, characterizes the variation in goodness of model predictions
    % across a range of prediction lengths, l, which is made to vary from
    % 1-step ahead to maxsteps steps-ahead predictions.
    % 
    % Models are fit using code from Matlab's System Identification Toolbox:
    % (i) AR models using the ar function,
    % (ii) ARMA models using armax code, and
    % (iii) state-space models using n4sid code.
    % 
    % The model is fitted on the full time series and then used to predict the same
    % data.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % model, the time-series model to fit: 'ar', 'arma', or 'ss'
    % 
    % order, the order of the model to fit
    % 
    % maxsteps, the maximum number of steps ahead to predict
    % 
    %---OUTPUTS: include the errors, for prediction lengths l = 1, 2, ..., maxsteps,
    % returned for each model relative to the best performance from basic null
    % predictors, including sliding 1- and 2-sample mean predictors and simply
    % predicting each point as the mean of the full time series. Additional outputs
    % quantify how the errors change as the prediction length increases from l = 1,
    % ..., maxsteps (relative to a simple predictor).
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (23,)

    TAGS = ('ar', 'arfit', 'arma', 'model', 'prediction', 'statespace', 'systemidentificationtoolbox')

    def __init__(self, model='ar', order='best', maxsteps=6.0):
        super(MF_steps_ahead, self).__init__()
        self.model = model
        self.order = order
        self.maxsteps = maxsteps

    def _eval_hook(self, eng, x):
        if self.model is None:
            return eng.run_function(1, 'MF_steps_ahead', x, )
        elif self.order is None:
            return eng.run_function(1, 'MF_steps_ahead', x, self.model)
        elif self.maxsteps is None:
            return eng.run_function(1, 'MF_steps_ahead', x, self.model, self.order)
        return eng.run_function(1, 'MF_steps_ahead', x, self.model, self.order, self.maxsteps)


class NL_BoxCorrDim(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % References TSTOOL code, corrdim, to estimate the correlation dimension of a
    % time-delay embedded time series using a box-counting approach.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, column vector of time series data
    % 
    % nbins, maximum number of partitions per axis
    % 
    % embedparams [opt], embedding parameters as {tau,m} in 2-entry cell for a
    %                   time-delay, tau, and embedding dimension, m. As inputs to BF_embed.
    % 
    %---OUTPUTS: Simple summaries of the outputs from corrdim.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (85,)

    TAGS = ('corrdim', 'correlation', 'nonlinear', 'tstool')

    def __init__(self, nbins=50.0, embedparams=('ac', 5)):
        super(NL_BoxCorrDim, self).__init__()
        self.nbins = nbins
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.nbins is None:
            return eng.run_function(1, 'NL_BoxCorrDim', x, )
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_BoxCorrDim', x, self.nbins)
        return eng.run_function(1, 'NL_BoxCorrDim', x, self.nbins, self.embedparams)


class NL_CaosMethod(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % References TSTOOL code cao, to determine the minimum embedding dimension for a
    % time series using Cao's method:
    % 
    % "Practical method for determining the minimum embedding dimension of a scalar
    % time series", L. Cao, Physica D 110(1-2) 43 (1997)
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    % It computes the quantities E and E* for a range of embedding dimensions
    % m = 1, ..., m_{max}.
    % 
    %---INPUTS:
    % 
    % y, time series as a column vector
    % 
    % maxdim, maximum embedding dimension to consider
    % 
    % tau, time delay (can also be 'ac' or 'mi' for first zero-crossing of the
    %          autocorrelation function or the first minimum of the automutual information
    %          function)
    %
    % NNR, number of nearest neighbours to use
    % 
    % Nref, number of reference points (can also be a fraction; of data length)
    % 
    % justanum [opt]: if not empty can just return a number, the embedding
    %                   dimension, based on the specified criterion:
    %                 (i) 'thresh', caoo1 passes above a threshold, th (given as
    %                               justanum = {'thresh',th})
    %                 (ii) 'mthresh', when gradient passes below a threshold (levels
    %                                 off), given as {'mthresh',mthresh}, where
    %                                 mthresh in the threshold
    %                 (iii) 'mmthresh', analyzes incremental differences to find
    %                                   level-off point
    %   
    % 
    %---OUTPUTS: statistics on the result, including when the output quantity first
    % passes a given threshold, and the m at which it levels off.
    % 
    %---HISTORY:
    % Ben Fulcher, October 2009
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (48,)

    TAGS = ('cao', 'dimension', 'nonlinear', 'stochastic', 'tstool')

    def __init__(self, maxdim=10.0, tau='mi', NNR=2.0, Nref=100.0, justanum=None):
        super(NL_CaosMethod, self).__init__()
        self.maxdim = maxdim
        self.tau = tau
        self.NNR = NNR
        self.Nref = Nref
        self.justanum = justanum

    def _eval_hook(self, eng, x):
        if self.maxdim is None:
            return eng.run_function(1, 'NL_CaosMethod', x, )
        elif self.tau is None:
            return eng.run_function(1, 'NL_CaosMethod', x, self.maxdim)
        elif self.NNR is None:
            return eng.run_function(1, 'NL_CaosMethod', x, self.maxdim, self.tau)
        elif self.Nref is None:
            return eng.run_function(1, 'NL_CaosMethod', x, self.maxdim, self.tau, self.NNR)
        elif self.justanum is None:
            return eng.run_function(1, 'NL_CaosMethod', x, self.maxdim, self.tau, self.NNR, self.Nref)
        return eng.run_function(1, 'NL_CaosMethod', x, self.maxdim, self.tau, self.NNR, self.Nref, self.justanum)


class NL_MS_LZcomplexity(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the Lempel-Ziv complexity of a n-bit encoding of the time
    % series using Michael Small's code: 'complexity' (renamed MS_complexity here).
    % 
    % cf. M. Small, Applied Nonlinear Time Series Analysis: Applications in Physics,
    % Physiology, and Finance (book) World Scientific, Nonlinear Science Series A,
    % Vol. 52 (2005)
    % Code is available at http://small.eie.polyu.edu.hk/matlab/
    % 
    % The code is a wrapper for Michael Small's original code and uses the
    % associated mex file compiled from complexitybs.c (renamed MS_complexitybs.c
    % here).
    % 
    %---INPUTS:
    % y, the input time series
    % n, the (integer) number of bits to encode the data into
    % PreProc [opt], first apply a given PreProcessing to the time series. For now,
    %               just 'diff' is implemented, which zscores incremental
    %               differences and then applies the complexity method.
    % 
    %---OUTPUT: the normalized Lempel-Ziv complexity: i.e., the number of distinct
    %           symbol sequences in the time series divided by the expected number
    %           of distinct symbols for a noise sequence.
    % 
    %---HISTORY:
    % Ben Fulcher, 19/2/2010
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('LempelZiv', 'MichaelSmall', 'complexity', 'mex')

    def __init__(self, n=7.0, PreProc='diff'):
        super(NL_MS_LZcomplexity, self).__init__()
        self.n = n
        self.PreProc = PreProc

    def _eval_hook(self, eng, x):
        if self.n is None:
            return eng.run_function(1, 'NL_MS_LZcomplexity', x, )
        elif self.PreProc is None:
            return eng.run_function(1, 'NL_MS_LZcomplexity', x, self.n)
        return eng.run_function(1, 'NL_MS_LZcomplexity', x, self.n, self.PreProc)


class NL_MS_fnn(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Determines the number of false nearest neighbors for the embedded time series
    % using Michael Small's false nearest neighbor code, fnn (renamed MS_fnn here)
    % 
    % cf. M. Small, Applied Nonlinear Time Series Analysis: Applications in Physics,
    % Physiology, and Finance (book) World Scientific, Nonlinear Science Series A,
    % Vol. 52 (2005)
    % Code available at http://small.eie.polyu.edu.hk/matlab/
    % 
    % False nearest neighbors are judged using a ratio of the distances between the
    % next k points and the neighboring points of a given datapoint.
    % 
    %---INPUTS:
    % y, the input time series
    % de, the embedding dimensions to compare across (a vector)
    % tau, the time-delay (can be 'ac' or 'mi' to be the first zero-crossing of ACF,
    %                       or first minimum of AMI, respectively)
    % th, the distance threshold for neighbours
    % kth, the the distance to next points
    % [opt] justbest, can be set to 1 to just return the best embedding dimension, m_{best}
    % [opt] bestp, if justbest = 1, can set bestp as the proportion of false nearest
    %              neighbours at which the optimal embedding dimension is selected.
    % 
    % This function returns statistics on the proportion of false nearest neighbors
    % as a function of the embedding dimension m = m_{min}, m_{min}+1, ..., m_{max}
    % for a given time lag tau, and distance threshold for neighbors, d_{th}.
    % 
    %---OUTPUTS: include the proportion of false nearest neighbors at each m, the mean
    % and spread, and the smallest m at which the proportion of false nearest
    % neighbors drops below each of a set of fixed thresholds.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (18,)

    TAGS = ('MichaelSmall', 'fnn', 'nonlinear', 'slow')

    def __init__(self, de=MatlabSequence('1:10'), tau='mi', th=5.0, kth=1.0, justbest=None, bestp=None):
        super(NL_MS_fnn, self).__init__()
        self.de = de
        self.tau = tau
        self.th = th
        self.kth = kth
        self.justbest = justbest
        self.bestp = bestp

    def _eval_hook(self, eng, x):
        if self.de is None:
            return eng.run_function(1, 'NL_MS_fnn', x, )
        elif self.tau is None:
            return eng.run_function(1, 'NL_MS_fnn', x, self.de)
        elif self.th is None:
            return eng.run_function(1, 'NL_MS_fnn', x, self.de, self.tau)
        elif self.kth is None:
            return eng.run_function(1, 'NL_MS_fnn', x, self.de, self.tau, self.th)
        elif self.justbest is None:
            return eng.run_function(1, 'NL_MS_fnn', x, self.de, self.tau, self.th, self.kth)
        elif self.bestp is None:
            return eng.run_function(1, 'NL_MS_fnn', x, self.de, self.tau, self.th, self.kth, self.justbest)
        return eng.run_function(1, 'NL_MS_fnn', x, self.de, self.tau, self.th, self.kth, self.justbest, self.bestp)


class NL_MS_nlpe(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the normalized 'drop-one-out' constant interpolation nonlinear
    % prediction error for a time-delay embedded time series using Michael Small's
    % code nlpe (renamed MS_nlpe here):
    % 
    % cf. M. Small, Applied Nonlinear Time Series Analysis: Applications in Physics,
    % Physiology, and Finance (book) World Scientific, Nonlinear Science Series A,
    % Vol. 52 (2005)
    % 
    % Michael Small's Matlab code is available at http://small.eie.polyu.edu.hk/matlab/
    % 
    %---INPUTS:
    % y, the input time series
    % de, the embedding dimension (can be an integer, or 'fnn' to select as the
    %       point where the proportion of false nearest neighbors falls below 5%
    %       using NL_MS_fnn)
    % tau, the time-delay (can be an integer or 'ac' to be the first zero-crossing
    %       of the ACF or 'mi' to be the first minimum of the automutual information
    %       function)
    % 
    %---OUTPUTS: include measures of the meanerror of the nonlinear predictor, and a
    % set of measures on the correlation, Gaussianity, etc. of the residuals.
    % 
    %---HISTORY:
    % Ben Fulcher, 19/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (29,)

    TAGS = ('MichaelSmall', 'model', 'nlpe', 'nonlinear', 'slow')

    def __init__(self, de='fnn', tau='mi', maxN=None):
        super(NL_MS_nlpe, self).__init__()
        self.de = de
        self.tau = tau
        self.maxN = maxN

    def _eval_hook(self, eng, x):
        if self.de is None:
            return eng.run_function(1, 'NL_MS_nlpe', x, )
        elif self.tau is None:
            return eng.run_function(1, 'NL_MS_nlpe', x, self.de)
        elif self.maxN is None:
            return eng.run_function(1, 'NL_MS_nlpe', x, self.de, self.tau)
        return eng.run_function(1, 'NL_MS_nlpe', x, self.de, self.tau, self.maxN)


class NL_TISEAN_c1(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements the c1 and c2d routines from the TISEAN nonlinear time-series
    % analysis package that compute curves for the fixed mass computation of the
    % information dimension.
    % 
    % cf. "Practical implementation of nonlinear time series methods: The TISEAN
    % package" Hegger, R. and Kantz, H. and Schreiber, T., Chaos 9(2) 413 (1999)
    % 
    % Available here:
    % http://www.mpipks-dresden.mpg.de/~tisean/Tisean_3.0.1/index.html
    % 
    % The TISEAN routines are performed in the command line using 'system' commands
    % in Matlab, and require that TISEAN is installed and compiled, and able to be
    % executed in the command line.
    % 
    %---INPUTS:
    % 
    % y, the time series to analyze
    % 
    % tau, the time-delay (can be 'ac' or 'mi' for the first zero-crossing of the
    %           autocorrelation function or first minimum of the automutual
    %           information function)
    % 
    % mmm, a two-vector specifying the minimum and maximum embedding dimensions,
    %       e.g., [2,10] for m = 2 up to m = 10
    % 
    % tsep, time separation (can be between 0 and 1 for a proportion of the
    %       time-series length)
    %       
    % Nref, the number of reference points (can also be between 0 and 1 to specify a
    %       proportion of the time-series length)
    % 
    % 
    %---OUTPUTS: optimal scaling ranges and dimension estimates for a time delay,
    % tau, embedding dimensions, m, ranging from m_{min} to m_{max}, a time
    % separation, tsep, and a number of reference points, Nref.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('dimension', 'entropy', 'nonlinear', 'tisean')

    def __init__(self, tau=1.0, mmm=(1.0, 7.0), tsep=0.02, Nref=0.5):
        super(NL_TISEAN_c1, self).__init__()
        self.tau = tau
        self.mmm = mmm
        self.tsep = tsep
        self.Nref = Nref

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'NL_TISEAN_c1', x, )
        elif self.mmm is None:
            return eng.run_function(1, 'NL_TISEAN_c1', x, self.tau)
        elif self.tsep is None:
            return eng.run_function(1, 'NL_TISEAN_c1', x, self.tau, self.mmm)
        elif self.Nref is None:
            return eng.run_function(1, 'NL_TISEAN_c1', x, self.tau, self.mmm, self.tsep)
        return eng.run_function(1, 'NL_TISEAN_c1', x, self.tau, self.mmm, self.tsep, self.Nref)


class NL_TISEAN_d2(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements the d2 routine from the popular TISEAN package for
    % nonlinear time-series analysis:
    % 
    % cf. "Practical implementation of nonlinear time series methods: The TISEAN
    % package", R. Hegger, H. Kantz, and T. Schreiber, Chaos 9(2) 413 (1999)
    % 
    % The TISEAN package is available here:
    % http://www.mpipks-dresden.mpg.de/~tisean/Tisean_3.0.1/index.html
    % 
    % The TISEAN routines are performed in the command line using 'system' commands
    % in Matlab, and require that TISEAN is installed and compiled, and able to be
    % executed in the command line.
    % 
    % The function estimates the correlation sum, the correlation dimension and
    % the correlation entropy of a given time series, y. Our code uses the outputs
    % from this algorithm to return a set of informative features about the results.
    % 
    %---INPUTS:
    % 
    % y, input time series
    % 
    % tau, time-delay (can be 'ac' or 'mi' for first zero-crossing of
    %       autocorrelation function, or first minimum of the automutual
    %       information)
    %       
    % maxm, the maximum embedding dimension
    % 
    % theilerwin, the Theiler window
    % 
    % cf. "Spurious dimension from correlation algorithms applied to limited
    % time-series data", J. Theiler, Phys. Rev. A, 34(3) 2427 (1986)
    % 
    % cf. "Nonlinear Time Series Analysis", Cambridge University Press, H. Kantz
    % and T. Schreiber (2004)
    % 
    % Taken's estimator is computed for the correlation dimension, as well as related
    % statistics, including other dimension estimates by finding appropriate scaling
    % ranges, and searching for a flat region in the output of TISEAN's h2
    % algorithm, which indicates determinism/deterministic chaos.
    % 
    % To find a suitable scaling range, a penalized regression procedure is used to
    % determine an optimal scaling range that simultaneously spans the greatest
    % range of scales and shows the best fit to the data, and return the range, a
    % goodness of fit statistic, and a dimension estimate.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (51,)

    TAGS = ('dimension', 'nonlinear', 'tisean')

    def __init__(self, tau=1.0, maxm=10.0, theilerwin=0.0):
        super(NL_TISEAN_d2, self).__init__()
        self.tau = tau
        self.maxm = maxm
        self.theilerwin = theilerwin

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'NL_TISEAN_d2', x, )
        elif self.maxm is None:
            return eng.run_function(1, 'NL_TISEAN_d2', x, self.tau)
        elif self.theilerwin is None:
            return eng.run_function(1, 'NL_TISEAN_d2', x, self.tau, self.maxm)
        return eng.run_function(1, 'NL_TISEAN_d2', x, self.tau, self.maxm, self.theilerwin)


class NL_TSTL_FractalDimensions(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the fractal dimension spectrum, D(q), using moments of neighbor
    % distances for time-delay embedded time series by referencing the code,
    % fracdims, from the TSTOOL package.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % 
    % y, column vector of time series data
    % 
    % kmin, minimum number of neighbours for each reference point
    % 
    % kmax, maximum number of neighbours for each reference point
    % 
    % Nref, number of randomly-chosen reference points (-1: use all points)
    % 
    % gstart, starting value for moments
    % 
    % gend, end value for moments
    % 
    % past [opt], number of samples to exclude before an after each reference
    %             index (default=0)
    % 
    % steps [opt], number of moments to calculate (default=32);
    % 
    % embedparams, how to embed the time series using a time-delay reconstruction
    % 
    % 
    %---OUTPUTS: include basic statistics of D(q) and q, statistics from a linear fit,
    % and an exponential fit of the form D(q) = Aexp(Bq) + C.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (17,)

    TAGS = ('correlation', 'dimension', 'nonlinear', 'stochastic', 'tstool')

    def __init__(self, kmin=2.0, kmax=100.0, Nref=0.2, gstart=1.0,
                 gend=5.0, past=10.0, steps=32.0, embedparams=(1.0, 5.0)):
        super(NL_TSTL_FractalDimensions, self).__init__()
        self.kmin = kmin
        self.kmax = kmax
        self.Nref = Nref
        self.gstart = gstart
        self.gend = gend
        self.past = past
        self.steps = steps
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.kmin is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, )
        elif self.kmax is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin)
        elif self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax)
        elif self.gstart is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax, self.Nref)
        elif self.gend is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax, self.Nref, self.gstart)
        elif self.past is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax,
                                    self.Nref, self.gstart, self.gend)
        elif self.steps is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax,
                                    self.Nref, self.gstart, self.gend, self.past)
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax,
                                    self.Nref, self.gstart, self.gend, self.past, self.steps)
        return eng.run_function(1, 'NL_TSTL_FractalDimensions', x, self.kmin, self.kmax, self.Nref,
                                self.gstart, self.gend, self.past, self.steps, self.embedparams)


class NL_TSTL_GPCorrSum(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses TSTOOL code corrsum (or corrsum2) to compute scaling of the correlation sum for a
    % time-delay reconstructed time series by the Grassberger-Proccacia algorithm
    % using fast nearest neighbor search.
    % 
    % cf. "Characterization of Strange Attractors", P. Grassberger and I. Procaccia,
    % Phys. Rev. Lett. 50(5) 346 (1983)
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, column vector of time-series data
    % 
    % Nref, number of (randomly-chosen) reference points (-1: use all points,
    %       if a decimal, then use this fraction of the time series length)
    %       
    % r, maximum search radius relative to attractor size, 0 < r < 1
    % 
    % thwin, number of samples to exclude before and after each reference index
    %        (~ Theiler window)
    % 
    % nbins, number of partitioned bins
    % 
    % embedparams, embedding parameters to feed BF_embed.m for embedding the
    %               signal in the form {tau,m}
    % 
    % dotwo, if this is set to 1, will use corrsum, if set to 2, will use corrsum2.
    %           For corrsum2, n specifies the number of pairs per bin. Default is 1,
    %           to use corrsum.
    % 
    % 
    %---OUTPUTS: basic statistics on the outputs of corrsum, including iteratively
    % re-weighted least squares linear fits to log-log plots using the robustfit
    % function in Matlab's Statistics Toolbox.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (15,)

    TAGS = ('correlation', 'corrsum', 'corrsum2', 'nonlinear', 'stochastic', 'tstool')

    def __init__(self, Nref=-1.0, r=0.1, thwin=40.0, nbins=20.0, embedparams=('ac', 'cao'), dotwo=2.0):
        super(NL_TSTL_GPCorrSum, self).__init__()
        self.Nref = Nref
        self.r = r
        self.thwin = thwin
        self.nbins = nbins
        self.embedparams = embedparams
        self.dotwo = dotwo

    def _eval_hook(self, eng, x):
        if self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, )
        elif self.r is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref)
        elif self.thwin is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref, self.r)
        elif self.nbins is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref, self.r, self.thwin)
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref, self.r, self.thwin, self.nbins)
        elif self.dotwo is None:
            return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref, self.r, self.thwin,
                                    self.nbins, self.embedparams)
        return eng.run_function(1, 'NL_TSTL_GPCorrSum', x, self.Nref, self.r, self.thwin, self.nbins,
                                self.embedparams, self.dotwo)


class NL_TSTL_LargestLyap(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the largest Lyapunov exponent of a time-delay reconstructed time
    % series using the TSTOOL code 'largelyap'.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    % The algorithm used (using formula (1.5) in Parlitz Nonlinear Time Series
    % Analysis book) is very similar to the Wolf algorithm:
    % "Determining Lyapunov exponents from a time series", A. Wolf et al., Physica D
    % 16(3) 285 (1985)
    % 
    %---INPUTS:
    % 
    % y, the time series to analyze
    % 
    % Nref, number of randomly-chosen reference points (-1 == all)
    % 
    % maxtstep, maximum prediction length (samples)
    % 
    % past, exclude -- Theiler window idea
    % 
    % NNR, number of nearest neighbours
    % 
    % embedparams, input to BF_embed, how to time-delay-embed the time series, in
    %               the form {tau,m}, where string specifiers can indicate standard
    %               methods of determining tau or m.
    % 
    %---OUTPUTS: a range of statistics on the outputs from this function, including
    % a penalized linear regression to the scaling range in an attempt to fit to as
    % much of the range of scales as possible while simultaneously achieving the
    % best possible linear fit.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (29,)

    TAGS = ('largelyap', 'nonlinear', 'stochastic', 'tstool')

    def __init__(self, Nref=0.5, maxtstep=0.1, past=0.01, NNR=3.0, embedparams=('mi', 'cao')):
        super(NL_TSTL_LargestLyap, self).__init__()
        self.Nref = Nref
        self.maxtstep = maxtstep
        self.past = past
        self.NNR = NNR
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_LargestLyap', x, )
        elif self.maxtstep is None:
            return eng.run_function(1, 'NL_TSTL_LargestLyap', x, self.Nref)
        elif self.past is None:
            return eng.run_function(1, 'NL_TSTL_LargestLyap', x, self.Nref, self.maxtstep)
        elif self.NNR is None:
            return eng.run_function(1, 'NL_TSTL_LargestLyap', x, self.Nref, self.maxtstep, self.past)
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_LargestLyap', x, self.Nref, self.maxtstep, self.past, self.NNR)
        return eng.run_function(1, 'NL_TSTL_LargestLyap', x, self.Nref, self.maxtstep, self.past,
                                self.NNR, self.embedparams)


class NL_TSTL_PoincareSection(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Obtains a Poincare section of the time-delay embedded time series, producing a
    % set of vector points projected orthogonal to the tangential vector at the
    % specified index using TSTOOL code 'poincare'. This function then tries to
    % obtain interesting structural measures from this output.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % ref: the reference point. Can be an absolute number (2 takes the second point
    %      in the (embedded) time series) or a string like 'max' or 'min' that takes
    %      the first maximum, ... in the (scalar) time series, ...
    % 
    % embedparams: the usual thing to give BF_embed for the time-delay embedding, as
    %               {tau,m}. A common choice for m is 3 -- i.e., embed in a 3
    %               dimensional space so that the Poincare section is 2-dimensional.
    % 
    % 
    %---OUTPUTS: include statistics on the x- and y- components of these vectors on the
    % Poincare surface, on distances between adjacent points, distances from the
    % mean position, and the entropy of the vector cloud.
    % 
    % Another thing that could be cool to do is to analyze variation in the plots as
    % ref changes... (not done here)
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (50,)

    TAGS = ('nonlinear', 'poincare', 'tstool')

    def __init__(self, ref='max', embedparams=('ac', 3)):
        super(NL_TSTL_PoincareSection, self).__init__()
        self.ref = ref
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.ref is None:
            return eng.run_function(1, 'NL_TSTL_PoincareSection', x, )
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_PoincareSection', x, self.ref)
        return eng.run_function(1, 'NL_TSTL_PoincareSection', x, self.ref, self.embedparams)


class NL_TSTL_ReturnTime(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes a histogram of return times, the time taken for the time series to
    % return to a similar location in phase space for a given reference point using
    % the code return_time from TSTOOL.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    % Strong peaks in the histogram are indicative of periodicities in the data.
    % 
    %---INPUTS:
    % 
    % y, scalar time series as a column vector
    % NNR, number of nearest neighbours
    % maxT, maximum return time to consider
    % past, Theiler window
    % Nref, number of reference indicies
    % embedparams, to feed into BF_embed
    % 
    %---OUTPUTS: include basic measures from the histogram, including the occurrence of
    % peaks, spread, proportion of zeros, and the distributional entropy.
    % 
    %---HISTORY:
    % Ben Fulcher, 12/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (19,)

    TAGS = ('nonlinear', 'returntime', 'tstool')

    def __init__(self, NNR=0.05, maxT=1.0, past=0.05, Nref=-1.0, embedparams=(1.0, 3.0)):
        super(NL_TSTL_ReturnTime, self).__init__()
        self.NNR = NNR
        self.maxT = maxT
        self.past = past
        self.Nref = Nref
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.NNR is None:
            return eng.run_function(1, 'NL_TSTL_ReturnTime', x, )
        elif self.maxT is None:
            return eng.run_function(1, 'NL_TSTL_ReturnTime', x, self.NNR)
        elif self.past is None:
            return eng.run_function(1, 'NL_TSTL_ReturnTime', x, self.NNR, self.maxT)
        elif self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_ReturnTime', x, self.NNR, self.maxT, self.past)
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_ReturnTime', x, self.NNR, self.maxT, self.past, self.Nref)
        return eng.run_function(1, 'NL_TSTL_ReturnTime', x, self.NNR, self.maxT, self.past,
                                self.Nref, self.embedparams)


class NL_TSTL_TakensEstimator(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements the Taken's estimator for correlation dimension using the
    % TSTOOL code takens_estimator.
    %
    % cf. "Detecting strange attractors in turbulence", F. Takens.
    % Lect. Notes Math. 898 p366 (1981)
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, the input time series
    % Nref, the number of reference points (can be -1 to use all points)
    % rad, the maximum search radius (as a proportion of the attractor size)
    % past, the Theiler window
    % embedparams, the embedding parameters for BF_embed, in the form {tau,m}
    % 
    %---OUTPUT: the Taken's estimator of the correlation dimension, d2.
    % 
    %---HISTORY:
    % Ben Fulcher, 14/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('crptool', 'dimension', 'nonlinear', 'scaling', 'stochastic', 'takens', 'tstool')

    def __init__(self, Nref=-1.0, rad=0.05, past=0.05, embedparams=('ac', 3)):
        super(NL_TSTL_TakensEstimator, self).__init__()
        self.Nref = Nref
        self.rad = rad
        self.past = past
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_TakensEstimator', x, )
        elif self.rad is None:
            return eng.run_function(1, 'NL_TSTL_TakensEstimator', x, self.Nref)
        elif self.past is None:
            return eng.run_function(1, 'NL_TSTL_TakensEstimator', x, self.Nref, self.rad)
        elif self.embedparams is None:
            return eng.run_function(1, 'NL_TSTL_TakensEstimator', x, self.Nref, self.rad, self.past)
        return eng.run_function(1, 'NL_TSTL_TakensEstimator', x, self.Nref, self.rad, self.past, self.embedparams)


class NL_TSTL_acp(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements the TSTOOL routine acp using a time lag, tau, a Theiler window,
    % past, maximum delay, maxdelay, maximum embedding dimension, maxdim, and number
    % of reference points, Nref.
    % 
    % The documentation isn't crystal clear, but I think this function has to do
    % with cross-prediction.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    %
    %---INPUTS:
    % 
    % y, time series
    % 
    % tau, delay time
    % 
    % past, number of samples to exclude before and after each index (to avoid
    %               correlation effects ~ Theiler window)
    % 
    % maxdelay, maximal delay (<< length(y))
    % 
    % maxdim, maximal dimension to use
    % 
    % Nref, number of reference points
    % 
    %---OUTPUTS: statistics summarizing the output of the routine.
    % 
    % May in future want to also make outputs normalized by first value; so get
    % metrics on both absolute values at each dimension but also some
    % indication of the shape
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (52,)

    TAGS = ('acp', 'correlation', 'nonlinear', 'slow', 'stochastic', 'tstool')

    def __init__(self, tau='mi', past=1.0, maxdelay=(), maxdim=10.0, Nref=()):
        super(NL_TSTL_acp, self).__init__()
        self.tau = tau
        self.past = past
        self.maxdelay = maxdelay
        self.maxdim = maxdim
        self.Nref = Nref

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'NL_TSTL_acp', x, )
        elif self.past is None:
            return eng.run_function(1, 'NL_TSTL_acp', x, self.tau)
        elif self.maxdelay is None:
            return eng.run_function(1, 'NL_TSTL_acp', x, self.tau, self.past)
        elif self.maxdim is None:
            return eng.run_function(1, 'NL_TSTL_acp', x, self.tau, self.past, self.maxdelay)
        elif self.Nref is None:
            return eng.run_function(1, 'NL_TSTL_acp', x, self.tau, self.past, self.maxdelay, self.maxdim)
        return eng.run_function(1, 'NL_TSTL_acp', x, self.tau, self.past, self.maxdelay, self.maxdim, self.Nref)


class NL_TSTL_dimensions(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes the box counting, information, and correlation dimension of a
    % time-delay embedded time series using the TSTOOL code 'dimensions'.
    % This function contains extensive code for estimating the best scaling range to
    % estimate the dimension using a penalized regression procedure.
    % 
    % TSTOOL, http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % 
    % y, column vector of time series data
    % 
    % nbins, maximum number of partitions per axis.
    % 
    % embedParams, embedding parameters to feed BF_embed.m for embedding the
    %              signal in the form {tau,m}
    % 
    % 
    %---OUTPUTS:
    % A range of statistics are returned about how each dimension estimate changes
    % with m, the scaling range in r, and the embedding dimension at which the best
    % fit is obtained.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (198,)

    TAGS = ('dimension', 'nonlinear', 'scaling', 'stochastic', 'tstool')

    def __init__(self, nbins=50.0, embedParams=('ac', 'cao')):
        super(NL_TSTL_dimensions, self).__init__()
        self.nbins = nbins
        self.embedParams = embedParams

    def _eval_hook(self, eng, x):
        if self.nbins is None:
            return eng.run_function(1, 'NL_TSTL_dimensions', x, )
        elif self.embedParams is None:
            return eng.run_function(1, 'NL_TSTL_dimensions', x, self.nbins)
        return eng.run_function(1, 'NL_TSTL_dimensions', x, self.nbins, self.embedParams)


class NL_crptool_fnn(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Computes and analyzes the false-nearest neighbours statistic.
    % 
    % Computation is done by referencing N. Marwan's code from the CRP Toolbox:
    % http://tocsy.pik-potsdam.de/CRPtoolbox/
    % 
    %---INPUTS:
    % y, the input time series
    % maxm, the maximum embedding dimension to consider
    % r, the threshold; neighbourhood criterion
    % taum, the method of determining the time delay, 'corr' for first zero-crossing
    %       of autocorrelation function, or 'mi' for the first minimum of the mutual
    %       information
    % 
    % th [opt], returns the first time the number of false nearest neighbours drops
    %           under this threshold
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (15,)

    TAGS = ('crptool', 'dimension', 'nonlinear', 'stochastic')

    def __init__(self, maxm=10.0, r=2.0, taum='ac', th=None):
        super(NL_crptool_fnn, self).__init__()
        self.maxm = maxm
        self.r = r
        self.taum = taum
        self.th = th

    def _eval_hook(self, eng, x):
        if self.maxm is None:
            return eng.run_function(1, 'NL_crptool_fnn', x, )
        elif self.r is None:
            return eng.run_function(1, 'NL_crptool_fnn', x, self.maxm)
        elif self.taum is None:
            return eng.run_function(1, 'NL_crptool_fnn', x, self.maxm, self.r)
        elif self.th is None:
            return eng.run_function(1, 'NL_crptool_fnn', x, self.maxm, self.r, self.taum)
        return eng.run_function(1, 'NL_crptool_fnn', x, self.maxm, self.r, self.taum, self.th)


class NL_embed_PCA(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Reconstructs the time series as a time-delay embedding, and performs Principal
    % Components Analysis on the result using princomp code from
    % Matlab's Bioinformatics Toolbox.
    % 
    % This technique is known as singular spectrum analysis
    % 
    % "Extracting qualitative dynamics from experimental data"
    % D. S. Broomhead and G. P. King, Physica D 20(2-3) 217 (1986)
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % tau, the time-delay, can be an integer or 'ac', or 'mi' for first
    %               zero-crossing of the autocorrelation function or first minimum
    %               of the automutual information, respectively
    %               
    % m, the embedding dimension
    % 
    % OUTPUTS: Various statistics summarizing the obtained eigenvalue distribution.
    % 
    % The suggestion to implement this idea was provided by Siddarth Arora.
    % (Siddharth Arora, <arora@maths.ox.ac.uk>)
    % 
    %---HISTORY:
    % Ben Fulcher, 25/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (9,)

    TAGS = ('pca', 'tdembedding')

    def __init__(self, tau='mi', m=10.0):
        super(NL_embed_PCA, self).__init__()
        self.tau = tau
        self.m = m

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'NL_embed_PCA', x, )
        elif self.m is None:
            return eng.run_function(1, 'NL_embed_PCA', x, self.tau)
        return eng.run_function(1, 'NL_embed_PCA', x, self.tau, self.m)


class NW_VisibilityGraph(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Constructs a visibility graph of the time series and returns various
    % statistics on the properties of the resulting network.
    % 
    % cf.: "From time series to complex networks: The visibility graph"
    % Lacasa, Lucas and Luque, Bartolo and Ballesteros, Fernando and Luque, Jordi
    % and Nuno, Juan Carlos P. Natl. Acad. Sci. USA. 105(13) 4972 (2008)
    % 
    % "Horizontal visibility graphs: Exact results for random time series"
    % Luque, B. and Lacasa, L. and Ballesteros, F. and Luque, J.
    % Phys. Rev. E. 80(4) 046103 (2009)
    % 
    % The normal visibility graph may not be implemented correctly, we focused only
    % on the horizontal visibility graph.
    % 
    %---INPUTS:
    % y, the time series (a column vector)
    % 
    % meth, the method for constructing:
    % 			(i) 'norm': the normal visibility definition
    % 			(ii) 'horiz': uses only horizonatal lines to link nodes/datums
    %             
    % maxL, the maximum number of samples to consider. Due to memory constraints,
    %               only the first maxL (6000 by default) points of time series are
    %               analyzed. Longer time series are reduced to their first maxL
    %               samples.
    % 
    % 
    %---OUTPUTS: statistics on the degree distribution, including the mode, mean,
    % spread, histogram entropy, and fits to gaussian, exponential, and powerlaw
    % distributions.
    % 
    %---HISTORY:
    % Ben Fulcher, October 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (47,)

    TAGS = ('lengthdep', 'network', 'visibilitygraph')

    def __init__(self, meth='horiz', maxL=None):
        super(NW_VisibilityGraph, self).__init__()
        self.meth = meth
        self.maxL = maxL

    def _eval_hook(self, eng, x):
        if self.meth is None:
            return eng.run_function(1, 'NW_VisibilityGraph', x, )
        elif self.maxL is None:
            return eng.run_function(1, 'NW_VisibilityGraph', x, self.meth)
        return eng.run_function(1, 'NW_VisibilityGraph', x, self.meth, self.maxL)


class PD_PeriodicityWang(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements an idea based on the periodicity extraction measure proposed in:
    % 
    % "Structure-based Statistical Features and Multivariate Time Series Clustering"
    % Wang, X. and Wirth, A. and Wang, L.
    % Seventh IEEE International Conference on Data Mining, 351--360 (2007)
    % DOI: 10.1109/ICDM.2007.103
    %
    % This function detrends the time series using a single-knot cubic regression
    % spline, and then computes autocorrelations up to one third of the length of
    % the time series. The frequency is the first peak in the autocorrelation
    % function satisfying a set of conditions.
    % 
    %---INPUTS:
    % y, the input time series.
    % 
    % The single threshold of 0.01 was considered in the original paper, this code
    % uses a range of thresholds: 0, 0.01, 0.1, 0.2, 1\sqrt{N}, 5\sqrt{N}, and
    % 10\sqrt{N}, where N is the length of the time series.
    % 
    %---HISTORY:
    % Ben Fulcher, 9/7/09
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (7,)

    TAGS = ('periodicity', 'spline')

    def __init__(self):
        super(PD_PeriodicityWang, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'PD_PeriodicityWang', x, )


class PH_ForcePotential(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Couples the values of the time series to a given dynamical system. The input
    % time series forces a particle in the given potential well.
    % 
    % The time series contributes to a forcing term on a simulated particle in a:
    % 
    % (i) Quartic double-well potential with potential energy V(x) = x^4/4 - alpha^2
    %           x^2/2, or a force F(x) = -x^3 + alpha^2 x
    % 
    % (ii) Sinusoidal potential with V(x) = -cos(x/alpha), or F(x) = sin(x/alpha)/alpha
    %
    %---INPUTS:
    % y, the input time series
    % 
    % whatpot, the potential function to simulate:
    %               (i) 'dblwell' (a double well potential function)
    %               (ii) 'sine' (a sinusoidal potential function)
    % 
    % params, the parameters for simulation, should be in the form:
    %                   params = [alpha, kappa, deltat]
    %                   
    %           (i) The double-well potential has three parameters:
    %               * alpha controls the relative positions of the wells,
    %               * kappa is the coefficient of friction,
    %               * deltat sets the time step for the simulation.
    %           
    %           (ii) The sinusoidal potential also has three parameters:
    %               * alpha controls the period of oscillations in the potential
    %               * kappa is the coefficient of friction,
    %               * deltat sets the time step for the simulation.
    % 
    %---OUTPUTS: statistics summarizing the trajectory of the simulated particle,
    % including its mean, the range, proportion positive, proportion of times it
    % crosses zero, its autocorrelation, final position, and standard deviation.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (13, 11)

    TAGS = ('dblwell', 'dynsys', 'sine')

    def __init__(self, whatpot='dblwell', params=(1.0, 0.20000000000000001, 0.10000000000000001)):
        super(PH_ForcePotential, self).__init__()
        self.whatpot = whatpot
        self.params = params

    def _eval_hook(self, eng, x):
        if self.whatpot is None:
            return eng.run_function(1, 'PH_ForcePotential', x, )
        elif self.params is None:
            return eng.run_function(1, 'PH_ForcePotential', x, self.whatpot)
        return eng.run_function(1, 'PH_ForcePotential', x, self.whatpot, self.params)


class PH_Walker(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This operation simulates a hypothetical particle (or 'walker'), that moves in
    % the time domain in response to values of the time series at each point.
    % 
    % Outputs from this operation are summaries of the walker's motion, and
    % comparisons of it to the original time series.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % walkerrule, the kinematic rule by which the walker moves in response to the
    %             time series over time:
    %             
    %             (i) 'prop': the walker narrows the gap between its value and that
    %                         of the time series by a given proportion p.
    %                         wparam = p;
    %                         
    %             (ii) 'biasprop': the walker is biased to move more in one
    %                          direction; when it is being pushed up by the time
    %                          series, it narrows the gap by a proportion p_{up},
    %                          and when it is being pushed down by the time series,
    %                          it narrows the gap by a (potentially different)
    %                          proportion p_{down}. wparam = [pup,pdown].
    %                          
    %             (iii) 'momentum': the walker moves as if it has mass m and inertia
    %                          from the previous time step and the time series acts
    %                          as a force altering its motion in a classical
    %                          Newtonian dynamics framework. [wparam = m], the mass.
    %                          
    %              (iv) 'runningvar': the walker moves with inertia as above, but
    %                          its values are also adjusted so as to match the local
    %                          variance of time series by a multiplicative factor.
    %                          wparam = [m,wl], where m is the inertial mass and wl
    %                          is the window length.
    % 
    % wparam, the parameters for the specified walkerrule, explained above.
    % 
    %---OUTPUTS: include the mean, spread, maximum, minimum, and autocorrelation of the
    % walker's trajectory, the number of crossings between the walker and the
    % original time series, the ratio or difference of some basic summary statistics
    % between the original time series and the walker, an Ansari-Bradley test
    % comparing the distributions of the walker and original time series, and
    % various statistics summarizing properties of the residuals between the
    % walker's trajectory and the original time series.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (21,)

    TAGS = ('trend',)

    def __init__(self, walkerrule='prop', wparam=0.9):
        super(PH_Walker, self).__init__()
        self.walkerrule = walkerrule
        self.wparam = wparam

    def _eval_hook(self, eng, x):
        if self.walkerrule is None:
            return eng.run_function(1, 'PH_Walker', x, )
        elif self.wparam is None:
            return eng.run_function(1, 'PH_Walker', x, self.walkerrule)
        return eng.run_function(1, 'PH_Walker', x, self.walkerrule, self.wparam)


class PP_Compare(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Applies a given pre-processing transformation to the time series, and returns
    % statistics on how various time-series properties change as a result.
    % 
    % Inputs are structured in a clunky way, unfortunately...
    % 
    %---INPUTS:
    % y, the input time series
    % detrndmeth, the method to use for detrending:
    %      (i) 'poly': polynomial detrendings, both linear and quadratic. Can
    %                  be of the following forms:
    %            (a) polynomial of given order: 'poly1', 'poly2', 'poly3',
    %                'poly4', 'poly5', 'poly6', 'poly7', 'poly8', 'poly9'
    %            (b) fit best polynomial: 'polybest' determines 'best' by
    %                            various tests (e.g., whiteness of residuals,
    %                            etc.)
    %            (c) 'fitstrong' only fits if a 'strong' trend.
    %      (ii) 'sin': sinusoidal detrending with either one or two frequency
    %                components,
    %            (a) fit a sine series of a given order
    %               Fits a form like: a1*sin(b1*x+c1) + a2*sin(b2*x+c2) + ...
    %               Additional number determines how many terms to include in the
    %               series: 'sin1', 'sin2', 'sin3', 'sin4', 'sin5', 'sin6', 'sin7',
    %               'sin8'
    %            (b) 'sin_st1': fit only if a strong trend (i.e., if the amplitudes
    %                                           are above a given threshold)
    %      (iii) 'spline': removes a least squares spline using Matlab's
    %                      Spline Toolbox function spap2
    %                      Input of the form 'spline<nknots><interpolant_order>'
    %                      e.g., 'spline45' uses four knots and 5th order
    %                      interpolants (Implements a least squares spline via the
    %                      spline toolbox function spap2)
    %      (iv) 'diff': takes incremental differences of the time series. Of form
    %                 'diff<ndiff>' where ndiff is the number of differencings to
    %                 perform. e.g., 'diff3' performs three recursive differences
    %      (v) 'medianf': a running median filter using a given window lengths
    %                   Of form 'medianf<n>' where n is the window length.
    %                   e.g., 'medianf3' takes a running median using the median of
    %                     every 3 consecutive values as a point in the filtered
    %                     time series. Uses the Signal Processing Toolbox
    %                     function medfilt1
    %      (vi) 'rav': running mean filter of a given window length.
    %                  Uses Matlab's filter function to perform a running
    %                  average of order n. Of form 'rav<n>' where n is the order of
    %                  the running average.
    %      (vii) 'resample': resamples the data by a given ratio using the resample
    %                        function in Matlab.
    %                        Of form 'resample_<p>_<q>', where the ratio p/q is the
    %                        new sampling rate e.g., 'resample_1_2' will downsample
    %                        the signal by one half e.g., resample_10_1' will
    %                        resample the signal to 10 times its original length
    %      (viii) 'logr': takes log returns of the data. Only valid for positive
    %                       data, else returns a NaN.
    %      (ix) 'boxcox': makes a Box-Cox transformation of the data. Only valid for
    %                     positive only data; otherwise returns a NaN.
    % 
    % If multiple detrending methods are specified, they should be in a cell of
    % strings; the methods will be executed in order, e.g., {'poly1','sin1'} does a
    % linear polynomial then a simple one-frequency seasonal detrend (in that order)
    % 
    %---OUTPUTS: include comparisons of stationarity and distributional measures
    % between the original and transformed time series.
    % 
    %---HISTORY:
    % Ben Fulcher, 9/7/09
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (40,)

    TAGS = ('locdep', 'preprocessing', 'raw', 'spline')

    def __init__(self, detrndmeth='medianf4'):
        super(PP_Compare, self).__init__()
        self.detrndmeth = detrndmeth

    def _eval_hook(self, eng, x):
        if self.detrndmeth is None:
            return eng.run_function(1, 'PP_Compare', x, )
        return eng.run_function(1, 'PP_Compare', x, self.detrndmeth)


class PP_Iterate(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Iteratively applies a transformation to the time series and measures how
    % various properties of is change as the transformation is iteratively applied
    % to it.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % dtMeth, the detrending method to apply:
    %           (i) 'spline' removes a spine fit,
    %           (ii) 'diff' takes incremental differences,
    %           (iii) 'medianf' applies a median filter,
    %           (iv) 'rav' applies a running mean filter,
    %           (v) 'resampleup' progressively upsamples the time series,
    %           (vi) 'resampledown' progressively downsamples the time series.
    %
    %---HISTORY:
    % Ben Fulcher, 10/7/09
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (40,)

    TAGS = ('locdep', 'preprocessing', 'raw')

    def __init__(self, dtMeth='diff'):
        super(PP_Iterate, self).__init__()
        self.dtMeth = dtMeth

    def _eval_hook(self, eng, x):
        if self.dtMeth is None:
            return eng.run_function(1, 'PP_Iterate', x, )
        return eng.run_function(1, 'PP_Iterate', x, self.dtMeth)


class PP_ModelFit(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Carries out a variety of preprocessings to look at improvement of fit to
    % an AR model.
    % 
    % After performing the range of transformations to the time series, returns the
    % in-sample root-mean-square (RMS) prediction errors for an AR model on each
    % transformed time series as a ratio of the RMS prediction error of the original
    % time series.
    % 
    % PP_PreProcess.m is used to perform the preprocessings
    % 
    % The AR model is fitted using the function ar and pe from Matlab's System
    % Identification Toolbox
    % 
    % Transformations performed include:
    % (i) incremental differencing,
    % (ii) filtering of the power spectral density function,
    % (iii) removal of piece-wise polynomial trends, and
    % (iv) rank mapping the values of the time series to a Gaussian distribution.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % model, the time-series model to fit to the transformed time series (currently
    %           'ar' is the only option)
    %           
    % order, the order of the AR model to fit to the data
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (16,)

    TAGS = ('preprocessing', 'stochastic', 'trend')

    def __init__(self, model='ar', order=2.0):
        super(PP_ModelFit, self).__init__()
        self.model = model
        self.order = order

    def _eval_hook(self, eng, x):
        if self.model is None:
            return eng.run_function(1, 'PP_ModelFit', x, )
        elif self.order is None:
            return eng.run_function(1, 'PP_ModelFit', x, self.model)
        return eng.run_function(1, 'PP_ModelFit', x, self.model, self.order)


class SB_BinaryStats(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns statistics on a binary symbolization of the time series (to a symbolic
    % string of 0s and 1s).
    % 
    % Provides information about the coarse-grained behavior of the time series
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % binarymeth, the symbolization rule:
    %         (i) 'diff': by whether incremental differences of the time series are
    %                      positive (1), or negative (0),
    %          (ii) 'mean': by whether each point is above (1) or below the mean (0)
    %          (iii) 'iqr': by whether the time series is within the interquartile range
    %                      (1), or not (0).
    % 
    %---OUTPUTS: include the Shannon entropy of the string, the longest stretches of 0s
    % or 1s, the mean length of consecutive 0s or 1s, and the spread of consecutive
    % strings of 0s or 1s.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (16,)

    TAGS = ('distribution', 'stationarity')

    def __init__(self, binarymeth='diff'):
        super(SB_BinaryStats, self).__init__()
        self.binarymeth = binarymeth

    def _eval_hook(self, eng, x):
        if self.binarymeth is None:
            return eng.run_function(1, 'SB_BinaryStats', x, )
        return eng.run_function(1, 'SB_BinaryStats', x, self.binarymeth)


class SB_BinaryStretch(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the longest stretch of consecutive zeros or ones in a symbolized time
    % series as a proportion of the time-series length.
    % 
    % The time series is symbolized to a binary string by whether it's above (1) or
    % below (0) its mean.
    % 
    % It doesn't actually measure this correctly, due to an error in the code, but
    % it's still kind of an interesting operation...?!
    % 
    %---INPUTS:
    % x, the input time series
    % stretchwhat, (i) 'lseq1', measures something related to consecutive 1s
    %              (ii) 'lseq0', measures something related to consecutive 0s
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('binary',)

    def __init__(self, stretchwhat='lseq0'):
        super(SB_BinaryStretch, self).__init__()
        self.stretchwhat = stretchwhat

    def _eval_hook(self, eng, x):
        if self.stretchwhat is None:
            return eng.run_function(1, 'SB_BinaryStretch', x, )
        return eng.run_function(1, 'SB_BinaryStretch', x, self.stretchwhat)


class SB_CoarseGrain(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Coarse-grains the continuous time series to a discrete alphabet
    % by a given method.
    % 
    %---INPUTS:
    % howtocg, the method of coarse-graining
    % 
    % ng, either specifies the size of the alphabet for 'quantile' and 'updown'
    %       or sets the timedelay for the embedding subroutines
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self, howtocg=None, ng=None):
        super(SB_CoarseGrain, self).__init__()
        self.howtocg = howtocg
        self.ng = ng

    def _eval_hook(self, eng, x):
        if self.howtocg is None:
            return eng.run_function(1, 'SB_CoarseGrain', x, )
        elif self.ng is None:
            return eng.run_function(1, 'SB_CoarseGrain', x, self.howtocg)
        return eng.run_function(1, 'SB_CoarseGrain', x, self.howtocg, self.ng)


class SB_MotifThree(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % As for SB_MotifTwo, but using an alphabet of three letters, i.e., looks for
    % motifs in a course-graining of the time series to an alphabet of three letters
    % 
    %---INPUTS:
    % y, time series to analyze
    % trit, the coarse-graining method to use:
    %       (i) 'quantile': equiprobable alphabet by time-series value
    %       (ii) 'diffquant': equiprobably alphabet by time-series increments
    % 
    %---OUTPUTS:
    % Statistics on words of length 1, 2, 3, and 4.
    % 
    %---HISTORY:
    % This code was laboriously written by Ben Fulcher, 2009.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (120,)

    TAGS = ('motifs',)

    def __init__(self, trit='diffquant'):
        super(SB_MotifThree, self).__init__()
        self.trit = trit

    def _eval_hook(self, eng, x):
        if self.trit is None:
            return eng.run_function(1, 'SB_MotifThree', x, )
        return eng.run_function(1, 'SB_MotifThree', x, self.trit)


class SB_MotifTwo(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Looks at local motifs in a binary symbolization of the time series, which is
    % performed by:
    % 
    %---INPUTS:
    %
    % y, the input time series
    % 
    % bint, the binary transformation method:
    %       (i) 'diff': incremental time-series increases are encoded as 1, and
    %                   decreases as 0,
    %       (ii) 'mean': time-series values above its mean are given 1, and those
    %                    below the mean are 0,
    %       (iii) 'median': time-series values above the median are given 1, and
    %       those below the median 0.
    % 
    %---OUTPUTS:
    % Probabilities of words in the binary alphabet of lengths 1, 2, 3, and 4, and
    % their entropies.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (34,)

    TAGS = ('motifs',)

    def __init__(self, bint='mean'):
        super(SB_MotifTwo, self).__init__()
        self.bint = bint

    def _eval_hook(self, eng, x):
        if self.bint is None:
            return eng.run_function(1, 'SB_MotifTwo', x, )
        return eng.run_function(1, 'SB_MotifTwo', x, self.bint)


class SB_TransitionMatrix(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the transition probabilities between different states of the time
    % series given a method to symbolize or coarse-grain the time series.
    % 
    % The input time series is transformed into a symbolic string using an
    % equiprobable alphabet of numGroups letters. The transition probabilities are
    % calculated at a lag tau.
    % 
    %---INPUTS:
    % y, the input time series
    %
    % howtocg, the method of discretization (currently 'quantile' is the only
    %           option; could incorporate SB_CoarseGrain for more options in future)
    %
    % numGroups: number of groups in the course-graining
    %
    % tau: analyze transition matricies corresponding to this lag. We
    %      could either downsample the time series at this lag and then do the
    %      discretization as normal, or do the discretization and then just
    %      look at this dicrete lag. Here we do the former. Can also set tau to 'ac'
    %      to set tau to the first zero-crossing of the autocorrelation function.
    % 
    %---OUTPUTS: include the transition probabilities themselves, as well as the trace
    % of the transition matrix, measures of asymmetry, and eigenvalues of the
    % transition matrix.
    % 
    %---HISTORY:
    % Ben Fulcher, August 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (23, 17, 19, 18)

    TAGS = ('transitionmat',)

    def __init__(self, howtocg='quantile', numGroups=2.0, tau=1.0):
        super(SB_TransitionMatrix, self).__init__()
        self.howtocg = howtocg
        self.numGroups = numGroups
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.howtocg is None:
            return eng.run_function(1, 'SB_TransitionMatrix', x, )
        elif self.numGroups is None:
            return eng.run_function(1, 'SB_TransitionMatrix', x, self.howtocg)
        elif self.tau is None:
            return eng.run_function(1, 'SB_TransitionMatrix', x, self.howtocg, self.numGroups)
        return eng.run_function(1, 'SB_TransitionMatrix', x, self.howtocg, self.numGroups, self.tau)


class SB_TransitionpAlphabet(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates the transition probabilities and measures how they change as the
    % size of the alphabet increases.
    % 
    % Discretization is done by quantile separation.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % ng, the number of groups in the coarse-graining (scalar for constant, or a
    %       vector of ng to compare across this range)
    % 
    % tau: the time-delay; transition matricies corresponding to this time-delay. We
    %      can either downsample the time series at this lag and then do the
    %      discretization as normal, or do the discretization and then just
    %      look at this dicrete lag. Here we do the former. (scalar for
    %      constant tau, vector for range to vary across)
    % 
    %---OUTPUTS: include the decay rate of the sum, mean, and maximum of diagonal
    % elements of the transition matrices, changes in symmetry, and the eigenvalues
    % of the transition matrix.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (45,)

    TAGS = ('transitionmat',)

    def __init__(self, ng=MatlabSequence('2:40'), tau=1.0):
        super(SB_TransitionpAlphabet, self).__init__()
        self.ng = ng
        self.tau = tau

    def _eval_hook(self, eng, x):
        if self.ng is None:
            return eng.run_function(1, 'SB_TransitionpAlphabet', x, )
        elif self.tau is None:
            return eng.run_function(1, 'SB_TransitionpAlphabet', x, self.ng)
        return eng.run_function(1, 'SB_TransitionpAlphabet', x, self.ng, self.tau)


class SC_FluctAnal(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements fluctuation analysis by a variety of methods.
    % 
    % Much of our implementation is based on the well-explained discussion of
    % scaling methods in:
    % "Power spectrum and detrended fluctuation analysis: Application to daily
    % temperatures" P. Talkner and R. O. Weber, Phys. Rev. E 62(1) 150 (2000)
    % 
    % The main difference between algorithms for estimating scaling exponents amount to
    % differences in how fluctuations, F, are quantified in time-series segments.
    % Many alternatives are implemented in this function.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % q, the parameter in the fluctuation function q = 2 (usual) gives RMS fluctuations.
    % 
    % wtf, (what to fluctuate)
    %       (i) 'endptdiff', calculates the differences in end points in each segment
    %       (ii) 'range' calculates the range in each segment
    %       (iii) 'std' takes the standard deviation in each segment
    %       
    %           cf. "Evaluating scaled windowed variance methods for estimating the
    %               Hurst coefficient of time series", M. J. Cannon et al. Physica A
    %               241(3-4) 606 (1997)
    %       
    %       (iv) 'iqr' takes the interquartile range in each segment
    %       (v) 'dfa' removes a polynomial trend of order k in each segment,
    %       (vi) 'rsrange' returns the range after removing a straight line fit
    %       
    %           cf. "Analyzing exact fractal time series: evaluating dispersional
    %           analysis and rescaled range methods",  D. C. Caccia et al., Physica
    %           A 246(3-4) 609 (1997)
    %       
    %       (vii) 'rsrangefit' fits a polynomial of order k and then returns the
    %           range. The parameter q controls the order of fluctuations, for which
    %           we mostly use the standard choice, q = 2, corresponding to root mean
    %           square fluctuations.
    %           An optional input parameter to this operation is a timelag for
    %           computing the cumulative sum (or integrated profile), as suggested
    %           by: "Using detrended fluctuation analysis for lagged correlation
    %           analysis of nonstationary signals" J. Alvarez-Ramirez et al. Phys.
    %           Rev. E 79(5) 057202 (2009)
    % 
    % taustep, increments in tau for linear range (i.e., if loginc = 0), or number of tau
    %           steps in logarithmic range if login = 1
    %           The spacing of time scales, tau, is commonly logarithmic through a range from
    %           5 samples to a quarter of the length of the time series, as suggested in
    %           "Statistical properties of DNA sequences", C.-K. Peng et al. Physica A
    %           221(1-3) 180 (1995)
    %           
    %           Max A. Little's fractal paper used L = 4 to L = N/2:
    %           "Exploiting Nonlinear Recurrence and Fractal Scaling Properties for Voice Disorder Detection"
    %           M. A. Little et al. Biomed. Eng. Online 6(1) 23 (2007)
    %           
    % k, polynomial order of detrending for 'dfa', 'rsrangefit'
    % 
    % lag, optional time-lag, as in Alvarez-Ramirez (see (vii) above)
    % 
    % loginc, whether to use logarithmic increments in tau (it should be logarithmic).
    % 
    %---OUTPUTS: include statistics of fitting a linear function to a plot of log(F) as
    % a function of log(tau), and for fitting two straight lines to the same data,
    % choosing the split point at tau = tau_{split} as that which minimizes the
    % combined fitting errors.
    % 
    % This function can also be applied to the absolute deviations of the time
    % series from its mean, and also for just the sign of deviations from the mean
    % (i.e., converting the time series into a series of +1, when the time series is
    % above its mean, and -1 when the time series is below its mean).
    % 
    % All results are obtained with both linearly, and logarithmically-spaced time
    % scales tau.
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (24,)

    TAGS = ('dfa', 'fa', 'lengthdep', 'lini', 'rsrange', 'scaling')

    def __init__(self, q=2.0, wtf='dfa', taustep=2.0, k=2.0, lag=(), loginc=0.0):
        super(SC_FluctAnal, self).__init__()
        self.q = q
        self.wtf = wtf
        self.taustep = taustep
        self.k = k
        self.lag = lag
        self.loginc = loginc

    def _eval_hook(self, eng, x):
        if self.q is None:
            return eng.run_function(1, 'SC_FluctAnal', x, )
        elif self.wtf is None:
            return eng.run_function(1, 'SC_FluctAnal', x, self.q)
        elif self.taustep is None:
            return eng.run_function(1, 'SC_FluctAnal', x, self.q, self.wtf)
        elif self.k is None:
            return eng.run_function(1, 'SC_FluctAnal', x, self.q, self.wtf, self.taustep)
        elif self.lag is None:
            return eng.run_function(1, 'SC_FluctAnal', x, self.q, self.wtf, self.taustep, self.k)
        elif self.loginc is None:
            return eng.run_function(1, 'SC_FluctAnal', x, self.q, self.wtf, self.taustep, self.k, self.lag)
        return eng.run_function(1, 'SC_FluctAnal', x, self.q, self.wtf, self.taustep, self.k, self.lag, self.loginc)


class SC_fastdfa(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the scaling exponent of the time series using a fast implementation
    % of detrended fluctuation analysis (DFA).
    % 
    % The original fastdfa code is by Max A. Little and publicly-available at
    % http://www.maxlittle.net/software/index.php
    %
    %---INPUT:
    % y, the input time series, is fed straight into the fastdfa script.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('dfa', 'mex', 'scaling')

    def __init__(self):
        super(SC_fastdfa, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'SC_fastdfa', x, )


class SD_MakeSurrogates(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Generates surrogate time series given a method (surrogates), number of
    % surrogates (nsurrs), and any extra parameters (extrap)
    % 
    % Method described relatively clearly in Guarin Lopez et al. (arXiv, 2010)
    % Used bits of aaft code that references (and presumably was obtained from)
    % "ìSurrogate data test for nonlinearity including monotonic
    % transformations", D. Kugiumtzis, Phys. Rev. E, vol. 62, no. 1, 2000.
    % 
    % Note that many other surrogate data methods exist that could later be
    % implemented, cf. references in "Improvements to surrogate data methods for
    % nonstationary time series", J. H. Lucio et al., Phys. Rev. E 85, 056202 (2012)
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % surrmethod, the method for generating surrogates:
    %             (i) 'RP' -- random phase surrogates
    %             (ii) 'AAFT' -- amplitude adjusted Fourier transform
    %             (iii) 'TFT' -- truncated Fourier transform
    % 
    % nsurrs, the number of surrogates to generate
    % 
    % extrap, extra parameters required by the selected surrogate generation method
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self, surrmethod=None, nsurrs=None, extrap=None):
        super(SD_MakeSurrogates, self).__init__()
        self.surrmethod = surrmethod
        self.nsurrs = nsurrs
        self.extrap = extrap

    def _eval_hook(self, eng, x):
        if self.surrmethod is None:
            return eng.run_function(1, 'SD_MakeSurrogates', x, )
        elif self.nsurrs is None:
            return eng.run_function(1, 'SD_MakeSurrogates', x, self.surrmethod)
        elif self.extrap is None:
            return eng.run_function(1, 'SD_MakeSurrogates', x, self.surrmethod, self.nsurrs)
        return eng.run_function(1, 'SD_MakeSurrogates', x, self.surrmethod, self.nsurrs, self.extrap)


class SD_SurrogateTest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyzes the test statistics obtained from surrogate time series compared to
    % those measured from the given time series.
    % 
    % This code was based on information found in:
    % "Surrogate data test for nonlinearity including nonmonotonic transforms"
    % D. Kugiumtzis Phys. Rev. E 62(1) R25 (2000)
    % 
    % The generation of surrogates is done by the periphery function,
    % SD_MakeSurrogates
    % 
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % surrmeth, the method for generating surrogate time series:
    %       (i) 'RP': random phase surrogates that maintain linear correlations in
    %                 the data but destroy any nonlinear structure through phase
    %                 randomization
    %       (ii) 'AAFT': the amplitude-adjusted Fourier transform method maintains
    %                    linear correlations but destroys nonlinear structure
    %                    through phase randomization, yet preserves the approximate
    %                    amplitude distribution,
    %       (iii) 'TFT': preserves low-frequency phases but randomizes high-frequency phases (as a way of dealing
    %                    with non-stationarity, cf.:
    %               "A new surrogate data method for nonstationary time series",
    %                   D. L. Guarin Lopez et al., arXiv 1008.1804 (2010)
    % 
    % nsurrs, the number of surrogates to compute (default is 99 for a 0.01
    %         significance level 1-sided test)
    % 
    % extrap, extra parameter, the cut-off frequency for 'TFT'
    % 
    % teststat, the test statistic to evalute on all surrogates and the original
    %           time series. Can specify multiple options in a cell and will return
    %           output for each specified test statistic:
    %           (i) 'ami': the automutual information at lag 1, cf.
    %                 "Testing for nonlinearity in irregular fluctuations with
    %                 long-term trends" T. Nakamura and M. Small and Y. Hirata,
    %                 Phys. Rev. E 74(2) 026205 (2006)
    %           (ii) 'fmmi': the first minimum of the automutual information
    %                       function
    %           (iii) 'o3': a third-order statistic used in: "Surrogate time
    %                 series", T. Schreiber and A. Schmitz, Physica D 142(3-4) 346
    %                 (2000)
    %           (iv) 'tc3': a time-reversal asymmetry measure. Outputs of the
    %                 function include a z-test between the two distributions, and
    %                 some comparative rank-based statistics.
    % 
    %---HISTORY:
    % Ben Fulcher, 28/1/2011
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (20,)

    TAGS = ('nonlinearity', 'stochastic', 'surrogatedata')

    def __init__(self, surrmeth='RP', nsurrs=99.0, extrap=(), teststat=('ami1', 'fmmi', 'o3', 'tc3')):
        super(SD_SurrogateTest, self).__init__()
        self.surrmeth = surrmeth
        self.nsurrs = nsurrs
        self.extrap = extrap
        self.teststat = teststat

    def _eval_hook(self, eng, x):
        if self.surrmeth is None:
            return eng.run_function(1, 'SD_SurrogateTest', x, )
        elif self.nsurrs is None:
            return eng.run_function(1, 'SD_SurrogateTest', x, self.surrmeth)
        elif self.extrap is None:
            return eng.run_function(1, 'SD_SurrogateTest', x, self.surrmeth, self.nsurrs)
        elif self.teststat is None:
            return eng.run_function(1, 'SD_SurrogateTest', x, self.surrmeth, self.nsurrs, self.extrap)
        return eng.run_function(1, 'SD_SurrogateTest', x, self.surrmeth, self.nsurrs, self.extrap, self.teststat)


class SD_TSTL_surrogates(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Generates surrogate time series and tests them against the original time
    % series according to some test statistics: T_{C3}, using the
    % TSTOOL code tc3 or T_{rev}, using TSTOOL code trev.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % tau, the autocorrelation lag length <x_n x_{n-tau} x_{n-2tau)>/abs(<x_n
    %                                                   x_{n-tau}|^3/2
    % nsurr, the number of surrogates to generate
    % 
    % surrmeth, the method of generating surrogates:
    %               (i) 1: randomizes phases of fourier spectrum
    %               (ii) 2:  (see Theiler algorithm II)
    %               (iii) 3: permutes samples randomly
    % 
    % 
    % surrfn, the surrogate statistic to evaluate on all surrogates, either 'tc3' or
    %           'trev'
    % 
    %---OUTPUTS: include the Gaussianity of the test statistics, a z-test, and
    % various tests based on fitted kernel densities.
    % 
    %---HISTORY:
    % Ben Fulcher, 15/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (9,)

    TAGS = ('correlation', 'nonlinear', 'stochastic', 'surrogate', 'tstool')

    def __init__(self, tau='mi', nsurr=100.0, surrmethod=1.0, surrfn='tc3'):
        super(SD_TSTL_surrogates, self).__init__()
        self.tau = tau
        self.nsurr = nsurr
        self.surrmethod = surrmethod
        self.surrfn = surrfn

    def _eval_hook(self, eng, x):
        if self.tau is None:
            return eng.run_function(1, 'SD_TSTL_surrogates', x, )
        elif self.nsurr is None:
            return eng.run_function(1, 'SD_TSTL_surrogates', x, self.tau)
        elif self.surrmethod is None:
            return eng.run_function(1, 'SD_TSTL_surrogates', x, self.tau, self.nsurr)
        elif self.surrfn is None:
            return eng.run_function(1, 'SD_TSTL_surrogates', x, self.tau, self.nsurr, self.surrmethod)
        return eng.run_function(1, 'SD_TSTL_surrogates', x, self.tau, self.nsurr, self.surrmethod, self.surrfn)


class SP_Summaries(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns a set of measures summarizing an estimate of the Fourier transform of
    % the signal.
    % 
    % The estimation can be done using a periodogram, using the periodogram code in
    % Matlab's Signal Processing Toolbox, or a fast fourier transform, implemented
    % using Matlab's fft code.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % psdmeth, the method of obtaining the spectrum from the signal:
    %               (i) 'periodogram': periodogram
    %               (ii) 'fft': fast fourier transform
    % 
    % wmeth, the window to use:
    %               (i) 'boxcar'
    %               (iii) 'bartlett'
    %               (iv) 'hann'
    %               (v) 'hamming'
    %               (vi) 'none'
    %               
    % nf, the number of frequency components to include, if
    %           empty (default), it's approx length(y)
    %       
    % dologabs, if 1, takes log amplitude of the signal before
    %           transforming to the frequency domain.
    % 
    % doPower, analyzes the power spectrum rather than amplitudes of a Fourier
    %          transform
    % 
    %---OUTPUTS: statistics summarizing various properties of the spectrum,
    % including its maximum, minimum, spread, correlation, centroid, area in certain
    % (normalized) frequency bands, moments of the spectrum, Shannon spectral
    % entropy, a spectral flatness measure, power-law fits, and the number of
    % crossings of the spectrum at various amplitude thresholds.
    % 
    %---HISTORY:
    % Ben Fulcher, August 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (151,)

    TAGS = ('powerspectrum',)

    def __init__(self, psdmeth='fft', wmeth=(), nf=(), dologabs=1.0, doPower=1.0):
        super(SP_Summaries, self).__init__()
        self.psdmeth = psdmeth
        self.wmeth = wmeth
        self.nf = nf
        self.dologabs = dologabs
        self.doPower = doPower

    def _eval_hook(self, eng, x):
        if self.psdmeth is None:
            return eng.run_function(1, 'SP_Summaries', x, )
        elif self.wmeth is None:
            return eng.run_function(1, 'SP_Summaries', x, self.psdmeth)
        elif self.nf is None:
            return eng.run_function(1, 'SP_Summaries', x, self.psdmeth, self.wmeth)
        elif self.dologabs is None:
            return eng.run_function(1, 'SP_Summaries', x, self.psdmeth, self.wmeth, self.nf)
        elif self.doPower is None:
            return eng.run_function(1, 'SP_Summaries', x, self.psdmeth, self.wmeth, self.nf, self.dologabs)
        return eng.run_function(1, 'SP_Summaries', x, self.psdmeth, self.wmeth, self.nf, self.dologabs, self.doPower)


class ST_FitPolynomial(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Fits a polynomial of order k to the time series, and returns the mean
    % square error of the fit.
    % 
    % Usually kind of a stupid thing to do with a time series, but it's sometimes
    % somehow informative for time series with large trends.
    % 
    %---INPUTS:
    % y, the input time series.
    % k, the order of the polynomial to fit to y.
    % 
    %---OUTPUT:
    % RMS error of the fit.
    %
    %---HISTORY:
    % Ben Fulcher, 2009
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('raw', 'spreaddep', 'trend')

    def __init__(self, k=10.0):
        super(ST_FitPolynomial, self).__init__()
        self.k = k

    def _eval_hook(self, eng, x):
        if self.k is None:
            return eng.run_function(1, 'ST_FitPolynomial', x, )
        return eng.run_function(1, 'ST_FitPolynomial', x, self.k)


class ST_Length(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures the length of the input time series vector.
    % 
    %---INPUT:
    % y, the time series vector
    % 
    %---OUTPUT: the length of the time series
    %
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('lengthdep', 'misc', 'raw')

    def __init__(self):
        super(ST_Length, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'ST_Length', x, )


class ST_LocalExtrema(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Finds maximums and minimums within given segments of the time series and
    % analyses the results. Outputs quantify how local maximums and minimums vary
    % across the time series.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % lorf, whether to use:
    %     (i) 'l', windows of a given length (in which case the third input, n
    %             specifies the length)
    %     (ii) 'n', a specified number of windows to break the time series up into
    %               (in which case the third input, n specifies this number)
    %     (iii) 'tau', sets a window length equal to the correlation length of the
    %                 time series, the first zero-crossing of the autocorrelation
    %                 function.
    %                   
    % n, somehow specifies the window length given the setting of lorf above.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (22,)

    TAGS = ('distribution', 'stationarity')

    def __init__(self, lorf='l', n=50.0):
        super(ST_LocalExtrema, self).__init__()
        self.lorf = lorf
        self.n = n

    def _eval_hook(self, eng, x):
        if self.lorf is None:
            return eng.run_function(1, 'ST_LocalExtrema', x, )
        elif self.n is None:
            return eng.run_function(1, 'ST_LocalExtrema', x, self.lorf)
        return eng.run_function(1, 'ST_LocalExtrema', x, self.lorf, self.n)


class ST_MomentCorr(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Calculates correlations between simple statistics summarizing the distribution
    % of values in local windows of the signal.
    % 
    % Idea to implement this operation was of Nick S. Jones.
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % wl, the sliding window length (can be a fraction to specify a proportion of
    %       the time-series length)
    %       
    % olap, the overlap between consecutive windows as a fraction of the window
    %       length,
    % 
    % mom1, mom2: the statistics to investigate correlations between (in each window):
    %               (i) 'iqr': interquartile range
    %               (ii) 'median': median
    %               (iii) 'std': standard deviation (about the local mean)
    %               (iv) 'mean': mean
    % 
    % transf: the pre-processing transformation to apply to the time series before
    %         analyzing it:
    %               (i) 'abs': takes absolute values of all data points
    %               (ii) 'sqrt': takes the square root of absolute values of all
    %                            data points
    %               (iii) 'sq': takes the square of every data point
    %               (iv) 'none': does no transformation
    %           
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (4,)

    TAGS = ('statistics',)

    def __init__(self, wl=0.02, olap=0.2, mom1='median', mom2='iqr', transf='abs'):
        super(ST_MomentCorr, self).__init__()
        self.wl = wl
        self.olap = olap
        self.mom1 = mom1
        self.mom2 = mom2
        self.transf = transf

    def _eval_hook(self, eng, x):
        if self.wl is None:
            return eng.run_function(1, 'ST_MomentCorr', x, )
        elif self.olap is None:
            return eng.run_function(1, 'ST_MomentCorr', x, self.wl)
        elif self.mom1 is None:
            return eng.run_function(1, 'ST_MomentCorr', x, self.wl, self.olap)
        elif self.mom2 is None:
            return eng.run_function(1, 'ST_MomentCorr', x, self.wl, self.olap, self.mom1)
        elif self.transf is None:
            return eng.run_function(1, 'ST_MomentCorr', x, self.wl, self.olap, self.mom1, self.mom2)
        return eng.run_function(1, 'ST_MomentCorr', x, self.wl, self.olap, self.mom1, self.mom2, self.transf)


class ST_SimpleStats(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Returns a basic statistic about the input time series, depending on the input whatstat
    % 
    %---INPUTS:
    % x, the input time series
    % 
    % whatstat, the statistic to return:
    %          (i) 'zcross': the proportionof zero-crossings of the time series
    %                        (z-scored input thus returns mean-crossings),
    %          (ii) 'maxima': the proportion of the time series that is a local maximum
    %          (iii) 'minima': the proportion of the time series that is a local minimum
    %          (iv) 'pmcross': the ratio of the number of times that the (ideally
    %                          z-scored) time-series crosses +1 (i.e., 1 standard
    %                          deviation above the mean) to the number of times
    %                          that it crosses -1 (i.e., 1 standard deviation below
    %                          the mean).
    %          (v) 'zsczcross': the ratio of zero crossings of raw to detrended
    %                           time series where the raw has zero mean.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('distribution', 'noisiness')

    def __init__(self, whatstat='pmcross'):
        super(ST_SimpleStats, self).__init__()
        self.whatstat = whatstat

    def _eval_hook(self, eng, x):
        if self.whatstat is None:
            return eng.run_function(1, 'ST_SimpleStats', x, )
        return eng.run_function(1, 'ST_SimpleStats', x, self.whatstat)


class SY_DriftingMean(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This function implements an idea found in the Matlab Central forum:
    % http://www.mathworks.de/matlabcentral/newsreader/view_thread/136539
    % 
    % >> It seems to me that you are looking for a measure for a drifting mean.
    % >> If so, this is what I would try:
    % >> 
    % >> - Decide on a frame length N
    % >> - Split your signal in a number of frames of length N
    % >> - Compute the means of each frame
    % >> - Compute the variance for each frame
    % >> - Compare the ratio of maximum and minimum mean
    % >>   with the mean variance of the frames.
    % >> 
    % >> Rune
    % 
    % This operation splits the time series into segments, computes the mean and
    % variance in each segment and compares the maximum and minimum mean to the mean
    % variance.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % howl, (i) 'fix': fixed-length segments (of length l)
    %       (ii) 'num': a given number, l, of segments
    %       
    % l, either the length ('fix') or number of segments ('num')
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('stationarity',)

    def __init__(self, howl='num', l=10.0):
        super(SY_DriftingMean, self).__init__()
        self.howl = howl
        self.l = l

    def _eval_hook(self, eng, x):
        if self.howl is None:
            return eng.run_function(1, 'SY_DriftingMean', x, )
        elif self.l is None:
            return eng.run_function(1, 'SY_DriftingMean', x, self.howl)
        return eng.run_function(1, 'SY_DriftingMean', x, self.howl, self.l)


class SY_DynWin(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Analyzes how stationarity estimates depend on the number of segments used to
    % segment up the time series.
    % 
    % Specifically, variation in a range of local measures are implemented: mean,
    % standard deviation, skewness, kurtosis, ApEn(1,0.2), SampEn(1,0.2), AC(1),
    % AC(2), and the first zero-crossing of the autocorrelation function.
    % 
    % The standard deviation of local estimates of these quantities across the time
    % series are calculated as an estimate of the stationarity in this quantity as a
    % function of the number of splits, n_{seg}, of the time series.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % maxnseg, the maximum number of segments to consider. Will sweep from 2
    %           segments to maxnseg.
    % 
    % 
    %---OUTPUTS: the standard deviation of this set of 'stationarity' estimates
    % across these window sizes.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (11,)

    TAGS = ('stationarity',)

    def __init__(self, maxnseg=10.0):
        super(SY_DynWin, self).__init__()
        self.maxnseg = maxnseg

    def _eval_hook(self, eng, x):
        if self.maxnseg is None:
            return eng.run_function(1, 'SY_DynWin', x, )
        return eng.run_function(1, 'SY_DynWin', x, self.maxnseg)


class SY_KPSStest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Performs the KPSS stationarity test, of Kwiatkowski, Phillips, Schmidt, and Shin,
    % "Testing the null hypothesis of stationarity against the alternative of a
    % unit root: How sure are we that economic time series have a unit root?"
    % Kwiatkowski, Denis and Phillips, Peter C. B. and Schmidt, Peter and Shin, Yongcheol
    % J. Econometrics, 54(1-3) 159 (2002)
    % 
    % Uses the function kpsstest from Matlab's Econometrics Toolbox. The null
    % hypothesis is that a univariate time series is trend stationary, the
    % alternative hypothesis is that it is a non-stationary unit-root process.
    % 
    % The code can implemented for a specific time lag, tau. Alternatively, measures
    % of change in p-values and test statistics will be outputted if the input is a
    % vector of time lags.
    % 
    %---INPUTS:
    % y, the input time series
    % lags, can be either a scalar (returns basic test statistic and p-value), or
    %                   vector (returns statistics on changes across these time lags)
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (6, 2)

    TAGS = ('econometricstoolbox', 'hypothesistest', 'kpsstest', 'pvalue', 'stationarity')

    def __init__(self, lags=MatlabSequence('0:10')):
        super(SY_KPSStest, self).__init__()
        self.lags = lags

    def _eval_hook(self, eng, x):
        if self.lags is None:
            return eng.run_function(1, 'SY_KPSStest', x, )
        return eng.run_function(1, 'SY_KPSStest', x, self.lags)


class SY_LinearTrend(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Linearly detrends the time series using the Matlab algorithm detrend,
    % and returns the ratio of standard deviations before and after the linear
    % detrending.
    % 
    % If a strong linear trend is present in the time series, this  operation should
    % output a low value.
    % 
    %---INPUT:
    % x, the input time series
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('raw', 'stationarity')

    def __init__(self):
        super(SY_LinearTrend, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'SY_LinearTrend', x, )


class SY_LocalDistributions(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Compares the distribution in consecutive partitions of the signal,
    % returning the sum of differences between each kernel-smoothed distributions
    % (using the Matlab function ksdensity).
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % nseg, the number of segments to break the time series into
    % 
    % eachorpar, (i) 'par': compares each local distribution to the parent (full time
    %                       series) distribution
    %            (ii) 'each': compare each local distribution to all other local
    %                         distributions
    % 
    % npoints, number of points to compute the distribution across (in each local
    %          segments)
    % 
    % The operation behaves in one of two modes: each compares the distribution in
    % each segment to that in every other segment, and par compares each
    % distribution to the so-called 'parent' distribution, that of the full signal.
    % 
    %---OUTPUTS: measures of the sum of absolute deviations between distributions
    % across the different pairwise comparisons.
    % 
    %---HISTORY:
    % Ben Fulcher, August 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1, 4, 3)

    TAGS = ('stationarity',)

    def __init__(self, nseg=4.0, eachorpar='each', npoints=None):
        super(SY_LocalDistributions, self).__init__()
        self.nseg = nseg
        self.eachorpar = eachorpar
        self.npoints = npoints

    def _eval_hook(self, eng, x):
        if self.nseg is None:
            return eng.run_function(1, 'SY_LocalDistributions', x, )
        elif self.eachorpar is None:
            return eng.run_function(1, 'SY_LocalDistributions', x, self.nseg)
        elif self.npoints is None:
            return eng.run_function(1, 'SY_LocalDistributions', x, self.nseg, self.eachorpar)
        return eng.run_function(1, 'SY_LocalDistributions', x, self.nseg, self.eachorpar, self.npoints)


class SY_LocalGlobal(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Compares statistics measured in a local region of the time series to that
    % measured of the full time series.
    % 
    %---INPUTS:
    % y, the time series to analyze
    % 
    % lorp, the local subset of time series to study:
    %             (i) 'l': the first n points in a time series,
    %             (ii) 'p': an initial proportion of the full time series, n
    %             (iii) 'unicg': n evenly-spaced points throughout the time series
    %             (iv) 'randcg': n randomly-chosen points from the time series (chosen with replacement)
    % 
    % n, the parameter for the method specified above
    % 
    % 
    %---OUTPUTS: the mean, standard deviation, median, interquartile range,
    % skewness, kurtosis, AC(1), and SampEn(1,0.1).
    % 
    % This is not the most reliable or systematic operation because only a single
    % sample is taken from the time series and compared to the full time series.
    % A better approach would be to repeat over many local subsets and compare the
    % statistics of these local regions to the full time series.
    % 
    % 
    %---HISTORY:
    % Ben Fulcher, September 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (7,)

    TAGS = ('stationarity', 'stochastic')

    def __init__(self, lorp='l', n=50.0):
        super(SY_LocalGlobal, self).__init__()
        self.lorp = lorp
        self.n = n

    def _eval_hook(self, eng, x):
        if self.lorp is None:
            return eng.run_function(1, 'SY_LocalGlobal', x, )
        elif self.n is None:
            return eng.run_function(1, 'SY_LocalGlobal', x, self.lorp)
        return eng.run_function(1, 'SY_LocalGlobal', x, self.lorp, self.n)


class SY_PPtest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Performs the Phillips-Peron unit root test for a time series via the code
    % pptest from Matlab's Econometrics Toolbox.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % lags, a vector of lags
    % 
    % model, a specified model:
    %               'ar': autoregressive
    %               'ard': autoregressive with drift, or
    %               'ts': trend stationary,
    %               (see Matlab documentation for information)
    %               
    % teststat, the test statistic:
    %               't1': the standard t-statistic, or
    %               't2' a lag-adjusted, 'unStudentized' t statistic.
    %               (see Matlab documentation for information)
    %               
    %---OUTPUTS: statistics on the p-values and lags obtained from the set of tests, as
    % well as measures of the regression statistics.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (15,)

    TAGS = ('aic', 'bic', 'econometricstoolbox', 'hqc', 'pptest', 'pvalue', 'rmse', 'unitroot')

    def __init__(self, lags=MatlabSequence('0:5'), model='ts', teststat='t1'):
        super(SY_PPtest, self).__init__()
        self.lags = lags
        self.model = model
        self.teststat = teststat

    def _eval_hook(self, eng, x):
        if self.lags is None:
            return eng.run_function(1, 'SY_PPtest', x, )
        elif self.model is None:
            return eng.run_function(1, 'SY_PPtest', x, self.lags)
        elif self.teststat is None:
            return eng.run_function(1, 'SY_PPtest', x, self.lags, self.model)
        return eng.run_function(1, 'SY_PPtest', x, self.lags, self.model, self.teststat)


class SY_RangeEvolve(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Measures of the range of the time series as a function of time,
    % i.e., range(x_{1:i}) for i = 1, 2, ..., N, where N is the length of the time
    % series.
    % 
    %---INPUT:
    % y, the time series
    % 
    %---OUTPUTS: based on the dynamics of how new extreme events occur with time.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (17,)

    TAGS = ('stationarity',)

    def __init__(self):
        super(SY_RangeEvolve, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'SY_RangeEvolve', x, )


class SY_SlidingWindow(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This function is based on sliding a window along the time series, measuring
    % some quantity in each window, and outputting some summary of this set of local
    % estimates of that quantity.
    % 
    % Another way of saying it: calculate 'windowstat' in each window, and computes
    % 'acrosswindowstat' for the set of statistics calculated in each window.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % windowstat, the measure to calculate in each window:
    %               (i) 'mean', mean
    %               (ii) 'std', standard deviation
    %               (iii) 'ent', distribution entropy
    %               (iv) 'mom3', skewness
    %               (v) 'mom4', kurtosis
    %               (vi) 'mom5', the fifth moment of the distribution
    %               (vii) 'lillie', the p-value for a Lilliefors Gaussianity test
    %               (viii) 'AC1', the lag-1 autocorrelation
    %               (ix) 'apen', Approximate Entropy
    % 
    % acrosswindowstat, controls how the obtained sequence of local estimates is
    %                   compared (as a ratio to the full time series):
    %                       (i) 'std': standard deviation
    %                       (ii) 'ent' histogram entropy
    %                       (iii) 'apen': Approximate Entropy, ApEn(1,0.2)
    %                               cf. "Approximate entropy as a measure of system
    %                               complexity", S. M. Pincus, P. Natl. Acad. Sci.
    %                               USA 88(6) 2297 (1991)
    % 
    % nseg, the number of segments to divide the time series up into, thus
    %       controlling the window length
    % 
    % nmov, the increment to move the window at each iteration, as 1/fraction of the
    %       window length (e.g., nmov = 2, means the window moves half the length of the
    %       window at each increment)
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('slidingwin', 'stationarity')

    def __init__(self, windowstat='ent', acrosswindowstat='ent', nseg=5.0, nmov=2.0):
        super(SY_SlidingWindow, self).__init__()
        self.windowstat = windowstat
        self.acrosswindowstat = acrosswindowstat
        self.nseg = nseg
        self.nmov = nmov

    def _eval_hook(self, eng, x):
        if self.windowstat is None:
            return eng.run_function(1, 'SY_SlidingWindow', x, )
        elif self.acrosswindowstat is None:
            return eng.run_function(1, 'SY_SlidingWindow', x, self.windowstat)
        elif self.nseg is None:
            return eng.run_function(1, 'SY_SlidingWindow', x, self.windowstat, self.acrosswindowstat)
        elif self.nmov is None:
            return eng.run_function(1, 'SY_SlidingWindow', x, self.windowstat, self.acrosswindowstat, self.nseg)
        return eng.run_function(1, 'SY_SlidingWindow', x, self.windowstat, self.acrosswindowstat, self.nseg, self.nmov)


class SY_SpreadRandomLocal(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Implements a bootstrap-based stationarity measure: nseg time-series segments
    % of length l are selected at random from the time series and in each
    % segment some statistic is calculated: mean, standard deviation, skewness,
    % kurtosis, ApEn(1,0.2), SampEn(1,0.2), AC(1), AC(2), and the first
    % zero-crossing of the autocorrelation function.
    % Outputs summarize how these quantities vary in different local segments of the
    % time series.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % l, the length of local time-series segments to analyze as a positive integer.
    %    Can also be a specified character string:
    %       (i) 'ac2': twice the first zero-crossing of the autocorrelation function
    %       (ii) 'ac5': five times the first zero-crossing of the autocorrelation function
    % 
    % nseg, the number of randomly-selected local segments to analyze
    % 
    %---OUTPUTS: the mean and also the standard deviation of this set of 100 local
    % estimates.
    % 
    %---HISTORY:
    % Ben Fulcher, August 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (18,)

    TAGS = ('correlation', 'stationarity', 'stochastic')

    def __init__(self, l=50.0, nseg=100.0):
        super(SY_SpreadRandomLocal, self).__init__()
        self.l = l
        self.nseg = nseg

    def _eval_hook(self, eng, x):
        if self.l is None:
            return eng.run_function(1, 'SY_SpreadRandomLocal', x, )
        elif self.nseg is None:
            return eng.run_function(1, 'SY_SpreadRandomLocal', x, self.l)
        return eng.run_function(1, 'SY_SpreadRandomLocal', x, self.l, self.nseg)


class SY_StatAv(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % The StatAv measure is a simple mean-stationarity metric that divides
    % the time series into non-overlapping subsegments, calculates the mean in each
    % of these segments and returns the standard deviation of this set of means.
    % 
    % "Heart rate control in normal and aborted-SIDS infants", S. M. Pincus et al.
    % Am J. Physiol. Regul. Integr. Comp. Physiol. 264(3) R638 (1993)
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % WhatType, the type of StatAv to perform:
    %           (i) 'seg': divide the time series into n segments
    %           (ii) 'len': divide the time series into segments of length n
    % 
    % n, either the number of subsegments ('seg') or their length ('len')
    % 
    %---HISTORY:
    % Ben Fulcher, 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('StatAv', 'stationarity')

    def __init__(self, WhatType='len', n=100.0):
        super(SY_StatAv, self).__init__()
        self.WhatType = WhatType
        self.n = n

    def _eval_hook(self, eng, x):
        if self.WhatType is None:
            return eng.run_function(1, 'SY_StatAv', x, )
        elif self.n is None:
            return eng.run_function(1, 'SY_StatAv', x, self.WhatType)
        return eng.run_function(1, 'SY_StatAv', x, self.WhatType, self.n)


class SY_StdNthDer(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates the standard deviation of the nth derivative of the time series.
    % 
    % Based on an idea by Vladimir Vassilevsky, a DSP and Mixed Signal Design
    % Consultant in a Matlab forum, who stated that You can measure the standard
    % deviation of the nth derivative, if you like".
    % 
    % cf. http://www.mathworks.de/matlabcentral/newsreader/view_thread/136539
    % 
    % The derivative is estimated very simply by simply taking successive increments
    % of the time series; the process is repeated to obtain higher order
    % derivatives.
    % 
    %---INPUTS:
    % 
    % y, time series to analyze
    % 
    % n, the order of derivative to analyze
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (1,)

    TAGS = ('entropy',)

    def __init__(self, n=6.0):
        super(SY_StdNthDer, self).__init__()
        self.n = n

    def _eval_hook(self, eng, x):
        if self.n is None:
            return eng.run_function(1, 'SY_StdNthDer', x, )
        return eng.run_function(1, 'SY_StdNthDer', x, self.n)


class SY_StdNthDerChange(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This operation returns statistics on how the output of SY_StdNthDer changes
    % with the order of the derivative of the signal.
    % 
    % Operation inspired by a comment on the Matlab Central forum: "You can
    % measure the standard deviation of the n-th derivative, if you like." --
    % Vladimir Vassilevsky, DSP and Mixed Signal Design Consultant from
    % http://www.mathworks.de/matlabcentral/newsreader/view_thread/136539
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % maxd, the maximum derivative to take.
    % 
    % An exponential function, f(x) = Aexp(bx), is fitted to the variation across
    % successive derivatives; outputs are the parameters and quality of this fit.
    % 
    % Typically an excellent fit to exponential: regular signals decrease, irregular
    % signals increase...?
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (5,)

    TAGS = ('entropy',)

    def __init__(self, maxd=None):
        super(SY_StdNthDerChange, self).__init__()
        self.maxd = maxd

    def _eval_hook(self, eng, x):
        if self.maxd is None:
            return eng.run_function(1, 'SY_StdNthDerChange', x, )
        return eng.run_function(1, 'SY_StdNthDerChange', x, self.maxd)


class SY_TISEAN_nstat_z(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses the nstat_z routine from the TISEAN package for nonlinear time-series
    % analysis to calculate cross-forecast errors of zeroth-order models for the
    % time-delay embedded time series.
    % 
    % The program looks for nonstationarity in a time series by dividing it
    % into a number of segments and calculating the cross-forecast errors
    % between the different segments. The model used for the forecast is
    % zeroth order model as proposed by Schreiber.
    % 
    % cf. "Practical implementation of nonlinear time series methods: The TISEAN
    % package", R. Hegger, H. Kantz, and T. Schreiber, Chaos 9(2) 413 (1999)
    % 
    % Available here:
    % http://www.mpipks-dresden.mpg.de/~tisean/Tisean_3.0.1/index.html
    % 
    % The TISEAN routines are performed in the command line using 'system' commands
    % in Matlab, and require that TISEAN is installed and compiled, and able to be
    % executed in the command line.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % nseg, the number of equally-spaced segments to divide the time series into,
    %       and used to predict the other time series segments
    % 
    % embedparams, in the form {tau,m}, as usual for BF_embed. That is, for an
    %               embedding dimension, tau, and embedding dimension, m. E.g.,
    %               {1,3} has a time-delay of 1 and embedding dimension of 3.
    % 
    % 
    %---OUTPUTS: include the trace of the cross-prediction error matrix, the mean,
    % minimum, and maximum cross-prediction error, the minimum off-diagonal
    % cross-prediction error, and eigenvalues of the cross-prediction error matrix.
    % 
    %---HISTORY:
    % Ben Fulcher, 17/11/2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (28,)

    TAGS = ('model', 'nonlinear', 'stationarity', 'tisean')

    def __init__(self, nseg=5.0, embedparams=(1.0, 3.0)):
        super(SY_TISEAN_nstat_z, self).__init__()
        self.nseg = nseg
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.nseg is None:
            return eng.run_function(1, 'SY_TISEAN_nstat_z', x, )
        elif self.embedparams is None:
            return eng.run_function(1, 'SY_TISEAN_nstat_z', x, self.nseg)
        return eng.run_function(1, 'SY_TISEAN_nstat_z', x, self.nseg, self.embedparams)


class SY_VarRatioTest(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % This code performs a variance ratio test on the time series, implemented using
    % the vratiotest function from Matlab's Econometrics Toolbox.
    % 
    % The test assesses the null hypothesis of a random walk in the time series,
    % which is rejected for some critical p-value.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % periods, a vector (or scalar) of period(s)
    % 
    % IIDs, a vector (or scalar) representing boolean values indicating whether to
    %       assume independent and identically distributed (IID) innovations for
    %       each period.
    % 
    %---HISTORY:
    % Ben Fulcher, 26/2/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (10, 3)

    TAGS = ('econometricstoolbox', 'pvalue', 'vratiotest')

    def __init__(self, periods=4.0, IIDs=0.0):
        super(SY_VarRatioTest, self).__init__()
        self.periods = periods
        self.IIDs = IIDs

    def _eval_hook(self, eng, x):
        if self.periods is None:
            return eng.run_function(1, 'SY_VarRatioTest', x, )
        elif self.IIDs is None:
            return eng.run_function(1, 'SY_VarRatioTest', x, self.periods)
        return eng.run_function(1, 'SY_VarRatioTest', x, self.periods, self.IIDs)


class TSTL_delaytime(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses the TSTOOL code delaytime, that computes an optimal delay time using the
    % method of Parlitz and Wichard (this method is specified in the TSTOOL
    % documentation but without reference).
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % y, column vector of time series data
    % 
    % maxdelay, maximum value of the delay to consider (can also specify a
    %           proportion of time series length)
    %           
    % past, the TSTOOL documentation describes this parameter as "?", which is
    %       relatively uninformative.
    % 
    % 
    % It's a stochastic algorithm, so it must rely on some random sampling of the
    % input time series... A bit of a strange one, but I'll return some statistics
    % and see what they do.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (9,)

    TAGS = ('correlation', 'nonlinear', 'stochastic', 'tau', 'tstool')

    def __init__(self, maxdelay=0.1, past=1.0):
        super(TSTL_delaytime, self).__init__()
        self.maxdelay = maxdelay
        self.past = past

    def _eval_hook(self, eng, x):
        if self.maxdelay is None:
            return eng.run_function(1, 'TSTL_delaytime', x, )
        elif self.past is None:
            return eng.run_function(1, 'TSTL_delaytime', x, self.maxdelay)
        return eng.run_function(1, 'TSTL_delaytime', x, self.maxdelay, self.past)


class TSTL_localdensity(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses TSTOOL code localdensity, which is very poorly documented in the TSTOOL
    % documentation, but we can assume it returns local density estimates in the
    % time-delay embedding space.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % 
    % y, the time series as a column vector
    % 
    % NNR, number of nearest neighbours to compute
    % 
    % past, number of time-correlated points to discard (samples)
    % 
    % embedparams, the embedding parameters, inputs to BF_embed as {tau,m}, where
    %               tau and m can be characters specifying a given automatic method
    %               of determining tau and/or m (see BF_embed).
    % 
    %---OUTPUTS: various statistics on the local density estimates at each point in
    % the time-delay embedding, including the minimum and maximum values, the range,
    % the standard deviation, mean, median, and autocorrelation.
    % 
    %---HISTORY:
    % Ben Fulcher, November 2009
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (14,)

    TAGS = ('localdensity', 'nonlinear', 'stochastic', 'tstool')

    def __init__(self, NNR=5.0, past=40.0, embedparams=('ac', 'cao')):
        super(TSTL_localdensity, self).__init__()
        self.NNR = NNR
        self.past = past
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.NNR is None:
            return eng.run_function(1, 'TSTL_localdensity', x, )
        elif self.past is None:
            return eng.run_function(1, 'TSTL_localdensity', x, self.NNR)
        elif self.embedparams is None:
            return eng.run_function(1, 'TSTL_localdensity', x, self.NNR, self.past)
        return eng.run_function(1, 'TSTL_localdensity', x, self.NNR, self.past, self.embedparams)


class TSTL_predict(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % References TSTOOL code 'predict', which does local constant iterative
    % prediction for scalar data using fast nearest neighbour searching. There are
    % four modes available for the prediction output.
    % 
    % TSTOOL: http://www.physik3.gwdg.de/tstool/
    % 
    %---INPUTS:
    % 
    % y, scalar column vector time series
    % 
    % plen, prediction length in samples or as proportion of time series length NNR,
    % 
    % NNR, number of nearest neighbours
    % 
    % stepsize, number of samples to step for each prediction
    % 
    % pmode, prediction mode, four options:
    %           (i) 0: output vectors are means of images of nearest neighbours
    %           (ii) 1: output vectors are distance-weighted means of images
    %                     nearest neighbours
    %           (iii) 2: output vectors are calculated using local flow and the
    %                    mean of the images of the neighbours
    %           (iv) 3: output vectors are calculated using local flow and the
    %                    weighted mean of the images of the neighbours
    % embedparams, as usual to feed into BF_embed, except that now you can set
    %              to zero to not embed.
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = ()

    TAGS = ()

    def __init__(self, plen=None, NNR=None, stepsize=None, pmode=None, embedparams=None):
        super(TSTL_predict, self).__init__()
        self.plen = plen
        self.NNR = NNR
        self.stepsize = stepsize
        self.pmode = pmode
        self.embedparams = embedparams

    def _eval_hook(self, eng, x):
        if self.plen is None:
            return eng.run_function(1, 'TSTL_predict', x, )
        elif self.NNR is None:
            return eng.run_function(1, 'TSTL_predict', x, self.plen)
        elif self.stepsize is None:
            return eng.run_function(1, 'TSTL_predict', x, self.plen, self.NNR)
        elif self.pmode is None:
            return eng.run_function(1, 'TSTL_predict', x, self.plen, self.NNR, self.stepsize)
        elif self.embedparams is None:
            return eng.run_function(1, 'TSTL_predict', x, self.plen, self.NNR, self.stepsize, self.pmode)
        return eng.run_function(1, 'TSTL_predict', x, self.plen, self.NNR, self.stepsize, self.pmode, self.embedparams)


class WL_DetailCoeffs(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Compares the detail coefficients obtained at each level of the wavelet
    % decomposition from 1 to the maximum possible level for the wavelet given the
    % length of the input time series (computed using wmaxlev from
    % Matlab's Wavelet Toolbox).
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % wname, the name of the mother wavelet to analyze the data with: e.g., 'db3',
    %           'sym2', cf. Wavelet Toolbox Documentation for details
    %           
    % maxlevel, the maximum wavelet decomposition level (can also set to 'max' to be
    %               that determined by wmaxlev)
    % 
    %---OUTPUTS: A set of statistics on the detail coefficients.
    %       
    %---HISTORY:
    % Ben Fulcher 23/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (16,)

    TAGS = ('wavelet', 'waveletTB')

    def __init__(self, wname='db3', maxlevel='max'):
        super(WL_DetailCoeffs, self).__init__()
        self.wname = wname
        self.maxlevel = maxlevel

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'WL_DetailCoeffs', x, )
        elif self.maxlevel is None:
            return eng.run_function(1, 'WL_DetailCoeffs', x, self.wname)
        return eng.run_function(1, 'WL_DetailCoeffs', x, self.wname, self.maxlevel)


class WL_coeffs(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Performs a wavelet decomposition of the time series using a given wavelet at a
    % given level and returns a set of statistics on the coefficients obtained.
    % 
    % Uses Matlab's Wavelet Toolbox.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % wname, the wavelet name, e.g., 'db3' (see Wavelet Toolbox Documentation for
    %                                       all options)
    % 
    % level, the level of wavelet decomposition
    % 
    %---HISTORY:
    % Ben Fulcher, 23/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (10,)

    TAGS = ('lengthdep', 'wavelet', 'waveletTB')

    def __init__(self, wname='db3', level=5.0):
        super(WL_coeffs, self).__init__()
        self.wname = wname
        self.level = level

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'WL_coeffs', x, )
        elif self.level is None:
            return eng.run_function(1, 'WL_coeffs', x, self.wname)
        return eng.run_function(1, 'WL_coeffs', x, self.wname, self.level)


class WL_cwt(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Applies a continuous wavelet transform to the time series using the function
    % cwt from Matlab's Wavelet Toolbox.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % wname, the wavelet name, e.g., 'db3' (Daubechies wavelet), 'sym2' (Symlet),
    %                           etc. (see Wavelet Toolbox Documentation for all
    %                           options)
    % 
    % maxscale, the maximum scale of wavelet analysis.
    % 
    % 
    %---OUTPUTS: statistics on the coefficients, entropy, and results of
    % coefficients summed across scales.
    % 
    %---HISTORY:
    % Ben Fulcher, 26/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (30,)

    TAGS = ('cwt', 'lengthdep', 'statTB', 'wavelet', 'waveletTB')

    def __init__(self, wname='sym2', maxscale=32.0):
        super(WL_cwt, self).__init__()
        self.wname = wname
        self.maxscale = maxscale

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'WL_cwt', x, )
        elif self.maxscale is None:
            return eng.run_function(1, 'WL_cwt', x, self.wname)
        return eng.run_function(1, 'WL_cwt', x, self.wname, self.maxscale)


class WL_dwtcoeff(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Decomposes the time series using a given wavelet and outputs statistics on the
    % coefficients obtained up to a maximum level, level.
    % 
    %---INPUTS:
    % 
    % y, the input time series
    % 
    % wname, the mother wavelet, e.g., 'db3', 'sym2' (see Wavelet Toolbox
    %           Documentation)
    %           
    % level, the level of wavelet decomposition (can be set to 'max' for the maximum
    %               level determined by wmaxlev)
    % 
    %---HISTORY:
    % Ben Fulcher, January 2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (20,)

    TAGS = ('dwt', 'wavelet', 'waveletTB')

    def __init__(self, wname='sym2', level=5.0):
        super(WL_dwtcoeff, self).__init__()
        self.wname = wname
        self.level = level

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'WL_dwtcoeff', x, )
        elif self.level is None:
            return eng.run_function(1, 'WL_dwtcoeff', x, self.wname)
        return eng.run_function(1, 'WL_dwtcoeff', x, self.wname, self.level)


class WL_fBM(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Uses the wfbmesti function from Matlab's Wavelet Toolbox to estimate the
    % parameters of fractional Gaussian Noise, or fractional Brownian motion in a
    % time series.
    % 
    %---INPUT:
    % y, the time series to analyze.
    % 
    %---OUTPUTS: All three outputs of wfbmesti are returned from this function.
    % 
    %---HISTORY:
    % Ben Fulcher 23/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (3,)

    TAGS = ('wavelet', 'waveletTB')

    def __init__(self):
        super(WL_fBM, self).__init__()

    def _eval_hook(self, eng, x):
        return eng.run_function(1, 'WL_fBM', x, )


class WL_scal2frq(HCTSASuper):
    """
    Matlab doc:
    ----------------------------------------
    % 
    % Estimates frequency components in a periodic time series using functions from
    % Matlab's Wavelet Toolbox, including the scal2frq function.
    % 
    %---INPUTS:
    % y, the input time series
    % 
    % wname, the name of the mother wavelet to analyze the data with: e.g., 'db3',
    %           'sym2', cf. Wavelet Toolbox Documentation for details
    % 
    % amax, the maximum scale / level (can be 'max' to set according to wmaxlev)
    % 
    % delta, the sampling period
    % 
    %---OUTPUTS: the level with the highest energy coefficients, the dominant
    % period, and the dominant pseudo-frequency.
    % 
    % Adapted from example in Matlab Wavelet Toolbox documentation. It's kind of a
    % weird idea to apply the method to generic time series.
    % 
    %---HISTORY:
    % Ben Fulcher, 26/1/2010
    % 
    ----------------------------------------
    """

    KNOWN_OUTPUTS_SIZES = (3,)

    TAGS = ('wavelet', 'waveletTB')

    def __init__(self, wname='db3', amax='max', delta=1.0):
        super(WL_scal2frq, self).__init__()
        self.wname = wname
        self.amax = amax
        self.delta = delta

    def _eval_hook(self, eng, x):
        if self.wname is None:
            return eng.run_function(1, 'WL_scal2frq', x, )
        elif self.amax is None:
            return eng.run_function(1, 'WL_scal2frq', x, self.wname)
        elif self.delta is None:
            return eng.run_function(1, 'WL_scal2frq', x, self.wname, self.amax)
        return eng.run_function(1, 'WL_scal2frq', x, self.wname, self.amax, self.delta)


HCTSA_ALL_CLASSES = (
    CO_AddNoise,
    CO_AutoCorr,
    CO_AutoCorrShape,
    CO_CompareMinAMI,
    CO_Embed2,
    CO_Embed2_AngleTau,
    CO_Embed2_Basic,
    CO_Embed2_Dist,
    CO_Embed2_Shapes,
    CO_FirstMin,
    CO_FirstZero,
    CO_HistogramAMI,
    CO_NonlinearAutocorr,
    CO_RM_AMInformation,
    CO_StickAngles,
    CO_TSTL_AutoCorrMethod,
    CO_TSTL_amutual,
    CO_TSTL_amutual2,
    CO_TranslateShape,
    CO_f1ecac,
    CO_fzcglscf,
    CO_glscf,
    CO_tc3,
    CO_trev,
    CP_ML_StepDetect,
    CP_l1pwc_sweep_lambda,
    CP_wavelet_varchg,
    DN_Burstiness,
    DN_CompareKSFit,
    DN_Compare_zscore,
    DN_Cumulants,
    DN_CustomSkewness,
    DN_FitKernelSmooth,
    DN_Fit_mle,
    DN_HighLowMu,
    DN_HistogramMode,
    DN_Mean,
    DN_MinMax,
    DN_Moments,
    DN_OutlierInclude,
    DN_OutlierTest,
    DN_ProportionValues,
    DN_Quantile,
    DN_RemovePoints,
    DN_SimpleFit,
    DN_Spread,
    DN_TrimmedMean,
    DN_Withinp,
    DN_cv,
    DN_nlogL_norm,
    DN_pleft,
    DT_IsSeasonal,
    EN_ApEn,
    EN_DistributionEntropy,
    EN_MS_shannon,
    EN_PermEn,
    EN_RM_entropy,
    EN_Randomize,
    EN_SampEn,
    EN_Shannonpdf,
    EN_wentropy,
    EX_MovingThreshold,
    FC_LocalSimple,
    FC_LoopLocalSimple,
    FC_Surprise,
    HT_DistributionTest,
    HT_HypothesisTest,
    MD_hrv_classic,
    MD_pNN,
    MD_polvar,
    MD_rawHRVmeas,
    MF_ARMA_orders,
    MF_AR_arcov,
    MF_CompareAR,
    MF_CompareTestSets,
    MF_ExpSmoothing,
    MF_FitSubsegments,
    MF_GARCHcompare,
    MF_GARCHfit,
    MF_GP_FitAcross,
    MF_GP_LearnHyperp,
    MF_GP_LocalPrediction,
    MF_GP_hyperparameters,
    MF_ResidualAnalysis,
    MF_StateSpaceCompOrder,
    MF_StateSpace_n4sid,
    MF_arfit,
    MF_armax,
    MF_hmm_CompareNStates,
    MF_hmm_fit,
    MF_steps_ahead,
    NL_BoxCorrDim,
    NL_CaosMethod,
    NL_MS_LZcomplexity,
    NL_MS_fnn,
    NL_MS_nlpe,
    NL_TISEAN_c1,
    NL_TISEAN_d2,
    NL_TSTL_FractalDimensions,
    NL_TSTL_GPCorrSum,
    NL_TSTL_LargestLyap,
    NL_TSTL_PoincareSection,
    NL_TSTL_ReturnTime,
    NL_TSTL_TakensEstimator,
    NL_TSTL_acp,
    NL_TSTL_dimensions,
    NL_crptool_fnn,
    NL_embed_PCA,
    NW_VisibilityGraph,
    PD_PeriodicityWang,
    PH_ForcePotential,
    PH_Walker,
    PP_Compare,
    PP_Iterate,
    PP_ModelFit,
    SB_BinaryStats,
    SB_BinaryStretch,
    SB_CoarseGrain,
    SB_MotifThree,
    SB_MotifTwo,
    SB_TransitionMatrix,
    SB_TransitionpAlphabet,
    SC_FluctAnal,
    SC_fastdfa,
    SD_MakeSurrogates,
    SD_SurrogateTest,
    SD_TSTL_surrogates,
    SP_Summaries,
    ST_FitPolynomial,
    ST_Length,
    ST_LocalExtrema,
    ST_MomentCorr,
    ST_SimpleStats,
    SY_DriftingMean,
    SY_DynWin,
    SY_KPSStest,
    SY_LinearTrend,
    SY_LocalDistributions,
    SY_LocalGlobal,
    SY_PPtest,
    SY_RangeEvolve,
    SY_SlidingWindow,
    SY_SpreadRandomLocal,
    SY_StatAv,
    SY_StdNthDer,
    SY_StdNthDerChange,
    SY_TISEAN_nstat_z,
    SY_VarRatioTest,
    TSTL_delaytime,
    TSTL_localdensity,
    TSTL_predict,
    WL_DetailCoeffs,
    WL_coeffs,
    WL_cwt,
    WL_dwtcoeff,
    WL_fBM,
    WL_scal2frq,
)


class HCTSAOperations(object):
    """Namespace for HCTSA selected operations."""

    # outs: ac1,ac2,fitexpa,fitexpadjr2,fitexpb
    # outs: fitexpr2,fitexprmse,fitlina,fitlinb,meanch
    # outs: mse,pcrossmean,pdec
    # tags: AMI,correlation,entropy,stochastic
    CO_AddNoise_1_quantiles_20 = (
        'CO_AddNoise_1_quantiles_20',
        CO_AddNoise(tau=1, meth='quantiles', nbins=20))

    # outs: ac1,ac2,fitexpa,fitexpadjr2,fitexpb
    # outs: fitexpr2,fitexprmse,fitlina,fitlinb,meanch
    # outs: mse,pcrossmean,pdec
    # tags: AMI,correlation,entropy,stochastic
    CO_AddNoise_1_quantiles_10 = (
        'CO_AddNoise_1_quantiles_10',
        CO_AddNoise(tau=1, meth='quantiles', nbins=10))

    # outs: ac1,ac2,fitexpa,fitexpadjr2,fitexpb
    # outs: fitexpr2,fitexprmse,fitlina,fitlinb,meanch
    # outs: mse,pcrossmean,pdec
    # tags: AMI,correlation,entropy,stochastic
    CO_AddNoise_2_quantiles_20 = (
        'CO_AddNoise_2_quantiles_20',
        CO_AddNoise(tau=2, meth='quantiles', nbins=20))

    # outs: ac1,ac2,fitexpa,fitexpadjr2,fitexpb
    # outs: fitexpr2,fitexprmse,fitlina,fitlinb,meanch
    # outs: mse,pcrossmean,pdec
    # tags: AMI,correlation,entropy,stochastic
    CO_AddNoise_2_quantiles_10 = (
        'CO_AddNoise_2_quantiles_10',
        CO_AddNoise(tau=2, meth='quantiles', nbins=10))

    # outs: ac1,ac2,fitexpa,fitexpadjr2,fitexpb
    # outs: fitexpr2,fitexprmse,fitlina,fitlinb,meanch
    # outs: mse,pcrossmean,pdec
    # tags: AMI,correlation,entropy,stochastic
    CO_AddNoise_1_std1_10 = (
        'CO_AddNoise_1_std1_10',
        CO_AddNoise(tau=1, meth='std1', nbins=10))

    # outs: None
    # tags: autocorrelation,correlation
    AC_32_Fourier = (
        'AC_32_Fourier',
        CO_AutoCorr(tau=32, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_35_Fourier = (
        'AC_35_Fourier',
        CO_AutoCorr(tau=35, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_7_Fourier = (
        'AC_7_Fourier',
        CO_AutoCorr(tau=7, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_19_Fourier = (
        'AC_19_Fourier',
        CO_AutoCorr(tau=19, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_30_Fourier = (
        'AC_30_Fourier',
        CO_AutoCorr(tau=30, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_36_Fourier = (
        'AC_36_Fourier',
        CO_AutoCorr(tau=36, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_38_Fourier = (
        'AC_38_Fourier',
        CO_AutoCorr(tau=38, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_39 = (
        'AC_39',
        CO_AutoCorr(tau=39, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_38 = (
        'AC_38',
        CO_AutoCorr(tau=38, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_37 = (
        'AC_37',
        CO_AutoCorr(tau=37, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_36 = (
        'AC_36',
        CO_AutoCorr(tau=36, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_35 = (
        'AC_35',
        CO_AutoCorr(tau=35, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_34 = (
        'AC_34',
        CO_AutoCorr(tau=34, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_33 = (
        'AC_33',
        CO_AutoCorr(tau=33, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_32 = (
        'AC_32',
        CO_AutoCorr(tau=32, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_31 = (
        'AC_31',
        CO_AutoCorr(tau=31, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_30 = (
        'AC_30',
        CO_AutoCorr(tau=30, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_8_Fourier = (
        'AC_8_Fourier',
        CO_AutoCorr(tau=8, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_23_Fourier = (
        'AC_23_Fourier',
        CO_AutoCorr(tau=23, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_31_Fourier = (
        'AC_31_Fourier',
        CO_AutoCorr(tau=31, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_25_Fourier = (
        'AC_25_Fourier',
        CO_AutoCorr(tau=25, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_2_Fourier = (
        'AC_2_Fourier',
        CO_AutoCorr(tau=2, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_29_Fourier = (
        'AC_29_Fourier',
        CO_AutoCorr(tau=29, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_6_Fourier = (
        'AC_6_Fourier',
        CO_AutoCorr(tau=6, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_17_Fourier = (
        'AC_17_Fourier',
        CO_AutoCorr(tau=17, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_33_Fourier = (
        'AC_33_Fourier',
        CO_AutoCorr(tau=33, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_14_Fourier = (
        'AC_14_Fourier',
        CO_AutoCorr(tau=14, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_12_Fourier = (
        'AC_12_Fourier',
        CO_AutoCorr(tau=12, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_10_Fourier = (
        'AC_10_Fourier',
        CO_AutoCorr(tau=10, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_3 = (
        'AC_3',
        CO_AutoCorr(tau=3, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_1_Fourier = (
        'AC_1_Fourier',
        CO_AutoCorr(tau=1, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_2 = (
        'AC_2',
        CO_AutoCorr(tau=2, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_9 = (
        'AC_9',
        CO_AutoCorr(tau=9, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_8 = (
        'AC_8',
        CO_AutoCorr(tau=8, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_1 = (
        'AC_1',
        CO_AutoCorr(tau=1, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_5 = (
        'AC_5',
        CO_AutoCorr(tau=5, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_4 = (
        'AC_4',
        CO_AutoCorr(tau=4, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_7 = (
        'AC_7',
        CO_AutoCorr(tau=7, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_6 = (
        'AC_6',
        CO_AutoCorr(tau=6, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_28 = (
        'AC_28',
        CO_AutoCorr(tau=28, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_29 = (
        'AC_29',
        CO_AutoCorr(tau=29, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_3_Fourier = (
        'AC_3_Fourier',
        CO_AutoCorr(tau=3, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_20 = (
        'AC_20',
        CO_AutoCorr(tau=20, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_21 = (
        'AC_21',
        CO_AutoCorr(tau=21, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_22 = (
        'AC_22',
        CO_AutoCorr(tau=22, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_23 = (
        'AC_23',
        CO_AutoCorr(tau=23, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_24 = (
        'AC_24',
        CO_AutoCorr(tau=24, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_25 = (
        'AC_25',
        CO_AutoCorr(tau=25, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_26 = (
        'AC_26',
        CO_AutoCorr(tau=26, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_27 = (
        'AC_27',
        CO_AutoCorr(tau=27, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_11_Fourier = (
        'AC_11_Fourier',
        CO_AutoCorr(tau=11, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_27_Fourier = (
        'AC_27_Fourier',
        CO_AutoCorr(tau=27, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_15_Fourier = (
        'AC_15_Fourier',
        CO_AutoCorr(tau=15, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_18_Fourier = (
        'AC_18_Fourier',
        CO_AutoCorr(tau=18, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_16_Fourier = (
        'AC_16_Fourier',
        CO_AutoCorr(tau=16, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_11 = (
        'AC_11',
        CO_AutoCorr(tau=11, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_10 = (
        'AC_10',
        CO_AutoCorr(tau=10, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_13 = (
        'AC_13',
        CO_AutoCorr(tau=13, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_12 = (
        'AC_12',
        CO_AutoCorr(tau=12, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_15 = (
        'AC_15',
        CO_AutoCorr(tau=15, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_14 = (
        'AC_14',
        CO_AutoCorr(tau=14, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_17 = (
        'AC_17',
        CO_AutoCorr(tau=17, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_16 = (
        'AC_16',
        CO_AutoCorr(tau=16, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_19 = (
        'AC_19',
        CO_AutoCorr(tau=19, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_18 = (
        'AC_18',
        CO_AutoCorr(tau=18, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_9_Fourier = (
        'AC_9_Fourier',
        CO_AutoCorr(tau=9, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_5_Fourier = (
        'AC_5_Fourier',
        CO_AutoCorr(tau=5, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_24_Fourier = (
        'AC_24_Fourier',
        CO_AutoCorr(tau=24, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_37_Fourier = (
        'AC_37_Fourier',
        CO_AutoCorr(tau=37, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_40 = (
        'AC_40',
        CO_AutoCorr(tau=40, whatMethod='TimeDomain'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_28_Fourier = (
        'AC_28_Fourier',
        CO_AutoCorr(tau=28, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_34_Fourier = (
        'AC_34_Fourier',
        CO_AutoCorr(tau=34, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_13_Fourier = (
        'AC_13_Fourier',
        CO_AutoCorr(tau=13, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_4_Fourier = (
        'AC_4_Fourier',
        CO_AutoCorr(tau=4, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_21_Fourier = (
        'AC_21_Fourier',
        CO_AutoCorr(tau=21, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_39_Fourier = (
        'AC_39_Fourier',
        CO_AutoCorr(tau=39, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_40_Fourier = (
        'AC_40_Fourier',
        CO_AutoCorr(tau=40, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_20_Fourier = (
        'AC_20_Fourier',
        CO_AutoCorr(tau=20, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_26_Fourier = (
        'AC_26_Fourier',
        CO_AutoCorr(tau=26, whatMethod='Fourier'))

    # outs: None
    # tags: autocorrelation,correlation
    AC_22_Fourier = (
        'AC_22_Fourier',
        CO_AutoCorr(tau=22, whatMethod='Fourier'))

    # outs: Nac,ac1,ac1maxima,ac1minima,ac2
    # outs: ac3,actau,fexpabsacf_a,fexpabsacf_adjr2,fexpabsacf_b
    # outs: fexpabsacf_r2,fexpabsacf_rmse,fexpabsacf_varres,flinlmxacf_a,flinlmxacf_adjr2
    # outs: flinlmxacf_b,flinlmxacf_r2,flinlmxacf_rmse,maximaspread,meanabsacf
    # outs: meanacf,meanmaxima,meanminima,nextrema,nmaxima
    # outs: nminima,pextrema
    # tags: correlation
    CO_AutoCorrShape = (
        'CO_AutoCorrShape',
        CO_AutoCorrShape())

    # outs: conv4,iqr,max,maxp,mean
    # outs: median,min,mode,modef,nlocmax
    # outs: nunique,range,std
    # tags: AMI,correlation
    CO_CompareMinAMI_std2_2_80 = (
        'CO_CompareMinAMI_std2_2_80',
        CO_CompareMinAMI(meth='std2', nbins=[MatlabSequence('2:80')]))

    # outs: conv4,iqr,max,maxp,mean
    # outs: median,min,mode,modef,nlocmax
    # outs: nunique,range,std
    # tags: AMI,correlation
    CO_CompareMinAMI_quantiles_2_80 = (
        'CO_CompareMinAMI_quantiles_2_80',
        CO_CompareMinAMI(meth='quantiles', nbins=[MatlabSequence('2:80')]))

    # outs: conv4,iqr,max,maxp,mean
    # outs: median,min,mode,modef,nlocmax
    # outs: nunique,range,std
    # tags: AMI,correlation
    CO_CompareMinAMI_even_2_80 = (
        'CO_CompareMinAMI_even_2_80',
        CO_CompareMinAMI(meth='even', nbins=[MatlabSequence('2:80')]))

    # outs: conv4,iqr,max,maxp,mean
    # outs: median,min,mode,modef,nlocmax
    # outs: nunique,range,std
    # tags: AMI,correlation
    CO_CompareMinAMI_std1_2_80 = (
        'CO_CompareMinAMI_std1_2_80',
        CO_CompareMinAMI(meth='std1', nbins=[MatlabSequence('2:80')]))

    # outs: arearat,areas_50,areas_all,eucdm1,eucdm2
    # outs: eucdm3,eucdm4,eucdm5,eucds1,eucds2
    # outs: eucds3,eucds4,eucds5,hist10std,histent
    # outs: mean_eucdm,mean_eucds,meanspana,std_eucdm,std_eucds
    # outs: stdb1,stdb2,stdb3,stdb4,stdspana
    # outs: theta_ac1,theta_ac2,theta_ac3,theta_mean,theta_std
    # tags: correlation,embedding
    CO_Embed2_tau = (
        'CO_Embed2_tau',
        CO_Embed2(tau='tau'))

    # outs: ac1_thetaac1,ac1_thetaac2,ac1_thetaac3,diff_thetaac12,max_thetaac1
    # outs: max_thetaac2,max_thetaac3,mean_thetaac1,mean_thetaac2,mean_thetaac3
    # outs: meanrat_thetaac12,min_thetaac1,min_thetaac2,min_thetaac3
    # tags: correlation,embedding
    CO_Embed2_AngleTau_50 = (
        'CO_Embed2_AngleTau_50',
        CO_Embed2_AngleTau(maxtau=50))

    # outs: downdiag01,downdiag05,incircle_01,incircle_02,incircle_05
    # outs: incircle_1,incircle_2,incircle_3,medianincircle,parabdown01
    # outs: parabdown01_1,parabdown01_n1,parabdown05,parabdown05_1,parabdown05_n1
    # outs: parabup01,parabup01_1,parabup01_n1,parabup05,parabup05_1
    # outs: parabup05_n1,ratdiag01,ratdiag05,ring1_01,ring1_02
    # outs: ring1_05,stdincircle,updiag01,updiag05
    # tags: correlation
    CO_Embed2_Basic_1 = (
        'CO_Embed2_Basic_1',
        CO_Embed2_Basic(tau=1))

    # outs: downdiag01,downdiag05,incircle_01,incircle_02,incircle_05
    # outs: incircle_1,incircle_2,incircle_3,medianincircle,parabdown01
    # outs: parabdown01_1,parabdown01_n1,parabdown05,parabdown05_1,parabdown05_n1
    # outs: parabup01,parabup01_1,parabup01_n1,parabup05,parabup05_1
    # outs: parabup05_n1,ratdiag01,ratdiag05,ring1_01,ring1_02
    # outs: ring1_05,stdincircle,updiag01,updiag05
    # tags: correlation
    CO_Embed2_Basic_tau = (
        'CO_Embed2_Basic_tau',
        CO_Embed2_Basic(tau='tau'))

    # outs: d_ac1,d_ac2,d_ac3,d_cv,d_expfit_l
    # outs: d_expfit_nlogL,d_expfit_sumdiff,d_iqr,d_max,d_mean
    # outs: d_median,d_min,d_std
    # tags: correlation,embedding
    CO_Embed2_Dist_tau = (
        'CO_Embed2_Dist_tau',
        CO_Embed2_Dist(tau='tau'))

    # outs: ac1,ac2,hist10_ent,iqr,iqronrange
    # outs: max,median,mode,mode_val,poissfit_absdiff
    # outs: poissfit_l,poissfit_sqdiff,statav5_m,statav5_s,std
    # outs: tau
    # tags: correlation,embedding
    CO_Embed2_Shapes_tau_circle_1 = (
        'CO_Embed2_Shapes_tau_circle_1',
        CO_Embed2_Shapes(tau='tau', shape='circle', r=1))

    # outs: ac1,ac2,hist10_ent,iqr,iqronrange
    # outs: max,median,mode,mode_val,poissfit_absdiff
    # outs: poissfit_l,poissfit_sqdiff,statav5_m,statav5_s,std
    # outs: tau
    # tags: correlation,embedding
    CO_Embed2_Shapes_tau_circle_01 = (
        'CO_Embed2_Shapes_tau_circle_01',
        CO_Embed2_Shapes(tau='tau', shape='circle', r=0.1))

    # outs: None
    # tags: AMI,correlation,tau
    CO_FirstMin_mi = (
        'CO_FirstMin_mi',
        CO_FirstMin(MinWhat='mi'))

    # outs: None
    # tags: autocorrelation,correlation,tau
    CO_FirstMin_ac = (
        'CO_FirstMin_ac',
        CO_FirstMin(MinWhat='ac'))

    # outs: None
    # tags: autocorrelation,correlation,tau
    CO_FirstZero_ac = (
        'CO_FirstZero_ac',
        CO_FirstZero(corrfn='ac'))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_10 = (
        'CO_HistogramAMI_2_std2_10',
        CO_HistogramAMI(tau=2, meth='std2', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_2 = (
        'CO_HistogramAMI_2_std1_2',
        CO_HistogramAMI(tau=2, meth='std1', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_6 = (
        'CO_HistogramAMI_2_std1_6',
        CO_HistogramAMI(tau=2, meth='std1', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_4 = (
        'CO_HistogramAMI_2_std1_4',
        CO_HistogramAMI(tau=2, meth='std1', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_8 = (
        'CO_HistogramAMI_2_std1_8',
        CO_HistogramAMI(tau=2, meth='std1', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_4 = (
        'CO_HistogramAMI_2_quantiles_4',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_6 = (
        'CO_HistogramAMI_2_quantiles_6',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_2 = (
        'CO_HistogramAMI_2_quantiles_2',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_4 = (
        'CO_HistogramAMI_3_quantiles_4',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_2 = (
        'CO_HistogramAMI_3_quantiles_2',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_10 = (
        'CO_HistogramAMI_5_std1_10',
        CO_HistogramAMI(tau=5, meth='std1', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_8 = (
        'CO_HistogramAMI_3_quantiles_8',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_20 = (
        'CO_HistogramAMI_1_std1_20',
        CO_HistogramAMI(tau=1, meth='std1', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_8 = (
        'CO_HistogramAMI_5_std2_8',
        CO_HistogramAMI(tau=5, meth='std2', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_2 = (
        'CO_HistogramAMI_5_std2_2',
        CO_HistogramAMI(tau=5, meth='std2', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_4 = (
        'CO_HistogramAMI_5_std2_4',
        CO_HistogramAMI(tau=5, meth='std2', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_20 = (
        'CO_HistogramAMI_2_std1_20',
        CO_HistogramAMI(tau=2, meth='std1', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_8 = (
        'CO_HistogramAMI_4_std1_8',
        CO_HistogramAMI(tau=4, meth='std1', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_4 = (
        'CO_HistogramAMI_4_std1_4',
        CO_HistogramAMI(tau=4, meth='std1', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_6 = (
        'CO_HistogramAMI_4_std1_6',
        CO_HistogramAMI(tau=4, meth='std1', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_2 = (
        'CO_HistogramAMI_4_std1_2',
        CO_HistogramAMI(tau=4, meth='std1', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_10 = (
        'CO_HistogramAMI_4_std2_10',
        CO_HistogramAMI(tau=4, meth='std2', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_20 = (
        'CO_HistogramAMI_5_even_20',
        CO_HistogramAMI(tau=5, meth='even', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_20 = (
        'CO_HistogramAMI_5_std1_20',
        CO_HistogramAMI(tau=5, meth='std1', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_10 = (
        'CO_HistogramAMI_3_quantiles_10',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_6 = (
        'CO_HistogramAMI_5_std2_6',
        CO_HistogramAMI(tau=5, meth='std2', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_20 = (
        'CO_HistogramAMI_2_quantiles_20',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_8 = (
        'CO_HistogramAMI_1_quantiles_8',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_2 = (
        'CO_HistogramAMI_1_quantiles_2',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_6 = (
        'CO_HistogramAMI_1_quantiles_6',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_4 = (
        'CO_HistogramAMI_1_quantiles_4',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_8 = (
        'CO_HistogramAMI_2_std2_8',
        CO_HistogramAMI(tau=2, meth='std2', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_4 = (
        'CO_HistogramAMI_2_std2_4',
        CO_HistogramAMI(tau=2, meth='std2', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_6 = (
        'CO_HistogramAMI_2_std2_6',
        CO_HistogramAMI(tau=2, meth='std2', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_2 = (
        'CO_HistogramAMI_2_std2_2',
        CO_HistogramAMI(tau=2, meth='std2', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_20 = (
        'CO_HistogramAMI_1_quantiles_20',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_8 = (
        'CO_HistogramAMI_1_even_8',
        CO_HistogramAMI(tau=1, meth='even', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_2 = (
        'CO_HistogramAMI_1_even_2',
        CO_HistogramAMI(tau=1, meth='even', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_6 = (
        'CO_HistogramAMI_1_even_6',
        CO_HistogramAMI(tau=1, meth='even', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_4 = (
        'CO_HistogramAMI_1_even_4',
        CO_HistogramAMI(tau=1, meth='even', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_6 = (
        'CO_HistogramAMI_5_even_6',
        CO_HistogramAMI(tau=5, meth='even', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_4 = (
        'CO_HistogramAMI_5_even_4',
        CO_HistogramAMI(tau=5, meth='even', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_2 = (
        'CO_HistogramAMI_5_even_2',
        CO_HistogramAMI(tau=5, meth='even', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_8 = (
        'CO_HistogramAMI_5_even_8',
        CO_HistogramAMI(tau=5, meth='even', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_8 = (
        'CO_HistogramAMI_2_quantiles_8',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_20 = (
        'CO_HistogramAMI_4_quantiles_20',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std2_20 = (
        'CO_HistogramAMI_2_std2_20',
        CO_HistogramAMI(tau=2, meth='std2', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_20 = (
        'CO_HistogramAMI_4_std2_20',
        CO_HistogramAMI(tau=4, meth='std2', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_2 = (
        'CO_HistogramAMI_4_even_2',
        CO_HistogramAMI(tau=4, meth='even', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_4 = (
        'CO_HistogramAMI_4_even_4',
        CO_HistogramAMI(tau=4, meth='even', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_6 = (
        'CO_HistogramAMI_4_even_6',
        CO_HistogramAMI(tau=4, meth='even', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_8 = (
        'CO_HistogramAMI_4_even_8',
        CO_HistogramAMI(tau=4, meth='even', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_20 = (
        'CO_HistogramAMI_2_even_20',
        CO_HistogramAMI(tau=2, meth='even', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_2 = (
        'CO_HistogramAMI_4_std2_2',
        CO_HistogramAMI(tau=4, meth='std2', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_6 = (
        'CO_HistogramAMI_4_std2_6',
        CO_HistogramAMI(tau=4, meth='std2', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_8 = (
        'CO_HistogramAMI_4_std2_8',
        CO_HistogramAMI(tau=4, meth='std2', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_quantiles_10 = (
        'CO_HistogramAMI_2_quantiles_10',
        CO_HistogramAMI(tau=2, meth='quantiles', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_std1_10 = (
        'CO_HistogramAMI_2_std1_10',
        CO_HistogramAMI(tau=2, meth='std1', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_10 = (
        'CO_HistogramAMI_3_std1_10',
        CO_HistogramAMI(tau=3, meth='std1', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_2 = (
        'CO_HistogramAMI_3_even_2',
        CO_HistogramAMI(tau=3, meth='even', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_4 = (
        'CO_HistogramAMI_3_even_4',
        CO_HistogramAMI(tau=3, meth='even', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_6 = (
        'CO_HistogramAMI_3_even_6',
        CO_HistogramAMI(tau=3, meth='even', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_8 = (
        'CO_HistogramAMI_3_even_8',
        CO_HistogramAMI(tau=3, meth='even', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_10 = (
        'CO_HistogramAMI_4_std1_10',
        CO_HistogramAMI(tau=4, meth='std1', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_20 = (
        'CO_HistogramAMI_3_quantiles_20',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_2 = (
        'CO_HistogramAMI_3_std2_2',
        CO_HistogramAMI(tau=3, meth='std2', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_6 = (
        'CO_HistogramAMI_3_std2_6',
        CO_HistogramAMI(tau=3, meth='std2', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_4 = (
        'CO_HistogramAMI_3_std2_4',
        CO_HistogramAMI(tau=3, meth='std2', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_8 = (
        'CO_HistogramAMI_3_std2_8',
        CO_HistogramAMI(tau=3, meth='std2', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_20 = (
        'CO_HistogramAMI_3_std2_20',
        CO_HistogramAMI(tau=3, meth='std2', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_8 = (
        'CO_HistogramAMI_4_quantiles_8',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_6 = (
        'CO_HistogramAMI_4_quantiles_6',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_4 = (
        'CO_HistogramAMI_4_quantiles_4',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_2 = (
        'CO_HistogramAMI_4_quantiles_2',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_20 = (
        'CO_HistogramAMI_1_std2_20',
        CO_HistogramAMI(tau=1, meth='std2', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_quantiles_6 = (
        'CO_HistogramAMI_3_quantiles_6',
        CO_HistogramAMI(tau=3, meth='quantiles', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_8 = (
        'CO_HistogramAMI_1_std2_8',
        CO_HistogramAMI(tau=1, meth='std2', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_4 = (
        'CO_HistogramAMI_1_std2_4',
        CO_HistogramAMI(tau=1, meth='std2', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_6 = (
        'CO_HistogramAMI_1_std2_6',
        CO_HistogramAMI(tau=1, meth='std2', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_2 = (
        'CO_HistogramAMI_1_std2_2',
        CO_HistogramAMI(tau=1, meth='std2', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_10 = (
        'CO_HistogramAMI_1_even_10',
        CO_HistogramAMI(tau=1, meth='even', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_8 = (
        'CO_HistogramAMI_5_quantiles_8',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_20 = (
        'CO_HistogramAMI_4_even_20',
        CO_HistogramAMI(tau=4, meth='even', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_6 = (
        'CO_HistogramAMI_5_quantiles_6',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_quantiles_10 = (
        'CO_HistogramAMI_4_quantiles_10',
        CO_HistogramAMI(tau=4, meth='quantiles', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_quantiles_10 = (
        'CO_HistogramAMI_1_quantiles_10',
        CO_HistogramAMI(tau=1, meth='quantiles', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_10 = (
        'CO_HistogramAMI_5_quantiles_10',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_4 = (
        'CO_HistogramAMI_5_quantiles_4',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_2 = (
        'CO_HistogramAMI_5_quantiles_2',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_10 = (
        'CO_HistogramAMI_2_even_10',
        CO_HistogramAMI(tau=2, meth='even', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std2_10 = (
        'CO_HistogramAMI_3_std2_10',
        CO_HistogramAMI(tau=3, meth='std2', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_2 = (
        'CO_HistogramAMI_1_std1_2',
        CO_HistogramAMI(tau=1, meth='std1', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_6 = (
        'CO_HistogramAMI_1_std1_6',
        CO_HistogramAMI(tau=1, meth='std1', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_4 = (
        'CO_HistogramAMI_1_std1_4',
        CO_HistogramAMI(tau=1, meth='std1', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_8 = (
        'CO_HistogramAMI_1_std1_8',
        CO_HistogramAMI(tau=1, meth='std1', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std2_10 = (
        'CO_HistogramAMI_1_std2_10',
        CO_HistogramAMI(tau=1, meth='std2', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_8 = (
        'CO_HistogramAMI_3_std1_8',
        CO_HistogramAMI(tau=3, meth='std1', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_4 = (
        'CO_HistogramAMI_3_std1_4',
        CO_HistogramAMI(tau=3, meth='std1', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_6 = (
        'CO_HistogramAMI_3_std1_6',
        CO_HistogramAMI(tau=3, meth='std1', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_2 = (
        'CO_HistogramAMI_3_std1_2',
        CO_HistogramAMI(tau=3, meth='std1', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_even_20 = (
        'CO_HistogramAMI_1_even_20',
        CO_HistogramAMI(tau=1, meth='even', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_std1_20 = (
        'CO_HistogramAMI_3_std1_20',
        CO_HistogramAMI(tau=3, meth='std1', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_10 = (
        'CO_HistogramAMI_3_even_10',
        CO_HistogramAMI(tau=3, meth='even', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_20 = (
        'CO_HistogramAMI_5_std2_20',
        CO_HistogramAMI(tau=5, meth='std2', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_quantiles_20 = (
        'CO_HistogramAMI_5_quantiles_20',
        CO_HistogramAMI(tau=5, meth='quantiles', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_even_10 = (
        'CO_HistogramAMI_4_even_10',
        CO_HistogramAMI(tau=4, meth='even', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std1_20 = (
        'CO_HistogramAMI_4_std1_20',
        CO_HistogramAMI(tau=4, meth='std1', nbins=20))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std2_10 = (
        'CO_HistogramAMI_5_std2_10',
        CO_HistogramAMI(tau=5, meth='std2', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_8 = (
        'CO_HistogramAMI_2_even_8',
        CO_HistogramAMI(tau=2, meth='even', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_8 = (
        'CO_HistogramAMI_5_std1_8',
        CO_HistogramAMI(tau=5, meth='std1', nbins=8))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_6 = (
        'CO_HistogramAMI_5_std1_6',
        CO_HistogramAMI(tau=5, meth='std1', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_2 = (
        'CO_HistogramAMI_2_even_2',
        CO_HistogramAMI(tau=2, meth='even', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_4 = (
        'CO_HistogramAMI_5_std1_4',
        CO_HistogramAMI(tau=5, meth='std1', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_std1_2 = (
        'CO_HistogramAMI_5_std1_2',
        CO_HistogramAMI(tau=5, meth='std1', nbins=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_6 = (
        'CO_HistogramAMI_2_even_6',
        CO_HistogramAMI(tau=2, meth='even', nbins=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_2_even_4 = (
        'CO_HistogramAMI_2_even_4',
        CO_HistogramAMI(tau=2, meth='even', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_4_std2_4 = (
        'CO_HistogramAMI_4_std2_4',
        CO_HistogramAMI(tau=4, meth='std2', nbins=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_1_std1_10 = (
        'CO_HistogramAMI_1_std1_10',
        CO_HistogramAMI(tau=1, meth='std1', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_5_even_10 = (
        'CO_HistogramAMI_5_even_10',
        CO_HistogramAMI(tau=5, meth='even', nbins=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_HistogramAMI_3_even_20 = (
        'CO_HistogramAMI_3_even_20',
        CO_HistogramAMI(tau=3, meth='even', nbins=20))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_045 = (
        'AC_nl_045',
        CO_NonlinearAutocorr(taus=(0.0, 4.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_044 = (
        'AC_nl_044',
        CO_NonlinearAutocorr(taus=(0.0, 4.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_046 = (
        'AC_nl_046',
        CO_NonlinearAutocorr(taus=(0.0, 4.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_122 = (
        'AC_nl_122',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_123 = (
        'AC_nl_123',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_124 = (
        'AC_nl_124',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_1357 = (
        'AC_nl_1357',
        CO_NonlinearAutocorr(taus=(1.0, 3.0, 5.0, 7.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_1234567 = (
        'AC_nl_1234567',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_246 = (
        'AC_nl_246',
        CO_NonlinearAutocorr(taus=(2.0, 4.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_33 = (
        'AC_nl_33',
        CO_NonlinearAutocorr(taus=(3.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_012 = (
        'AC_nl_012',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_013 = (
        'AC_nl_013',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_011 = (
        'AC_nl_011',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 1.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_016 = (
        'AC_nl_016',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_014 = (
        'AC_nl_014',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_015 = (
        'AC_nl_015',
        CO_NonlinearAutocorr(taus=(0.0, 1.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_056 = (
        'AC_nl_056',
        CO_NonlinearAutocorr(taus=(0.0, 5.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_055 = (
        'AC_nl_055',
        CO_NonlinearAutocorr(taus=(0.0, 5.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_113 = (
        'AC_nl_113',
        CO_NonlinearAutocorr(taus=(1.0, 1.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_112 = (
        'AC_nl_112',
        CO_NonlinearAutocorr(taus=(1.0, 1.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_12345678 = (
        'AC_nl_12345678',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_44 = (
        'AC_nl_44',
        CO_NonlinearAutocorr(taus=(4.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_026 = (
        'AC_nl_026',
        CO_NonlinearAutocorr(taus=(0.0, 2.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_025 = (
        'AC_nl_025',
        CO_NonlinearAutocorr(taus=(0.0, 2.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_024 = (
        'AC_nl_024',
        CO_NonlinearAutocorr(taus=(0.0, 2.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_023 = (
        'AC_nl_023',
        CO_NonlinearAutocorr(taus=(0.0, 2.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_022 = (
        'AC_nl_022',
        CO_NonlinearAutocorr(taus=(0.0, 2.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_1234 = (
        'AC_nl_1234',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_066 = (
        'AC_nl_066',
        CO_NonlinearAutocorr(taus=(0.0, 6.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_13 = (
        'AC_nl_13',
        CO_NonlinearAutocorr(taus=(1.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_12 = (
        'AC_nl_12',
        CO_NonlinearAutocorr(taus=(1.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_11 = (
        'AC_nl_11',
        CO_NonlinearAutocorr(taus=(1.0, 1.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_14 = (
        'AC_nl_14',
        CO_NonlinearAutocorr(taus=(1.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_12345 = (
        'AC_nl_12345',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0, 4.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_223 = (
        'AC_nl_223',
        CO_NonlinearAutocorr(taus=(2.0, 2.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_55 = (
        'AC_nl_55',
        CO_NonlinearAutocorr(taus=(5.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_033 = (
        'AC_nl_033',
        CO_NonlinearAutocorr(taus=(0.0, 3.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_034 = (
        'AC_nl_034',
        CO_NonlinearAutocorr(taus=(0.0, 3.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_035 = (
        'AC_nl_035',
        CO_NonlinearAutocorr(taus=(0.0, 3.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_036 = (
        'AC_nl_036',
        CO_NonlinearAutocorr(taus=(0.0, 3.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_133 = (
        'AC_nl_133',
        CO_NonlinearAutocorr(taus=(1.0, 3.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_135 = (
        'AC_nl_135',
        CO_NonlinearAutocorr(taus=(1.0, 3.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_134 = (
        'AC_nl_134',
        CO_NonlinearAutocorr(taus=(1.0, 3.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_24 = (
        'AC_nl_24',
        CO_NonlinearAutocorr(taus=(2.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_22 = (
        'AC_nl_22',
        CO_NonlinearAutocorr(taus=(2.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_2468 = (
        'AC_nl_2468',
        CO_NonlinearAutocorr(taus=(2.0, 4.0, 6.0, 8.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_001 = (
        'AC_nl_001',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 1.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_003 = (
        'AC_nl_003',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_002 = (
        'AC_nl_002',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 2.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_005 = (
        'AC_nl_005',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 5.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_004 = (
        'AC_nl_004',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 4.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_006 = (
        'AC_nl_006',
        CO_NonlinearAutocorr(taus=(0.0, 0.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_123456 = (
        'AC_nl_123456',
        CO_NonlinearAutocorr(taus=(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_233 = (
        'AC_nl_233',
        CO_NonlinearAutocorr(taus=(2.0, 3.0, 3.0)))

    # outs: None
    # tags: autocorrelation,correlation,nonlinearautocorr
    AC_nl_66 = (
        'AC_nl_66',
        CO_NonlinearAutocorr(taus=(6.0, 6.0)))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_10 = (
        'CO_RM_AMInformation_10',
        CO_RM_AMInformation(tau=10))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_7 = (
        'CO_RM_AMInformation_7',
        CO_RM_AMInformation(tau=7))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_6 = (
        'CO_RM_AMInformation_6',
        CO_RM_AMInformation(tau=6))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_5 = (
        'CO_RM_AMInformation_5',
        CO_RM_AMInformation(tau=5))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_4 = (
        'CO_RM_AMInformation_4',
        CO_RM_AMInformation(tau=4))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_3 = (
        'CO_RM_AMInformation_3',
        CO_RM_AMInformation(tau=3))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_2 = (
        'CO_RM_AMInformation_2',
        CO_RM_AMInformation(tau=2))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_1 = (
        'CO_RM_AMInformation_1',
        CO_RM_AMInformation(tau=1))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_0 = (
        'CO_RM_AMInformation_0',
        CO_RM_AMInformation(tau=0))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_9 = (
        'CO_RM_AMInformation_9',
        CO_RM_AMInformation(tau=9))

    # outs: None
    # tags: AMI,correlation,information
    CO_RM_AMInformation_8 = (
        'CO_RM_AMInformation_8',
        CO_RM_AMInformation(tau=8))

    # outs: ac1_all,ac1_n,ac1_p,ac2_all,ac2_n
    # outs: ac2_p,kurtosis_all,kurtosis_n,kurtosis_p,mean
    # outs: mean_n,mean_p,median,median_n,median_p
    # outs: pnsumabsdiff,q10_all,q10_n,q10_p,q1_all
    # outs: q1_n,q1_p,q90_all,q90_n,q90_p
    # outs: q99_all,q99_n,q99_p,ratmean_n,ratmean_p
    # outs: skewness_all,skewness_n,skewness_p,statav2_all_m,statav2_all_s
    # outs: statav2_n_m,statav2_n_s,statav2_p_m,statav2_p_s,statav3_all_m
    # outs: statav3_all_s,statav3_n_m,statav3_n_s,statav3_p_m,statav3_p_s
    # outs: statav4_all_m,statav4_all_s,statav4_n_m,statav4_n_s,statav4_p_m
    # outs: statav4_p_s,statav5_all_m,statav5_all_s,statav5_n_m,statav5_n_s
    # outs: statav5_p_m,statav5_p_s,std,std_n,std_p
    # outs: symks_n,symks_p,tau_all,tau_n,tau_p
    # tags: correlation
    CO_StickAngles_y = (
        'CO_StickAngles_y',
        CO_StickAngles())

    # outs: ac1_all,ac1_n,ac1_p,ac2_all,ac2_n
    # outs: ac2_p,kurtosis_all,kurtosis_n,kurtosis_p,mean
    # outs: mean_n,mean_p,median,median_n,median_p
    # outs: pnsumabsdiff,q10_all,q10_n,q10_p,q1_all
    # outs: q1_n,q1_p,q90_all,q90_n,q90_p
    # outs: q99_all,q99_n,q99_p,ratmean_n,ratmean_p
    # outs: skewness_all,skewness_n,skewness_p,statav2_all_m,statav2_all_s
    # outs: statav2_n_m,statav2_n_s,statav2_p_m,statav2_p_s,statav3_all_m
    # outs: statav3_all_s,statav3_n_m,statav3_n_s,statav3_p_m,statav3_p_s
    # outs: statav4_all_m,statav4_all_s,statav4_n_m,statav4_n_s,statav4_p_m
    # outs: statav4_p_s,statav5_all_m,statav5_all_s,statav5_n_m,statav5_n_s
    # outs: statav5_p_m,statav5_p_s,std,std_n,std_p
    # outs: symks_n,symks_p,tau_all,tau_n,tau_p
    # tags: correlation,locdep,raw,spreaddep
    CO_StickAngles_x = (
        'CO_StickAngles_x',
        CO_StickAngles())

    # outs: None
    # tags: correlation
    CO_TSTL_AutoCorrMethod_err = (
        'CO_TSTL_AutoCorrMethod_err',
        CO_TSTL_AutoCorrMethod())

    # outs: ami1,ami10,ami11,ami12,ami13
    # outs: ami14,ami15,ami16,ami17,ami18
    # outs: ami19,ami2,ami20,ami21,ami3
    # outs: ami4,ami5,ami6,ami7,ami8
    # outs: ami9,fmmi,mami,modeperiodmax,pextrema
    # outs: pmaxima,pmodeperiodmax,stdami
    # tags: AMI,entropy,tstool
    CO_TSTL_amutual_20_10 = (
        'CO_TSTL_amutual_20_10',
        CO_TSTL_amutual(maxtau=20, nbins=10))

    # outs: ami1,ami10,ami11,ami12,ami13
    # outs: ami14,ami15,ami16,ami17,ami18
    # outs: ami19,ami2,ami20,ami21,ami3
    # outs: ami4,ami5,ami6,ami7,ami8
    # outs: ami9,fmmi,mami,modeperiodmax,pextrema
    # outs: pmaxima,pmodeperiodmax,stdami
    # tags: AMI,entropy,lengthdep,tstool
    CO_TSTL_amutual_20 = (
        'CO_TSTL_amutual_20',
        CO_TSTL_amutual(maxtau=20, nbins=()))

    # outs: ami1,ami10,ami11,ami12,ami13
    # outs: ami14,ami15,ami16,ami17,ami18
    # outs: ami19,ami2,ami20,ami21,ami22
    # outs: ami23,ami24,ami25,ami26,ami27
    # outs: ami28,ami29,ami3,ami30,ami31
    # outs: ami32,ami33,ami34,ami35,ami36
    # outs: ami37,ami38,ami39,ami4,ami40
    # outs: ami41,ami42,ami43,ami44,ami45
    # outs: ami46,ami47,ami48,ami49,ami5
    # outs: ami50,ami6,ami7,ami8,ami9
    # outs: amiac1,fmmi,mami,modeperiodmax,modeperiodmin
    # outs: pcrossmean,pcrossmedian,pcrossq10,pcrossq90,pextrema
    # outs: pmaxima,pminima,pmodeperiodmax,pmodeperiodmin,stdami
    # tags: AMI,entropy,tstool
    CO_TSTL_amutual2_50 = (
        'CO_TSTL_amutual2_50',
        CO_TSTL_amutual2(maxtau=50))

    # outs: ami1,ami10,ami11,ami12,ami13
    # outs: ami14,ami15,ami16,ami17,ami18
    # outs: ami19,ami2,ami20,ami21,ami22
    # outs: ami23,ami24,ami25,ami26,ami27
    # outs: ami28,ami29,ami3,ami30,ami31
    # outs: ami32,ami33,ami34,ami35,ami36
    # outs: ami37,ami38,ami39,ami4,ami40
    # outs: ami41,ami42,ami43,ami44,ami45
    # outs: ami46,ami47,ami48,ami49,ami5
    # outs: ami50,ami6,ami7,ami8,ami9
    # outs: amiac1,fmmi,mami,modeperiodmax,modeperiodmin
    # outs: pcrossmean,pcrossmedian,pcrossq10,pcrossq90,pextrema
    # outs: pmaxima,pminima,pmodeperiodmax,pmodeperiodmin,stdami
    # tags: AMI,entropy,tstool
    CO_TSTL_amutual2_diff__50 = (
        'CO_TSTL_amutual2_diff__50',
        CO_TSTL_amutual2(maxtau=50))

    # outs: fives,fours,max,mode,npatmode
    # outs: ones,statav2_m,statav2_s,statav3_m,statav3_s
    # outs: statav4_m,statav4_s,std,threes,twos
    # tags: correlation
    CO_TranslateShape_circle_25_pts = (
        'CO_TranslateShape_circle_25_pts',
        CO_TranslateShape(shape='circle', d=2.5, howtomove='pts'))

    # outs: fives,fours,max,mode,npatmode
    # outs: ones,sevens,sixes,statav2_m,statav2_s
    # outs: statav3_m,statav3_s,statav4_m,statav4_s,std
    # outs: threes,twos
    # tags: correlation
    CO_TranslateShape_circle_35_pts = (
        'CO_TranslateShape_circle_35_pts',
        CO_TranslateShape(shape='circle', d=3.5, howtomove='pts'))

    # outs: eights,elevens,fives,fours,mode
    # outs: nines,npatmode,ones,sevens,sixes
    # outs: statav2_m,statav2_s,statav3_m,statav3_s,statav4_m
    # outs: statav4_s,std,tens,threes,twos
    # tags: correlation
    CO_TranslateShape_circle_55_pts = (
        'CO_TranslateShape_circle_55_pts',
        CO_TranslateShape(shape='circle', d=5.5, howtomove='pts'))

    # outs: eights,fives,fours,mode,nines
    # outs: npatmode,ones,sevens,sixes,statav2_m
    # outs: statav2_s,statav3_m,statav3_s,statav4_m,statav4_s
    # outs: std,threes,twos
    # tags: correlation
    CO_TranslateShape_circle_45_pts = (
        'CO_TranslateShape_circle_45_pts',
        CO_TranslateShape(shape='circle', d=4.5, howtomove='pts'))

    # outs: max,mode,npatmode,ones,statav2_m
    # outs: statav2_s,statav3_m,statav3_s,statav4_m,statav4_s
    # outs: std,threes,twos
    # tags: correlation
    CO_TranslateShape_circle_15_pts = (
        'CO_TranslateShape_circle_15_pts',
        CO_TranslateShape(shape='circle', d=1.5, howtomove='pts'))

    # outs: None
    # tags: autocorrelation,correlation,tau
    CO_f1ecac = (
        'CO_f1ecac',
        CO_f1ecac())

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_5_10 = (
        'CO_fzcglscf_5_10',
        CO_fzcglscf(alpha=5, beta=10))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_2_5 = (
        'CO_fzcglscf_2_5',
        CO_fzcglscf(alpha=2, beta=5))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_2_2 = (
        'CO_fzcglscf_2_2',
        CO_fzcglscf(alpha=2, beta=2))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_2_10 = (
        'CO_fzcglscf_2_10',
        CO_fzcglscf(alpha=2, beta=10))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_10_10 = (
        'CO_fzcglscf_10_10',
        CO_fzcglscf(alpha=10, beta=10))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_1 = (
        'CO_fzcglscf_1_1',
        CO_fzcglscf(alpha=1, beta=1))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_3 = (
        'CO_fzcglscf_1_3',
        CO_fzcglscf(alpha=1, beta=3))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_2 = (
        'CO_fzcglscf_1_2',
        CO_fzcglscf(alpha=1, beta=2))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_5 = (
        'CO_fzcglscf_1_5',
        CO_fzcglscf(alpha=1, beta=5))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_4 = (
        'CO_fzcglscf_1_4',
        CO_fzcglscf(alpha=1, beta=4))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_7 = (
        'CO_fzcglscf_1_7',
        CO_fzcglscf(alpha=1, beta=7))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_6 = (
        'CO_fzcglscf_1_6',
        CO_fzcglscf(alpha=1, beta=6))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_9 = (
        'CO_fzcglscf_1_9',
        CO_fzcglscf(alpha=1, beta=9))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_8 = (
        'CO_fzcglscf_1_8',
        CO_fzcglscf(alpha=1, beta=8))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_1_10 = (
        'CO_fzcglscf_1_10',
        CO_fzcglscf(alpha=1, beta=10))

    # outs: None
    # tags: correlation,glscf,tau
    CO_fzcglscf_5_5 = (
        'CO_fzcglscf_5_5',
        CO_fzcglscf(alpha=5, beta=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_2 = (
        'CO_glscf_2_5_2',
        CO_glscf(alpha=2, beta=5, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_3 = (
        'CO_glscf_2_5_3',
        CO_glscf(alpha=2, beta=5, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_4 = (
        'CO_glscf_2_5_4',
        CO_glscf(alpha=2, beta=5, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_5 = (
        'CO_glscf_2_5_5',
        CO_glscf(alpha=2, beta=5, tau=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_tau = (
        'CO_glscf_1_1_tau',
        CO_glscf(alpha=1, beta=1, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_tau = (
        'CO_glscf_1_2_tau',
        CO_glscf(alpha=1, beta=2, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_tau = (
        'CO_glscf_1_5_tau',
        CO_glscf(alpha=1, beta=5, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_1 = (
        'CO_glscf_2_2_1',
        CO_glscf(alpha=2, beta=2, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_tau = (
        'CO_glscf_2_2_tau',
        CO_glscf(alpha=2, beta=2, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_3 = (
        'CO_glscf_2_2_3',
        CO_glscf(alpha=2, beta=2, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_2 = (
        'CO_glscf_2_2_2',
        CO_glscf(alpha=2, beta=2, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_5 = (
        'CO_glscf_2_2_5',
        CO_glscf(alpha=2, beta=2, tau=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_2_4 = (
        'CO_glscf_2_2_4',
        CO_glscf(alpha=2, beta=2, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_4 = (
        'CO_glscf_1_10_4',
        CO_glscf(alpha=1, beta=10, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_5 = (
        'CO_glscf_1_10_5',
        CO_glscf(alpha=1, beta=10, tau=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_2 = (
        'CO_glscf_1_10_2',
        CO_glscf(alpha=1, beta=10, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_3 = (
        'CO_glscf_1_10_3',
        CO_glscf(alpha=1, beta=10, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_1 = (
        'CO_glscf_1_10_1',
        CO_glscf(alpha=1, beta=10, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_tau = (
        'CO_glscf_2_5_tau',
        CO_glscf(alpha=2, beta=5, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_5 = (
        'CO_glscf_1_1_5',
        CO_glscf(alpha=1, beta=1, tau=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_4 = (
        'CO_glscf_1_1_4',
        CO_glscf(alpha=1, beta=1, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_3 = (
        'CO_glscf_1_1_3',
        CO_glscf(alpha=1, beta=1, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_2 = (
        'CO_glscf_1_1_2',
        CO_glscf(alpha=1, beta=1, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_1_1 = (
        'CO_glscf_1_1_1',
        CO_glscf(alpha=1, beta=1, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_3 = (
        'CO_glscf_1_5_3',
        CO_glscf(alpha=1, beta=5, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_2 = (
        'CO_glscf_1_5_2',
        CO_glscf(alpha=1, beta=5, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_1 = (
        'CO_glscf_1_5_1',
        CO_glscf(alpha=1, beta=5, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_5 = (
        'CO_glscf_1_5_5',
        CO_glscf(alpha=1, beta=5, tau=5))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_5_4 = (
        'CO_glscf_1_5_4',
        CO_glscf(alpha=1, beta=5, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_2_5_1 = (
        'CO_glscf_2_5_1',
        CO_glscf(alpha=2, beta=5, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_10_tau = (
        'CO_glscf_1_10_tau',
        CO_glscf(alpha=1, beta=10, tau='tau'))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_1 = (
        'CO_glscf_1_2_1',
        CO_glscf(alpha=1, beta=2, tau=1))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_2 = (
        'CO_glscf_1_2_2',
        CO_glscf(alpha=1, beta=2, tau=2))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_3 = (
        'CO_glscf_1_2_3',
        CO_glscf(alpha=1, beta=2, tau=3))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_4 = (
        'CO_glscf_1_2_4',
        CO_glscf(alpha=1, beta=2, tau=4))

    # outs: None
    # tags: correlation,glscf
    CO_glscf_1_2_5 = (
        'CO_glscf_1_2_5',
        CO_glscf(alpha=1, beta=2, tau=5))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_tc3_1 = (
        'CO_tc3_1',
        CO_tc3(tau=1))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_tc3_3 = (
        'CO_tc3_3',
        CO_tc3(tau=3))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_tc3_mi = (
        'CO_tc3_mi',
        CO_tc3(tau='mi'))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_tc3_ac = (
        'CO_tc3_ac',
        CO_tc3(tau='ac'))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_tc3_2 = (
        'CO_tc3_2',
        CO_tc3(tau=2))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_trev_ac = (
        'CO_trev_ac',
        CO_trev(tau='ac'))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_trev_mi = (
        'CO_trev_mi',
        CO_trev(tau='mi'))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_trev_2 = (
        'CO_trev_2',
        CO_trev(tau=2))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_trev_3 = (
        'CO_trev_3',
        CO_trev(tau=3))

    # outs: abs,absnum,denom,num,raw
    # tags: autocorrelation,correlation,nonlinear
    CO_trev_1 = (
        'CO_trev_1',
        CO_trev(tau=1))

    # outs: E,diffn12,lambdamax,maxstepint,meanerrstepint
    # outs: meanstepint,meanstepintgt3,medianstepint,minstepint,nsegments
    # outs: pshort_3,ratn12,rmsoff,rmsoffpstep,s
    # tags: l1pwc,lengthdep,stepdetection
    CP_ML_StepDetect_l1pwc_02 = (
        'CP_ML_StepDetect_l1pwc_02',
        CP_ML_StepDetect(method='l1pwc', params=0.2))

    # outs: E,diffn12,lambdamax,maxstepint,meanerrstepint
    # outs: meanstepint,meanstepintgt3,medianstepint,minstepint,nsegments
    # outs: pshort_3,ratn12,rmsoff,rmsoffpstep,s
    # tags: l1pwc,stepdetection
    CP_ML_StepDetect_l1pwc_10 = (
        'CP_ML_StepDetect_l1pwc_10',
        CP_ML_StepDetect(method='l1pwc', params=10))

    # outs: E,diffn12,lambdamax,maxstepint,meanerrstepint
    # outs: meanstepint,meanstepintgt3,medianstepint,minstepint,nsegments
    # outs: pshort_3,ratn12,rmsoff,rmsoffpstep,s
    # tags: l1pwc,lengthdep,stepdetection
    CP_ML_StepDetect_l1pwc_005 = (
        'CP_ML_StepDetect_l1pwc_005',
        CP_ML_StepDetect(method='l1pwc', params=0.05))

    # outs: bestlambda,bestrmserrpseg,corrsegerr,nsegsu001,nsegsu005
    # outs: rmserrsu01,rmserrsu02,rmserrsu05
    # tags: l1pwc,stepdetection
    CP_l1pwc_sweep_lambda_0_005_095 = (
        'CP_l1pwc_sweep_lambda_0_005_095',
        CP_l1pwc_sweep_lambda(lambdar=MatlabSequence('0:0.05:0.95')))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_db3_3_10_001 = (
        'CP_wavelet_varchg_db3_3_10_001',
        CP_wavelet_varchg(wname='db3', level=3, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_sym2_4_10_001 = (
        'CP_wavelet_varchg_sym2_4_10_001',
        CP_wavelet_varchg(wname='sym2', level=4, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_db3_2_10_001 = (
        'CP_wavelet_varchg_db3_2_10_001',
        CP_wavelet_varchg(wname='db3', level=2, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_db3_5_10_001 = (
        'CP_wavelet_varchg_db3_5_10_001',
        CP_wavelet_varchg(wname='db3', level=5, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_db3_4_10_001 = (
        'CP_wavelet_varchg_db3_4_10_001',
        CP_wavelet_varchg(wname='db3', level=4, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_sym2_3_10_001 = (
        'CP_wavelet_varchg_sym2_3_10_001',
        CP_wavelet_varchg(wname='sym2', level=3, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_sym2_5_10_001 = (
        'CP_wavelet_varchg_sym2_5_10_001',
        CP_wavelet_varchg(wname='sym2', level=5, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: varchg,wavelet,waveletTB
    CP_wavelet_varchg_sym2_2_10_001 = (
        'CP_wavelet_varchg_sym2_2_10_001',
        CP_wavelet_varchg(wname='sym2', level=2, maxnchpts=10, mindelay=0.01))

    # outs: None
    # tags: burstiness,locdep,raw
    DN_burstiness = (
        'DN_burstiness',
        DN_Burstiness())

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ksdensity,norm,olapint,peaksepx,peaksepy,raw,relent
    DN_CompareKSFit_norm = (
        'DN_CompareKSFit_norm',
        DN_CompareKSFit(whatDistn='norm'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,exp,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,relent,spreaddep,uni
    DN_CompareKSFit_exp = (
        'DN_CompareKSFit_exp',
        DN_CompareKSFit(whatDistn='exp'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,gamma,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,relent,uni
    DN_CompareKSFit_gamma = (
        'DN_CompareKSFit_gamma',
        DN_CompareKSFit(whatDistn='gamma'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,relent,uni
    DN_CompareKSFit_uni = (
        'DN_CompareKSFit_uni',
        DN_CompareKSFit(whatDistn='uni'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,rayleigh,relent,uni
    DN_CompareKSFit_rayleigh = (
        'DN_CompareKSFit_rayleigh',
        DN_CompareKSFit(whatDistn='rayleigh'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,beta,distribution,ksdensity,olapint,peaksepx,peaksepy,raw,relent,uni
    DN_CompareKSFit_beta = (
        'DN_CompareKSFit_beta',
        DN_CompareKSFit(whatDistn='beta'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ksdensity,locdep,lognormal,olapint,peaksepx,peaksepy,raw,relent,uni
    DN_CompareKSFit_logn = (
        'DN_CompareKSFit_logn',
        DN_CompareKSFit(whatDistn='logn'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ev,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,relent
    DN_CompareKSFit_ev = (
        'DN_CompareKSFit_ev',
        DN_CompareKSFit(whatDistn='ev'))

    # outs: adiff,olapint,peaksepx,peaksepy,relent
    # tags: adiff,distribution,ksdensity,locdep,olapint,peaksepx,peaksepy,raw,relent,uni,weibull
    DN_CompareKSFit_wbl = (
        'DN_CompareKSFit_wbl',
        DN_CompareKSFit(whatDistn='wbl'))

    # outs: entropy,max,numpeaks
    # tags: compare,distribution,entropy,ksdensity,max,numpeaks,raw,spreaddep
    DN_Compare_zscorex = (
        'DN_Compare_zscorex',
        DN_Compare_zscore())

    # outs: None
    # tags: distribution,locdep,moment,raw,shape
    DN_CustomSkewness_pearson = (
        'DN_CustomSkewness_pearson',
        DN_CustomSkewness(whichskew='pearson'))

    # outs: None
    # tags: distribution,moment,shape
    DN_CustomSkewness_bowley = (
        'DN_CustomSkewness_bowley',
        DN_CustomSkewness(whichskew='bowley'))

    # outs: arclength_010,arclength_050,arclength_100,arclength_200,area_005
    # outs: area_010,area_020,area_030,area_040,area_050
    # outs: asym,entropy,max,npeaks,numcross_005
    # outs: numcross_010,numcross_020,numcross_030,numcross_040,numcross_050
    # outs: plsym
    # tags: arclength,area,areaconst,crossconst,distribution,entropy,ksdensity,numpeaks,peakmax,raw,spreaddep,symmetry
    DN_FitKernelSmoothraw = (
        'DN_FitKernelSmoothraw',
        DN_FitKernelSmooth(varargin='numcross'))

    # outs: entropy,max
    # tags: distribution,entropy,ksdensity,peakmax
    DN_FitKernelSmoothzscore = (
        'DN_FitKernelSmoothzscore',
        DN_FitKernelSmooth())

    # outs: None
    # tags: distribution,fit
    DN_Fit_mle_geometric = (
        'DN_Fit_mle_geometric',
        DN_Fit_mle(fitwhat='geometric'))

    # outs: mean,std
    # tags: distribution,fit,location,locdep,raw,spread,spreaddep
    DN_Fit_mle_gaussian = (
        'DN_Fit_mle_gaussian',
        DN_Fit_mle(fitwhat='gaussian'))

    # outs: None
    # tags: distribution,locdep,raw,skewness,spreaddep
    DN_HighLowMu = (
        'DN_HighLowMu',
        DN_HighLowMu())

    # outs: None
    # tags: location
    DN_HistogramMode_10 = (
        'DN_HistogramMode_10',
        DN_HistogramMode(nbins=10))

    # outs: None
    # tags: location
    DN_HistogramMode_5 = (
        'DN_HistogramMode_5',
        DN_HistogramMode(nbins=5))

    # outs: None
    # tags: location
    DN_HistogramMode_20 = (
        'DN_HistogramMode_20',
        DN_HistogramMode(nbins=20))

    # outs: None
    # tags: location,locdep,raw
    DN_median = (
        'DN_median',
        DN_Mean(meantype='median'))

    # outs: None
    # tags: location,locdep,raw
    DN_hmean = (
        'DN_hmean',
        DN_Mean(meantype='harm'))

    # outs: None
    # tags: location,locdep,raw
    DN_mean = (
        'DN_mean',
        DN_Mean(meantype='norm'))

    # outs: None
    # tags: location,locdep,raw,spreaddep
    DN_rms = (
        'DN_rms',
        DN_Mean(meantype='rms'))

    # outs: None
    # tags: location,locdep,raw
    DN_midhinge = (
        'DN_midhinge',
        DN_Mean(meantype='midhinge'))

    # outs: None
    # tags: location,locdep,raw
    DN_iqm = (
        'DN_iqm',
        DN_Mean(meantype='iqm'))

    # outs: None
    # tags: distribution
    DN_max = (
        'DN_max',
        DN_MinMax(minormax='max'))

    # outs: None
    # tags: misc
    DN_min = (
        'DN_min',
        DN_MinMax(minormax='min'))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_3 = (
        'DN_Moments_raw_3',
        DN_Moments(n=3))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_10 = (
        'DN_Moments_raw_10',
        DN_Moments(n=10))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_11 = (
        'DN_Moments_raw_11',
        DN_Moments(n=11))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_8 = (
        'DN_Moments_raw_8',
        DN_Moments(n=8))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_9 = (
        'DN_Moments_raw_9',
        DN_Moments(n=9))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_6 = (
        'DN_Moments_raw_6',
        DN_Moments(n=6))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_7 = (
        'DN_Moments_raw_7',
        DN_Moments(n=7))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_4 = (
        'DN_Moments_raw_4',
        DN_Moments(n=4))

    # outs: None
    # tags: distribution,moment,raw,shape,spreaddep
    DN_Moments_raw_5 = (
        'DN_Moments_raw_5',
        DN_Moments(n=5))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_9 = (
        'DN_Moments_9',
        DN_Moments(n=9))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_8 = (
        'DN_Moments_8',
        DN_Moments(n=8))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_3 = (
        'DN_Moments_3',
        DN_Moments(n=3))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_5 = (
        'DN_Moments_5',
        DN_Moments(n=5))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_4 = (
        'DN_Moments_4',
        DN_Moments(n=4))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_7 = (
        'DN_Moments_7',
        DN_Moments(n=7))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_6 = (
        'DN_Moments_6',
        DN_Moments(n=6))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_11 = (
        'DN_Moments_11',
        DN_Moments(n=11))

    # outs: None
    # tags: distribution,moment,shape
    DN_Moments_10 = (
        'DN_Moments_10',
        DN_Moments(n=10))

    # outs: mdrm,mdrmd,mdrstd,mfexpa,mfexpadjr2
    # outs: mfexpb,mfexpc,mfexpr2,mfexprmse,mrm
    # outs: mrmd,mrstd,nfexpa,nfexpadjr2,nfexpb
    # outs: nfexpc,nfexpr2,nfexprmse,nfla,nfladjr2
    # outs: nflb,nflr2,nflrmse,stdrfexpa,stdrfexpadjr2
    # outs: stdrfexpb,stdrfexpc,stdrfexpr2,stdrfexprmse,stdrfla
    # outs: stdrfladjr2,stdrflb,stdrflr2,stdrflrmse,xcmerr1
    # outs: xcmerrn1
    # tags: distribution,outliers,stochastic
    DN_OutlierInclude_abs = (
        'DN_OutlierInclude_abs',
        DN_OutlierInclude(howth='abs'))

    # outs: mdrm,mdrmd,mdrstd,mfexpa,mfexpadjr2
    # outs: mfexpb,mfexpc,mfexpr2,mfexprmse,mrm
    # outs: mrmd,mrstd,nfexpa,nfexpadjr2,nfexpb
    # outs: nfexpc,nfexpr2,nfexprmse,nfla,nfladjr2
    # outs: nflb,nflr2,nflrmse,stdrfexpa,stdrfexpadjr2
    # outs: stdrfexpb,stdrfexpc,stdrfexpr2,stdrfexprmse,stdrfla
    # outs: stdrfladjr2,stdrflb,stdrflr2,stdrflrmse,xcmerr1
    # outs: xcmerrn1
    # tags: distribution,outliers,stochastic
    DN_OutlierInclude_p = (
        'DN_OutlierInclude_p',
        DN_OutlierInclude(howth='p'))

    # outs: mdrm,mdrmd,mdrstd,mfexpa,mfexpadjr2
    # outs: mfexpb,mfexpc,mfexpr2,mfexprmse,mrm
    # outs: mrmd,mrstd,nfexpa,nfexpadjr2,nfexpb
    # outs: nfexpc,nfexpr2,nfexprmse,nfla,nfladjr2
    # outs: nflb,nflr2,nflrmse,stdrfexpa,stdrfexpadjr2
    # outs: stdrfexpb,stdrfexpc,stdrfexpr2,stdrfexprmse,stdrfla
    # outs: stdrfladjr2,stdrflb,stdrflr2,stdrflrmse,xcmerr1
    # outs: xcmerrn1
    # tags: distribution,outliers,stochastic
    DN_OutlierInclude_n = (
        'DN_OutlierInclude_n',
        DN_OutlierInclude(howth='n'))

    # outs: mean,std
    # tags: distribution,outliers,spread
    DN_OutlierTest2 = (
        'DN_OutlierTest2',
        DN_OutlierTest(p=2))

    # outs: mean,std
    # tags: distribution,outliers,spread
    DN_OutlierTest5 = (
        'DN_OutlierTest5',
        DN_OutlierTest(p=5))

    # outs: mean,std
    # tags: distribution,outliers,spread
    DN_OutlierTest10 = (
        'DN_OutlierTest10',
        DN_OutlierTest(p=10))

    # outs: None
    # tags: locdep,raw
    DN_ProportionValues_positive = (
        'DN_ProportionValues_positive',
        DN_ProportionValues(propwhat='positive'))

    # outs: None
    # tags: locdep,raw
    DN_ProportionValues_geq0 = (
        'DN_ProportionValues_geq0',
        DN_ProportionValues(propwhat='geq0'))

    # outs: None
    # tags: raw
    DN_ProportionValues_zeros = (
        'DN_ProportionValues_zeros',
        DN_ProportionValues(propwhat='zeros'))

    # outs: None
    # tags: distribution
    DN_Quantile_60 = (
        'DN_Quantile_60',
        DN_Quantile(p=0.6))

    # outs: None
    # tags: distribution
    DN_Quantile_4 = (
        'DN_Quantile_4',
        DN_Quantile(p=0.04))

    # outs: None
    # tags: distribution
    DN_Quantile_5 = (
        'DN_Quantile_5',
        DN_Quantile(p=0.05))

    # outs: None
    # tags: distribution
    DN_Quantile_2 = (
        'DN_Quantile_2',
        DN_Quantile(p=0.02))

    # outs: None
    # tags: distribution
    DN_Quantile_3 = (
        'DN_Quantile_3',
        DN_Quantile(p=0.03))

    # outs: None
    # tags: distribution
    DN_Quantile_1 = (
        'DN_Quantile_1',
        DN_Quantile(p=0.01))

    # outs: None
    # tags: distribution
    DN_Quantile_10 = (
        'DN_Quantile_10',
        DN_Quantile(p=0.1))

    # outs: None
    # tags: distribution
    DN_Quantile_50 = (
        'DN_Quantile_50',
        DN_Quantile(p=0.5))

    # outs: None
    # tags: distribution
    DN_Quantile_90 = (
        'DN_Quantile_90',
        DN_Quantile(p=0.9))

    # outs: None
    # tags: distribution
    DN_Quantile_91 = (
        'DN_Quantile_91',
        DN_Quantile(p=0.91))

    # outs: None
    # tags: distribution
    DN_Quantile_92 = (
        'DN_Quantile_92',
        DN_Quantile(p=0.92))

    # outs: None
    # tags: distribution
    DN_Quantile_93 = (
        'DN_Quantile_93',
        DN_Quantile(p=0.93))

    # outs: None
    # tags: distribution
    DN_Quantile_94 = (
        'DN_Quantile_94',
        DN_Quantile(p=0.94))

    # outs: None
    # tags: distribution
    DN_Quantile_95 = (
        'DN_Quantile_95',
        DN_Quantile(p=0.95))

    # outs: None
    # tags: distribution
    DN_Quantile_96 = (
        'DN_Quantile_96',
        DN_Quantile(p=0.96))

    # outs: None
    # tags: distribution
    DN_Quantile_97 = (
        'DN_Quantile_97',
        DN_Quantile(p=0.97))

    # outs: None
    # tags: distribution
    DN_Quantile_98 = (
        'DN_Quantile_98',
        DN_Quantile(p=0.98))

    # outs: None
    # tags: distribution
    DN_Quantile_99 = (
        'DN_Quantile_99',
        DN_Quantile(p=0.99))

    # outs: None
    # tags: distribution
    DN_Quantile_30 = (
        'DN_Quantile_30',
        DN_Quantile(p=0.3))

    # outs: None
    # tags: distribution
    DN_Quantile_40 = (
        'DN_Quantile_40',
        DN_Quantile(p=0.4))

    # outs: None
    # tags: distribution
    DN_Quantile_70 = (
        'DN_Quantile_70',
        DN_Quantile(p=0.7))

    # outs: None
    # tags: distribution
    DN_Quantile_80 = (
        'DN_Quantile_80',
        DN_Quantile(p=0.8))

    # outs: None
    # tags: distribution
    DN_Quantile_20 = (
        'DN_Quantile_20',
        DN_Quantile(p=0.2))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absclose_01 = (
        'DN_RemovePoints_absclose_01',
        DN_RemovePoints(howtorem='absclose', p=0.1))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absclose_05 = (
        'DN_RemovePoints_absclose_05',
        DN_RemovePoints(howtorem='absclose', p=0.5))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absfar_08 = (
        'DN_RemovePoints_absfar_08',
        DN_RemovePoints(howtorem='absfar', p=0.8))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absfar_05 = (
        'DN_RemovePoints_absfar_05',
        DN_RemovePoints(howtorem='absfar', p=0.5))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absclose_08 = (
        'DN_RemovePoints_absclose_08',
        DN_RemovePoints(howtorem='absclose', p=0.8))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_min_08 = (
        'DN_RemovePoints_min_08',
        DN_RemovePoints(howtorem='min', p=0.8))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_max_08 = (
        'DN_RemovePoints_max_08',
        DN_RemovePoints(howtorem='max', p=0.8))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_min_01 = (
        'DN_RemovePoints_min_01',
        DN_RemovePoints(howtorem='min', p=0.1))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_max_05 = (
        'DN_RemovePoints_max_05',
        DN_RemovePoints(howtorem='max', p=0.5))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_max_01 = (
        'DN_RemovePoints_max_01',
        DN_RemovePoints(howtorem='max', p=0.1))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_absfar_01 = (
        'DN_RemovePoints_absfar_01',
        DN_RemovePoints(howtorem='absfar', p=0.1))

    # outs: ac2diff,ac2rat,ac3diff,ac3rat,fzcacrat
    # outs: kurtosisrat,mean,median,skewnessrat,std
    # outs: sumabsacfdiff
    # tags: correlation,distribution,outliers
    DN_RemovePoints_min_05 = (
        'DN_RemovePoints_min_05',
        DN_RemovePoints(howtorem='min', p=0.5))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,exp1,gof
    DN_SimpleFit_exp1_ks = (
        'DN_SimpleFit_exp1_ks',
        DN_SimpleFit(dmodel='exp1', nbins=0))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: adjr2,model,r2,resAC1,resAC2,resruns,rmse,sin1
    DN_SimpleFit_sin1 = (
        'DN_SimpleFit_sin1',
        DN_SimpleFit(dmodel='sin1'))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: adjr2,model,r2,resAC1,resAC2,resruns,rmse,sin2
    DN_SimpleFit_sin2 = (
        'DN_SimpleFit_sin2',
        DN_SimpleFit(dmodel='sin2'))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: adjr2,model,r2,resAC1,resAC2,resruns,rmse,sin3
    DN_SimpleFit_sin3 = (
        'DN_SimpleFit_sin3',
        DN_SimpleFit(dmodel='sin3'))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss1,gof
    DN_SimpleFit_gauss1_h30 = (
        'DN_SimpleFit_gauss1_h30',
        DN_SimpleFit(dmodel='gauss1', nbins=30))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss2,gof
    DN_SimpleFit_gauss2_h10 = (
        'DN_SimpleFit_gauss2_h10',
        DN_SimpleFit(dmodel='gauss2', nbins=10))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gof,power1
    DN_SimpleFit_power1_h10 = (
        'DN_SimpleFit_power1_h10',
        DN_SimpleFit(dmodel='power1', nbins=10))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,exp1,gof
    DN_SimpleFit_exp1_h10 = (
        'DN_SimpleFit_exp1_h10',
        DN_SimpleFit(dmodel='exp1', nbins=10))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: adjr2,fourier1,model,r2,resAC1,resAC2,resruns,rmse
    DN_SimpleFit_fourier1 = (
        'DN_SimpleFit_fourier1',
        DN_SimpleFit(dmodel='fourier1'))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss1,gof
    DN_SimpleFit_gauss1_ks = (
        'DN_SimpleFit_gauss1_ks',
        DN_SimpleFit(dmodel='gauss1', nbins=0))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gof,power1
    DN_SimpleFit_power1_ks = (
        'DN_SimpleFit_power1_ks',
        DN_SimpleFit(dmodel='power1', nbins=0))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss1,gof
    DN_SimpleFit_gauss1_h10 = (
        'DN_SimpleFit_gauss1_h10',
        DN_SimpleFit(dmodel='gauss1', nbins=10))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gof,power1
    DN_SimpleFit_power1_h30 = (
        'DN_SimpleFit_power1_h30',
        DN_SimpleFit(dmodel='power1', nbins=30))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss2,gof
    DN_SimpleFit_gauss2_h30 = (
        'DN_SimpleFit_gauss2_h30',
        DN_SimpleFit(dmodel='gauss2', nbins=30))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,gauss2,gof
    DN_SimpleFit_gauss2_ks = (
        'DN_SimpleFit_gauss2_ks',
        DN_SimpleFit(dmodel='gauss2', nbins=0))

    # outs: adjr2,r2,resAC1,resAC2,resruns
    # outs: rmse
    # tags: distribution,exp1,gof
    DN_SimpleFit_exp1_h30 = (
        'DN_SimpleFit_exp1_h30',
        DN_SimpleFit(dmodel='exp1', nbins=30))

    # outs: None
    # tags: raw,spread,spreaddep
    DN_Spread_std = (
        'DN_Spread_std',
        DN_Spread(SpreadMeasure='std'))

    # outs: None
    # tags: diff,raw,spread,spreaddep
    DN_Spread_std_diff = (
        'DN_Spread_std_diff',
        DN_Spread(SpreadMeasure='std'))

    # outs: None
    # tags: raw,spread,spreaddep
    DN_Spread_iqr = (
        'DN_Spread_iqr',
        DN_Spread(SpreadMeasure='iqr'))

    # outs: None
    # tags: raw,spread,spreaddep
    DN_Spread_mead = (
        'DN_Spread_mead',
        DN_Spread(SpreadMeasure='mead'))

    # outs: None
    # tags: raw,spread,spreaddep
    DN_Spread_mad = (
        'DN_Spread_mad',
        DN_Spread(SpreadMeasure='mad'))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_2 = (
        'DN_TrimmedMean_2',
        DN_TrimmedMean(n=2))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_1 = (
        'DN_TrimmedMean_1',
        DN_TrimmedMean(n=1))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_5 = (
        'DN_TrimmedMean_5',
        DN_TrimmedMean(n=5))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_50 = (
        'DN_TrimmedMean_50',
        DN_TrimmedMean(n=50))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_25 = (
        'DN_TrimmedMean_25',
        DN_TrimmedMean(n=25))

    # outs: None
    # tags: location,locdep,raw
    DN_TrimmedMean_10 = (
        'DN_TrimmedMean_10',
        DN_TrimmedMean(n=10))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_30 = (
        'DN_Withinp_30',
        DN_Withinp(p=3))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_20 = (
        'DN_Withinp_20',
        DN_Withinp(p=2))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_25 = (
        'DN_Withinp_25',
        DN_Withinp(p=2.5))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_10 = (
        'DN_Withinp_10',
        DN_Withinp(p=1))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_15 = (
        'DN_Withinp_15',
        DN_Withinp(p=1.5))

    # outs: None
    # tags: distribution,spread
    DN_Withinp_05 = (
        'DN_Withinp_05',
        DN_Withinp(p=0.5))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_4 = (
        'DN_cv_4',
        DN_cv(k=4))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_5 = (
        'DN_cv_5',
        DN_cv(k=5))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_6 = (
        'DN_cv_6',
        DN_cv(k=6))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_1 = (
        'DN_cv_1',
        DN_cv(k=1))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_2 = (
        'DN_cv_2',
        DN_cv(k=2))

    # outs: None
    # tags: cv,locdep,raw,spread,spreaddep
    DN_cv_3 = (
        'DN_cv_3',
        DN_cv(k=3))

    # outs: None
    # tags: distribution,gof,lengthdep
    DN_nlogL_norm = (
        'DN_nlogL_norm',
        DN_nlogL_norm())

    # outs: None
    # tags: distribution,spread
    DN_pleft_01 = (
        'DN_pleft_01',
        DN_pleft(th=0.1))

    # outs: None
    # tags: distribution,spread
    DN_pleft_03 = (
        'DN_pleft_03',
        DN_pleft(th=0.3))

    # outs: None
    # tags: distribution,spread
    DN_pleft_04 = (
        'DN_pleft_04',
        DN_pleft(th=0.4))

    # outs: None
    # tags: distribution,spread
    DN_pleft_05 = (
        'DN_pleft_05',
        DN_pleft(th=0.5))

    # outs: None
    # tags: distribution,spread
    DN_pleft_005 = (
        'DN_pleft_005',
        DN_pleft(th=0.05))

    # outs: None
    # tags: distribution,spread
    DN_pleft_02 = (
        'DN_pleft_02',
        DN_pleft(th=0.2))

    # outs: None
    # tags: periodicity
    DT_IsSeasonal = (
        'DT_IsSeasonal',
        DT_IsSeasonal())

    # outs: None
    # tags: entropy
    ApEn1_02 = (
        'ApEn1_02',
        EN_ApEn(mnom=1, rth=0.2))

    # outs: None
    # tags: entropy
    ApEn2_02 = (
        'ApEn2_02',
        EN_ApEn(mnom=2, rth=0.2))

    # outs: None
    # tags: entropy
    ApEn2_01 = (
        'ApEn2_01',
        EN_ApEn(mnom=2, rth=0.1))

    # outs: None
    # tags: entropy
    ApEn1_01 = (
        'ApEn1_01',
        EN_ApEn(mnom=1, rth=0.1))

    # outs: None
    # tags: entropy
    EN_histen_ks__01 = (
        'EN_histen_ks__01',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.1))

    # outs: None
    # tags: entropy
    EN_histen_ks__02 = (
        'EN_histen_ks__02',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.2))

    # outs: None
    # tags: entropy
    EN_histen_ks__03 = (
        'EN_histen_ks__03',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.3))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_005 = (
        'EN_histen_hist_10_005',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.05))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_001 = (
        'EN_histen_hist_10_001',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.01))

    # outs: None
    # tags: entropy
    EN_histen_ks_01_0 = (
        'EN_histen_ks_01_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.1, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_ks_05_0 = (
        'EN_histen_ks_05_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.5, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_02 = (
        'EN_histen_hist_10_02',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.2))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_01 = (
        'EN_histen_hist_10_01',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.1))

    # outs: None
    # tags: entropy
    EN_histen_hist_5_0 = (
        'EN_histen_hist_5_0',
        EN_DistributionEntropy(HistorKS='hist', nbins=5, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_002 = (
        'EN_histen_hist_10_002',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.02))

    # outs: None
    # tags: entropy
    EN_histen_ks_1_0 = (
        'EN_histen_ks_1_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=1, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_ks_02_0 = (
        'EN_histen_ks_02_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.2, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_01_0 = (
        'EN_histen_raw_ks_01_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.1, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__01 = (
        'EN_histen_raw_ks__01',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.1))

    # outs: None
    # tags: entropy
    EN_histen_hist_20_0 = (
        'EN_histen_hist_20_0',
        EN_DistributionEntropy(HistorKS='hist', nbins=20, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_1_0 = (
        'EN_histen_raw_ks_1_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=1, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__03 = (
        'EN_histen_raw_ks__03',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.3))

    # outs: None
    # tags: entropy
    EN_histen_ks_005_0 = (
        'EN_histen_ks_005_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.05, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_ks_001_0 = (
        'EN_histen_ks_001_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.01, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_05_0 = (
        'EN_histen_raw_ks_05_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.5, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_0 = (
        'EN_histen_hist_10_0',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_02_0 = (
        'EN_histen_raw_ks_02_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.2, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__02 = (
        'EN_histen_raw_ks__02',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.2))

    # outs: None
    # tags: entropy
    EN_histen_hist_50_0 = (
        'EN_histen_hist_50_0',
        EN_DistributionEntropy(HistorKS='hist', nbins=50, olremp=0))

    # outs: None
    # tags: entropy
    EN_histen_hist_10_03 = (
        'EN_histen_hist_10_03',
        EN_DistributionEntropy(HistorKS='hist', nbins=10, olremp=0.3))

    # outs: None
    # tags: entropy
    EN_histen_ks__001 = (
        'EN_histen_ks__001',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.01))

    # outs: None
    # tags: entropy
    EN_histen_ks__002 = (
        'EN_histen_ks__002',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.02))

    # outs: None
    # tags: entropy
    EN_histen_ks__005 = (
        'EN_histen_ks__005',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.05))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__005 = (
        'EN_histen_raw_ks__005',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.05))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__002 = (
        'EN_histen_raw_ks__002',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.02))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks__001 = (
        'EN_histen_raw_ks__001',
        EN_DistributionEntropy(HistorKS='ks', nbins=(), olremp=0.01))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_001_0 = (
        'EN_histen_raw_ks_001_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.01, olremp=0))

    # outs: None
    # tags: entropy,raw,spreaddep
    EN_histen_raw_ks_005_0 = (
        'EN_histen_raw_ks_005_0',
        EN_DistributionEntropy(HistorKS='ks', nbins=0.05, olremp=0))

    # outs: None
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2_2 = (
        'MS_shannon_2_2',
        EN_MS_shannon(nbin=2, depth=2))

    # outs: None
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2_3 = (
        'MS_shannon_2_3',
        EN_MS_shannon(nbin=2, depth=3))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2_1t10 = (
        'MS_shannon_2_1t10',
        EN_MS_shannon(nbin=2, depth=MatlabSequence('1:10')))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2t10_3 = (
        'MS_shannon_2t10_3',
        EN_MS_shannon(nbin=MatlabSequence('2:10'), depth=3))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_4_1t10 = (
        'MS_shannon_4_1t10',
        EN_MS_shannon(nbin=4, depth=MatlabSequence('1:10')))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2t10_2 = (
        'MS_shannon_2t10_2',
        EN_MS_shannon(nbin=MatlabSequence('2:10'), depth=2))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_2t10_4 = (
        'MS_shannon_2t10_4',
        EN_MS_shannon(nbin=MatlabSequence('2:10'), depth=4))

    # outs: maxent,meanent,medent,minent,stdent
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_3_1t10 = (
        'MS_shannon_3_1t10',
        EN_MS_shannon(nbin=3, depth=MatlabSequence('1:10')))

    # outs: None
    # tags: MichaelSmall,entropy,mex,shannon
    MS_shannon_3_2 = (
        'MS_shannon_3_2',
        EN_MS_shannon(nbin=3, depth=2))

    # outs: None
    # tags: entropy
    EN_PermEn_3 = (
        'EN_PermEn_3',
        EN_PermEn(ordd=3))

    # outs: None
    # tags: entropy
    EN_PermEn_5 = (
        'EN_PermEn_5',
        EN_PermEn(ordd=5))

    # outs: None
    # tags: entropy
    EN_PermEn_2 = (
        'EN_PermEn_2',
        EN_PermEn(ordd=2))

    # outs: None
    # tags: entropy
    EN_PermEn_4 = (
        'EN_PermEn_4',
        EN_PermEn(ordd=4))

    # outs: None
    # tags: entropy
    RM_entropy = (
        'RM_entropy',
        EN_RM_entropy())

    # outs: ac1diff,ac1fexpa,ac1fexpadjr2,ac1fexpb,ac1fexpr2
    # outs: ac1fexprmse,ac1hp,ac2diff,ac2fexpa,ac2fexpadjr2
    # outs: ac2fexpb,ac2fexpr2,ac2fexprmse,ac2hp,ac3diff
    # outs: ac3fexpa,ac3fexpadjr2,ac3fexpb,ac3fexpr2,ac3fexprmse
    # outs: ac3hp,ac4diff,ac4fexpa,ac4fexpadjr2,ac4fexpb
    # outs: ac4fexpr2,ac4fexprmse,ac4hp,d1fexpa,d1fexpadjr2
    # outs: d1fexpb,d1fexpc,d1fexpr2,d1fexprmse,d1hp
    # outs: sampen2_02diff,sampen2_02fexpa,sampen2_02fexpadjr2,sampen2_02fexpb,sampen2_02fexpc
    # outs: sampen2_02fexpr2,sampen2_02fexprmse,sampen2_02hp,statav5diff,statav5fexpa
    # outs: statav5fexpadjr2,statav5fexpb,statav5fexpc,statav5fexpr2,statav5fexprmse
    # outs: statav5hp,swss5_1diff,swss5_1fexpa,swss5_1fexpadjr2,swss5_1fexpb
    # outs: swss5_1fexpc,swss5_1fexpr2,swss5_1fexprmse,swss5_1hp,xc1diff
    # outs: xc1fexpa,xc1fexpadjr2,xc1fexpb,xc1fexpr2,xc1fexprmse
    # outs: xc1hp,xcn1diff,xcn1fexpa,xcn1fexpadjr2,xcn1fexpb
    # outs: xcn1fexpr2,xcn1fexprmse,xcn1hp
    # tags: entropy,lengthdep,slow,stochastic
    EN_Randomize_statdist = (
        'EN_Randomize_statdist',
        EN_Randomize(randomizeHow='statdist'))

    # outs: ac1diff,ac1fexpa,ac1fexpadjr2,ac1fexpb,ac1fexpr2
    # outs: ac1fexprmse,ac1hp,ac2diff,ac2fexpa,ac2fexpadjr2
    # outs: ac2fexpb,ac2fexpr2,ac2fexprmse,ac2hp,ac3diff
    # outs: ac3fexpa,ac3fexpadjr2,ac3fexpb,ac3fexpr2,ac3fexprmse
    # outs: ac3hp,ac4diff,ac4fexpa,ac4fexpadjr2,ac4fexpb
    # outs: ac4fexpr2,ac4fexprmse,ac4hp,d1fexpa,d1fexpadjr2
    # outs: d1fexpb,d1fexpc,d1fexpr2,d1fexprmse,d1hp
    # outs: sampen2_02diff,sampen2_02fexpa,sampen2_02fexpadjr2,sampen2_02fexpb,sampen2_02fexpc
    # outs: sampen2_02fexpr2,sampen2_02fexprmse,sampen2_02hp,statav5diff,statav5fexpa
    # outs: statav5fexpadjr2,statav5fexpb,statav5fexpc,statav5fexpr2,statav5fexprmse
    # outs: statav5hp,swss5_1diff,swss5_1fexpa,swss5_1fexpadjr2,swss5_1fexpb
    # outs: swss5_1fexpc,swss5_1fexpr2,swss5_1fexprmse,swss5_1hp,xc1diff
    # outs: xc1fexpa,xc1fexpadjr2,xc1fexpb,xc1fexpr2,xc1fexprmse
    # outs: xc1hp,xcn1diff,xcn1fexpa,xcn1fexpadjr2,xcn1fexpb
    # outs: xcn1fexpr2,xcn1fexprmse,xcn1hp
    # tags: entropy,lengthdep,slow,stochastic
    EN_Randomize_permute = (
        'EN_Randomize_permute',
        EN_Randomize(randomizeHow='permute'))

    # outs: ac1diff,ac1fexpa,ac1fexpadjr2,ac1fexpb,ac1fexpr2
    # outs: ac1fexprmse,ac1hp,ac2diff,ac2fexpa,ac2fexpadjr2
    # outs: ac2fexpb,ac2fexpr2,ac2fexprmse,ac2hp,ac3diff
    # outs: ac3fexpa,ac3fexpadjr2,ac3fexpb,ac3fexpr2,ac3fexprmse
    # outs: ac3hp,ac4diff,ac4fexpa,ac4fexpadjr2,ac4fexpb
    # outs: ac4fexpr2,ac4fexprmse,ac4hp,d1fexpa,d1fexpadjr2
    # outs: d1fexpb,d1fexpc,d1fexpr2,d1fexprmse,d1hp
    # outs: sampen2_02diff,sampen2_02fexpa,sampen2_02fexpadjr2,sampen2_02fexpb,sampen2_02fexpc
    # outs: sampen2_02fexpr2,sampen2_02fexprmse,sampen2_02hp,statav5diff,statav5fexpa
    # outs: statav5fexpadjr2,statav5fexpb,statav5fexpc,statav5fexpr2,statav5fexprmse
    # outs: statav5hp,swss5_1diff,swss5_1fexpa,swss5_1fexpadjr2,swss5_1fexpb
    # outs: swss5_1fexpc,swss5_1fexpr2,swss5_1fexprmse,swss5_1hp,xc1diff
    # outs: xc1fexpa,xc1fexpadjr2,xc1fexpb,xc1fexpr2,xc1fexprmse
    # outs: xc1hp,xcn1diff,xcn1fexpa,xcn1fexpadjr2,xcn1fexpb
    # outs: xcn1fexpr2,xcn1fexprmse,xcn1hp
    # tags: entropy,lengthdep,slow,stochastic
    EN_Randomize_dyndist = (
        'EN_Randomize_dyndist',
        EN_Randomize(randomizeHow='dyndist'))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: entropy,sampen
    EN_SampEn_4_01 = (
        'EN_SampEn_4_01',
        EN_SampEn(M=4, r=0.1))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: controlen,entropy
    EN_SampEn_4_02_diff1 = (
        'EN_SampEn_4_02_diff1',
        EN_SampEn(M=4, r=0.2, preprocess='diff1'))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: entropy,sampen
    EN_SampEn_4_02 = (
        'EN_SampEn_4_02',
        EN_SampEn(M=4, r=0.2))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: entropy,sampen
    EN_SampEn_4_03 = (
        'EN_SampEn_4_03',
        EN_SampEn(M=4, r=0.3))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: entropy,sampen
    EN_SampEn_4_015 = (
        'EN_SampEn_4_015',
        EN_SampEn(M=4, r=0.15))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: entropy,sampen
    EN_SampEn_4_005 = (
        'EN_SampEn_4_005',
        EN_SampEn(M=4, r=0.05))

    # outs: meanchp,meanchsampen,p1,p2,p3
    # outs: p4,sampen1,sampen2,sampen3,sampen4
    # tags: controlen,entropy
    EN_SampEn_4_01_diff1 = (
        'EN_SampEn_4_01_diff1',
        EN_SampEn(M=4, r=0.1, preprocess='diff1'))

    # outs: None
    # tags: entropy,shannonpdf
    EN_Shannonpdf = (
        'EN_Shannonpdf',
        EN_Shannonpdf())

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent1 = (
        'EN_wentropy_threshent1',
        EN_wentropy(whaten='threshold', p=1))

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent01 = (
        'EN_wentropy_threshent01',
        EN_wentropy(whaten='threshold', p=0.1))

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent05 = (
        'EN_wentropy_threshent05',
        EN_wentropy(whaten='threshold', p=0.5))

    # outs: None
    # tags: entropy,shannon
    EN_wentropy_shannon = (
        'EN_wentropy_shannon',
        EN_wentropy(whaten='shannon'))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent15 = (
        'EN_wentropy_sureent15',
        EN_wentropy(whaten='sure', p=1.5))

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent15 = (
        'EN_wentropy_threshent15',
        EN_wentropy(whaten='threshold', p=1.5))

    # outs: None
    # tags: entropy,logenergy
    EN_wentropy_logenent = (
        'EN_wentropy_logenent',
        EN_wentropy(whaten='logenergy'))

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent02 = (
        'EN_wentropy_threshent02',
        EN_wentropy(whaten='threshold', p=0.2))

    # outs: None
    # tags: entropy,threshold
    EN_wentropy_threshent2 = (
        'EN_wentropy_threshent2',
        EN_wentropy(whaten='threshold', p=2))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent2 = (
        'EN_wentropy_sureent2',
        EN_wentropy(whaten='sure', p=2))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent1 = (
        'EN_wentropy_sureent1',
        EN_wentropy(whaten='sure', p=1))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent05 = (
        'EN_wentropy_sureent05',
        EN_wentropy(whaten='sure', p=0.5))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent01 = (
        'EN_wentropy_sureent01',
        EN_wentropy(whaten='sure', p=0.1))

    # outs: None
    # tags: entropy,sure
    EN_wentropy_sureent02 = (
        'EN_wentropy_sureent02',
        EN_wentropy(whaten='sure', p=0.2))

    # outs: iqrq,maxq,meankickf,meanq,meanqover
    # outs: mediankickf,medianq,minq,pkick,stdkickf
    # outs: stdq
    # tags: outliers
    EX_MovingThreshold_1_002 = (
        'EX_MovingThreshold_1_002',
        EX_MovingThreshold(a=1, b=0.02))

    # outs: iqrq,maxq,meankickf,meanq,meanqover
    # outs: mediankickf,medianq,minq,pkick,stdkickf
    # outs: stdq
    # tags: outliers
    EX_MovingThreshold_01_01 = (
        'EX_MovingThreshold_01_01',
        EX_MovingThreshold(a=0.1, b=0.1))

    # outs: iqrq,maxq,meankickf,meanq,meanqover
    # outs: mediankickf,medianq,minq,pkick,stdkickf
    # outs: stdq
    # tags: outliers
    EX_MovingThreshold_1_01 = (
        'EX_MovingThreshold_1_01',
        EX_MovingThreshold(a=1, b=0.1))

    # outs: iqrq,maxq,meankickf,meanq,meanqover
    # outs: mediankickf,medianq,minq,pkick,stdkickf
    # outs: stdq
    # tags: outliers
    EX_MovingThreshold_01_002 = (
        'EX_MovingThreshold_01_002',
        EX_MovingThreshold(a=0.1, b=0.02))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_mean3 = (
        'FC_LocalSimple_mean3',
        FC_LocalSimple(fmeth='mean', ltrain=3))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_mean2 = (
        'FC_LocalSimple_mean2',
        FC_LocalSimple(fmeth='mean', ltrain=2))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_mean1 = (
        'FC_LocalSimple_mean1',
        FC_LocalSimple(fmeth='mean', ltrain=1))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_lfit4 = (
        'FC_LocalSimple_lfit4',
        FC_LocalSimple(fmeth='lfit', ltrain=4))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_lfittau = (
        'FC_LocalSimple_lfittau',
        FC_LocalSimple(fmeth='lfit', ltrain='ac'))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_mean4 = (
        'FC_LocalSimple_mean4',
        FC_LocalSimple(fmeth='mean', ltrain=4))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_lfit2 = (
        'FC_LocalSimple_lfit2',
        FC_LocalSimple(fmeth='lfit', ltrain=2))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_lfit3 = (
        'FC_LocalSimple_lfit3',
        FC_LocalSimple(fmeth='lfit', ltrain=3))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_lfit5 = (
        'FC_LocalSimple_lfit5',
        FC_LocalSimple(fmeth='lfit', ltrain=5))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_meantau = (
        'FC_LocalSimple_meantau',
        FC_LocalSimple(fmeth='mean', ltrain='ac'))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_median7 = (
        'FC_LocalSimple_median7',
        FC_LocalSimple(fmeth='median', ltrain=7))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_median5 = (
        'FC_LocalSimple_median5',
        FC_LocalSimple(fmeth='median', ltrain=5))

    # outs: ac1,ac2,gofnadjr2,meanabserr,meanerr
    # outs: rmserr,stderr,swm,sws,taures
    # outs: tauresrat
    # tags: forecasting
    FC_LocalSimple_median3 = (
        'FC_LocalSimple_median3',
        FC_LocalSimple(fmeth='median', ltrain=3))

    # outs: ac1_chn,ac1_meansgndiff,ac1_stdn,ac2_chn,ac2_meansgndiff
    # outs: ac2_stdn,rmserr_chn,rmserr_meansgndiff,rmserr_peakpos,rmserr_peaksize
    # outs: swm_chn,swm_meansgndiff,swm_stdn,sws_chn,sws_fexp_a
    # outs: sws_fexp_adjr2,sws_fexp_b,sws_fexp_c,sws_fexp_rmse,sws_meansgndiff
    # outs: sws_stdn,xcorrstdrmserr
    # tags: forecasting
    FC_LoopLocalSimple_mean = (
        'FC_LoopLocalSimple_mean',
        FC_LoopLocalSimple(fmeth='mean'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_50_3_q = (
        'FC_Surprise_dist_50_3_q',
        FC_Surprise(whatinf='dist', memory=50, ng=3, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_50_3_udq = (
        'FC_Surprise_dist_50_3_udq',
        FC_Surprise(whatinf='dist', memory=50, ng=3, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_20_2_udq = (
        'FC_Surprise_T1_20_2_udq',
        FC_Surprise(whatinf='T1', memory=20, ng=2, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_10_tau_m2quad = (
        'FC_Surprise_T1_10_tau_m2quad',
        FC_Surprise(whatinf='T1', memory=10, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_10_tau_m2quad = (
        'FC_Surprise_dist_10_tau_m2quad',
        FC_Surprise(whatinf='dist', memory=10, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_5_1_m2quad = (
        'FC_Surprise_dist_5_1_m2quad',
        FC_Surprise(whatinf='dist', memory=5, ng=1, cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_5_tau_m2quad = (
        'FC_Surprise_dist_5_tau_m2quad',
        FC_Surprise(whatinf='dist', memory=5, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_20_tau_m2quad = (
        'FC_Surprise_T1_20_tau_m2quad',
        FC_Surprise(whatinf='T1', memory=20, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_100_5_q = (
        'FC_Surprise_T1_100_5_q',
        FC_Surprise(whatinf='T1', memory=100, ng=5, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_100_4_q = (
        'FC_Surprise_dist_100_4_q',
        FC_Surprise(whatinf='dist', memory=100, ng=4, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_50_tau_m2quad = (
        'FC_Surprise_T1_50_tau_m2quad',
        FC_Surprise(whatinf='T1', memory=50, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_20_2_q = (
        'FC_Surprise_T1_20_2_q',
        FC_Surprise(whatinf='T1', memory=20, ng=2, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_100_5_udq = (
        'FC_Surprise_T2_100_5_udq',
        FC_Surprise(whatinf='T2', memory=100, ng=5, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_100_4_q = (
        'FC_Surprise_T2_100_4_q',
        FC_Surprise(whatinf='T2', memory=100, ng=4, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_50_3_udq = (
        'FC_Surprise_T1_50_3_udq',
        FC_Surprise(whatinf='T1', memory=50, ng=3, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_50_3_q = (
        'FC_Surprise_T2_50_3_q',
        FC_Surprise(whatinf='T2', memory=50, ng=3, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_100_tau_m2quad = (
        'FC_Surprise_T2_100_tau_m2quad',
        FC_Surprise(whatinf='T2', memory=100, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_100_4_udq = (
        'FC_Surprise_T2_100_4_udq',
        FC_Surprise(whatinf='T2', memory=100, ng=4, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_50_3_q = (
        'FC_Surprise_T1_50_3_q',
        FC_Surprise(whatinf='T1', memory=50, ng=3, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_20_tau_m2quad = (
        'FC_Surprise_dist_20_tau_m2quad',
        FC_Surprise(whatinf='dist', memory=20, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_100_4_udq = (
        'FC_Surprise_T1_100_4_udq',
        FC_Surprise(whatinf='T1', memory=100, ng=4, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_20_2_q = (
        'FC_Surprise_T2_20_2_q',
        FC_Surprise(whatinf='T2', memory=20, ng=2, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_100_4_udq = (
        'FC_Surprise_dist_100_4_udq',
        FC_Surprise(whatinf='dist', memory=100, ng=4, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_100_5_udq = (
        'FC_Surprise_T1_100_5_udq',
        FC_Surprise(whatinf='T1', memory=100, ng=5, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_5_2_q = (
        'FC_Surprise_dist_5_2_q',
        FC_Surprise(whatinf='dist', memory=5, ng=2, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_20_2_q = (
        'FC_Surprise_dist_20_2_q',
        FC_Surprise(whatinf='dist', memory=20, ng=2, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_20_2_udq = (
        'FC_Surprise_T2_20_2_udq',
        FC_Surprise(whatinf='T2', memory=20, ng=2, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_100_5_q = (
        'FC_Surprise_T2_100_5_q',
        FC_Surprise(whatinf='T2', memory=100, ng=5, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_100_5_q = (
        'FC_Surprise_dist_100_5_q',
        FC_Surprise(whatinf='dist', memory=100, ng=5, cgmeth='quantile'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_5_2_udq = (
        'FC_Surprise_dist_5_2_udq',
        FC_Surprise(whatinf='dist', memory=5, ng=2, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_50_3_udq = (
        'FC_Surprise_T2_50_3_udq',
        FC_Surprise(whatinf='T2', memory=50, ng=3, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_20_2_udq = (
        'FC_Surprise_dist_20_2_udq',
        FC_Surprise(whatinf='dist', memory=20, ng=2, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_dist_100_5_udq = (
        'FC_Surprise_dist_100_5_udq',
        FC_Surprise(whatinf='dist', memory=100, ng=5, cgmeth='updown'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T2_50_tau_m2quad = (
        'FC_Surprise_T2_50_tau_m2quad',
        FC_Surprise(whatinf='T2', memory=50, ng='tau', cgmeth='embed2quadrants'))

    # outs: lq,max,mean,median,min
    # outs: std,tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_100_4_q = (
        'FC_Surprise_T1_100_4_q',
        FC_Surprise(whatinf='T1', memory=100, ng=4, cgmeth='quantile'))

    # outs: lq,max,mean,median,std
    # outs: tstat,uq
    # tags: information,stochastic,symbolic
    FC_Surprise_T1_10_1_m2quad = (
        'FC_Surprise_T1_10_1_m2quad',
        FC_Surprise(whatinf='T1', memory=10, ng=1, cgmeth='embed2quadrants'))

    # outs: None
    # tags: distribution,hypothesistest,ks,raw
    HT_DistributionTest_ks_beta = (
        'HT_DistributionTest_ks_beta',
        HT_DistributionTest(thetest='ks', thedistn='beta'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2rayl100 = (
        'HT_DistributionTest_chi2rayl100',
        HT_DistributionTest(thetest='chi2gof', thedistn='rayleigh', nbins=100))

    # outs: None
    # tags: distribution,hypothesistest,lillie,raw
    HT_DistributionTest_lillie_norm = (
        'HT_DistributionTest_lillie_norm',
        HT_DistributionTest(thetest='lillie', thedistn='norm'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2logn5 = (
        'HT_DistributionTest_chi2logn5',
        HT_DistributionTest(thetest='chi2gof', thedistn='logn', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2rayl50 = (
        'HT_DistributionTest_chi2rayl50',
        HT_DistributionTest(thetest='chi2gof', thedistn='rayleigh', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2beta25 = (
        'HT_DistributionTest_chi2beta25',
        HT_DistributionTest(thetest='chi2gof', thedistn='beta', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2wbl100 = (
        'HT_DistributionTest_chi2wbl100',
        HT_DistributionTest(thetest='chi2gof', thedistn='wbl', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2rayl25 = (
        'HT_DistributionTest_chi2rayl25',
        HT_DistributionTest(thetest='chi2gof', thedistn='rayleigh', nbins=25))

    # outs: None
    # tags: distribution,hypothesistest,ks,locdep,raw
    HT_DistributionTest_ks_logn = (
        'HT_DistributionTest_ks_logn',
        HT_DistributionTest(thetest='ks', thedistn='logn'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2exp10 = (
        'HT_DistributionTest_chi2exp10',
        HT_DistributionTest(thetest='chi2gof', thedistn='exp', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2uni100 = (
        'HT_DistributionTest_chi2uni100',
        HT_DistributionTest(thetest='chi2gof', thedistn='uni', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2norm50 = (
        'HT_DistributionTest_chi2norm50',
        HT_DistributionTest(thetest='chi2gof', thedistn='norm', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2logn50 = (
        'HT_DistributionTest_chi2logn50',
        HT_DistributionTest(thetest='chi2gof', thedistn='logn', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2beta10 = (
        'HT_DistributionTest_chi2beta10',
        HT_DistributionTest(thetest='chi2gof', thedistn='beta', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2gam10 = (
        'HT_DistributionTest_chi2gam10',
        HT_DistributionTest(thetest='chi2gof', thedistn='gamma', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2ev50 = (
        'HT_DistributionTest_chi2ev50',
        HT_DistributionTest(thetest='chi2gof', thedistn='ev', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2wbl25 = (
        'HT_DistributionTest_chi2wbl25',
        HT_DistributionTest(thetest='chi2gof', thedistn='wbl', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2wbl5 = (
        'HT_DistributionTest_chi2wbl5',
        HT_DistributionTest(thetest='chi2gof', thedistn='wbl', nbins=5))

    # outs: None
    # tags: distribution,hypothesistest,ks,raw
    HT_DistributionTest_ks_norm = (
        'HT_DistributionTest_ks_norm',
        HT_DistributionTest(thetest='ks', thedistn='norm'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2beta5 = (
        'HT_DistributionTest_chi2beta5',
        HT_DistributionTest(thetest='chi2gof', thedistn='beta', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2logn100 = (
        'HT_DistributionTest_chi2logn100',
        HT_DistributionTest(thetest='chi2gof', thedistn='logn', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2uni10 = (
        'HT_DistributionTest_chi2uni10',
        HT_DistributionTest(thetest='chi2gof', thedistn='uni', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2gam25 = (
        'HT_DistributionTest_chi2gam25',
        HT_DistributionTest(thetest='chi2gof', thedistn='gamma', nbins=25))

    # outs: None
    # tags: distribution,hypothesistest,ks,raw
    HT_DistributionTest_ks_ev = (
        'HT_DistributionTest_ks_ev',
        HT_DistributionTest(thetest='ks', thedistn='ev'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2ev5 = (
        'HT_DistributionTest_chi2ev5',
        HT_DistributionTest(thetest='chi2gof', thedistn='ev', nbins=5))

    # outs: None
    # tags: distribution,hypothesistest,ks,raw
    HT_DistributionTest_ks_uni = (
        'HT_DistributionTest_ks_uni',
        HT_DistributionTest(thetest='ks', thedistn='uni'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2gam100 = (
        'HT_DistributionTest_chi2gam100',
        HT_DistributionTest(thetest='chi2gof', thedistn='gamma', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2logn10 = (
        'HT_DistributionTest_chi2logn10',
        HT_DistributionTest(thetest='chi2gof', thedistn='logn', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2uni25 = (
        'HT_DistributionTest_chi2uni25',
        HT_DistributionTest(thetest='chi2gof', thedistn='uni', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2rayl5 = (
        'HT_DistributionTest_chi2rayl5',
        HT_DistributionTest(thetest='chi2gof', thedistn='rayleigh', nbins=5))

    # outs: None
    # tags: distribution,hypothesistest,ks,locdep,raw
    HT_DistributionTest_ks_gam = (
        'HT_DistributionTest_ks_gam',
        HT_DistributionTest(thetest='ks', thedistn='gamma'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2ev25 = (
        'HT_DistributionTest_chi2ev25',
        HT_DistributionTest(thetest='chi2gof', thedistn='ev', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2wbl10 = (
        'HT_DistributionTest_chi2wbl10',
        HT_DistributionTest(thetest='chi2gof', thedistn='wbl', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2gam5 = (
        'HT_DistributionTest_chi2gam5',
        HT_DistributionTest(thetest='chi2gof', thedistn='gamma', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2beta50 = (
        'HT_DistributionTest_chi2beta50',
        HT_DistributionTest(thetest='chi2gof', thedistn='beta', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2rayl10 = (
        'HT_DistributionTest_chi2rayl10',
        HT_DistributionTest(thetest='chi2gof', thedistn='rayleigh', nbins=10))

    # outs: None
    # tags: distribution,hypothesistest,lillie,raw
    HT_DistributionTest_lillie_ev = (
        'HT_DistributionTest_lillie_ev',
        HT_DistributionTest(thetest='lillie', thedistn='ev'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2exp100 = (
        'HT_DistributionTest_chi2exp100',
        HT_DistributionTest(thetest='chi2gof', thedistn='exp', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2norm10 = (
        'HT_DistributionTest_chi2norm10',
        HT_DistributionTest(thetest='chi2gof', thedistn='norm', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2exp50 = (
        'HT_DistributionTest_chi2exp50',
        HT_DistributionTest(thetest='chi2gof', thedistn='exp', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2norm5 = (
        'HT_DistributionTest_chi2norm5',
        HT_DistributionTest(thetest='chi2gof', thedistn='norm', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2exp25 = (
        'HT_DistributionTest_chi2exp25',
        HT_DistributionTest(thetest='chi2gof', thedistn='exp', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2wbl50 = (
        'HT_DistributionTest_chi2wbl50',
        HT_DistributionTest(thetest='chi2gof', thedistn='wbl', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2logn25 = (
        'HT_DistributionTest_chi2logn25',
        HT_DistributionTest(thetest='chi2gof', thedistn='logn', nbins=25))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2ev10 = (
        'HT_DistributionTest_chi2ev10',
        HT_DistributionTest(thetest='chi2gof', thedistn='ev', nbins=10))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2gam50 = (
        'HT_DistributionTest_chi2gam50',
        HT_DistributionTest(thetest='chi2gof', thedistn='gamma', nbins=50))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2uni50 = (
        'HT_DistributionTest_chi2uni50',
        HT_DistributionTest(thetest='chi2gof', thedistn='uni', nbins=50))

    # outs: None
    # tags: distribution,hypothesistest,ks,locdep,raw
    HT_DistributionTest_ks_wbl = (
        'HT_DistributionTest_ks_wbl',
        HT_DistributionTest(thetest='ks', thedistn='wbl'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,locdep,raw
    HT_DistributionTest_chi2exp5 = (
        'HT_DistributionTest_chi2exp5',
        HT_DistributionTest(thetest='chi2gof', thedistn='exp', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2beta100 = (
        'HT_DistributionTest_chi2beta100',
        HT_DistributionTest(thetest='chi2gof', thedistn='beta', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2norm25 = (
        'HT_DistributionTest_chi2norm25',
        HT_DistributionTest(thetest='chi2gof', thedistn='norm', nbins=25))

    # outs: None
    # tags: distribution,hypothesistest,ks,locdep,raw
    HT_DistributionTest_ks_rayl = (
        'HT_DistributionTest_ks_rayl',
        HT_DistributionTest(thetest='ks', thedistn='rayleigh'))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2ev100 = (
        'HT_DistributionTest_chi2ev100',
        HT_DistributionTest(thetest='chi2gof', thedistn='ev', nbins=100))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2uni5 = (
        'HT_DistributionTest_chi2uni5',
        HT_DistributionTest(thetest='chi2gof', thedistn='uni', nbins=5))

    # outs: None
    # tags: chi2gof,distribution,hypothesistest,raw
    HT_DistributionTest_chi2norm100 = (
        'HT_DistributionTest_chi2norm100',
        HT_DistributionTest(thetest='chi2gof', thedistn='norm', nbins=100))

    # outs: None
    # tags: distribution,hypothesistest,ks,locdep,raw
    HT_DistributionTest_ks_exp = (
        'HT_DistributionTest_ks_exp',
        HT_DistributionTest(thetest='ks', thedistn='exp'))

    # outs: None
    # tags: distribution,hypothesistest,lillie,locdep,raw
    HT_DistributionTest_lillie_exp = (
        'HT_DistributionTest_lillie_exp',
        HT_DistributionTest(thetest='lillie', thedistn='exp'))

    # outs: None
    # tags: hypothesistest,randomness,raw,runstest
    HT_HypothesisTest_runstestraw = (
        'HT_HypothesisTest_runstestraw',
        HT_HypothesisTest(theTest='runstest'))

    # outs: None
    # tags: hypothesistest,signtest
    HT_HypothesisTest_signtest = (
        'HT_HypothesisTest_signtest',
        HT_HypothesisTest(theTest='signtest'))

    # outs: None
    # tags: hypothesistest,ztest
    HT_HypothesisTest_ztest = (
        'HT_HypothesisTest_ztest',
        HT_HypothesisTest(theTest='ztest'))

    # outs: None
    # tags: hypothesistest,jbtest,raw
    HT_HypothesisTest_jbtest = (
        'HT_HypothesisTest_jbtest',
        HT_HypothesisTest(theTest='jbtest'))

    # outs: None
    # tags: hypothesistest,randomness,runstest
    HT_HypothesisTest_runstest = (
        'HT_HypothesisTest_runstest',
        HT_HypothesisTest(theTest='runstest'))

    # outs: None
    # tags: econometricstoolbox,hypothesistest,lbq,randomness
    HT_HypothesisTest_lbqtest = (
        'HT_HypothesisTest_lbqtest',
        HT_HypothesisTest(theTest='lbq'))

    # outs: None
    # tags: hypothesistest,signrank
    HT_HypothesisTest_signrank = (
        'HT_HypothesisTest_signrank',
        HT_HypothesisTest(theTest='signrank'))

    # outs: None
    # tags: econometricstoolbox,hypothesistest,lbq,randomness,raw
    HT_HypothesisTest_lbqtestraw = (
        'HT_HypothesisTest_lbqtestraw',
        HT_HypothesisTest(theTest='lbq'))

    # outs: SD1,SD2,hf,lf,lfhf
    # outs: pnn10,pnn20,pnn30,pnn40,pnn5
    # outs: tri,vlf
    # tags: maxlittle,medical
    MD_hrv_classic = (
        'MD_hrv_classic',
        MD_hrv_classic())

    # outs: pnn10,pnn100,pnn20,pnn30,pnn40
    # outs: pnn5,pnn50,pnn60,pnn70,pnn80
    # outs: pnn90
    # tags: maxlittle,medical,raw,spreaddep
    MD_pNN_raw = (
        'MD_pNN_raw',
        MD_pNN())

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_01_3 = (
        'MD_polvar_01_3',
        MD_polvar(d=0.1, D=3))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_1_6 = (
        'MD_polvar_1_6',
        MD_polvar(d=1, D=6))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_1_4 = (
        'MD_polvar_1_4',
        MD_polvar(d=1, D=4))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_1_5 = (
        'MD_polvar_1_5',
        MD_polvar(d=1, D=5))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_1_3 = (
        'MD_polvar_1_3',
        MD_polvar(d=1, D=3))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_05_5 = (
        'MD_polvar_05_5',
        MD_polvar(d=0.5, D=5))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_05_3 = (
        'MD_polvar_05_3',
        MD_polvar(d=0.5, D=3))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_01_6 = (
        'MD_polvar_01_6',
        MD_polvar(d=0.1, D=6))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_01_5 = (
        'MD_polvar_01_5',
        MD_polvar(d=0.1, D=5))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_01_4 = (
        'MD_polvar_01_4',
        MD_polvar(d=0.1, D=4))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_05_6 = (
        'MD_polvar_05_6',
        MD_polvar(d=0.5, D=6))

    # outs: None
    # tags: maxlittle,medical,symbolic
    MD_polvar_05_4 = (
        'MD_polvar_05_4',
        MD_polvar(d=0.5, D=4))

    # outs: SD1,SD2,tri10,tri20,trisqrt
    # tags: maxlittle,medical,raw,spreaddep
    MD_rawHRVmeas = (
        'MD_rawHRVmeas',
        MD_rawHRVmeas())

    # outs: aic_min,mean_all_aics,meanstd_aicsp,meanstd_aicsq,p_aic_opt
    # outs: q_aic_opt,std_all_aics
    # tags: arma,model,systemidentificationtoolbox
    MF_ARMA_orders_1_6_1_4 = (
        'MF_ARMA_orders_1_6_1_4',
        MF_ARMA_orders(pr=MatlabSequence('1:6'), qr=MatlabSequence('1:4')))

    # outs: AC1,AC2,a2,a3,a4
    # outs: e,mu,rms,std
    # tags: AR,fit,gof,model,var
    MF_AR_arcov_3 = (
        'MF_AR_arcov_3',
        MF_AR_arcov(p=3))

    # outs: AC1,AC2,a2,a3,e
    # outs: mu,rms,std
    # tags: AR,fit,gof,model,var
    MF_AR_arcov_2 = (
        'MF_AR_arcov_2',
        MF_AR_arcov(p=2))

    # outs: AC1,AC2,a2,mu,rms
    # outs: std
    # tags: AR,fit,gof,model
    MF_AR_arcov_1 = (
        'MF_AR_arcov_1',
        MF_AR_arcov(p=1))

    # outs: AC1,AC2,a2,a3,a4
    # outs: a5,a6,e,mu,rms
    # outs: std
    # tags: AR,fit,gof,model,var
    MF_AR_arcov_5 = (
        'MF_AR_arcov_5',
        MF_AR_arcov(p=5))

    # outs: AC1,AC2,a2,a3,a4
    # outs: a5,e,mu,rms,std
    # tags: AR,fit,gof,model,var
    MF_AR_arcov_4 = (
        'MF_AR_arcov_4',
        MF_AR_arcov(p=4))

    # outs: aic_n,best_n,bestaic,bestmdl,firstonmin
    # outs: maxdiff,maxonmed,maxv,mdl_n,meandiff
    # outs: meanv,meddiff,medianv,minstdfromi,minv
    # outs: stddiff,where01max,whereen4
    # tags: ar,model,systemidentificationtoolbox
    MF_CompareAR_1_10_all = (
        'MF_CompareAR_1_10_all',
        MF_CompareAR(orders=MatlabSequence('1:10'), howtotest='all'))

    # outs: aic_n,best_n,bestaic,bestmdl,firstonmin
    # outs: maxdiff,maxonmed,maxv,mdl_n,meandiff
    # outs: meanv,meddiff,medianv,minstdfromi,minv
    # outs: stddiff,where01max,whereen4
    # tags: ar,model,systemidentificationtoolbox
    MF_CompareAR_1_10_05 = (
        'MF_CompareAR_1_10_05',
        MF_CompareAR(orders=MatlabSequence('1:10'), howtotest=0.5))

    # outs: ac1s_iqr,ac1s_mean,ac1s_median,ac1s_std,mabserr_iqr
    # outs: mabserr_mean,mabserr_median,mabserr_std,meandiffs_iqr,meandiffs_mean
    # outs: meandiffs_median,meandiffs_std,rmserr_iqr,rmserr_mean,rmserr_median
    # outs: rmserr_std,stdrats_iqr,stdrats_mean,stdrats_median,stdrats_std
    # tags: ar,arfit,model,prediction,systemidentificationtoolbox
    MF_CompareTestSets_y_ar_best_uniform_25_01_1 = (
        'MF_CompareTestSets_y_ar_best_uniform_25_01_1',
        MF_CompareTestSets(model='ar', ordd='best', howtosubset='uniform', samplep=(25.0, 0.10000000000000001),
                           steps=1))

    # outs: ac1s_iqr,ac1s_mean,ac1s_median,ac1s_std,mabserr_iqr
    # outs: mabserr_mean,mabserr_median,mabserr_std,meandiffs_iqr,meandiffs_mean
    # outs: meandiffs_median,meandiffs_std,rmserr_iqr,rmserr_mean,rmserr_median
    # outs: rmserr_std,stdrats_iqr,stdrats_mean,stdrats_median,stdrats_std
    # tags: model,prediction,statespace,systemidentificationtoolbox
    MF_CompareTestSets_y_ss_2_uniform_25_01_1 = (
        'MF_CompareTestSets_y_ss_2_uniform_25_01_1',
        MF_CompareTestSets(model='ss', ordd=2, howtosubset='uniform', samplep=(25.0, 0.10000000000000001),
                           steps=1))

    # outs: ac1s_iqr,ac1s_mean,ac1s_median,ac1s_std,mabserr_iqr
    # outs: mabserr_mean,mabserr_median,mabserr_std,meandiffs_iqr,meandiffs_mean
    # outs: meandiffs_median,meandiffs_std,rmserr_iqr,rmserr_mean,rmserr_median
    # outs: rmserr_std,stdrats_iqr,stdrats_mean,stdrats_median,stdrats_std
    # tags: ar,model,prediction,stochastic,systemidentificationtoolbox
    MF_CompareTestSets_y_ar_4_rand_25_01_1 = (
        'MF_CompareTestSets_y_ar_4_rand_25_01_1',
        MF_CompareTestSets(model='ar', ordd=4, howtosubset='rand', samplep=(25.0, 0.10000000000000001),
                           steps=1))

    # outs: ac1s_iqr,ac1s_mean,ac1s_median,ac1s_std,mabserr_iqr
    # outs: mabserr_mean,mabserr_median,mabserr_std,meandiffs_iqr,meandiffs_mean
    # outs: meandiffs_median,meandiffs_std,rmserr_iqr,rmserr_mean,rmserr_median
    # outs: rmserr_std,stdrats_iqr,stdrats_mean,stdrats_median,stdrats_std
    # tags: model,prediction,statespace,systemidentificationtoolbox
    MF_CompareTestSets_y_ss_best_uniform_25_01_1 = (
        'MF_CompareTestSets_y_ss_best_uniform_25_01_1',
        MF_CompareTestSets(model='ss', ordd='best', howtosubset='uniform', samplep=(25.0, 0.10000000000000001),
                           steps=1))

    # outs: ac1,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,alphamin,alphamin_1
    # outs: cup_1,dwts,ftbth,maxonmean,meanabs
    # outs: meane,minfpe,minsbc,mms,normksstat
    # outs: normp,p1_1,p1_5,p2_5,p3_5
    # outs: p4_5,p5_5,popt,propbth,rmse
    # outs: sbc1,stde
    # tags: expsmoothing,model,siddarth
    MF_ExpSmoothing_05_best = (
        'MF_ExpSmoothing_05_best',
        MF_ExpSmoothing(ntrain=0.5, alpha='best'))

    # outs: a_1_max,a_1_mean,a_1_min,a_1_std,a_2_max
    # outs: a_2_mean,a_2_min,a_2_std,fpe_max,fpe_mean
    # outs: fpe_min,fpe_range,fpe_std
    # tags: ar,model,prediction,systemidentificationtoolbox
    MF_FitSubsegments_ar_2_uniform_25_01 = (
        'MF_FitSubsegments_ar_2_uniform_25_01',
        MF_FitSubsegments(model='ar', order=2, howtosubset='uniform', samplep=(25.0, 0.10000000000000001)))

    # outs: fpe_max,fpe_mean,fpe_min,fpe_range,fpe_std
    # outs: p_1_max,p_1_mean,p_1_min,p_1_std,p_2_max
    # outs: p_2_mean,p_2_min,p_2_std,q_1_max,q_1_mean
    # outs: q_1_min,q_1_std,q_2_max,q_2_mean,q_2_min
    # outs: q_2_std
    # tags: arma,model,prediction,systemidentificationtoolbox
    MF_FitSubsegments_arma_2_2_uniform_25_01 = (
        'MF_FitSubsegments_arma_2_2_uniform_25_01',
        MF_FitSubsegments(model='arma', order=(2.0, 2.0), howtosubset='uniform', samplep=(25.0,
                          0.10000000000000001)))

    # outs: orders_max,orders_mean,orders_min,orders_mode,orders_range
    # outs: orders_std,sbcs_max,sbcs_mean,sbcs_min,sbcs_range
    # outs: sbcs_std
    # tags: ar,arfit,model,prediction,stochastic,systemidentificationtoolbox
    MF_FitSubsegments_arsbc_rand_25_01 = (
        'MF_FitSubsegments_arsbc_rand_25_01',
        MF_FitSubsegments(model='arsbc', order=(), howtosubset='rand', samplep=(25.0, 0.10000000000000001)))

    # outs: orders_max,orders_mean,orders_min,orders_mode,orders_range
    # outs: orders_std,sbcs_max,sbcs_mean,sbcs_min,sbcs_range
    # outs: sbcs_std
    # tags: ar,arfit,model,prediction,systemidentificationtoolbox
    MF_FitSubsegments_arsbc_uniform_25_01 = (
        'MF_FitSubsegments_arsbc_uniform_25_01',
        MF_FitSubsegments(model='arsbc', order=(), howtosubset='uniform', samplep=(25.0, 0.10000000000000001)))

    # outs: fpe_max,fpe_mean,fpe_min,fpe_range,fpe_std
    # tags: model,prediction,statespace,systemidentificationtoolbox
    MF_FitSubsegments_ss_2_uniform_25_01 = (
        'MF_FitSubsegments_ss_2_uniform_25_01',
        MF_FitSubsegments(model='ss', order=2, howtosubset='uniform', samplep=(25.0, 0.10000000000000001)))

    # outs: Ks_vary_p,Ks_vary_q,bestpAIC,bestpLLF,bestqAIC
    # outs: bestqLLF,maxAIC,maxBIC,maxK,maxLLF
    # outs: max_maxarchps,max_maxlbqps,max_meanarchps,max_meanlbqps,meanAIC
    # outs: meanBIC,meanK,meanLLF,mean_maxarchps,mean_maxlbqps
    # outs: mean_meanarchps,mean_meanlbqps,minAIC,minBIC,minK
    # outs: minLLF,min_maxarchps,min_maxlbqps,min_meanarchps,min_meanlbqps
    # tags: aic,bic,econometricstoolbox,garch,model
    MF_compare_GARCH_ar_1_3_1_3 = (
        'MF_compare_GARCH_ar_1_3_1_3',
        MF_GARCHcompare(preproc='ar', pr=MatlabSequence('1:3'), qr=MatlabSequence('1:3')))

    # outs: ARCH_1,ARCHerr_1,GARCH_1,GARCHerr_1,LLF
    # outs: ac1_stde2,aic,bic,constant,constanterr
    # outs: diff_ac1,engle_max_diff_p,engle_mean_diff_p,engle_pval_stde_1,engle_pval_stde_10
    # outs: engle_pval_stde_5,lbq_max_diff_p,lbq_mean_diff_p,lbq_pval_stde_1,lbq_pval_stde_10
    # outs: lbq_pval_stde_5,maxenglepval_stde,maxlbqpval_stde2,maxsigma,meansigma
    # outs: minenglepval_stde,minlbqpval_stde2,minsigma,nparams,rangesigma
    # outs: stde_ac1,stde_ac1n,stde_ac2,stde_ac2n,stde_ac3
    # outs: stde_ac3n,stde_acmnd0,stde_acsnd0,stde_dwts,stde_ftbth
    # outs: stde_maxonmean,stde_meanabs,stde_meane,stde_minfpe,stde_minsbc
    # outs: stde_mms,stde_normksstat,stde_normp,stde_p1_5,stde_p2_5
    # outs: stde_p3_5,stde_p4_5,stde_p5_5,stde_popt,stde_propbth
    # outs: stde_rmse,stde_sbc1,stde_stde,stdsigma,summaryexitflag
    # tags: aic,bic,econometricstoolbox,garch,model,stochastic
    MF_GARCHfit_ar_P1_Q1 = (
        'MF_GARCHfit_ar_P1_Q1',
        MF_GARCHfit(preproc='ar', P=1, Q=1))

    # outs: ARCH_1,ARCH_2,ARCHerr_1,ARCHerr_2,GARCH_1
    # outs: GARCHerr_1,LLF,ac1_stde2,aic,bic
    # outs: constant,constanterr,diff_ac1,engle_max_diff_p,engle_mean_diff_p
    # outs: engle_pval_stde_1,engle_pval_stde_10,engle_pval_stde_5,lbq_max_diff_p,lbq_mean_diff_p
    # outs: lbq_pval_stde_1,lbq_pval_stde_10,lbq_pval_stde_5,maxenglepval_stde,maxlbqpval_stde2
    # outs: maxsigma,meansigma,minenglepval_stde,minlbqpval_stde2,minsigma
    # outs: nparams,rangesigma,stde_ac1,stde_ac1n,stde_ac2
    # outs: stde_ac2n,stde_ac3,stde_ac3n,stde_acmnd0,stde_acsnd0
    # outs: stde_dwts,stde_ftbth,stde_maxonmean,stde_meanabs,stde_meane
    # outs: stde_minfpe,stde_minsbc,stde_mms,stde_normksstat,stde_normp
    # outs: stde_p1_5,stde_p2_5,stde_p3_5,stde_p4_5,stde_p5_5
    # outs: stde_popt,stde_propbth,stde_rmse,stde_sbc1,stde_stde
    # outs: stdsigma,summaryexitflag
    # tags: aic,bic,econometricstoolbox,garch,model,stochastic
    MF_GARCHfit_ar_P1_Q2 = (
        'MF_GARCHfit_ar_P1_Q2',
        MF_GARCHfit(preproc='ar', P=1, Q=2))

    # outs: h_lonN,logh1,logh2,logh3,meanS
    # outs: meanstderr,mlikelihood,rmserr,stdS,stdmu
    # tags: gaussianprocess
    MF_GP_FitAcross_covSEiso_covNoise_20 = (
        'MF_GP_FitAcross_covSEiso_covNoise_20',
        MF_GP_FitAcross(covFunc=('covSum', ('covSEiso', 'covNoise')), npoints=20))

    # outs: maxabserr,maxabserr_run,maxerrbar,maxmlik,maxstderr
    # outs: maxstderr_run,meanabserr,meanabserr_run,meanerrbar,meanlogh1
    # outs: meanlogh2,meanlogh3,meanstderr,meanstderr_run,minabserr
    # outs: minabserr_run,minerrbar,minmlik,minstderr,minstderr_run
    # outs: stdlogh1,stdlogh2,stdlogh3,stdmlik
    # tags: gaussianprocess
    MF_GP_LocalPrediction_covSEiso_covNoise_10_3_20_frombefore = (
        'MF_GP_LocalPrediction_covSEiso_covNoise_10_3_20_frombefore',
        MF_GP_LocalPrediction(covFunc=('covSum', ('covSEiso', 'covNoise')), ntrain=10, ntest=3,
                              npreds=20, pmode='frombefore'))

    # outs: maxabserr,maxabserr_run,maxerrbar,maxmlik,maxstderr
    # outs: maxstderr_run,meanabserr,meanabserr_run,meanerrbar,meanlogh1
    # outs: meanlogh2,meanlogh3,meanstderr,meanstderr_run,minabserr
    # outs: minabserr_run,minerrbar,minmlik,minstderr,minstderr_run
    # outs: stdlogh1,stdlogh2,stdlogh3,stdmlik
    # tags: gaussianprocess
    MF_GP_LocalPrediction_covSEiso_covNoise_5_3_10_beforeafter = (
        'MF_GP_LocalPrediction_covSEiso_covNoise_5_3_10_beforeafter',
        MF_GP_LocalPrediction(covFunc=('covSum', ('covSEiso', 'covNoise')), ntrain=5, ntest=3, npreds=10,
                              pmode='beforeafter'))

    # outs: maxabserr,maxabserr_run,maxerrbar,maxmlik,maxstderr
    # outs: maxstderr_run,meanabserr,meanabserr_run,meanerrbar,meanlogh1
    # outs: meanlogh2,meanlogh3,meanstderr,meanstderr_run,minabserr
    # outs: minabserr_run,minerrbar,minmlik,minstderr,minstderr_run
    # outs: stdlogh1,stdlogh2,stdlogh3,stdmlik
    # tags: gaussianprocess,stochastic
    MF_GP_LocalPrediction_covSEiso_covNoise_10_3_20_randomgap = (
        'MF_GP_LocalPrediction_covSEiso_covNoise_10_3_20_randomgap',
        MF_GP_LocalPrediction(covFunc=('covSum', ('covSEiso', 'covNoise')), ntrain=10, ntest=3,
                              npreds=20, pmode='randomgap'))

    # outs: h1,h2,h3,logh1,logh2
    # outs: logh3,mabserr_std,maxS,meanS,minS
    # outs: mlikelihood,rmserr,std_S_data,std_mu_data
    # tags: gaussianprocess
    MF_GP_hyperparameters_covSEiso_covNoise_1_200_first = (
        'MF_GP_hyperparameters_covSEiso_covNoise_1_200_first',
        MF_GP_hyperparameters(covFunc=('covSum', ('covSEiso', 'covNoise')), squishorsquash=1, maxN=200,
                              methds='first'))

    # outs: h1,h2,h3,h4,h5
    # outs: logh1,logh2,logh3,logh4,logh5
    # outs: mabserr_std,maxS,meanS,minS,mlikelihood
    # outs: rmserr,std_S_data,std_mu_data
    # tags: gaussianprocess
    MF_GP_hyperparameters_covSEiso_covPeriodic_covNoise_1_200_first = (
        'MF_GP_hyperparameters_covSEiso_covPeriodic_covNoise_1_200_first',
        MF_GP_hyperparameters(covFunc=('covSum', ('covSEiso', 'covPeriodic', 'covNoise')), squishorsquash=1,
                              maxN=200, methds='first'))

    # outs: h1,h2,h3,logh1,logh2
    # outs: logh3,mabserr_std,maxS,meanS,minS
    # outs: mlikelihood,rmserr,std_S_data,std_mu_data
    # tags: gaussianprocess
    MF_GP_hyperparameters_covSEiso_covNoise_1_200_resample = (
        'MF_GP_hyperparameters_covSEiso_covNoise_1_200_resample',
        MF_GP_hyperparameters(covFunc=('covSum', ('covSEiso', 'covNoise')), squishorsquash=1, maxN=200,
                              methds='resample'))

    # outs: h1,h2,h3,h4,h5
    # outs: logh1,logh2,logh3,logh4,logh5
    # outs: mabserr_std,maxS,meanS,minS,mlikelihood
    # outs: rmserr,std_S_data,std_mu_data
    # tags: gaussianprocess
    MF_GP_hyperparameters_covSEiso_covPeriodic_covNoise_1_200_resample = (
        'MF_GP_hyperparameters_covSEiso_covPeriodic_covNoise_1_200_resample',
        MF_GP_hyperparameters(covFunc=('covSum', ('covSEiso', 'covPeriodic', 'covNoise')), squishorsquash=1,
                              maxN=200, methds='resample'))

    # outs: h1,h2,h3,logh1,logh2
    # outs: logh3,mabserr_std,maxS,meanS,minS
    # outs: mlikelihood,rmserr,std_S_data,std_mu_data
    # tags: gaussianprocess,stochastic
    MF_GP_hyperparameters_covSEiso_covNoise_1_50_random_i = (
        'MF_GP_hyperparameters_covSEiso_covNoise_1_50_random_i',
        MF_GP_hyperparameters(covFunc=('covSum', ('covSEiso', 'covNoise')), squishorsquash=1, maxN=50,
                              methds='random_i'))

    # outs: aic2,aicopt,fpe2,lossfn2,lossfnopt
    # outs: maxdiffaic,meandiffaic,minaic,mindiffaic,minlossfn
    # outs: ndownaic
    # tags: model,statespace,systemidentificationtoolbox
    MF_StateSpaceCompOrder_8 = (
        'MF_StateSpaceCompOrder_8',
        MF_StateSpaceCompOrder(maxorder=8))

    # outs: A_1,A_2,A_3,A_4,A_5
    # outs: A_6,A_7,A_8,A_9,ac1
    # outs: ac1diff,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,c_1,c_2
    # outs: c_3,dwts,ftbth,k_1,k_2
    # outs: k_3,m_aic,m_fpe,m_lossfn,m_noisevar
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,normksstat,normp,p1_5,p2_5
    # outs: p3_5,p4_5,p5_5,popt,propbth
    # outs: rmse,sbc1,stde,x0mod
    # tags: model,statespace,systemidentificationtoolbox
    MF_StateSpace_n4sid_3_05_1 = (
        'MF_StateSpace_n4sid_3_05_1',
        MF_StateSpace_n4sid(ordd=3, ptrain=0.5, steps=1))

    # outs: A_1,A_2,A_3,A_4,ac1
    # outs: ac1diff,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,c_1,c_2
    # outs: dwts,ftbth,k_1,k_2,m_aic
    # outs: m_fpe,m_lossfn,m_noisevar,maxonmean,meanabs
    # outs: meane,minfpe,minsbc,mms,normksstat
    # outs: normp,p1_5,p2_5,p3_5,p4_5
    # outs: p5_5,popt,propbth,rmse,sbc1
    # outs: stde,x0mod
    # tags: model,statespace,systemidentificationtoolbox
    MF_StateSpace_n4sid_2_05_1 = (
        'MF_StateSpace_n4sid_2_05_1',
        MF_StateSpace_n4sid(ordd=2, ptrain=0.5, steps=1))

    # outs: A_1,ac1,ac1diff,ac1n,ac2
    # outs: ac2n,ac3,ac3n,acmnd0,acsnd0
    # outs: c_1,dwts,ftbth,k_1,m_aic
    # outs: m_fpe,m_lossfn,m_noisevar,maxonmean,meanabs
    # outs: meane,minfpe,minsbc,mms,normksstat
    # outs: normp,p1_5,p2_5,p3_5,p4_5
    # outs: p5_5,popt,propbth,rmse,sbc1
    # outs: stde,x0mod
    # tags: model,statespace,systemidentificationtoolbox
    MF_StateSpace_n4sid_1_05_1 = (
        'MF_StateSpace_n4sid_1_05_1',
        MF_StateSpace_n4sid(ordd=1, ptrain=0.5, steps=1))

    # outs: A1,A2,A3,A4,A5
    # outs: A6,C,aerr_max,aerr_mean,aerr_min
    # outs: aroundmin_fpe,aroundmin_sbc,fpe_1,fpe_2,fpe_3
    # outs: fpe_4,fpe_5,fpe_6,fpe_7,fpe_8
    # outs: maxA,maxImS,maxReS,maxabsS,maxexctn
    # outs: maxper,maxtau,meanA,meanexctn,meanper
    # outs: meanpererr,meantau,meantauerr,minA,minexctn
    # outs: minfpe,minper,minsbc,mintau,pcorr_res
    # outs: popt_fpe,popt_sbc,res_ac1,res_ac1_norm,res_siglev
    # outs: rmsA,sbc_1,sbc_2,sbc_3,sbc_4
    # outs: sbc_5,sbc_6,sbc_7,sbc_8,stdA
    # outs: stdabsS,stdexctn,stdper,stdtau,sumA
    # outs: sumsqA
    # tags: arfit,modelfit
    MF_arfit_1_8_sbc = (
        'MF_arfit_1_8_sbc',
        MF_arfit(pmin=1, pmax=8, selector='sbc'))

    # outs: AR_1,AR_2,MA_1,MA_2,ac1
    # outs: ac1n,ac2,ac2n,ac3,ac3n
    # outs: acmnd0,acsnd0,aic,dwts,fpe
    # outs: ftbth,lastimprovement,lossfn,maxda,maxdc
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,noisevar,normksstat,normp,p1_5
    # outs: p2_5,p3_5,p4_5,p5_5,popt
    # outs: propbth,rmse,sbc1,stde
    # tags: arma,model,systemidentificationtoolbox
    MF_armax_2_2_05_1 = (
        'MF_armax_2_2_05_1',
        MF_armax(orders=(2.0, 2.0), ptrain=0.5, nsteps=1))

    # outs: AR_1,AR_2,AR_3,MA_1,ac1
    # outs: ac1n,ac2,ac2n,ac3,ac3n
    # outs: acmnd0,acsnd0,aic,dwts,fpe
    # outs: ftbth,lastimprovement,lossfn,maxda,maxdc
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,noisevar,normksstat,normp,p1_5
    # outs: p2_5,p3_5,p4_5,p5_5,popt
    # outs: propbth,rmse,sbc1,stde
    # tags: arma,model,systemidentificationtoolbox
    MF_armax_3_1_05_1 = (
        'MF_armax_3_1_05_1',
        MF_armax(orders=(3.0, 1.0), ptrain=0.5, nsteps=1))

    # outs: AR_1,MA_1,ac1,ac1n,ac2
    # outs: ac2n,ac3,ac3n,acmnd0,acsnd0
    # outs: aic,dwts,fpe,ftbth,lastimprovement
    # outs: lossfn,maxda,maxdc,maxonmean,meanabs
    # outs: meane,minfpe,minsbc,mms,noisevar
    # outs: normksstat,normp,p1_5,p2_5,p3_5
    # outs: p4_5,p5_5,popt,propbth,rmse
    # outs: sbc1,stde
    # tags: arma,model,systemidentificationtoolbox
    MF_armax_1_1_05_1 = (
        'MF_armax_1_1_05_1',
        MF_armax(orders=(1.0, 1.0), ptrain=0.5, nsteps=1))

    # outs: LLtestdiff1,LLtestdiff2,chLLtest,chLLtrain,maxLLtest
    # outs: maxLLtrain,meanLLtest,meanLLtrain,meandiffLLtt
    # tags: gharamani,hmm,model
    MF_hmm_CompareNStates_06_24 = (
        'MF_hmm_CompareNStates_06_24',
        MF_hmm_CompareNStates(trainp=0.6, nstater=MatlabSequence('2:4')))

    # outs: Cov,LLdifference,LLtestpersample,LLtrainpersample,Mu_1
    # outs: Mu_2,Mu_3,Pmeandiag,maxP,meanMu
    # outs: nit,rangeMu,stdP,stdmeanP
    # tags: gharamani,hmm,model
    MF_hmm_07_3 = (
        'MF_hmm_07_3',
        MF_hmm_fit(trainp=0.7, numStates=3))

    # outs: Cov,LLdifference,LLtestpersample,LLtrainpersample,Mu_1
    # outs: Mu_2,Pmeandiag,maxP,meanMu,nit
    # outs: rangeMu,stdP,stdmeanP
    # tags: gharamani,hmm,model
    MF_hmm_08_2 = (
        'MF_hmm_08_2',
        MF_hmm_fit(trainp=0.8, numStates=2))

    # outs: ac1_1,ac1_2,ac1_3,ac1_4,ac1_5
    # outs: ac1_6,mabserr_1,mabserr_2,mabserr_3,mabserr_4
    # outs: mabserr_5,mabserr_6,maxdiffrms,meandiffrms,meandiffrmsabs
    # outs: ndown,rmserr_1,rmserr_2,rmserr_3,rmserr_4
    # outs: rmserr_5,rmserr_6,stddiffrms
    # tags: ar,arfit,model,prediction,systemidentificationtoolbox
    MF_steps_ahead_ar_best_6 = (
        'MF_steps_ahead_ar_best_6',
        MF_steps_ahead(model='ar', order='best', maxsteps=6))

    # outs: ac1_1,ac1_2,ac1_3,ac1_4,ac1_5
    # outs: ac1_6,mabserr_1,mabserr_2,mabserr_3,mabserr_4
    # outs: mabserr_5,mabserr_6,maxdiffrms,meandiffrms,meandiffrmsabs
    # outs: ndown,rmserr_1,rmserr_2,rmserr_3,rmserr_4
    # outs: rmserr_5,rmserr_6,stddiffrms
    # tags: ar,model,prediction,systemidentificationtoolbox
    MF_steps_ahead_ar_2_6 = (
        'MF_steps_ahead_ar_2_6',
        MF_steps_ahead(model='ar', order=2, maxsteps=6))

    # outs: ac1_1,ac1_2,ac1_3,ac1_4,ac1_5
    # outs: ac1_6,mabserr_1,mabserr_2,mabserr_3,mabserr_4
    # outs: mabserr_5,mabserr_6,maxdiffrms,meandiffrms,meandiffrmsabs
    # outs: ndown,rmserr_1,rmserr_2,rmserr_3,rmserr_4
    # outs: rmserr_5,rmserr_6,stddiffrms
    # tags: model,prediction,statespace,systemidentificationtoolbox
    MF_steps_ahead_ss_best_6 = (
        'MF_steps_ahead_ss_best_6',
        MF_steps_ahead(model='ss', order='best', maxsteps=6))

    # outs: ac1_1,ac1_2,ac1_3,ac1_4,ac1_5
    # outs: ac1_6,mabserr_1,mabserr_2,mabserr_3,mabserr_4
    # outs: mabserr_5,mabserr_6,maxdiffrms,meandiffrms,meandiffrmsabs
    # outs: ndown,rmserr_1,rmserr_2,rmserr_3,rmserr_4
    # outs: rmserr_5,rmserr_6,stddiffrms
    # tags: arma,model,prediction,systemidentificationtoolbox
    MF_steps_ahead_arma_3_1_6 = (
        'MF_steps_ahead_arma_3_1_6',
        MF_steps_ahead(model='arma', order=(3.0, 1.0), maxsteps=6))

    # outs: iqrstretch,meanchr10,meanchr11,meanchr12,meanchr13
    # outs: meanchr14,meanchr15,meanchr16,meanchr17,meanchr18
    # outs: meanchr2,meanchr3,meanchr4,meanchr5,meanchr6
    # outs: meanchr7,meanchr8,meanchr9,meand2,meand3
    # outs: meand4,meand5,meanr10,meanr11,meanr12
    # outs: meanr13,meanr14,meanr15,meanr16,meanr17
    # outs: meanr18,meanr2,meanr3,meanr4,meanr5
    # outs: meanr6,meanr7,meanr8,meanr9,mediand2
    # outs: mediand3,mediand4,mediand5,medianr10,medianr11
    # outs: medianr12,medianr13,medianr14,medianr15,medianr16
    # outs: medianr17,medianr18,medianr2,medianr3,medianr4
    # outs: medianr5,medianr6,medianr7,medianr8,medianr9
    # outs: medianstretch,mind2,mind3,mind4,mind5
    # outs: minr10,minr11,minr12,minr13,minr14
    # outs: minr15,minr16,minr17,minr18,minr2
    # outs: minr3,minr4,minr5,minr6,minr7
    # outs: minr8,minr9,minstretch,stdmean,stdmedian
    # tags: corrdim,correlation,nonlinear,tstool
    NL_BoxCorrDim_50_ac_5 = (
        'NL_BoxCorrDim_50_ac_5',
        NL_BoxCorrDim(nbins=50, embedparams=('ac', 5)))

    # outs: caoo1_1,caoo1_10,caoo1_2,caoo1_3,caoo1_4
    # outs: caoo1_5,caoo1_6,caoo1_7,caoo1_8,caoo1_9
    # outs: caoo2_1,caoo2_10,caoo2_2,caoo2_3,caoo2_4
    # outs: caoo2_5,caoo2_6,caoo2_7,caoo2_8,caoo2_9
    # outs: fm005_1,fm005_2,fm01_1,fm01_2,fm02_1
    # outs: fm02_2,fmm10_1,fmm10_2,fmm20_1,fmm20_2
    # outs: fmm40_1,fmm40_2,fmmmax_1,fmmmax_2,fp05_1
    # outs: fp05_2,fp08_1,fp08_2,fp09_1,fp09_2
    # outs: max1,max2,median1,median2,min1
    # outs: min2,std1,std2
    # tags: cao,dimension,nonlinear,stochastic,tstool
    NL_CaosMethod_10_mi_2_100 = (
        'NL_CaosMethod_10_mi_2_100',
        NL_CaosMethod(maxdim=10, tau='mi', NNR=2, Nref=100))

    # outs: caoo1_1,caoo1_10,caoo1_2,caoo1_3,caoo1_4
    # outs: caoo1_5,caoo1_6,caoo1_7,caoo1_8,caoo1_9
    # outs: caoo2_1,caoo2_10,caoo2_2,caoo2_3,caoo2_4
    # outs: caoo2_5,caoo2_6,caoo2_7,caoo2_8,caoo2_9
    # outs: fm005_1,fm005_2,fm01_1,fm01_2,fm02_1
    # outs: fm02_2,fmm10_1,fmm10_2,fmm20_1,fmm20_2
    # outs: fmm40_1,fmm40_2,fmmmax_1,fmmmax_2,fp05_1
    # outs: fp05_2,fp08_1,fp08_2,fp09_1,fp09_2
    # outs: max1,max2,median1,median2,min1
    # outs: min2,std1,std2
    # tags: cao,dimension,nonlinear,stochastic,tstool
    NL_CaosMethod_10_mi_2_02 = (
        'NL_CaosMethod_10_mi_2_02',
        NL_CaosMethod(maxdim=10, tau='mi', NNR=2, Nref=0.2))

    # outs: caoo1_1,caoo1_10,caoo1_2,caoo1_3,caoo1_4
    # outs: caoo1_5,caoo1_6,caoo1_7,caoo1_8,caoo1_9
    # outs: caoo2_1,caoo2_10,caoo2_2,caoo2_3,caoo2_4
    # outs: caoo2_5,caoo2_6,caoo2_7,caoo2_8,caoo2_9
    # outs: fm005_1,fm005_2,fm01_1,fm01_2,fm02_1
    # outs: fm02_2,fmm10_1,fmm10_2,fmm20_1,fmm20_2
    # outs: fmm40_1,fmm40_2,fmmmax_1,fmmmax_2,fp05_1
    # outs: fp05_2,fp08_1,fp08_2,fp09_1,fp09_2
    # outs: max1,max2,median1,median2,min1
    # outs: min2,std1,std2
    # tags: cao,dimension,nonlinear,stochastic,tstool
    NL_CaosMethod_10_mi_3_500 = (
        'NL_CaosMethod_10_mi_3_500',
        NL_CaosMethod(maxdim=10, tau='mi', NNR=3, Nref=500))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_7_diff = (
        'NL_MS_LZcomplexity_7_diff',
        NL_MS_LZcomplexity(n=7, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_9 = (
        'NL_MS_LZcomplexity_9',
        NL_MS_LZcomplexity(n=9, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_8 = (
        'NL_MS_LZcomplexity_8',
        NL_MS_LZcomplexity(n=8, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_2 = (
        'NL_MS_LZcomplexity_2',
        NL_MS_LZcomplexity(n=2, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_7 = (
        'NL_MS_LZcomplexity_7',
        NL_MS_LZcomplexity(n=7, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_6 = (
        'NL_MS_LZcomplexity_6',
        NL_MS_LZcomplexity(n=6, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_5 = (
        'NL_MS_LZcomplexity_5',
        NL_MS_LZcomplexity(n=5, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_3 = (
        'NL_MS_LZcomplexity_3',
        NL_MS_LZcomplexity(n=3, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_8_diff = (
        'NL_MS_LZcomplexity_8_diff',
        NL_MS_LZcomplexity(n=8, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_10 = (
        'NL_MS_LZcomplexity_10',
        NL_MS_LZcomplexity(n=10, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_6_diff = (
        'NL_MS_LZcomplexity_6_diff',
        NL_MS_LZcomplexity(n=6, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_9_diff = (
        'NL_MS_LZcomplexity_9_diff',
        NL_MS_LZcomplexity(n=9, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_4 = (
        'NL_MS_LZcomplexity_4',
        NL_MS_LZcomplexity(n=4, PreProc=()))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_3_diff = (
        'NL_MS_LZcomplexity_3_diff',
        NL_MS_LZcomplexity(n=3, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_2_diff = (
        'NL_MS_LZcomplexity_2_diff',
        NL_MS_LZcomplexity(n=2, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_4_diff = (
        'NL_MS_LZcomplexity_4_diff',
        NL_MS_LZcomplexity(n=4, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_5_diff = (
        'NL_MS_LZcomplexity_5_diff',
        NL_MS_LZcomplexity(n=5, PreProc='diff'))

    # outs: None
    # tags: LempelZiv,MichaelSmall,complexity,mex
    NL_MS_LZcomplexity_10_diff = (
        'NL_MS_LZcomplexity_10_diff',
        NL_MS_LZcomplexity(n=10, PreProc='diff'))

    # outs: firstunder001,firstunder002,firstunder005,firstunder01,firstunder02
    # outs: max1stepchange,meanpfnn,pfnn_1,pfnn_10,pfnn_2
    # outs: pfnn_3,pfnn_4,pfnn_5,pfnn_6,pfnn_7
    # outs: pfnn_8,pfnn_9,stdpfnn
    # tags: MichaelSmall,fnn,nonlinear,slow
    NL_MS_fnn_1_10_mi_5_1 = (
        'NL_MS_fnn_1_10_mi_5_1',
        NL_MS_fnn(de=MatlabSequence('1:10'), tau='mi', th=5, kth=1))

    # outs: ac1,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,dwts,ftbth
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,msqerr,normksstat,normp,p1_5
    # outs: p2_5,p3_5,p4_5,p5_5,popt
    # outs: propbth,rmse,sbc1,stde
    # tags: MichaelSmall,model,nlpe,nonlinear,slow
    NL_MS_nlpe_fnn_mi = (
        'NL_MS_nlpe_fnn_mi',
        NL_MS_nlpe(de='fnn', tau='mi'))

    # outs: ac1,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,dwts,ftbth
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,msqerr,normksstat,normp,p1_5
    # outs: p2_5,p3_5,p4_5,p5_5,popt
    # outs: propbth,rmse,sbc1,stde
    # tags: MichaelSmall,model,nlpe,nonlinear
    NL_MS_nlpe_2_mi = (
        'NL_MS_nlpe_2_mi',
        NL_MS_nlpe(de=2, tau='mi'))

    # outs: ac1,ac1n,ac2,ac2n,ac3
    # outs: ac3n,acmnd0,acsnd0,dwts,ftbth
    # outs: maxonmean,meanabs,meane,minfpe,minsbc
    # outs: mms,msqerr,normksstat,normp,p1_5
    # outs: p2_5,p3_5,p4_5,p5_5,popt
    # outs: propbth,rmse,sbc1,stde
    # tags: MichaelSmall,model,nlpe,nonlinear
    NL_MS_nlpe_3_ac = (
        'NL_MS_nlpe_3_ac',
        NL_MS_nlpe(de=3, tau='ac'))

    # outs: bestestd,bestestdstd,bestgoodness,bestscrd,longestscr
    # outs: maxd,maxmd,meanstd,mediand,mind
    # outs: ranged
    # tags: dimension,entropy,nonlinear,tisean
    NL_TISEAN_c1_1_1_7_002_05 = (
        'NL_TISEAN_c1_1_1_7_002_05',
        NL_TISEAN_c1(tau=1, mmm=(1.0, 7.0), tsep=0.02, Nref=0.5))

    # outs: bestestd,bestestdstd,bestgoodness,bestscrd,longestscr
    # outs: maxd,maxmd,meanstd,mediand,mind
    # outs: ranged
    # tags: dimension,entropy,nonlinear,tisean
    NL_TISEAN_c1_1_2_6_25_01 = (
        'NL_TISEAN_c1_1_2_6_25_01',
        NL_TISEAN_c1(tau=1, mmm=(2.0, 6.0), tsep=25, Nref=0.1))

    # outs: bend2_maxdim,bend2_meandim,bend2_meangoodness,bend2_mindim,bend2g_maxdim
    # outs: bend2g_meandim,bend2g_meangoodness,bend2g_mindim,benmmind2_goodness,benmmind2_linrmserr
    # outs: benmmind2_logminl,benmmind2_stabledim,benmmind2g_goodness,benmmind2g_linrmserr,benmmind2g_logminl
    # outs: benmmind2g_stabledim,d2_dimest,d2_dimstd,d2_goodness,d2_logmaxscr
    # outs: d2_logminscr,d2_logscr,d2g_dimest,d2g_dimstd,d2g_goodness
    # outs: d2g_logmaxscr,d2g_logminscr,d2g_logscr,flatsh2min_goodness,flatsh2min_linrmserr
    # outs: flatsh2min_ri1,flatsh2min_stabled,h2bestgoodness,h2besth2,h2meangoodness
    # outs: meanh2,medianh2,slopesh2_goodness,slopesh2_linrmserr,slopesh2_ri1
    # outs: slopesh2_stabled,takens05_iqr,takens05_max,takens05_mean,takens05_median
    # outs: takens05_min,takens05_std,takens05mmin_goodness,takens05mmin_linrmserr,takens05mmin_ri
    # outs: takens05mmin_stabled
    # tags: dimension,nonlinear,tisean
    NL_TISEAN_d2_1_10_0 = (
        'NL_TISEAN_d2_1_10_0',
        NL_TISEAN_d2(tau=1, maxm=10, theilerwin=0))

    # outs: bend2_maxdim,bend2_meandim,bend2_meangoodness,bend2_mindim,bend2g_maxdim
    # outs: bend2g_meandim,bend2g_meangoodness,bend2g_mindim,benmmind2_goodness,benmmind2_linrmserr
    # outs: benmmind2_logminl,benmmind2_stabledim,benmmind2g_goodness,benmmind2g_linrmserr,benmmind2g_logminl
    # outs: benmmind2g_stabledim,d2_dimest,d2_dimstd,d2_goodness,d2_logmaxscr
    # outs: d2_logminscr,d2_logscr,d2g_dimest,d2g_dimstd,d2g_goodness
    # outs: d2g_logmaxscr,d2g_logminscr,d2g_logscr,flatsh2min_goodness,flatsh2min_linrmserr
    # outs: flatsh2min_ri1,flatsh2min_stabled,h2bestgoodness,h2besth2,h2meangoodness
    # outs: meanh2,medianh2,slopesh2_goodness,slopesh2_linrmserr,slopesh2_ri1
    # outs: slopesh2_stabled,takens05_iqr,takens05_max,takens05_mean,takens05_median
    # outs: takens05_min,takens05_std,takens05mmin_goodness,takens05mmin_linrmserr,takens05mmin_ri
    # outs: takens05mmin_stabled
    # tags: dimension,nonlinear,tisean
    NL_TISEAN_d2_ac_10_001 = (
        'NL_TISEAN_d2_ac_10_001',
        NL_TISEAN_d2(tau='ac', maxm=10, theilerwin=0.01))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_c,expfit_r2
    # outs: expfit_rmse,linfit_a,linfit_b,linfit_rmsqres,maxDq
    # outs: maxq,meanDq,meanq,minDq,minq
    # outs: rangeDq,rangeq
    # tags: correlation,dimension,nonlinear,stochastic,tstool
    NL_TSTL_FractalDimensions_2_100_02_1_5_10_32_1_5 = (
        'NL_TSTL_FractalDimensions_2_100_02_1_5_10_32_1_5',
        NL_TSTL_FractalDimensions(kmin=2, kmax=100, Nref=0.2, gstart=1, gend=5, past=10, steps=32,
                                  embedparams=(1.0, 5.0)))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_c,expfit_r2
    # outs: expfit_rmse,linfit_a,linfit_b,linfit_rmsqres,maxDq
    # outs: maxq,meanDq,meanq,minDq,minq
    # outs: rangeDq,rangeq
    # tags: correlation,dimension,nonlinear,stochastic,tstool
    NL_TSTL_FractalDimensions_5_100_02_1_10_0_32_ac_3 = (
        'NL_TSTL_FractalDimensions_5_100_02_1_10_0_32_ac_3',
        NL_TSTL_FractalDimensions(kmin=5, kmax=100, Nref=0.2, gstart=1, gend=10, past=0, steps=32,
                                  embedparams=('ac', 3)))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_c,expfit_r2
    # outs: expfit_rmse,linfit_a,linfit_b,linfit_rmsqres,maxDq
    # outs: maxq,meanDq,meanq,minDq,minq
    # outs: rangeDq,rangeq
    # tags: correlation,dimension,nonlinear,tstool
    NL_TSTL_FractalDimensions_2_10_n1_1_5_10_32_1_5 = (
        'NL_TSTL_FractalDimensions_2_10_n1_1_5_10_32_1_5',
        NL_TSTL_FractalDimensions(kmin=2, kmax=10, Nref=-1, gstart=1, gend=5, past=10, steps=32,
                                  embedparams=(1.0, 5.0)))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_c,expfit_r2
    # outs: expfit_rmse,linfit_a,linfit_b,linfit_rmsqres,maxDq
    # outs: maxq,meanDq,meanq,minDq,minq
    # outs: rangeDq,rangeq
    # tags: correlation,dimension,nonlinear,stochastic,tstool
    NL_TSTL_FractalDimensions_2_100_02_1_5_10_32_ac_5 = (
        'NL_TSTL_FractalDimensions_2_100_02_1_5_10_32_ac_5',
        NL_TSTL_FractalDimensions(kmin=2, kmax=100, Nref=0.2, gstart=1, gend=5, past=10, steps=32,
                                  embedparams=('ac', 5)))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_c,expfit_r2
    # outs: expfit_rmse,linfit_a,linfit_b,linfit_rmsqres,maxDq
    # outs: maxq,meanDq,meanq,minDq,minq
    # outs: rangeDq,rangeq
    # tags: correlation,dimension,nonlinear,stochastic,tstool
    NL_TSTL_FractalDimensions_5_20_02_1_10_0_32_ac_cao = (
        'NL_TSTL_FractalDimensions_5_20_02_1_10_0_32_ac_cao',
        NL_TSTL_FractalDimensions(kmin=5, kmax=20, Nref=0.2, gstart=1, gend=10, past=0, steps=32,
                                  embedparams=('ac', 'cao')))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum2,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum2_n1_01_40_20_ac_cao = (
        'NL_TSTL_GPCorrSum2_n1_01_40_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.1, thwin=40, nbins=20, embedparams=('ac', 'cao'), dotwo=2))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum_n1_05_40_20_ac_cao = (
        'NL_TSTL_GPCorrSum_n1_05_40_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.5, thwin=40, nbins=20, embedparams=('ac', 'cao')))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum_n1_01_40_20_ac_cao = (
        'NL_TSTL_GPCorrSum_n1_01_40_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.1, thwin=40, nbins=20, embedparams=('ac', 'cao')))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum_n1_01_40_40_ac_cao = (
        'NL_TSTL_GPCorrSum_n1_01_40_40_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.1, thwin=40, nbins=40, embedparams=('ac', 'cao')))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum2,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum2_n1_05_100_20_ac_cao = (
        'NL_TSTL_GPCorrSum2_n1_05_100_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.5, thwin=100, nbins=20, embedparams=('ac', 'cao'), dotwo=2))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum_n1_05_100_20_ac_cao = (
        'NL_TSTL_GPCorrSum_n1_05_100_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.5, thwin=100, nbins=20, embedparams=('ac', 'cao')))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum2,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum2_n1_05_40_20_ac_cao = (
        'NL_TSTL_GPCorrSum2_n1_05_40_20_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.5, thwin=40, nbins=20, embedparams=('ac', 'cao'), dotwo=2))

    # outs: maxlnCr,maxlnr,meanlnCr,minlnCr,minlnr
    # outs: rangelnCr,robfit_a1,robfit_a2,robfit_s,robfit_sea1
    # outs: robfit_sea2,robfit_sigrat,robfitresac1,robfitresmeanabs,robfitresmeansq
    # tags: correlation,corrsum2,nonlinear,stochastic,tstool
    NL_TSTL_GPCorrSum2_n1_01_40_40_ac_cao = (
        'NL_TSTL_GPCorrSum2_n1_01_40_40_ac_cao',
        NL_TSTL_GPCorrSum(Nref=-1, r=0.1, thwin=40, nbins=40, embedparams=('ac', 'cao'), dotwo=2))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_r2,expfit_rmse
    # outs: maxp,ncross08max,ncross09max,p2,p3
    # outs: p4,p5,pcross08max,pcross09max,to05max
    # outs: to07max,to08max,to095max,to09max,ve_gradient
    # outs: ve_intercept,ve_meanabsres,ve_minbad,ve_rmsres,vse_gradient
    # outs: vse_intercept,vse_meanabsres,vse_minbad,vse_rmsres
    # tags: largelyap,nonlinear,stochastic,tstool
    NL_TSTL_LargestLyap_05_01_001_3_mi_cao = (
        'NL_TSTL_LargestLyap_05_01_001_3_mi_cao',
        NL_TSTL_LargestLyap(Nref=0.5, maxtstep=0.1, past=0.01, NNR=3, embedparams=('mi', 'cao')))

    # outs: expfit_a,expfit_adjr2,expfit_b,expfit_r2,expfit_rmse
    # outs: maxp,ncross08max,ncross09max,p2,p3
    # outs: p4,p5,pcross08max,pcross09max,to05max
    # outs: to07max,to08max,to095max,to09max,ve_gradient
    # outs: ve_intercept,ve_meanabsres,ve_minbad,ve_rmsres,vse_gradient
    # outs: vse_intercept,vse_meanabsres,vse_minbad,vse_rmsres
    # tags: largelyap,nonlinear,tstool
    NL_TSTL_LargestLyap_n1_01_001_3_1_4 = (
        'NL_TSTL_LargestLyap_n1_01_001_3_1_4',
        NL_TSTL_LargestLyap(Nref=-1, maxtstep=0.1, past=0.01, NNR=3, embedparams=(1.0, 4.0)))

    # outs: ac1D,ac1x,ac1y,ac2D,ac2x
    # outs: ac2y,boxarea,hboxcounts10,hboxcounts5,iqrD
    # outs: iqrds,iqrx,iqry,maxD,maxds
    # outs: maxpbox10,maxpbox5,maxx,maxy,meanD
    # outs: meands,meanpbox10,meanpbox5,meanx,meany
    # outs: minD,minds,minpbox10,minpbox5,minx
    # outs: miny,pcross,pwithin02,pwithin03,pwithin05
    # outs: pwithin1,pwithin2,pwithinr01,rangepbox10,rangepbox5
    # outs: stdD,stdx,stdy,tauacD,tauacx
    # outs: tauacy,tracepbox10,tracepbox5,zerospbox10,zerospbox5
    # tags: nonlinear,poincare,tstool
    NL_TSTL_PoincareSection_max_ac = (
        'NL_TSTL_PoincareSection_max_ac',
        NL_TSTL_PoincareSection(ref='max', embedparams=('ac', 3)))

    # outs: ac1D,ac1x,ac1y,ac2D,ac2x
    # outs: ac2y,boxarea,hboxcounts10,hboxcounts5,iqrD
    # outs: iqrds,iqrx,iqry,maxD,maxds
    # outs: maxpbox10,maxpbox5,maxx,maxy,meanD
    # outs: meands,meanpbox10,meanpbox5,meanx,meany
    # outs: minD,minds,minpbox10,minpbox5,minx
    # outs: miny,pcross,pwithin02,pwithin03,pwithin05
    # outs: pwithin1,pwithin2,pwithinr01,rangepbox10,rangepbox5
    # outs: stdD,stdx,stdy,tauacD,tauacx
    # outs: tauacy,tracepbox10,tracepbox5,zerospbox10,zerospbox5
    # tags: nonlinear,poincare,tstool
    NL_TSTL_PoincareSection_max_1 = (
        'NL_TSTL_PoincareSection_max_1',
        NL_TSTL_PoincareSection(ref='max', embedparams=(1.0, 3.0)))

    # outs: ac1D,ac1x,ac1y,ac2D,ac2x
    # outs: ac2y,boxarea,hboxcounts10,hboxcounts5,iqrD
    # outs: iqrds,iqrx,iqry,maxD,maxds
    # outs: maxpbox10,maxpbox5,maxx,maxy,meanD
    # outs: meands,meanpbox10,meanpbox5,meanx,meany
    # outs: minD,minds,minpbox10,minpbox5,minx
    # outs: miny,pcross,pwithin02,pwithin03,pwithin05
    # outs: pwithin1,pwithin2,pwithinr01,rangepbox10,rangepbox5
    # outs: stdD,stdx,stdy,tauacD,tauacx
    # outs: tauacy,tracepbox10,tracepbox5,zerospbox10,zerospbox5
    # tags: nonlinear,poincare,tstool
    NL_TSTL_PoincareSection_max_mi = (
        'NL_TSTL_PoincareSection_max_mi',
        NL_TSTL_PoincareSection(ref='max', embedparams=('mi', 3)))

    # outs: hcgdist,hhist,hhisthist,iqr,max
    # outs: maxhisthist,maxpeaksep,meanpeaksep,minpeaksep,pg05
    # outs: phisthistmin,pzeros,pzeroscgdist,rangecgdist,rangepeaksep
    # outs: statrtym,statrtys,std,stdpeaksep
    # tags: nonlinear,returntime,tstool
    NL_TSTL_ReturnTime_005_1_005_n1_1_3 = (
        'NL_TSTL_ReturnTime_005_1_005_n1_1_3',
        NL_TSTL_ReturnTime(NNR=0.05, maxT=1, past=0.05, Nref=-1, embedparams=(1.0, 3.0)))

    # outs: hcgdist,hhist,hhisthist,iqr,max
    # outs: maxhisthist,maxpeaksep,meanpeaksep,minpeaksep,pg05
    # outs: phisthistmin,pzeros,pzeroscgdist,rangecgdist,rangepeaksep
    # outs: statrtym,statrtys,std,stdpeaksep
    # tags: nonlinear,returntime,tstool
    NL_TSTL_ReturnTime_10_1_1_n1_ac_8 = (
        'NL_TSTL_ReturnTime_10_1_1_n1_ac_8',
        NL_TSTL_ReturnTime(NNR=10, maxT=1, past=1, Nref=-1, embedparams=('ac', 8)))

    # outs: hcgdist,hhist,hhisthist,iqr,max
    # outs: maxhisthist,maxpeaksep,meanpeaksep,minpeaksep,pg05
    # outs: phisthistmin,pzeros,pzeroscgdist,rangecgdist,rangepeaksep
    # outs: statrtym,statrtys,std,stdpeaksep
    # tags: nonlinear,returntime,tstool
    NL_TSTL_ReturnTime_5_1_40_n1_1_8 = (
        'NL_TSTL_ReturnTime_5_1_40_n1_1_8',
        NL_TSTL_ReturnTime(NNR=5, maxT=1, past=40, Nref=-1, embedparams=(1.0, 8.0)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_ac_3 = (
        'NL_TSTL_TakensEstimator_n1_005_005_ac_3',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('ac', 3)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_mi_8 = (
        'NL_TSTL_TakensEstimator_n1_005_005_mi_8',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('mi', 8)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_mi_3 = (
        'NL_TSTL_TakensEstimator_n1_005_005_mi_3',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('mi', 3)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_ac_8 = (
        'NL_TSTL_TakensEstimator_n1_005_005_ac_8',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('ac', 8)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_mi_cao = (
        'NL_TSTL_TakensEstimator_n1_005_005_mi_cao',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('mi', 'cao')))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_01_005_1_10 = (
        'NL_TSTL_TakensEstimator_n1_01_005_1_10',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.1, past=0.05, embedparams=(1.0, 10.0)))

    # outs: None
    # tags: crptool,dimension,nonlinear,scaling,stochastic,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_mi_fnnmar = (
        'NL_TSTL_TakensEstimator_n1_005_005_mi_fnnmar',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=('mi', 'fnnmar')))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_1_3 = (
        'NL_TSTL_TakensEstimator_n1_005_005_1_3',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=(1.0, 3.0)))

    # outs: None
    # tags: dimension,nonlinear,scaling,takens,tstool
    NL_TSTL_TakensEstimator_n1_005_005_1_8 = (
        'NL_TSTL_TakensEstimator_n1_005_005_1_8',
        NL_TSTL_TakensEstimator(Nref=-1, rad=0.05, past=0.05, embedparams=(1.0, 8.0)))

    # outs: ac1_acpf_1,ac1_acpf_10,ac1_acpf_2,ac1_acpf_3,ac1_acpf_4
    # outs: ac1_acpf_5,ac1_acpf_6,ac1_acpf_7,ac1_acpf_8,ac1_acpf_9
    # outs: iqracpf_1,iqracpf_10,iqracpf_2,iqracpf_3,iqracpf_4
    # outs: iqracpf_5,iqracpf_6,iqracpf_7,iqracpf_8,iqracpf_9
    # outs: macpf_1,macpf_10,macpf_2,macpf_3,macpf_4
    # outs: macpf_5,macpf_6,macpf_7,macpf_8,macpf_9
    # outs: macpfdrop_1,macpfdrop_2,macpfdrop_3,macpfdrop_4,macpfdrop_5
    # outs: macpfdrop_6,macpfdrop_7,macpfdrop_8,macpfdrop_9,mmacpfdiff
    # outs: propdecmacpf,sacpf_1,sacpf_10,sacpf_2,sacpf_3
    # outs: sacpf_4,sacpf_5,sacpf_6,sacpf_7,sacpf_8
    # outs: sacpf_9,stdmacpfdiff
    # tags: acp,correlation,nonlinear,stochastic,tstool
    NL_TSTL_acp_mi_1__10 = (
        'NL_TSTL_acp_mi_1__10',
        NL_TSTL_acp(tau='mi', past=1, maxdelay=(), maxdim=10, Nref=()))

    # outs: ac1_acpf_1,ac1_acpf_10,ac1_acpf_2,ac1_acpf_3,ac1_acpf_4
    # outs: ac1_acpf_5,ac1_acpf_6,ac1_acpf_7,ac1_acpf_8,ac1_acpf_9
    # outs: iqracpf_1,iqracpf_10,iqracpf_2,iqracpf_3,iqracpf_4
    # outs: iqracpf_5,iqracpf_6,iqracpf_7,iqracpf_8,iqracpf_9
    # outs: macpf_1,macpf_10,macpf_2,macpf_3,macpf_4
    # outs: macpf_5,macpf_6,macpf_7,macpf_8,macpf_9
    # outs: macpfdrop_1,macpfdrop_2,macpfdrop_3,macpfdrop_4,macpfdrop_5
    # outs: macpfdrop_6,macpfdrop_7,macpfdrop_8,macpfdrop_9,mmacpfdiff
    # outs: propdecmacpf,sacpf_1,sacpf_10,sacpf_2,sacpf_3
    # outs: sacpf_4,sacpf_5,sacpf_6,sacpf_7,sacpf_8
    # outs: sacpf_9,stdmacpfdiff
    # tags: acp,correlation,nonlinear,slow,stochastic,tstool
    NL_TSTL_acp_1_001_025_10_05 = (
        'NL_TSTL_acp_1_001_025_10_05',
        NL_TSTL_acp(tau=1, past=0.01, maxdelay=0.25, maxdim=10, Nref=0.5))

    # outs: bc_lfitb1,bc_lfitb2,bc_lfitb3,bc_lfitbmax,bc_lfitm1
    # outs: bc_lfitm2,bc_lfitm3,bc_lfitmeansqdev1,bc_lfitmeansqdev2,bc_lfitmeansqdev3
    # outs: bc_lfitmeansqdevmax,bc_lfitmmax,bc_maxscalingexp,bc_mbestfit,bc_meandiff
    # outs: bc_meanm1,bc_meanm2,bc_meanm3,bc_meanmmax,bc_meanscalingexp
    # outs: bc_mindiff,bc_minm1,bc_minm2,bc_minm3,bc_minmmax
    # outs: bc_minscalingexp,bc_range1,bc_range2,bc_range3,bc_rangemmax
    # outs: co_lfitb1,co_lfitb2,co_lfitb3,co_lfitbmax,co_lfitm1
    # outs: co_lfitm2,co_lfitm3,co_lfitmeansqdev1,co_lfitmeansqdev2,co_lfitmeansqdev3
    # outs: co_lfitmeansqdevmax,co_lfitmmax,co_maxscalingexp,co_mbestfit,co_meandiff
    # outs: co_meanm1,co_meanm2,co_meanm3,co_meanmmax,co_meanscalingexp
    # outs: co_mindiff,co_minm1,co_minm2,co_minm3,co_minmmax
    # outs: co_minscalingexp,co_range1,co_range2,co_range3,co_rangemmax
    # outs: in_lfitb1,in_lfitb2,in_lfitb3,in_lfitbmax,in_lfitm1
    # outs: in_lfitm2,in_lfitm3,in_lfitmeansqdev1,in_lfitmeansqdev2,in_lfitmeansqdev3
    # outs: in_lfitmeansqdevmax,in_lfitmmax,in_maxscalingexp,in_mbestfit,in_meandiff
    # outs: in_meanm1,in_meanm2,in_meanm3,in_meanmmax,in_meanscalingexp
    # outs: in_mindiff,in_minm1,in_minm2,in_minm3,in_minmmax
    # outs: in_minscalingexp,in_range1,in_range2,in_range3,in_rangemmax
    # outs: scr_bc_m1_logrmax,scr_bc_m1_logrmin,scr_bc_m1_logrrange,scr_bc_m1_meanabsres,scr_bc_m1_meansqres
    # outs: scr_bc_m1_minbad,scr_bc_m1_pgone,scr_bc_m1_scaling_exp,scr_bc_m1_scaling_int,scr_bc_m2_logrmax
    # outs: scr_bc_m2_logrmin,scr_bc_m2_logrrange,scr_bc_m2_meanabsres,scr_bc_m2_meansqres,scr_bc_m2_minbad
    # outs: scr_bc_m2_pgone,scr_bc_m2_scaling_exp,scr_bc_m2_scaling_int,scr_bc_m3_logrmax,scr_bc_m3_logrmin
    # outs: scr_bc_m3_logrrange,scr_bc_m3_meanabsres,scr_bc_m3_meansqres,scr_bc_m3_minbad,scr_bc_m3_pgone
    # outs: scr_bc_m3_scaling_exp,scr_bc_m3_scaling_int,scr_bc_mopt_logrmax,scr_bc_mopt_logrmin,scr_bc_mopt_logrrange
    # outs: scr_bc_mopt_meanabsres,scr_bc_mopt_meansqres,scr_bc_mopt_minbad,scr_bc_mopt_pgone,scr_bc_mopt_scaling_exp
    # outs: scr_bc_mopt_scaling_int,scr_co_m1_logrmax,scr_co_m1_logrmin,scr_co_m1_logrrange,scr_co_m1_meanabsres
    # outs: scr_co_m1_meansqres,scr_co_m1_minbad,scr_co_m1_pgone,scr_co_m1_scaling_exp,scr_co_m1_scaling_int
    # outs: scr_co_m2_logrmax,scr_co_m2_logrmin,scr_co_m2_logrrange,scr_co_m2_meanabsres,scr_co_m2_meansqres
    # outs: scr_co_m2_minbad,scr_co_m2_pgone,scr_co_m2_scaling_exp,scr_co_m2_scaling_int,scr_co_m3_logrmax
    # outs: scr_co_m3_logrmin,scr_co_m3_logrrange,scr_co_m3_meanabsres,scr_co_m3_meansqres,scr_co_m3_minbad
    # outs: scr_co_m3_pgone,scr_co_m3_scaling_exp,scr_co_m3_scaling_int,scr_co_mopt_logrmax,scr_co_mopt_logrmin
    # outs: scr_co_mopt_logrrange,scr_co_mopt_meanabsres,scr_co_mopt_meansqres,scr_co_mopt_minbad,scr_co_mopt_pgone
    # outs: scr_co_mopt_scaling_exp,scr_co_mopt_scaling_int,scr_in_m1_logrmax,scr_in_m1_logrmin,scr_in_m1_logrrange
    # outs: scr_in_m1_meanabsres,scr_in_m1_meansqres,scr_in_m1_minbad,scr_in_m1_pgone,scr_in_m1_scaling_exp
    # outs: scr_in_m1_scaling_int,scr_in_m2_logrmax,scr_in_m2_logrmin,scr_in_m2_logrrange,scr_in_m2_meanabsres
    # outs: scr_in_m2_meansqres,scr_in_m2_minbad,scr_in_m2_pgone,scr_in_m2_scaling_exp,scr_in_m2_scaling_int
    # outs: scr_in_m3_logrmax,scr_in_m3_logrmin,scr_in_m3_logrrange,scr_in_m3_meanabsres,scr_in_m3_meansqres
    # outs: scr_in_m3_minbad,scr_in_m3_pgone,scr_in_m3_scaling_exp,scr_in_m3_scaling_int,scr_in_mopt_logrmax
    # outs: scr_in_mopt_logrmin,scr_in_mopt_logrrange,scr_in_mopt_meanabsres,scr_in_mopt_meansqres,scr_in_mopt_minbad
    # outs: scr_in_mopt_pgone,scr_in_mopt_scaling_exp,scr_in_mopt_scaling_int
    # tags: dimension,nonlinear,scaling,stochastic,tstool
    NL_TSTL_dimensions_50_ac_cao = (
        'NL_TSTL_dimensions_50_ac_cao',
        NL_TSTL_dimensions(nbins=50, embedParams=('ac', 'cao')))

    # outs: fnn10,fnn2,fnn3,fnn4,fnn5
    # outs: fnn6,fnn7,fnn8,fnn9,m005
    # outs: m01,m02,m05,mdrop,pdrop
    # tags: crptool,dimension,nonlinear,stochastic
    NL_crptool_fnn_10_2_ac = (
        'NL_crptool_fnn_10_2_ac',
        NL_crptool_fnn(maxm=10, r=2, taum='ac'))

    # outs: fnn10,fnn2,fnn3,fnn4,fnn5
    # outs: fnn6,fnn7,fnn8,fnn9,m005
    # outs: m01,m02,m05,mdrop,pdrop
    # tags: crptool,dimension,nonlinear,stochastic
    NL_crptool_fnn_10_2_1 = (
        'NL_crptool_fnn_10_2_1',
        NL_crptool_fnn(maxm=10, r=2, taum=1))

    # outs: fnn10,fnn2,fnn3,fnn4,fnn5
    # outs: fnn6,fnn7,fnn8,fnn9,m005
    # outs: m01,m02,m05,mdrop,pdrop
    # tags: crptool,dimension,nonlinear,stochastic
    NL_crptool_fnn_10_2_mi = (
        'NL_crptool_fnn_10_2_mi',
        NL_crptool_fnn(maxm=10, r=2, taum='mi'))

    # outs: fb001,fb01,max,min,nto80
    # outs: nto90,range,std,top2
    # tags: pca,tdembedding
    NL_embed_PCA_mi_10 = (
        'NL_embed_PCA_mi_10',
        NL_embed_PCA(tau='mi', m=10))

    # outs: fb001,fb01,max,min,nto80
    # outs: nto90,range,std,top2
    # tags: pca,tdembedding
    NL_embed_PCA_1_10 = (
        'NL_embed_PCA_1_10',
        NL_embed_PCA(tau=1, m=10))

    # outs: dexpk_adjr2,dexpk_r2,dexpk_resAC1,dexpk_resAC2,dexpk_resruns
    # outs: dexpk_rmse,dgaussk_adjr2,dgaussk_r2,dgaussk_resAC1,dgaussk_resAC2
    # outs: dgaussk_resruns,dgaussk_rmse,dpowerk_adjr2,dpowerk_r2,dpowerk_resAC1
    # outs: dpowerk_resAC2,dpowerk_resruns,dpowerk_rmse,evnlogL,evparm1
    # outs: evparm2,explambda,expmu,expnlogL,gaussmu
    # outs: gaussnlogL,gausssigma,iqrk,kac1,kac2
    # outs: kac3,ktau,maxent,maxk,maxonmedian
    # outs: meanchent,meanent,meank,mediank,mink
    # outs: minnbinmaxent,modek,ol90,olu90,propmode
    # outs: rangek,stdk
    # tags: lengthdep,network,visibilitygraph
    NW_VisibilityGraph_horiz = (
        'NW_VisibilityGraph_horiz',
        NW_VisibilityGraph(meth='horiz'))

    # outs: th1,th2,th3,th4,th5
    # outs: th6,th7
    # tags: periodicity,spline
    PD_PeriodicityWang = (
        'PD_PeriodicityWang',
        PD_PeriodicityWang())

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,pcrossdown,pcrossup,proppos
    # outs: range,std,tau
    # tags: dblwell,dynsys
    PH_ForcePotential_dblwell_1_02_01 = (
        'PH_ForcePotential_dblwell_1_02_01',
        PH_ForcePotential(whatpot='dblwell', params=(1.0, 0.20000000000000001, 0.10000000000000001)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,pcrossdown,pcrossup,proppos
    # outs: range,std,tau
    # tags: dblwell,dynsys
    PH_ForcePotential_dblwell_3_001_01 = (
        'PH_ForcePotential_dblwell_3_001_01',
        PH_ForcePotential(whatpot='dblwell', params=(3.0, 0.01, 0.10000000000000001)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,proppos,range,std
    # outs: tau
    # tags: dynsys,sine
    PH_ForcePotential_sine_3_05_1 = (
        'PH_ForcePotential_sine_3_05_1',
        PH_ForcePotential(whatpot='sine', params=(3.0, 0.5, 1.0)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,pcrossdown,pcrossup,proppos
    # outs: range,std,tau
    # tags: dblwell,dynsys
    PH_ForcePotential_dblwell_1_05_02 = (
        'PH_ForcePotential_dblwell_1_05_02',
        PH_ForcePotential(whatpot='dblwell', params=(1.0, 0.5, 0.20000000000000001)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,proppos,range,std
    # outs: tau
    # tags: dynsys,sine
    PH_ForcePotential_sine_1_1_1 = (
        'PH_ForcePotential_sine_1_1_1',
        PH_ForcePotential(whatpot='sine', params=(1.0, 1.0, 1.0)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,pcrossdown,pcrossup,proppos
    # outs: range,std,tau
    # tags: dblwell,dynsys
    PH_ForcePotential_dblwell_2_005_02 = (
        'PH_ForcePotential_dblwell_2_005_02',
        PH_ForcePotential(whatpot='dblwell', params=(2.0, 0.050000000000000003, 0.20000000000000001)))

    # outs: ac1,ac10,ac50,finaldev,mean
    # outs: median,pcross,proppos,range,std
    # outs: tau
    # tags: dynsys,sine
    PH_ForcePotential_sine_10_004_10 = (
        'PH_ForcePotential_sine_10_004_10',
        PH_ForcePotential(whatpot='sine', params=(10.0, 0.040000000000000001, 10.0)))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_prop_09 = (
        'PH_Walker_prop_09',
        PH_Walker(walkerrule='prop', wparam=0.9))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_momentum_5 = (
        'PH_Walker_momentum_5',
        PH_Walker(walkerrule='momentum', wparam=5))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_biasprop_01_05 = (
        'PH_Walker_biasprop_01_05',
        PH_Walker(walkerrule='biasprop', wparam=(0.10000000000000001, 0.5)))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_runningvar_15_50 = (
        'PH_Walker_runningvar_15_50',
        PH_Walker(walkerrule='runningvar', wparam=(1.5, 50.0)))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_momentum_2 = (
        'PH_Walker_momentum_2',
        PH_Walker(walkerrule='momentum', wparam=2))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_prop_05 = (
        'PH_Walker_prop_05',
        PH_Walker(walkerrule='prop', wparam=0.5))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_biasprop_05_01 = (
        'PH_Walker_biasprop_05_01',
        PH_Walker(walkerrule='biasprop', wparam=(0.5, 0.10000000000000001)))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_prop_11 = (
        'PH_Walker_prop_11',
        PH_Walker(walkerrule='prop', wparam=1.1))

    # outs: res_ac1,res_runstest,res_swss5_1,sw_ac1rat,sw_ansarib_pval
    # outs: sw_distdiff,sw_maxrat,sw_meanabsdiff,sw_minrat,sw_propcross
    # outs: sw_stdrat,sw_taudiff,w_ac1,w_ac2,w_max
    # outs: w_mean,w_median,w_min,w_propzcross,w_std
    # outs: w_tau
    # tags: trend
    PH_Walker_prop_01 = (
        'PH_Walker_prop_01',
        PH_Walker(walkerrule='prop', wparam=0.1))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_medianf4 = (
        'PP_Compare_medianf4',
        PP_Compare(detrndmeth='medianf4'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_medianf3 = (
        'PP_Compare_medianf3',
        PP_Compare(detrndmeth='medianf3'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_rav4 = (
        'PP_Compare_rav4',
        PP_Compare(detrndmeth='rav4'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_rav3 = (
        'PP_Compare_rav3',
        PP_Compare(detrndmeth='rav3'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw
    PP_Compare_poly1 = (
        'PP_Compare_poly1',
        PP_Compare(detrndmeth='poly1'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw,spline
    PP_Compare_spline24 = (
        'PP_Compare_spline24',
        PP_Compare(detrndmeth='spline24'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_resample_2_1 = (
        'PP_Compare_resample_2_1',
        PP_Compare(detrndmeth='resample_2_1'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw
    PP_Compare_poly2 = (
        'PP_Compare_poly2',
        PP_Compare(detrndmeth='poly2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_resample_1_2 = (
        'PP_Compare_resample_1_2',
        PP_Compare(detrndmeth='resample_1_2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw,spline
    PP_Compare_spline44 = (
        'PP_Compare_spline44',
        PP_Compare(detrndmeth='spline44'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_medianf2 = (
        'PP_Compare_medianf2',
        PP_Compare(detrndmeth='medianf2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw,spline
    PP_Compare_spline64 = (
        'PP_Compare_spline64',
        PP_Compare(detrndmeth='spline64'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_sin1 = (
        'PP_Compare_sin1',
        PP_Compare(detrndmeth='sin1'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_rav2 = (
        'PP_Compare_rav2',
        PP_Compare(detrndmeth='rav2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_medianf10 = (
        'PP_Compare_medianf10',
        PP_Compare(detrndmeth='medianf10'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_sin2 = (
        'PP_Compare_sin2',
        PP_Compare(detrndmeth='sin2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: locdep,preprocessing,raw
    PP_Compare_rav10 = (
        'PP_Compare_rav10',
        PP_Compare(detrndmeth='rav10'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw
    PP_Compare_diff2 = (
        'PP_Compare_diff2',
        PP_Compare(detrndmeth='diff2'))

    # outs: gauss1_h10_adjr2,gauss1_h10_r2,gauss1_h10_resAC1,gauss1_h10_resAC2,gauss1_h10_resruns
    # outs: gauss1_h10_rmse,gauss1_kd_adjr2,gauss1_kd_r2,gauss1_kd_resAC1,gauss1_kd_resAC2
    # outs: gauss1_kd_resruns,gauss1_kd_rmse,htdt_chi2n,htdt_ksn,htdt_llfn
    # outs: kscn_adiff,kscn_olapint,kscn_peaksepx,kscn_peaksepy,kscn_relent
    # outs: olbt_m2,olbt_m5,olbt_s2,olbt_s5,statav10
    # outs: statav2,statav4,statav6,statav8,swms10_1
    # outs: swms2_1,swms2_2,swms5_1,swms5_2,swss10_1
    # outs: swss10_2,swss2_1,swss2_2,swss5_1,swss5_2
    # tags: preprocessing,raw
    PP_Compare_diff1 = (
        'PP_Compare_diff1',
        PP_Compare(detrndmeth='diff1'))

    # outs: gauss1_h10_exp,gauss1_h10_jump,gauss1_h10_lin,gauss1_h10_trend,gauss1_kd_exp
    # outs: gauss1_kd_jump,gauss1_kd_lin,gauss1_kd_trend,norm_kscomp_exp,norm_kscomp_jump
    # outs: norm_kscomp_lin,norm_kscomp_trend,normdiff_exp,normdiff_jump,normdiff_lin
    # outs: normdiff_trend,ol_exp,ol_jump,ol_lin,ol_trend
    # outs: statav5_exp,statav5_jump,statav5_lin,statav5_trend,swms5_2_exp
    # outs: swms5_2_jump,swms5_2_lin,swms5_2_trend,swss5_2_exp,swss5_2_jump
    # outs: swss5_2_lin,swss5_2_trend,xc1_exp,xc1_jump,xc1_lin
    # outs: xc1_trend,xcn1_exp,xcn1_jump,xcn1_lin,xcn1_trend
    # tags: preprocessing,raw
    PP_Iterate_diff = (
        'PP_Iterate_diff',
        PP_Iterate(dtMeth='diff'))

    # outs: gauss1_h10_exp,gauss1_h10_jump,gauss1_h10_lin,gauss1_h10_trend,gauss1_kd_exp
    # outs: gauss1_kd_jump,gauss1_kd_lin,gauss1_kd_trend,norm_kscomp_exp,norm_kscomp_jump
    # outs: norm_kscomp_lin,norm_kscomp_trend,normdiff_exp,normdiff_jump,normdiff_lin
    # outs: normdiff_trend,ol_exp,ol_jump,ol_lin,ol_trend
    # outs: statav5_exp,statav5_jump,statav5_lin,statav5_trend,swms5_2_exp
    # outs: swms5_2_jump,swms5_2_lin,swms5_2_trend,swss5_2_exp,swss5_2_jump
    # outs: swss5_2_lin,swss5_2_trend,xc1_exp,xc1_jump,xc1_lin
    # outs: xc1_trend,xcn1_exp,xcn1_jump,xcn1_lin,xcn1_trend
    # tags: locdep,preprocessing,raw
    PP_Iterate_resampledown = (
        'PP_Iterate_resampledown',
        PP_Iterate(dtMeth='resampledown'))

    # outs: gauss1_h10_exp,gauss1_h10_jump,gauss1_h10_lin,gauss1_h10_trend,gauss1_kd_exp
    # outs: gauss1_kd_jump,gauss1_kd_lin,gauss1_kd_trend,norm_kscomp_exp,norm_kscomp_jump
    # outs: norm_kscomp_lin,norm_kscomp_trend,normdiff_exp,normdiff_jump,normdiff_lin
    # outs: normdiff_trend,ol_exp,ol_jump,ol_lin,ol_trend
    # outs: statav5_exp,statav5_jump,statav5_lin,statav5_trend,swms5_2_exp
    # outs: swms5_2_jump,swms5_2_lin,swms5_2_trend,swss5_2_exp,swss5_2_jump
    # outs: swss5_2_lin,swss5_2_trend,xc1_exp,xc1_jump,xc1_lin
    # outs: xc1_trend,xcn1_exp,xcn1_jump,xcn1_lin,xcn1_trend
    # tags: locdep,preprocessing,raw
    PP_Iterate_medianf = (
        'PP_Iterate_medianf',
        PP_Iterate(dtMeth='medianf'))

    # outs: gauss1_h10_exp,gauss1_h10_jump,gauss1_h10_lin,gauss1_h10_trend,gauss1_kd_exp
    # outs: gauss1_kd_jump,gauss1_kd_lin,gauss1_kd_trend,norm_kscomp_exp,norm_kscomp_jump
    # outs: norm_kscomp_lin,norm_kscomp_trend,normdiff_exp,normdiff_jump,normdiff_lin
    # outs: normdiff_trend,ol_exp,ol_jump,ol_lin,ol_trend
    # outs: statav5_exp,statav5_jump,statav5_lin,statav5_trend,swms5_2_exp
    # outs: swms5_2_jump,swms5_2_lin,swms5_2_trend,swss5_2_exp,swss5_2_jump
    # outs: swss5_2_lin,swss5_2_trend,xc1_exp,xc1_jump,xc1_lin
    # outs: xc1_trend,xcn1_exp,xcn1_jump,xcn1_lin,xcn1_trend
    # tags: locdep,preprocessing,raw
    PP_Iterate_resampleup = (
        'PP_Iterate_resampleup',
        PP_Iterate(dtMeth='resampleup'))

    # outs: gauss1_h10_exp,gauss1_h10_jump,gauss1_h10_lin,gauss1_h10_trend,gauss1_kd_exp
    # outs: gauss1_kd_jump,gauss1_kd_lin,gauss1_kd_trend,norm_kscomp_exp,norm_kscomp_jump
    # outs: norm_kscomp_lin,norm_kscomp_trend,normdiff_exp,normdiff_jump,normdiff_lin
    # outs: normdiff_trend,ol_exp,ol_jump,ol_lin,ol_trend
    # outs: statav5_exp,statav5_jump,statav5_lin,statav5_trend,swms5_2_exp
    # outs: swms5_2_jump,swms5_2_lin,swms5_2_trend,swss5_2_exp,swss5_2_jump
    # outs: swss5_2_lin,swss5_2_trend,xc1_exp,xc1_jump,xc1_lin
    # outs: xc1_trend,xcn1_exp,xcn1_jump,xcn1_lin,xcn1_trend
    # tags: locdep,preprocessing,raw
    PP_Iterate_rav = (
        'PP_Iterate_rav',
        PP_Iterate(dtMeth='rav'))

    # outs: rmserrrat_d1,rmserrrat_d2,rmserrrat_d3,rmserrrat_lf_02,rmserrrat_lf_02_d1
    # outs: rmserrrat_p1_10,rmserrrat_p1_20,rmserrrat_p1_40,rmserrrat_p1_5,rmserrrat_p2_10
    # outs: rmserrrat_p2_20,rmserrrat_p2_40,rmserrrat_p2_5,rmserrrat_peaks_08,rmserrrat_peaks_08_d1
    # outs: rmserrrat_rmgd
    # tags: preprocessing,stochastic,trend
    PP_ModelFit_ar_2 = (
        'PP_ModelFit_ar_2',
        PP_ModelFit(model='ar', order=2))

    # outs: h,longstretch0,longstretch1,meanstretch0,meanstretch1
    # outs: meanstretchrat,pstretch0,pstretch1,pstretches,pup
    # outs: pupstat2,rat21stretch0,rat21stretch1,stdstretch0,stdstretch1
    # outs: stdstretchrat
    # tags: distribution,stationarity
    SB_BinaryStats_diff = (
        'SB_BinaryStats_diff',
        SB_BinaryStats(binarymeth='diff'))

    # outs: h,longstretch0,longstretch1,meanstretch0,meanstretch1
    # outs: meanstretchrat,pstretch0,pstretch1,pstretches,pup
    # outs: pupstat2,rat21stretch0,rat21stretch1,stdstretch0,stdstretch1
    # outs: stdstretchrat
    # tags: distribution,stationarity
    SB_BinaryStats_mean = (
        'SB_BinaryStats_mean',
        SB_BinaryStats(binarymeth='mean'))

    # outs: h,longstretch0,longstretch1,meanstretch0,meanstretch1
    # outs: meanstretchrat,pstretch0,pstretch1,pstretches,pup
    # outs: pupstat2,rat21stretch0,rat21stretch1,stdstretch0,stdstretch1
    # outs: stdstretchrat
    # tags: distribution,stationarity
    SB_BinaryStats_iqr = (
        'SB_BinaryStats_iqr',
        SB_BinaryStats(binarymeth='iqr'))

    # outs: None
    # tags: binary
    SB_BinaryStretch_lseq0 = (
        'SB_BinaryStretch_lseq0',
        SB_BinaryStretch(stretchwhat='lseq0'))

    # outs: None
    # tags: binary
    SB_BinaryStretch_lseq1 = (
        'SB_BinaryStretch_lseq1',
        SB_BinaryStretch(stretchwhat='lseq1'))

    # outs: aa,aaa,aaaa,aaab,aaac
    # outs: aab,aaba,aabb,aabc,aac
    # outs: aaca,aacb,aacc,ab,aba
    # outs: abaa,abab,abac,abb,abba
    # outs: abbb,abbc,abc,abca,abcb
    # outs: abcc,ac,aca,acaa,acab
    # outs: acac,acb,acba,acbb,acbc
    # outs: acc,acca,accb,accc,ba
    # outs: baa,baaa,baab,baac,bab
    # outs: baba,babb,babc,bac,baca
    # outs: bacb,bacc,bb,bba,bbaa
    # outs: bbab,bbac,bbb,bbba,bbbb
    # outs: bbbc,bbc,bbca,bbcb,bbcc
    # outs: bc,bca,bcaa,bcab,bcac
    # outs: bcb,bcba,bcbb,bcbc,bcc
    # outs: bcca,bccb,bccc,ca,caa
    # outs: caaa,caab,caac,cab,caba
    # outs: cabb,cabc,cac,caca,cacb
    # outs: cacc,cb,cba,cbaa,cbab
    # outs: cbac,cbb,cbba,cbbb,cbbc
    # outs: cbc,cbca,cbcb,cbcc,cc
    # outs: cca,ccaa,ccab,ccac,ccb
    # outs: ccba,ccbb,ccbc,ccc,ccca
    # outs: cccb,cccc,hh,hhh,hhhh
    # tags: motifs
    SB_MotifThree_diffquant = (
        'SB_MotifThree_diffquant',
        SB_MotifThree(trit='diffquant'))

    # outs: aa,aaa,aaaa,aaab,aaac
    # outs: aab,aaba,aabb,aabc,aac
    # outs: aaca,aacb,aacc,ab,aba
    # outs: abaa,abab,abac,abb,abba
    # outs: abbb,abbc,abc,abca,abcb
    # outs: abcc,ac,aca,acaa,acab
    # outs: acac,acb,acba,acbb,acbc
    # outs: acc,acca,accb,accc,ba
    # outs: baa,baaa,baab,baac,bab
    # outs: baba,babb,babc,bac,baca
    # outs: bacb,bacc,bb,bba,bbaa
    # outs: bbab,bbac,bbb,bbba,bbbb
    # outs: bbbc,bbc,bbca,bbcb,bbcc
    # outs: bc,bca,bcaa,bcab,bcac
    # outs: bcb,bcba,bcbb,bcbc,bcc
    # outs: bcca,bccb,bccc,ca,caa
    # outs: caaa,caab,caac,cab,caba
    # outs: cabb,cabc,cac,caca,cacb
    # outs: cacc,cb,cba,cbaa,cbab
    # outs: cbac,cbb,cbba,cbbb,cbbc
    # outs: cbc,cbca,cbcb,cbcc,cc
    # outs: cca,ccaa,ccab,ccac,ccb
    # outs: ccba,ccbb,ccbc,ccc,ccca
    # outs: cccb,cccc,hh,hhh,hhhh
    # tags: motifs
    SB_MotifThree_quantile = (
        'SB_MotifThree_quantile',
        SB_MotifThree(trit='quantile'))

    # outs: d,dd,ddd,dddd,dddu
    # outs: ddu,ddud,dduu,du,dud
    # outs: dudd,dudu,duu,duud,duuu
    # outs: h,hh,hhh,hhhh,u
    # outs: ud,udd,uddd,uddu,udu
    # outs: udud,uduu,uu,uud,uudd
    # outs: uudu,uuu,uuud,uuuu
    # tags: motifs
    SB_MotifTwo_mean = (
        'SB_MotifTwo_mean',
        SB_MotifTwo(bint='mean'))

    # outs: d,dd,ddd,dddd,dddu
    # outs: ddu,ddud,dduu,du,dud
    # outs: dudd,dudu,duu,duud,duuu
    # outs: h,hh,hhh,hhhh,u
    # outs: ud,udd,uddd,uddu,udu
    # outs: udud,uduu,uu,uud,uudd
    # outs: uudu,uuu,uuud,uuuu
    # tags: motifs
    SB_MotifTwo_median = (
        'SB_MotifTwo_median',
        SB_MotifTwo(bint='median'))

    # outs: d,dd,ddd,dddd,dddu
    # outs: ddu,ddud,dduu,du,dud
    # outs: dudd,dudu,duu,duud,duuu
    # outs: h,hh,hhh,hhhh,u
    # outs: ud,udd,uddd,uddu,udu
    # outs: udud,uduu,uu,uud,uudd
    # outs: uudu,uuu,uuud,uuuu
    # tags: motifs
    SB_MotifTwo_diff = (
        'SB_MotifTwo_diff',
        SB_MotifTwo(bint='diff'))

    # outs: T1,T2,T3,T4,maxeig
    # outs: maxeigcov,meaneig,meaneigcov,mineig,mineigcov
    # outs: ondiag,stddiag,stdeig,stdeigcov,sumdiagcov
    # outs: symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_21 = (
        'SB_TransitionMatrix_21',
        SB_TransitionMatrix(howtocg='quantile', numGroups=2, tau=1))

    # outs: T1,T2,T3,T4,T5
    # outs: T6,T7,T8,T9,maxeig
    # outs: maxeigcov,maximeig,meaneig,meaneigcov,mineig
    # outs: mineigcov,ondiag,stddiag,stdeig,stdeigcov
    # outs: sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_31 = (
        'SB_TransitionMatrix_31',
        SB_TransitionMatrix(howtocg='quantile', numGroups=3, tau=1))

    # outs: TD1,TD2,TD3,TD4,maxeig
    # outs: maxeigcov,maximeig,meaneig,meaneigcov,mineig
    # outs: mineigcov,ondiag,stddiag,stdeig,stdeigcov
    # outs: sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_4ac = (
        'SB_TransitionMatrix_4ac',
        SB_TransitionMatrix(howtocg='quantile', numGroups=4, tau='ac'))

    # outs: TD1,TD2,TD3,TD4,TD5
    # outs: maxeig,maxeigcov,maximeig,meaneig,meaneigcov
    # outs: mineig,mineigcov,ondiag,stddiag,stdeig
    # outs: stdeigcov,sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_51 = (
        'SB_TransitionMatrix_51',
        SB_TransitionMatrix(howtocg='quantile', numGroups=5, tau=1))

    # outs: TD1,TD2,TD3,TD4,maxeig
    # outs: maxeigcov,maximeig,meaneig,meaneigcov,mineig
    # outs: mineigcov,ondiag,stddiag,stdeig,stdeigcov
    # outs: sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_41 = (
        'SB_TransitionMatrix_41',
        SB_TransitionMatrix(howtocg='quantile', numGroups=4, tau=1))

    # outs: T1,T2,T3,T4,maxeig
    # outs: maxeigcov,meaneig,meaneigcov,mineig,mineigcov
    # outs: ondiag,stddiag,stdeig,stdeigcov,sumdiagcov
    # outs: symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_2ac = (
        'SB_TransitionMatrix_2ac',
        SB_TransitionMatrix(howtocg='quantile', numGroups=2, tau='ac'))

    # outs: T1,T2,T3,T4,T5
    # outs: T6,T7,T8,T9,maxeig
    # outs: maxeigcov,maximeig,meaneig,meaneigcov,mineig
    # outs: mineigcov,ondiag,stddiag,stdeig,stdeigcov
    # outs: sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_3ac = (
        'SB_TransitionMatrix_3ac',
        SB_TransitionMatrix(howtocg='quantile', numGroups=3, tau='ac'))

    # outs: TD1,TD2,TD3,TD4,TD5
    # outs: maxeig,maxeigcov,maximeig,meaneig,meaneigcov
    # outs: mineig,mineigcov,ondiag,stddiag,stdeig
    # outs: stdeigcov,sumdiagcov,symdiff,symsumdiff
    # tags: transitionmat
    SB_TransitionMatrix_5ac = (
        'SB_TransitionMatrix_5ac',
        SB_TransitionMatrix(howtocg='quantile', numGroups=5, tau='ac'))

    # outs: maxdiagfexp_a,maxdiagfexp_adjr2,maxdiagfexp_b,maxdiagfexp_r2,maxdiagfexp_rmse
    # outs: maxeig_fexpa,maxeig_fexpadjr2,maxeig_fexpb,maxeig_fexpr2,maxeig_fexprmse
    # outs: meandiagfexp_a,meandiagfexp_adjr2,meandiagfexp_b,meandiagfexp_r2,meandiagfexp_rmse
    # outs: meaneigfexp_a,meaneigfexp_adjr2,meaneigfexp_b,meaneigfexp_r2,meaneigfexp_rmse
    # outs: mineigfexp_a,mineigfexp_adjr2,mineigfexp_b,mineigfexp_r2,mineigfexp_rmse
    # outs: stdeigfexp_a,stdeigfexp_adjr2,stdeigfexp_b,stdeigfexp_r2,stdeigfexp_rmse
    # outs: symd_a,symd_risept,trcov_jump,trcovfexp_a,trcovfexp_adjr2
    # outs: trcovfexp_b,trcovfexp_r2,trcovfexp_rmse,trfexp_a,trfexp_adjr2
    # outs: trfexp_b,trfexp_r2,trfexp_rmse,trflin10adjr2,trflin5_adjr2
    # tags: transitionmat
    SB_TransitionpAlphabet_40_1 = (
        'SB_TransitionpAlphabet_40_1',
        SB_TransitionpAlphabet(ng=MatlabSequence('2:40'), tau=1))

    # outs: maxdiagfexp_a,maxdiagfexp_adjr2,maxdiagfexp_b,maxdiagfexp_r2,maxdiagfexp_rmse
    # outs: maxeig_fexpa,maxeig_fexpadjr2,maxeig_fexpb,maxeig_fexpr2,maxeig_fexprmse
    # outs: meandiagfexp_a,meandiagfexp_adjr2,meandiagfexp_b,meandiagfexp_r2,meandiagfexp_rmse
    # outs: meaneigfexp_a,meaneigfexp_adjr2,meaneigfexp_b,meaneigfexp_r2,meaneigfexp_rmse
    # outs: mineigfexp_a,mineigfexp_adjr2,mineigfexp_b,mineigfexp_r2,mineigfexp_rmse
    # outs: stdeigfexp_a,stdeigfexp_adjr2,stdeigfexp_b,stdeigfexp_r2,stdeigfexp_rmse
    # outs: symd_a,symd_risept,trcov_jump,trcovfexp_a,trcovfexp_adjr2
    # outs: trcovfexp_b,trcovfexp_r2,trcovfexp_rmse,trfexp_a,trfexp_adjr2
    # outs: trfexp_b,trfexp_r2,trfexp_rmse,trflin10adjr2,trflin5_adjr2
    # tags: transitionmat
    SB_TransitionpAlphabet_20_ac = (
        'SB_TransitionpAlphabet_20_ac',
        SB_TransitionpAlphabet(ng=MatlabSequence('2:20'), tau='ac'))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_sign_2_dfa_2_2 = (
        'SC_FluctAnal_sign_2_dfa_2_2',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=2, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,scaling
    SC_FluctAnal_2_nothing_25_logi = (
        'SC_FluctAnal_2_nothing_25_logi',
        SC_FluctAnal(q=2, wtf='nothing', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_2_logi = (
        'SC_FluctAnal_2_dfa_25_2_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=2, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_1_2_logi = (
        'SC_FluctAnal_2_dfa_25_1_2_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=1, lag=2, loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_1_2 = (
        'SC_FluctAnal_2_dfa_2_1_2',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=1, lag=2, loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_1_3 = (
        'SC_FluctAnal_2_dfa_2_1_3',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=1, lag=3, loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,scaling
    SC_FluctAnal_2_range_25_logi = (
        'SC_FluctAnal_2_range_25_logi',
        SC_FluctAnal(q=2, wtf='range', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: lengthdep,lini,rsrange,scaling
    SC_FluctAnal_2_rsrange_1 = (
        'SC_FluctAnal_2_rsrange_1',
        SC_FluctAnal(q=2, wtf='rsrange', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,scaling
    SC_FluctAnal_2_endptdiff_25_logi = (
        'SC_FluctAnal_2_endptdiff_25_logi',
        SC_FluctAnal(q=2, wtf='endptdiff', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,scaling
    SC_FluctAnal_2_iqr_25_logi = (
        'SC_FluctAnal_2_iqr_25_logi',
        SC_FluctAnal(q=2, wtf='iqr', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,lini,scaling
    SC_FluctAnal_2_std_1 = (
        'SC_FluctAnal_2_std_1',
        SC_FluctAnal(q=2, wtf='std', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: lengthdep,lini,rsrange,scaling
    SC_FluctAnal_2_rsrangefit_2_1 = (
        'SC_FluctAnal_2_rsrangefit_2_1',
        SC_FluctAnal(q=2, wtf='rsrangefit', taustep=2, k=1, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_1_logi = (
        'SC_FluctAnal_2_dfa_25_1_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=1, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,lini,scaling
    SC_FluctAnal_2_iqr_1 = (
        'SC_FluctAnal_2_iqr_1',
        SC_FluctAnal(q=2, wtf='iqr', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,lini,scaling
    SC_FluctAnal_2_nothing_1 = (
        'SC_FluctAnal_2_nothing_1',
        SC_FluctAnal(q=2, wtf='nothing', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_3_logi = (
        'SC_FluctAnal_2_dfa_25_3_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=3, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: lengthdep,rsrange,scaling
    SC_FluctAnal_2_rsrangefit_25_1_logi = (
        'SC_FluctAnal_2_rsrangefit_25_1_logi',
        SC_FluctAnal(q=2, wtf='rsrangefit', taustep=25, k=1, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_0_logi = (
        'SC_FluctAnal_2_dfa_25_0_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=0, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_0 = (
        'SC_FluctAnal_2_dfa_2_0',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=0, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_2 = (
        'SC_FluctAnal_2_dfa_2_2',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=2, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_1 = (
        'SC_FluctAnal_2_dfa_2_1',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=1, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_mag_2_dfa_2_2 = (
        'SC_FluctAnal_mag_2_dfa_2_2',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=2, lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_2_dfa_25_1_3_logi = (
        'SC_FluctAnal_2_dfa_25_1_3_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=1, lag=3, loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: lengthdep,rsrange,scaling
    SC_FluctAnal_2_rsrange_25_logi = (
        'SC_FluctAnal_2_rsrange_25_logi',
        SC_FluctAnal(q=2, wtf='rsrange', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,lini,scaling
    SC_FluctAnal_2_endptdiff_1 = (
        'SC_FluctAnal_2_endptdiff_1',
        SC_FluctAnal(q=2, wtf='endptdiff', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_mag_2_dfa_25_2_logi = (
        'SC_FluctAnal_mag_2_dfa_25_2_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=2, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,scaling
    SC_FluctAnal_sign_2_dfa_25_2_logi = (
        'SC_FluctAnal_sign_2_dfa_25_2_logi',
        SC_FluctAnal(q=2, wtf='dfa', taustep=25, k=2, lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,scaling
    SC_FluctAnal_2_std_25_logi = (
        'SC_FluctAnal_2_std_25_logi',
        SC_FluctAnal(q=2, wtf='std', taustep=25, k=(), lag=(), loginc=1))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: fa,lengthdep,lini,scaling
    SC_FluctAnal_2_range_1 = (
        'SC_FluctAnal_2_range_1',
        SC_FluctAnal(q=2, wtf='range', taustep=1, k=(), lag=(), loginc=0))

    # outs: alpha,alpharat,linfitint,logtausplit,r1_alpha
    # outs: r1_linfitint,r1_resac1,r1_se1,r1_se2,r1_ssr
    # outs: r1_stats_coeffcorr,r2_alpha,r2_linfitint,r2_resac1,r2_se1
    # outs: r2_se2,r2_ssr,r2_stats_coeffcorr,ratsplitminerr,resac1
    # outs: se1,se2,ssr,stats_coeffcorr
    # tags: dfa,lengthdep,lini,scaling
    SC_FluctAnal_2_dfa_2_3 = (
        'SC_FluctAnal_2_dfa_2_3',
        SC_FluctAnal(q=2, wtf='dfa', taustep=2, k=3, lag=(), loginc=0))

    # outs: None
    # tags: dfa,mex,scaling
    SC_fastdfa = (
        'SC_fastdfa',
        SC_fastdfa())

    # outs: ami_f,ami_mediqr,ami_p,ami_prank,ami_zscore
    # outs: fmmi_f,fmmi_mediqr,fmmi_p,fmmi_prank,fmmi_zscore
    # outs: o3_f,o3_mediqr,o3_p,o3_prank,o3_zscore
    # outs: tc3_f,tc3_mediqr,tc3_p,tc3_prank,tc3_zscore
    # tags: nonlinearity,stochastic,surrogatedata
    SD_SurrogateTest_RP_99 = (
        'SD_SurrogateTest_RP_99',
        SD_SurrogateTest(surrmeth='RP', nsurrs=99, extrap=(), teststat=('ami1', 'fmmi', 'o3', 'tc3')))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_mi_100_1 = (
        'TSTL_tc3_mi_100_1',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=1, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_mi_100_3 = (
        'TSTL_tc3_mi_100_3',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=3, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_mi_100_2 = (
        'TSTL_tc3_mi_100_2',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=2, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_1_100_3 = (
        'TSTL_trev_1_100_3',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=3, surrfn='trev'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_1_100_1 = (
        'TSTL_tc3_1_100_1',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=1, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_mi_100_1 = (
        'TSTL_trev_mi_100_1',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=1, surrfn='trev'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_mi_100_2 = (
        'TSTL_trev_mi_100_2',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=2, surrfn='trev'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_1_100_3 = (
        'TSTL_tc3_1_100_3',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=3, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_tc3_1_100_2 = (
        'TSTL_tc3_1_100_2',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=2, surrfn='tc3'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_mi_100_3 = (
        'TSTL_trev_mi_100_3',
        SD_TSTL_surrogates(tau='mi', nsurr=100, surrmethod=3, surrfn='trev'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_1_100_1 = (
        'TSTL_trev_1_100_1',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=1, surrfn='trev'))

    # outs: iqrsfrommedian,ksiqrsfrommode,ksphereonmax,kspminfromext,meansurr
    # outs: normpatponmax,stdfrommean,stdsurr,ztestp
    # tags: correlation,nonlinear,stochastic,surrogate,tstool
    TSTL_trev_1_100_2 = (
        'TSTL_trev_1_100_2',
        SD_TSTL_surrogates(tau=1, nsurr=100, surrmethod=2, surrfn='trev'))

    # outs: ac1,ac2,ac3,ac4,area_2_1
    # outs: area_2_2,area_3_1,area_3_2,area_3_3,area_4_1
    # outs: area_4_2,area_4_3,area_4_4,area_5_1,area_5_2
    # outs: area_5_3,area_5_4,area_5_5,areatopeak,centroid
    # outs: fpoly2_adjr2,fpoly2_r2,fpoly2_rmse,fpoly2_sse,fpoly2csS_p1
    # outs: fpoly2csS_p2,fpoly2csS_p3,fpolysat_a,fpolysat_adjr2,fpolysat_b
    # outs: fpolysat_r2,fpolysat_rmse,iqr,linfitloglog_all_a1,linfitloglog_all_a2
    # outs: linfitloglog_all_s,linfitloglog_all_sea1,linfitloglog_all_sea2,linfitloglog_all_sigrat,linfitloglog_hf_a1
    # outs: linfitloglog_hf_a2,linfitloglog_hf_s,linfitloglog_hf_sea1,linfitloglog_hf_sea2,linfitloglog_hf_sigrat
    # outs: linfitloglog_lf_a1,linfitloglog_lf_a2,linfitloglog_lf_s,linfitloglog_lf_sea1,linfitloglog_lf_sea2
    # outs: linfitloglog_lf_sigrat,linfitloglog_mf_a1,linfitloglog_mf_a2,linfitloglog_mf_s,linfitloglog_mf_sea1
    # outs: linfitloglog_mf_sea2,linfitloglog_mf_sigrat,logac1,logac2,logac3
    # outs: logac4,logarea_2_1,logarea_2_2,logarea_3_1,logarea_3_2
    # outs: logarea_3_3,logarea_4_1,logarea_4_2,logarea_4_3,logarea_4_4
    # outs: logarea_5_1,logarea_5_2,logarea_5_3,logarea_5_4,logarea_5_5
    # outs: logiqr,logmaxonlogmean1e,logmean,logstd,logtau
    # outs: maxS,maxSlog,maxw,maxwidth,mean
    # outs: meanlog,median,medianlog,melmax,mom3
    # outs: mom4,mom5,mom6,mom7,mom8
    # outs: mom9,ncross01,ncross02,ncross05,ncross1
    # outs: ncross10,ncross2,ncross20,ncross5,q1
    # outs: q10,q10mel,q1mel,q25,q25log
    # outs: q25mel,q5,q50,q50mel,q5mel
    # outs: q75,q75log,q75mel,q90,q90mel
    # outs: q95,q95mel,q99,q99mel,rawstatav2_m
    # outs: rawstatav3_m,rawstatav4_m,rawstatav5_m,sfm,spect_shann_ent
    # outs: spect_shann_ent_norm,statav2_m,statav2_s,statav3_m,statav3_s
    # outs: statav4_m,statav4_s,statav5_m,statav5_s,std
    # outs: stdlog,tau,w10_90,w10_90mel,w1_99
    # outs: w1_99mel,w25_75,w25_75mel,w5_95,w5_95mel
    # outs: ylogareatopeak
    # tags: powerspectrum
    SP_basic_fft_logdev_power = (
        'SP_basic_fft_logdev_power',
        SP_Summaries(psdmeth='fft', wmeth=(), nf=(), dologabs=1, doPower=1))

    # outs: ac1,ac2,ac3,ac4,area_2_1
    # outs: area_2_2,area_3_1,area_3_2,area_3_3,area_4_1
    # outs: area_4_2,area_4_3,area_4_4,area_5_1,area_5_2
    # outs: area_5_3,area_5_4,area_5_5,areatopeak,centroid
    # outs: fpoly2_adjr2,fpoly2_r2,fpoly2_rmse,fpoly2_sse,fpoly2csS_p1
    # outs: fpoly2csS_p2,fpoly2csS_p3,fpolysat_a,fpolysat_adjr2,fpolysat_b
    # outs: fpolysat_r2,fpolysat_rmse,iqr,linfitloglog_all_a1,linfitloglog_all_a2
    # outs: linfitloglog_all_s,linfitloglog_all_sea1,linfitloglog_all_sea2,linfitloglog_all_sigrat,linfitloglog_hf_a1
    # outs: linfitloglog_hf_a2,linfitloglog_hf_s,linfitloglog_hf_sea1,linfitloglog_hf_sea2,linfitloglog_hf_sigrat
    # outs: linfitloglog_lf_a1,linfitloglog_lf_a2,linfitloglog_lf_s,linfitloglog_lf_sea1,linfitloglog_lf_sea2
    # outs: linfitloglog_lf_sigrat,linfitloglog_mf_a1,linfitloglog_mf_a2,linfitloglog_mf_s,linfitloglog_mf_sea1
    # outs: linfitloglog_mf_sea2,linfitloglog_mf_sigrat,logac1,logac2,logac3
    # outs: logac4,logarea_2_1,logarea_2_2,logarea_3_1,logarea_3_2
    # outs: logarea_3_3,logarea_4_1,logarea_4_2,logarea_4_3,logarea_4_4
    # outs: logarea_5_1,logarea_5_2,logarea_5_3,logarea_5_4,logarea_5_5
    # outs: logiqr,logmaxonlogmean1e,logmean,logstd,logtau
    # outs: maxS,maxSlog,maxw,maxwidth,mean
    # outs: meanlog,median,medianlog,melmax,mom3
    # outs: mom4,mom5,mom6,mom7,mom8
    # outs: mom9,ncross01,ncross02,ncross05,ncross1
    # outs: ncross10,ncross2,ncross20,ncross5,q1
    # outs: q10,q10mel,q1mel,q25,q25log
    # outs: q25mel,q5,q50,q50mel,q5mel
    # outs: q75,q75log,q75mel,q90,q90mel
    # outs: q95,q95mel,q99,q99mel,rawstatav2_m
    # outs: rawstatav3_m,rawstatav4_m,rawstatav5_m,sfm,spect_shann_ent
    # outs: spect_shann_ent_norm,statav2_m,statav2_s,statav3_m,statav3_s
    # outs: statav4_m,statav4_s,statav5_m,statav5_s,std
    # outs: stdlog,tau,w10_90,w10_90mel,w1_99
    # outs: w1_99mel,w25_75,w25_75mel,w5_95,w5_95mel
    # outs: ylogareatopeak
    # tags: powerspectrum
    SP_basic_pgram_hamm_power = (
        'SP_basic_pgram_hamm_power',
        SP_Summaries(psdmeth='periodogram', wmeth='hamming', nf=(), dologabs=0, doPower=1))

    # outs: ac1,ac2,ac3,ac4,area_2_1
    # outs: area_2_2,area_3_1,area_3_2,area_3_3,area_4_1
    # outs: area_4_2,area_4_3,area_4_4,area_5_1,area_5_2
    # outs: area_5_3,area_5_4,area_5_5,areatopeak,centroid
    # outs: fpoly2_adjr2,fpoly2_r2,fpoly2_rmse,fpoly2_sse,fpoly2csS_p1
    # outs: fpoly2csS_p2,fpoly2csS_p3,fpolysat_a,fpolysat_adjr2,fpolysat_b
    # outs: fpolysat_r2,fpolysat_rmse,iqr,linfitloglog_all_a1,linfitloglog_all_a2
    # outs: linfitloglog_all_s,linfitloglog_all_sea1,linfitloglog_all_sea2,linfitloglog_all_sigrat,linfitloglog_hf_a1
    # outs: linfitloglog_hf_a2,linfitloglog_hf_s,linfitloglog_hf_sea1,linfitloglog_hf_sea2,linfitloglog_hf_sigrat
    # outs: linfitloglog_lf_a1,linfitloglog_lf_a2,linfitloglog_lf_s,linfitloglog_lf_sea1,linfitloglog_lf_sea2
    # outs: linfitloglog_lf_sigrat,linfitloglog_mf_a1,linfitloglog_mf_a2,linfitloglog_mf_s,linfitloglog_mf_sea1
    # outs: linfitloglog_mf_sea2,linfitloglog_mf_sigrat,logac1,logac2,logac3
    # outs: logac4,logarea_2_1,logarea_2_2,logarea_3_1,logarea_3_2
    # outs: logarea_3_3,logarea_4_1,logarea_4_2,logarea_4_3,logarea_4_4
    # outs: logarea_5_1,logarea_5_2,logarea_5_3,logarea_5_4,logarea_5_5
    # outs: logiqr,logmaxonlogmean1e,logmean,logstd,logtau
    # outs: maxS,maxSlog,maxw,maxwidth,mean
    # outs: meanlog,median,medianlog,melmax,mom3
    # outs: mom4,mom5,mom6,mom7,mom8
    # outs: mom9,ncross01,ncross02,ncross05,ncross1
    # outs: ncross10,ncross2,ncross20,ncross5,q1
    # outs: q10,q10mel,q1mel,q25,q25log
    # outs: q25mel,q5,q50,q50mel,q5mel
    # outs: q75,q75log,q75mel,q90,q90mel
    # outs: q95,q95mel,q99,q99mel,rawstatav2_m
    # outs: rawstatav3_m,rawstatav4_m,rawstatav5_m,sfm,spect_shann_ent
    # outs: spect_shann_ent_norm,statav2_m,statav2_s,statav3_m,statav3_s
    # outs: statav4_m,statav4_s,statav5_m,statav5_s,std
    # outs: stdlog,tau,w10_90,w10_90mel,w1_99
    # outs: w1_99mel,w25_75,w25_75mel,w5_95,w5_95mel
    # outs: ylogareatopeak
    # tags: powerspectrum
    SP_basic_fft_power = (
        'SP_basic_fft_power',
        SP_Summaries(psdmeth='fft', wmeth=(), nf=(), dologabs=0, doPower=1))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_10 = (
        'ST_FitPolynomial_10',
        ST_FitPolynomial(k=10))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_7 = (
        'ST_FitPolynomial_7',
        ST_FitPolynomial(k=7))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_8 = (
        'ST_FitPolynomial_8',
        ST_FitPolynomial(k=8))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_1 = (
        'ST_FitPolynomial_1',
        ST_FitPolynomial(k=1))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_2 = (
        'ST_FitPolynomial_2',
        ST_FitPolynomial(k=2))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_3 = (
        'ST_FitPolynomial_3',
        ST_FitPolynomial(k=3))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_4 = (
        'ST_FitPolynomial_4',
        ST_FitPolynomial(k=4))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_5 = (
        'ST_FitPolynomial_5',
        ST_FitPolynomial(k=5))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_6 = (
        'ST_FitPolynomial_6',
        ST_FitPolynomial(k=6))

    # outs: None
    # tags: raw,spreaddep,trend
    ST_FitPolynomial_9 = (
        'ST_FitPolynomial_9',
        ST_FitPolynomial(k=9))

    # outs: None
    # tags: lengthdep,misc,raw
    ST_length = (
        'ST_length',
        ST_Length())

    # outs: diffmaxabsmin,maxabsext,maxmaxmed,meanabsext,meanabsmin
    # outs: meanext,meanmax,meanrat,medianabsext,medianabsmin
    # outs: medianext,medianmax,medianrat,minabsmin,minmax
    # outs: minmaxonminabsmin,minminmed,stdext,stdmax,stdmin
    # outs: uord,zcext
    # tags: distribution,stationarity
    ST_LocalExtrema_l50 = (
        'ST_LocalExtrema_l50',
        ST_LocalExtrema(lorf='l', n=50))

    # outs: diffmaxabsmin,maxabsext,maxmaxmed,meanabsext,meanabsmin
    # outs: meanext,meanmax,meanrat,medianabsext,medianabsmin
    # outs: medianext,medianmax,medianrat,minabsmin,minmax
    # outs: minmaxonminabsmin,minminmed,stdext,stdmax,stdmin
    # outs: uord,zcext
    # tags: distribution,stationarity
    ST_LocalExtrema_n100 = (
        'ST_LocalExtrema_n100',
        ST_LocalExtrema(lorf='n', n=100))

    # outs: diffmaxabsmin,maxabsext,maxmaxmed,meanabsext,meanabsmin
    # outs: meanext,meanmax,meanrat,medianabsext,medianabsmin
    # outs: medianext,medianmax,medianrat,minabsmin,minmax
    # outs: minmaxonminabsmin,minminmed,stdext,stdmax,stdmin
    # outs: uord,zcext
    # tags: distribution,stationarity
    ST_LocalExtrema_l100 = (
        'ST_LocalExtrema_l100',
        ST_LocalExtrema(lorf='l', n=100))

    # outs: diffmaxabsmin,maxabsext,maxmaxmed,meanabsext,meanabsmin
    # outs: meanext,meanmax,meanrat,medianabsext,medianabsmin
    # outs: medianext,medianmax,medianrat,minabsmin,minmax
    # outs: minmaxonminabsmin,minminmed,stdext,stdmax,stdmin
    # outs: uord,zcext
    # tags: distribution,stationarity
    ST_LocalExtrema_n50 = (
        'ST_LocalExtrema_n50',
        ST_LocalExtrema(lorf='n', n=50))

    # outs: diffmaxabsmin,maxabsext,maxmaxmed,meanabsext,meanabsmin
    # outs: meanext,meanmax,meanrat,medianabsext,medianabsmin
    # outs: medianext,medianmax,medianrat,minabsmin,minmax
    # outs: minmaxonminabsmin,minminmed,stdext,stdmax,stdmin
    # outs: uord,zcext
    # tags: distribution,stationarity
    ST_LocalExtrema_n25 = (
        'ST_LocalExtrema_n25',
        ST_LocalExtrema(lorf='n', n=25))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_median_iqr_abs = (
        'ST_MomentCorr_002_02_median_iqr_abs',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='median', mom2='iqr', transf='abs'))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_median_iqr_sqrt = (
        'ST_MomentCorr_002_02_median_iqr_sqrt',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='median', mom2='iqr', transf='sqrt'))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_mean_std_none = (
        'ST_MomentCorr_002_02_mean_std_none',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='mean', mom2='std', transf='none'))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_mean_std_abs = (
        'ST_MomentCorr_002_02_mean_std_abs',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='mean', mom2='std', transf='abs'))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_median_iqr_none = (
        'ST_MomentCorr_002_02_median_iqr_none',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='median', mom2='iqr', transf='none'))

    # outs: R,absR,density,mi
    # tags: statistics
    ST_MomentCorr_002_02_mean_std_sqrt = (
        'ST_MomentCorr_002_02_mean_std_sqrt',
        ST_MomentCorr(wl=0.02, olap=0.2, mom1='mean', mom2='std', transf='sqrt'))

    # outs: None
    # tags: distribution
    ST_SimpleStats_pmcross = (
        'ST_SimpleStats_pmcross',
        ST_SimpleStats(whatstat='pmcross'))

    # outs: None
    # tags: noisiness
    ST_SimpleStats_zcross = (
        'ST_SimpleStats_zcross',
        ST_SimpleStats(whatstat='zcross'))

    # outs: None
    # tags: noisiness
    ST_SimpleStats_min = (
        'ST_SimpleStats_min',
        ST_SimpleStats(whatstat='minima'))

    # outs: None
    # tags: noisiness
    ST_SimpleStats_max = (
        'ST_SimpleStats_max',
        ST_SimpleStats(whatstat='maxima'))

    # outs: max,mean,meanabsmaxmin,meanmaxmin,min
    # tags: stationarity
    SY_DriftingMeann10 = (
        'SY_DriftingMeann10',
        SY_DriftingMean(howl='num', l=10))

    # outs: max,mean,meanabsmaxmin,meanmaxmin,min
    # tags: stationarity
    SY_DriftingMeann5 = (
        'SY_DriftingMeann5',
        SY_DriftingMean(howl='num', l=5))

    # outs: max,mean,meanabsmaxmin,meanmaxmin,min
    # tags: stationarity
    SY_DriftingMean100 = (
        'SY_DriftingMean100',
        SY_DriftingMean(howl='fix', l=100))

    # outs: max,mean,meanabsmaxmin,meanmaxmin,min
    # tags: stationarity
    SY_DriftingMean20 = (
        'SY_DriftingMean20',
        SY_DriftingMean(howl='fix', l=20))

    # outs: max,mean,meanabsmaxmin,meanmaxmin,min
    # tags: stationarity
    SY_DriftingMean50 = (
        'SY_DriftingMean50',
        SY_DriftingMean(howl='fix', l=50))

    # outs: stdac1,stdac2,stdactaug,stdactaul,stdapen1_02
    # outs: stdkurt,stdmean,stdsampen1_02,stdskew,stdstd
    # outs: stdtaul
    # tags: stationarity
    SY_DynWin10 = (
        'SY_DynWin10',
        SY_DynWin(maxnseg=10))

    # outs: lagmaxstat,lagminstat,maxpValue,maxstat,minpValue
    # outs: minstat
    # tags: econometricstoolbox,hypothesistest,kpsstest,pvalue,stationarity
    SY_KPSStest_0_10 = (
        'SY_KPSStest_0_10',
        SY_KPSStest(lags=MatlabSequence('0:10')))

    # outs: pValue,stat
    # tags: econometricstoolbox,hypothesistest,kpsstest,pvalue,stationarity
    SY_KPSStest_1 = (
        'SY_KPSStest_1',
        SY_KPSStest(lags=1))

    # outs: pValue,stat
    # tags: econometricstoolbox,hypothesistest,kpsstest,pvalue,stationarity
    SY_KPSStest_0 = (
        'SY_KPSStest_0',
        SY_KPSStest(lags=0))

    # outs: pValue,stat
    # tags: econometricstoolbox,hypothesistest,kpsstest,pvalue,stationarity
    SY_KPSStest_2 = (
        'SY_KPSStest_2',
        SY_KPSStest(lags=2))

    # outs: None
    # tags: raw,stationarity
    SY_LinearTrend = (
        'SY_LinearTrend',
        SY_LinearTrend())

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_4_each = (
        'SY_LocalDistributions_4_each',
        SY_LocalDistributions(nseg=4, eachorpar='each'))

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_5_each = (
        'SY_LocalDistributions_5_each',
        SY_LocalDistributions(nseg=5, eachorpar='each'))

    # outs: meandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_2_par = (
        'SY_LocalDistributions_2_par',
        SY_LocalDistributions(nseg=2, eachorpar='par'))

    # outs: None
    # tags: stationarity
    SY_LocalDistributions_2_each = (
        'SY_LocalDistributions_2_each',
        SY_LocalDistributions(nseg=2, eachorpar='each'))

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_3_each = (
        'SY_LocalDistributions_3_each',
        SY_LocalDistributions(nseg=3, eachorpar='each'))

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_5_par = (
        'SY_LocalDistributions_5_par',
        SY_LocalDistributions(nseg=5, eachorpar='par'))

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_3_par = (
        'SY_LocalDistributions_3_par',
        SY_LocalDistributions(nseg=3, eachorpar='par'))

    # outs: meandiv,mediandiv,mindiv,stddiv
    # tags: stationarity
    SY_LocalDistributions_4_par = (
        'SY_LocalDistributions_4_par',
        SY_LocalDistributions(nseg=4, eachorpar='par'))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_l50 = (
        'SY_LocalGlobal_l50',
        SY_LocalGlobal(lorp='l', n=50))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity,stochastic
    SY_LocalGlobal_randcg10 = (
        'SY_LocalGlobal_randcg10',
        SY_LocalGlobal(lorp='randcg', n=10))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity,stochastic
    SY_LocalGlobal_randcg100 = (
        'SY_LocalGlobal_randcg100',
        SY_LocalGlobal(lorp='randcg', n=100))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity,stochastic
    SY_LocalGlobal_randcg50 = (
        'SY_LocalGlobal_randcg50',
        SY_LocalGlobal(lorp='randcg', n=50))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_l10 = (
        'SY_LocalGlobal_l10',
        SY_LocalGlobal(lorp='l', n=10))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_p05 = (
        'SY_LocalGlobal_p05',
        SY_LocalGlobal(lorp='p', n=0.05))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_p1 = (
        'SY_LocalGlobal_p1',
        SY_LocalGlobal(lorp='p', n=0.1))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_p5 = (
        'SY_LocalGlobal_p5',
        SY_LocalGlobal(lorp='p', n=0.5))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity,stochastic
    SY_LocalGlobal_randcg20 = (
        'SY_LocalGlobal_randcg20',
        SY_LocalGlobal(lorp='randcg', n=20))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_unicg500 = (
        'SY_LocalGlobal_unicg500',
        SY_LocalGlobal(lorp='unicg', n=500))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_unicg20 = (
        'SY_LocalGlobal_unicg20',
        SY_LocalGlobal(lorp='unicg', n=20))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_p01 = (
        'SY_LocalGlobal_p01',
        SY_LocalGlobal(lorp='p', n=0.01))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity,stochastic
    SY_LocalGlobal_randcg500 = (
        'SY_LocalGlobal_randcg500',
        SY_LocalGlobal(lorp='randcg', n=500))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_l500 = (
        'SY_LocalGlobal_l500',
        SY_LocalGlobal(lorp='l', n=500))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_l20 = (
        'SY_LocalGlobal_l20',
        SY_LocalGlobal(lorp='l', n=20))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_unicg10 = (
        'SY_LocalGlobal_unicg10',
        SY_LocalGlobal(lorp='unicg', n=10))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_l100 = (
        'SY_LocalGlobal_l100',
        SY_LocalGlobal(lorp='l', n=100))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_unicg100 = (
        'SY_LocalGlobal_unicg100',
        SY_LocalGlobal(lorp='unicg', n=100))

    # outs: absmean,ac1,iqr,kurtosis,median
    # outs: skewness,std
    # tags: stationarity
    SY_LocalGlobal_unicg50 = (
        'SY_LocalGlobal_unicg50',
        SY_LocalGlobal(lorp='unicg', n=50))

    # outs: lagmaxp,lagminp,maxpValue,maxrmse,maxstat
    # outs: meanloglikelihood,meanpValue,meanstat,minAIC,minBIC
    # outs: minHQC,minpValue,minrmse,minstat,stdpValue
    # tags: aic,bic,econometricstoolbox,hqc,pptest,pvalue,rmse,unitroot
    SY_PPtest_0_5_ts_t1 = (
        'SY_PPtest_0_5_ts_t1',
        SY_PPtest(lags=MatlabSequence('0:5'), model='ts', teststat='t1'))

    # outs: lagmaxp,lagminp,maxpValue,maxrmse,maxstat
    # outs: meanloglikelihood,meanpValue,meanstat,minAIC,minBIC
    # outs: minHQC,minpValue,minrmse,minstat,stdpValue
    # tags: aic,bic,econometricstoolbox,hqc,pptest,pvalue,rmse,unitroot
    SY_PPtest_0_5_ard_t1 = (
        'SY_PPtest_0_5_ard_t1',
        SY_PPtest(lags=MatlabSequence('0:5'), model='ard', teststat='t1'))

    # outs: lagmaxp,lagminp,maxpValue,maxrmse,maxstat
    # outs: meanloglikelihood,meanpValue,meanstat,minAIC,minBIC
    # outs: minHQC,minpValue,minrmse,minstat,stdpValue
    # tags: aic,bic,econometricstoolbox,hqc,pptest,pvalue,rmse,unitroot
    SY_PPtest_0_5_ar_t1 = (
        'SY_PPtest_0_5_ar_t1',
        SY_PPtest(lags=MatlabSequence('0:5'), model='ar', teststat='t1'))

    # outs: l10,l100,l1000,l50,nuql10
    # outs: nuql100,nuql1000,nuql50,nuqp1,nuqp10
    # outs: nuqp20,nuqp50,p1,p10,p20
    # outs: p50,totnuq
    # tags: stationarity
    SY_RangeEvolve = (
        'SY_RangeEvolve',
        SY_RangeEvolve())

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent5_2 = (
        'SY_SlidingWindow_ent_ent5_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent5_1 = (
        'SY_SlidingWindow_ent_ent5_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent10_2 = (
        'SY_SlidingWindow_m_ent10_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent5_10 = (
        'SY_SlidingWindow_s_ent5_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s10_1 = (
        'SY_SlidingWindow_s_s10_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen2_10 = (
        'SY_SlidingWindow_ac1_apen2_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent10_2 = (
        'SY_SlidingWindow_lil_ent10_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen10_2 = (
        'SY_SlidingWindow_apen_apen10_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s10_1 = (
        'SY_SlidingWindow_lil_s10_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent10_10 = (
        'SY_SlidingWindow_ac1_ent10_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s10_10 = (
        'SY_SlidingWindow_s_s10_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen2_10 = (
        'SY_SlidingWindow_s_apen2_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen10_2 = (
        'SY_SlidingWindow_m_apen10_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s5_1 = (
        'SY_SlidingWindow_m_s5_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s5_2 = (
        'SY_SlidingWindow_m_s5_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s5_10 = (
        'SY_SlidingWindow_ent_s5_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent5_10 = (
        'SY_SlidingWindow_apen_ent5_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen2_1 = (
        'SY_SlidingWindow_apen_apen2_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen5_2 = (
        'SY_SlidingWindow_ac1_apen5_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen5_2 = (
        'SY_SlidingWindow_m_apen5_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen5_1 = (
        'SY_SlidingWindow_m_apen5_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen2_10 = (
        'SY_SlidingWindow_lil_apen2_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen10_1 = (
        'SY_SlidingWindow_mom3_apen10_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s10_10 = (
        'SY_SlidingWindow_mom4_s10_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen5_10 = (
        'SY_SlidingWindow_s_apen5_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen2_10 = (
        'SY_SlidingWindow_m_apen2_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen2_1 = (
        'SY_SlidingWindow_mom4_apen2_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen2_2 = (
        'SY_SlidingWindow_mom4_apen2_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent2_10 = (
        'SY_SlidingWindow_m_ent2_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen10_2 = (
        'SY_SlidingWindow_mom3_apen10_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen5_10 = (
        'SY_SlidingWindow_apen_apen5_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent2_1 = (
        'SY_SlidingWindow_mom3_ent2_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s10_2 = (
        'SY_SlidingWindow_mom4_s10_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s2_2 = (
        'SY_SlidingWindow_lil_s2_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent5_10 = (
        'SY_SlidingWindow_mom3_ent5_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s5_10 = (
        'SY_SlidingWindow_mom3_s5_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s2_10 = (
        'SY_SlidingWindow_mom4_s2_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent2_1 = (
        'SY_SlidingWindow_apen_ent2_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent2_2 = (
        'SY_SlidingWindow_apen_ent2_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent10_10 = (
        'SY_SlidingWindow_m_ent10_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent2_10 = (
        'SY_SlidingWindow_s_ent2_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen2_2 = (
        'SY_SlidingWindow_ac1_apen2_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen2_1 = (
        'SY_SlidingWindow_ac1_apen2_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s10_10 = (
        'SY_SlidingWindow_lil_s10_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent5_10 = (
        'SY_SlidingWindow_mom4_ent5_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen2_1 = (
        'SY_SlidingWindow_ent_apen2_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen2_2 = (
        'SY_SlidingWindow_ent_apen2_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent10_1 = (
        'SY_SlidingWindow_ent_ent10_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen2_10 = (
        'SY_SlidingWindow_ent_apen2_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent10_2 = (
        'SY_SlidingWindow_ent_ent10_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen2_1 = (
        'SY_SlidingWindow_m_apen2_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen2_2 = (
        'SY_SlidingWindow_m_apen2_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s10_2 = (
        'SY_SlidingWindow_lil_s10_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s10_1 = (
        'SY_SlidingWindow_mom3_s10_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s10_2 = (
        'SY_SlidingWindow_mom3_s10_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent5_1 = (
        'SY_SlidingWindow_m_ent5_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen5_10 = (
        'SY_SlidingWindow_ac1_apen5_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s10_10 = (
        'SY_SlidingWindow_m_s10_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s5_1 = (
        'SY_SlidingWindow_apen_s5_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s5_2 = (
        'SY_SlidingWindow_apen_s5_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen2_10 = (
        'SY_SlidingWindow_mom4_apen2_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen5_1 = (
        'SY_SlidingWindow_apen_apen5_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen10_1 = (
        'SY_SlidingWindow_lil_apen10_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen5_2 = (
        'SY_SlidingWindow_lil_apen5_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen10_10 = (
        'SY_SlidingWindow_ent_apen10_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent10_1 = (
        'SY_SlidingWindow_mom3_ent10_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen5_1 = (
        'SY_SlidingWindow_lil_apen5_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen10_2 = (
        'SY_SlidingWindow_lil_apen10_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent10_1 = (
        'SY_SlidingWindow_m_ent10_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s5_10 = (
        'SY_SlidingWindow_m_s5_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent5_10 = (
        'SY_SlidingWindow_m_ent5_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent10_10 = (
        'SY_SlidingWindow_s_ent10_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent2_2 = (
        'SY_SlidingWindow_mom3_ent2_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen10_10 = (
        'SY_SlidingWindow_m_apen10_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent10_10 = (
        'SY_SlidingWindow_apen_ent10_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent5_1 = (
        'SY_SlidingWindow_mom4_ent5_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s5_10 = (
        'SY_SlidingWindow_ac1_s5_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen2_2 = (
        'SY_SlidingWindow_s_apen2_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent2_2 = (
        'SY_SlidingWindow_mom4_ent2_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent2_10 = (
        'SY_SlidingWindow_ent_ent2_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent2_1 = (
        'SY_SlidingWindow_mom4_ent2_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent2_1 = (
        'SY_SlidingWindow_m_ent2_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent2_2 = (
        'SY_SlidingWindow_m_ent2_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen5_2 = (
        'SY_SlidingWindow_ent_apen5_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen10_2 = (
        'SY_SlidingWindow_s_apen10_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen10_1 = (
        'SY_SlidingWindow_s_apen10_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s5_2 = (
        'SY_SlidingWindow_ac1_s5_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s5_1 = (
        'SY_SlidingWindow_ac1_s5_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent2_1 = (
        'SY_SlidingWindow_s_ent2_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s10_1 = (
        'SY_SlidingWindow_ent_s10_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen5_1 = (
        'SY_SlidingWindow_s_apen5_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen5_2 = (
        'SY_SlidingWindow_s_apen5_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s10_10 = (
        'SY_SlidingWindow_ent_s10_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent2_2 = (
        'SY_SlidingWindow_lil_ent2_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent10_1 = (
        'SY_SlidingWindow_mom4_ent10_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent10_2 = (
        'SY_SlidingWindow_mom4_ent10_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s5_2 = (
        'SY_SlidingWindow_mom4_s5_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s5_1 = (
        'SY_SlidingWindow_mom4_s5_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s2_1 = (
        'SY_SlidingWindow_s_s2_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s2_10 = (
        'SY_SlidingWindow_s_s2_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent2_10 = (
        'SY_SlidingWindow_lil_ent2_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent2_1 = (
        'SY_SlidingWindow_lil_ent2_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s10_10 = (
        'SY_SlidingWindow_mom3_s10_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen5_10 = (
        'SY_SlidingWindow_m_apen5_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s2_2 = (
        'SY_SlidingWindow_apen_s2_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s2_1 = (
        'SY_SlidingWindow_apen_s2_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s10_2 = (
        'SY_SlidingWindow_s_s10_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent2_10 = (
        'SY_SlidingWindow_apen_ent2_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s2_2 = (
        'SY_SlidingWindow_ent_s2_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s2_1 = (
        'SY_SlidingWindow_ent_s2_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_apen10_1 = (
        'SY_SlidingWindow_m_apen10_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen2_1 = (
        'SY_SlidingWindow_lil_apen2_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen2_2 = (
        'SY_SlidingWindow_lil_apen2_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s2_2 = (
        'SY_SlidingWindow_s_s2_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen2_2 = (
        'SY_SlidingWindow_apen_apen2_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent2_10 = (
        'SY_SlidingWindow_mom4_ent2_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s2_10 = (
        'SY_SlidingWindow_mom3_s2_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent5_10 = (
        'SY_SlidingWindow_ac1_ent5_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s2_1 = (
        'SY_SlidingWindow_ac1_s2_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s2_2 = (
        'SY_SlidingWindow_ac1_s2_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen5_1 = (
        'SY_SlidingWindow_ent_apen5_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent5_1 = (
        'SY_SlidingWindow_mom3_ent5_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent5_2 = (
        'SY_SlidingWindow_mom3_ent5_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen2_10 = (
        'SY_SlidingWindow_mom3_apen2_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s2_10 = (
        'SY_SlidingWindow_lil_s2_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen5_2 = (
        'SY_SlidingWindow_apen_apen5_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s10_2 = (
        'SY_SlidingWindow_apen_s10_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s10_1 = (
        'SY_SlidingWindow_apen_s10_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s5_10 = (
        'SY_SlidingWindow_apen_s5_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent10_1 = (
        'SY_SlidingWindow_lil_ent10_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen5_2 = (
        'SY_SlidingWindow_mom4_apen5_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s2_10 = (
        'SY_SlidingWindow_ent_s2_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen5_10 = (
        'SY_SlidingWindow_lil_apen5_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent5_2 = (
        'SY_SlidingWindow_mom4_ent5_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent10_10 = (
        'SY_SlidingWindow_mom3_ent10_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s2_1 = (
        'SY_SlidingWindow_mom4_s2_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s2_2 = (
        'SY_SlidingWindow_mom4_s2_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent5_2 = (
        'SY_SlidingWindow_lil_ent5_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s2_2 = (
        'SY_SlidingWindow_m_s2_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen2_1 = (
        'SY_SlidingWindow_s_apen2_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen10_1 = (
        'SY_SlidingWindow_apen_apen10_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen10_2 = (
        'SY_SlidingWindow_ac1_apen10_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen10_1 = (
        'SY_SlidingWindow_ac1_apen10_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s2_10 = (
        'SY_SlidingWindow_ac1_s2_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent2_10 = (
        'SY_SlidingWindow_mom3_ent2_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent10_10 = (
        'SY_SlidingWindow_ent_ent10_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s5_1 = (
        'SY_SlidingWindow_ent_s5_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s5_2 = (
        'SY_SlidingWindow_ent_s5_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_ent5_2 = (
        'SY_SlidingWindow_m_ent5_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_apen10_10 = (
        'SY_SlidingWindow_s_apen10_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_s10_2 = (
        'SY_SlidingWindow_ent_s10_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent2_10 = (
        'SY_SlidingWindow_ac1_ent2_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen5_10 = (
        'SY_SlidingWindow_ent_apen5_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent5_1 = (
        'SY_SlidingWindow_s_ent5_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent5_2 = (
        'SY_SlidingWindow_s_ent5_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent10_10 = (
        'SY_SlidingWindow_lil_ent10_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen5_1 = (
        'SY_SlidingWindow_mom3_apen5_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_apen10_10 = (
        'SY_SlidingWindow_lil_apen10_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s2_1 = (
        'SY_SlidingWindow_mom3_s2_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s2_2 = (
        'SY_SlidingWindow_mom3_s2_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen10_1 = (
        'SY_SlidingWindow_ent_apen10_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_apen10_2 = (
        'SY_SlidingWindow_ent_apen10_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen10_2 = (
        'SY_SlidingWindow_mom4_apen10_2',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen10_1 = (
        'SY_SlidingWindow_mom4_apen10_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s10_10 = (
        'SY_SlidingWindow_apen_s10_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen5_2 = (
        'SY_SlidingWindow_mom3_apen5_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen10_10 = (
        'SY_SlidingWindow_mom4_apen10_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen10_10 = (
        'SY_SlidingWindow_ac1_apen10_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s5_2 = (
        'SY_SlidingWindow_s_s5_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s5_1 = (
        'SY_SlidingWindow_s_s5_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen5_10 = (
        'SY_SlidingWindow_mom3_apen5_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen10_10 = (
        'SY_SlidingWindow_apen_apen10_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent2_1 = (
        'SY_SlidingWindow_ent_ent2_1',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent2_2 = (
        'SY_SlidingWindow_ent_ent2_2',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s5_2 = (
        'SY_SlidingWindow_mom3_s5_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_s5_1 = (
        'SY_SlidingWindow_mom3_s5_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s2_10 = (
        'SY_SlidingWindow_m_s2_10',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent2_2 = (
        'SY_SlidingWindow_ac1_ent2_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent2_1 = (
        'SY_SlidingWindow_ac1_ent2_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen5_10 = (
        'SY_SlidingWindow_mom4_apen5_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent5_10 = (
        'SY_SlidingWindow_lil_ent5_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_ent10_10 = (
        'SY_SlidingWindow_mom4_ent10_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='ent', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent2_2 = (
        'SY_SlidingWindow_s_ent2_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_s5_10 = (
        'SY_SlidingWindow_s_s5_10',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent10_2 = (
        'SY_SlidingWindow_s_ent10_2',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_s_ent10_1 = (
        'SY_SlidingWindow_s_ent10_1',
        SY_SlidingWindow(windowstat='std', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s10_1 = (
        'SY_SlidingWindow_ac1_s10_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen10_10 = (
        'SY_SlidingWindow_mom3_apen10_10',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s10_2 = (
        'SY_SlidingWindow_m_s10_2',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s10_1 = (
        'SY_SlidingWindow_m_s10_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s5_10 = (
        'SY_SlidingWindow_mom4_s5_10',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s10_2 = (
        'SY_SlidingWindow_ac1_s10_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_apen2_10 = (
        'SY_SlidingWindow_apen_apen2_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='apen', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s5_10 = (
        'SY_SlidingWindow_lil_s5_10',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_apen5_1 = (
        'SY_SlidingWindow_mom4_apen5_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ent_ent5_10 = (
        'SY_SlidingWindow_ent_ent5_10',
        SY_SlidingWindow(windowstat='ent', acrosswindowstat='ent', nseg=5, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent10_2 = (
        'SY_SlidingWindow_ac1_ent10_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent10_1 = (
        'SY_SlidingWindow_ac1_ent10_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_m_s2_1 = (
        'SY_SlidingWindow_m_s2_1',
        SY_SlidingWindow(windowstat='mean', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent10_1 = (
        'SY_SlidingWindow_apen_ent10_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent10_2 = (
        'SY_SlidingWindow_apen_ent10_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_ent5_1 = (
        'SY_SlidingWindow_lil_ent5_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_apen5_1 = (
        'SY_SlidingWindow_ac1_apen5_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='apen', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent5_1 = (
        'SY_SlidingWindow_ac1_ent5_1',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_ent5_2 = (
        'SY_SlidingWindow_ac1_ent5_2',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen2_2 = (
        'SY_SlidingWindow_mom3_apen2_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=2, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_apen2_1 = (
        'SY_SlidingWindow_mom3_apen2_1',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='apen', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_ac1_s10_10 = (
        'SY_SlidingWindow_ac1_s10_10',
        SY_SlidingWindow(windowstat='AC1', acrosswindowstat='std', nseg=10, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s5_1 = (
        'SY_SlidingWindow_lil_s5_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=5, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s5_2 = (
        'SY_SlidingWindow_lil_s5_2',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom4_s10_1 = (
        'SY_SlidingWindow_mom4_s10_1',
        SY_SlidingWindow(windowstat='mom4', acrosswindowstat='std', nseg=10, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_mom3_ent10_2 = (
        'SY_SlidingWindow_mom3_ent10_2',
        SY_SlidingWindow(windowstat='mom3', acrosswindowstat='ent', nseg=10, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_lil_s2_1 = (
        'SY_SlidingWindow_lil_s2_1',
        SY_SlidingWindow(windowstat='lillie', acrosswindowstat='std', nseg=2, nmov=1))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_s2_10 = (
        'SY_SlidingWindow_apen_s2_10',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='std', nseg=2, nmov=10))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent5_2 = (
        'SY_SlidingWindow_apen_ent5_2',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=5, nmov=2))

    # outs: None
    # tags: slidingwin,stationarity
    SY_SlidingWindow_apen_ent5_1 = (
        'SY_SlidingWindow_apen_ent5_1',
        SY_SlidingWindow(windowstat='apen', acrosswindowstat='ent', nseg=5, nmov=1))

    # outs: meanac1,meanac2,meanapen1_02,meankurt,meanmean
    # outs: meansampen1_02,meanskew,meanstd,meantaul,stdac1
    # outs: stdac2,stdapen1_02,stdkurt,stdmean,stdsampen1_02
    # outs: stdskew,stdstd,stdtaul
    # tags: stationarity,stochastic
    SY_SpreadRandomLocal_50_100 = (
        'SY_SpreadRandomLocal_50_100',
        SY_SpreadRandomLocal(l=50, nseg=100))

    # outs: meanac1,meanac2,meanapen1_02,meankurt,meanmean
    # outs: meansampen1_02,meanskew,meanstd,meantaul,stdac1
    # outs: stdac2,stdapen1_02,stdkurt,stdmean,stdsampen1_02
    # outs: stdskew,stdstd,stdtaul
    # tags: correlation,stationarity,stochastic
    SY_SpreadRandomLocal_200_100 = (
        'SY_SpreadRandomLocal_200_100',
        SY_SpreadRandomLocal(l=200, nseg=100))

    # outs: meanac1,meanac2,meanapen1_02,meankurt,meanmean
    # outs: meansampen1_02,meanskew,meanstd,meantaul,stdac1
    # outs: stdac2,stdapen1_02,stdkurt,stdmean,stdsampen1_02
    # outs: stdskew,stdstd,stdtaul
    # tags: stationarity,stochastic
    SY_SpreadRandomLocal_ac2_100 = (
        'SY_SpreadRandomLocal_ac2_100',
        SY_SpreadRandomLocal(l='ac2', nseg=100))

    # outs: meanac1,meanac2,meanapen1_02,meankurt,meanmean
    # outs: meansampen1_02,meanskew,meanstd,meantaul,stdac1
    # outs: stdac2,stdapen1_02,stdkurt,stdmean,stdsampen1_02
    # outs: stdskew,stdstd,stdtaul
    # tags: correlation,stationarity,stochastic
    SY_SpreadRandomLocal_100_100 = (
        'SY_SpreadRandomLocal_100_100',
        SY_SpreadRandomLocal(l=100, nseg=100))

    # outs: meanac1,meanac2,meanapen1_02,meankurt,meanmean
    # outs: meansampen1_02,meanskew,meanstd,meantaul,stdac1
    # outs: stdac2,stdapen1_02,stdkurt,stdmean,stdsampen1_02
    # outs: stdskew,stdstd,stdtaul
    # tags: stationarity,stochastic
    SY_SpreadRandomLocal_ac5_100 = (
        'SY_SpreadRandomLocal_ac5_100',
        SY_SpreadRandomLocal(l='ac5', nseg=100))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl100 = (
        'StatAvl100',
        SY_StatAv(WhatType='len', n=100))

    # outs: None
    # tags: StatAv,stationarity
    StatAv10 = (
        'StatAv10',
        SY_StatAv(WhatType='seg', n=10))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl25 = (
        'StatAvl25',
        SY_StatAv(WhatType='len', n=25))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl250 = (
        'StatAvl250',
        SY_StatAv(WhatType='len', n=250))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl150 = (
        'StatAvl150',
        SY_StatAv(WhatType='len', n=150))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl2000 = (
        'StatAvl2000',
        SY_StatAv(WhatType='len', n=2000))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl200 = (
        'StatAvl200',
        SY_StatAv(WhatType='len', n=200))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl1000 = (
        'StatAvl1000',
        SY_StatAv(WhatType='len', n=1000))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl50 = (
        'StatAvl50',
        SY_StatAv(WhatType='len', n=50))

    # outs: None
    # tags: StatAv,stationarity
    StatAvl500 = (
        'StatAvl500',
        SY_StatAv(WhatType='len', n=500))

    # outs: None
    # tags: StatAv,stationarity
    StatAv8 = (
        'StatAv8',
        SY_StatAv(WhatType='seg', n=8))

    # outs: None
    # tags: StatAv,stationarity
    StatAv9 = (
        'StatAv9',
        SY_StatAv(WhatType='seg', n=9))

    # outs: None
    # tags: StatAv,stationarity
    StatAv2 = (
        'StatAv2',
        SY_StatAv(WhatType='seg', n=2))

    # outs: None
    # tags: StatAv,stationarity
    StatAv3 = (
        'StatAv3',
        SY_StatAv(WhatType='seg', n=3))

    # outs: None
    # tags: StatAv,stationarity
    StatAv6 = (
        'StatAv6',
        SY_StatAv(WhatType='seg', n=6))

    # outs: None
    # tags: StatAv,stationarity
    StatAv7 = (
        'StatAv7',
        SY_StatAv(WhatType='seg', n=7))

    # outs: None
    # tags: StatAv,stationarity
    StatAv4 = (
        'StatAv4',
        SY_StatAv(WhatType='seg', n=4))

    # outs: None
    # tags: StatAv,stationarity
    StatAv5 = (
        'StatAv5',
        SY_StatAv(WhatType='seg', n=5))

    # outs: None
    # tags: entropy
    SY_StdNthDer_6 = (
        'SY_StdNthDer_6',
        SY_StdNthDer(n=6))

    # outs: None
    # tags: entropy
    SY_StdNthDer_7 = (
        'SY_StdNthDer_7',
        SY_StdNthDer(n=7))

    # outs: None
    # tags: entropy
    SY_StdNthDer_4 = (
        'SY_StdNthDer_4',
        SY_StdNthDer(n=4))

    # outs: None
    # tags: entropy
    SY_StdNthDer_5 = (
        'SY_StdNthDer_5',
        SY_StdNthDer(n=5))

    # outs: None
    # tags: entropy
    SY_StdNthDer_8 = (
        'SY_StdNthDer_8',
        SY_StdNthDer(n=8))

    # outs: None
    # tags: entropy
    SY_StdNthDer_9 = (
        'SY_StdNthDer_9',
        SY_StdNthDer(n=9))

    # outs: None
    # tags: entropy
    SY_StdNthDer_3 = (
        'SY_StdNthDer_3',
        SY_StdNthDer(n=3))

    # outs: None
    # tags: entropy
    SY_StdNthDer_10 = (
        'SY_StdNthDer_10',
        SY_StdNthDer(n=10))

    # outs: None
    # tags: entropy
    SY_StdNthDer_2 = (
        'SY_StdNthDer_2',
        SY_StdNthDer(n=2))

    # outs: None
    # tags: entropy
    SY_StdNthDer_1 = (
        'SY_StdNthDer_1',
        SY_StdNthDer(n=1))

    # outs: fexp_a,fexp_adjr2,fexp_b,fexp_r2,fexp_rmse
    # tags: entropy
    SY_StdNthDerChange = (
        'SY_StdNthDerChange',
        SY_StdNthDerChange())

    # outs: iqr,iqroffdiag,max,maxeig,maximageig
    # outs: mean,median,min,mineig,minimageig
    # outs: minlower,minoffdiag,minupper,range,rangeeig
    # outs: rangemean,rangemedian,rangeoffdiag,rangerange,rangestd
    # outs: std,stdeig,stdmean,stdmedian,stdoffdiag
    # outs: stdrange,stdstd,trace
    # tags: model,nonlinear,stationarity,tisean
    SY_TISEAN_nstat_z_5_1_3 = (
        'SY_TISEAN_nstat_z_5_1_3',
        SY_TISEAN_nstat_z(nseg=5, embedparams=(1.0, 3.0)))

    # outs: iqr,iqroffdiag,max,maxeig,maximageig
    # outs: mean,median,min,mineig,minimageig
    # outs: minlower,minoffdiag,minupper,range,rangeeig
    # outs: rangemean,rangemedian,rangeoffdiag,rangerange,rangestd
    # outs: std,stdeig,stdmean,stdmedian,stdoffdiag
    # outs: stdrange,stdstd,trace
    # tags: model,nonlinear,stationarity,tisean
    SY_TISEAN_nstat_z_4_1_3 = (
        'SY_TISEAN_nstat_z_4_1_3',
        SY_TISEAN_nstat_z(nseg=4, embedparams=(1.0, 3.0)))

    # outs: iqr,iqroffdiag,max,maxeig,maximageig
    # outs: mean,median,min,mineig,minimageig
    # outs: minlower,minoffdiag,minupper,range,rangeeig
    # outs: rangemean,rangemedian,rangeoffdiag,rangerange,rangestd
    # outs: std,stdeig,stdmean,stdmedian,stdoffdiag
    # outs: stdrange,stdstd,trace
    # tags: model,nonlinear,stationarity,tisean
    SY_TISEAN_nstat_z_4_ac_3 = (
        'SY_TISEAN_nstat_z_4_ac_3',
        SY_TISEAN_nstat_z(nseg=4, embedparams=('ac', 3)))

    # outs: pValue,ratio,stat
    # tags: econometricstoolbox,pvalue,vratiotest
    SY_VarRatioTest_4_0 = (
        'SY_VarRatioTest_4_0',
        SY_VarRatioTest(periods=4, IIDs=0))

    # outs: pValue,ratio,stat
    # tags: econometricstoolbox,pvalue,vratiotest
    SY_VarRatioTest_4_1 = (
        'SY_VarRatioTest_4_1',
        SY_VarRatioTest(periods=4, IIDs=1))

    # outs: pValue,ratio,stat
    # tags: econometricstoolbox,pvalue,vratiotest
    SY_VarRatioTest_2_0 = (
        'SY_VarRatioTest_2_0',
        SY_VarRatioTest(periods=2, IIDs=0))

    # outs: pValue,ratio,stat
    # tags: econometricstoolbox,pvalue,vratiotest
    SY_VarRatioTest_2_1 = (
        'SY_VarRatioTest_2_1',
        SY_VarRatioTest(periods=2, IIDs=1))

    # outs: IIDperiodmaxpValue,IIDperiodminpValue,maxpValue,maxstat,meanpValue
    # outs: meanstat,minpValue,minstat,periodmaxpValue,periodminpValue
    # tags: econometricstoolbox,pvalue,vratiotest
    SY_VarRatioTest_24682468_00001111 = (
        'SY_VarRatioTest_24682468_00001111',
        SY_VarRatioTest(periods=(2.0, 4.0, 6.0, 8.0, 2.0, 4.0, 6.0, 8.0), IIDs=(0.0, 0.0, 0.0, 0.0,
                        1.0, 1.0, 1.0, 1.0)))

    # outs: difftau12,difftau13,maxtau,meantau,mintau
    # outs: stdtau,tau1,tau2,tau3
    # tags: correlation,nonlinear,stochastic,tau,tstool
    TSTL_delaytime_01_1 = (
        'TSTL_delaytime_01_1',
        TSTL_delaytime(maxdelay=0.1, past=1))

    # outs: ac1den,ac2den,ac3den,ac4den,ac5den
    # outs: iqrden,maxden,meanden,medianden,minden
    # outs: rangeden,stdden,tauacden,taumiden
    # tags: localdensity,nonlinear,stochastic,tstool
    TSTL_localdensity_5_40_ac_cao = (
        'TSTL_localdensity_5_40_ac_cao',
        TSTL_localdensity(NNR=5, past=40, embedparams=('ac', 'cao')))

    # outs: ac1den,ac2den,ac3den,ac4den,ac5den
    # outs: iqrden,maxden,meanden,medianden,minden
    # outs: rangeden,stdden,tauacden,taumiden
    # tags: localdensity,nonlinear,tstool
    TSTL_localdensity_5_40_ac_2 = (
        'TSTL_localdensity_5_40_ac_2',
        TSTL_localdensity(NNR=5, past=40, embedparams=('ac', 2)))

    # outs: ac1den,ac2den,ac3den,ac4den,ac5den
    # outs: iqrden,maxden,meanden,medianden,minden
    # outs: rangeden,stdden,tauacden,taumiden
    # tags: localdensity,nonlinear,tstool
    TSTL_localdensity_5_40_1_3 = (
        'TSTL_localdensity_5_40_1_3',
        TSTL_localdensity(NNR=5, past=40, embedparams=(1.0, 3.0)))

    # outs: corrcoef_max_medians,max1on2_max,max1on2_mean,max1on2_median,max_max
    # outs: max_mean,max_median,std_max,std_mean,std_median
    # outs: wheremax_max,wheremax_mean,wheremax_median,wslesr_max,wslesr_mean
    # outs: wslesr_median
    # tags: wavelet,waveletTB
    WL_DetailCoeffs_db3_max = (
        'WL_DetailCoeffs_db3_max',
        WL_DetailCoeffs(wname='db3', maxlevel='max'))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_5 = (
        'WL_coeffs_db3_5',
        WL_coeffs(wname='db3', level=5))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_2 = (
        'WL_coeffs_db3_2',
        WL_coeffs(wname='db3', level=2))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_3 = (
        'WL_coeffs_db3_3',
        WL_coeffs(wname='db3', level=3))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_4 = (
        'WL_coeffs_db3_4',
        WL_coeffs(wname='db3', level=4))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_1 = (
        'WL_coeffs_db3_1',
        WL_coeffs(wname='db3', level=1))

    # outs: max_coeff,mean_coeff,med_coeff,wb10m,wb1m
    # outs: wb25m,wb50m,wb75m,wb90m,wb99m
    # tags: lengthdep,wavelet,waveletTB
    WL_coeffs_db3_max = (
        'WL_coeffs_db3_max',
        WL_coeffs(wname='db3', level='max'))

    # outs: SC_h,dd_SC_h,exp_muhat,gam1,gam2
    # outs: maxSC,max_ssc,maxabsC,maxonmedC,maxonmedSC
    # outs: maxonmed_ssc,meanC,meanSC,meanabsC,medianSC
    # outs: medianabsC,min_ssc,pcross_maxssc50,pover80,pover90
    # outs: pover95,pover98,pover99,stat_2_m_s,stat_2_s_m
    # outs: stat_2_s_s,stat_5_m_s,stat_5_s_m,stat_5_s_s,std_ssc
    # tags: cwt,lengthdep,statTB,wavelet,waveletTB
    WL_cwt_sym2_32 = (
        'WL_cwt_sym2_32',
        WL_cwt(wname='sym2', maxscale=32))

    # outs: SC_h,dd_SC_h,exp_muhat,gam1,gam2
    # outs: maxSC,max_ssc,maxabsC,maxonmedC,maxonmedSC
    # outs: maxonmed_ssc,meanC,meanSC,meanabsC,medianSC
    # outs: medianabsC,min_ssc,pcross_maxssc50,pover80,pover90
    # outs: pover95,pover98,pover99,stat_2_m_s,stat_2_s_m
    # outs: stat_2_s_s,stat_5_m_s,stat_5_s_m,stat_5_s_s,std_ssc
    # tags: cwt,lengthdep,statTB,wavelet,waveletTB
    WL_cwt_db3_32 = (
        'WL_cwt_db3_32',
        WL_cwt(wname='db3', maxscale=32))

    # outs: maxd_l1,maxd_l2,maxd_l3,maxd_l4,maxd_l5
    # outs: mind_l1,mind_l2,mind_l3,mind_l4,mind_l5
    # outs: stdd_l1,stdd_l2,stdd_l3,stdd_l4,stdd_l5
    # outs: stddd_l1,stddd_l2,stddd_l3,stddd_l4,stddd_l5
    # tags: dwt,wavelet,waveletTB
    WL_dwtcoeff_sym2_5 = (
        'WL_dwtcoeff_sym2_5',
        WL_dwtcoeff(wname='sym2', level=5))

    # outs: maxd_l1,maxd_l2,maxd_l3,maxd_l4,maxd_l5
    # outs: mind_l1,mind_l2,mind_l3,mind_l4,mind_l5
    # outs: stdd_l1,stdd_l2,stdd_l3,stdd_l4,stdd_l5
    # outs: stddd_l1,stddd_l2,stddd_l3,stddd_l4,stddd_l5
    # tags: dwt,wavelet,waveletTB
    WL_dwtcoeff_db3_5 = (
        'WL_dwtcoeff_db3_5',
        WL_dwtcoeff(wname='db3', level=5))

    # outs: p1,p2,p3
    # tags: wavelet,waveletTB
    WL_fBM = (
        'WL_fBM',
        WL_fBM())

    # outs: lmax,period,pf
    # tags: wavelet,waveletTB
    WL_scal2frq_db3_max_1 = (
        'WL_scal2frq_db3_max_1',
        WL_scal2frq(wname='db3', amax='max', delta=1))

    @staticmethod
    def all():
        return sorted((name, comp[1]) for name, comp in HCTSAOperations.__dict__.iteritems()
                      if not name.startswith('_') and not name == 'all')