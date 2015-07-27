PandaShells                           
===

Introduction
---
For decades, system administrators, devops engineeirs and data analysts have been
piping textual data between unix tools such as grep, awk, sed, etc.  Chaining these
tools together provides an extremely powerful workflow.

The more recent emergence of the "data-scientist" has resulted in the increasing
popularity of tools like R, Pandas, IPython, etc.  These tools have amazing power
for transforming, analyzing and visualizing data-sets in ways that grep, awk,
sed, and even the dreaded perl-one-liner could never accomplish.

Pandashells is an attempt to marry the expressive, concise workflow of the shell pipeline
with the statistical and visualization tools of the python data-stack.


What is PandaShells?
----
* A set of command-line tools for working with tabular data
* Easily read/write data in CSV, or space delimited formats
* Quickly aggregate, join, and summarize tabular data 
* Compute descriptive statistics
* Perform spectral decomposition and linear regression
* Create data visualizations that can be saved to images or rendered interactively using 
  either a native backend or html.
* Designed to be used with unix pipes for easy integration with awk, grep, sed, etc.

What's with the name?
----
PandaShells is a riff on Pandas, the library created by Wes McKinney
that has become the go-to tool for working with data in python.

Description
----
If you work with data using Python, you have almost certainly encountered 
<a href="http://pandas.pydata.org/">Pandas</a>,
<a href="http://www.scipy.org/">SciPy</a>, 
<a href="http://matplotlib.org/">Matplotlib</a>, 
<a href="http://statsmodels.sourceforge.net/">Statsmodels</a> and
<a href="http://stanford.edu/~mwaskom/software/seaborn/">Seaborn</a> and

Pandashells command syntax attempts to replicate as closely as possible the
structure of the underlying library.  This should allow those familiar with the
python data stack to be immediately productive.


Installation
----
<pre><code><strong>[~]$ pip install --upgrade  git+https://github.com/robdmc/pandashells.git
</code></pre>

Requirements
----
Pandashells was built using the 
<a href="https://store.continuum.io/cshop/anaconda/">Anaconda Python Distribution</a>, and
we strongly recommend using it to run Pandashells.  Most of the libraries required by
pandashells come pre-installed with Anaconda, though some tools will require additional
libraries.

There is no requirements.txt file with pandashells because some of the tools only require
the standard library, and there's no sense installing unnecessary packages if you only want
to use that subset of tools.  If a particular tool encounters a missing dependency, it will
gracefully fail with an informative message detailing the steps required for installing
the missing dependency.

Below is a comprehensive list of the packages used in the toolset.
* gatspy
* matplotlib
* mpld3
* numpy
* pandas
* scipy
* seaborn
* statsmodels


General properties
----

* All pandaShells executables begin with a "p."  This is designed to work
  nicely with the bash-completion feature.  If you can't remember the exact
  name of a command, simply typing p.[tab] will show you a complete list of
  all pandaShells commands.

* Every command can be run with a -h option to view help.  Each of these
  help messages will contain multiple examples of how to proerly use the tool.


DataFrame Maniuplations
----

* Show a few rows of an example data set.
  <pre><code><strong>[~]$ p.example_data -d tips | head</strong>
"total_bill","tip","sex","smoker","day","time","size"
16.99,1.01,"Female","No","Sun","Dinner",2
10.34,1.66,"Male","No","Sun","Dinner",3
21.01,3.5,"Male","No","Sun","Dinner",3
23.68,3.31,"Male","No","Sun","Dinner",2
  </code></pre>

* Transorm the sample data from csv format to table format
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.head()' -o table</strong>
  total_bill   tip     sex smoker  day    time  size
       16.99  1.01  Female     No  Sun  Dinner     2
       10.34  1.66    Male     No  Sun  Dinner     3
       21.01  3.50    Male     No  Sun  Dinner     3
       23.68  3.31    Male     No  Sun  Dinner     2
       24.59  3.61  Female     No  Sun  Dinner     4
    </code></pre>

* Compute statistics for numerical fields in the data set.
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.describe().T' -o table index </strong>
              count       mean       std   min      25%     50%      75%    max
  total_bill    244  19.785943  8.902412  3.07  13.3475  17.795  24.1275  50.81
  tip           244   2.998279  1.383638  1.00   2.0000   2.900   3.5625  10.00
  size          244   2.569672  0.951100  1.00   2.0000   2.000   3.0000   6.00
  </code></pre>

* Break down the number of tippers by gender. Output of each command is stored as df for next command to use.
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.sex.value_counts()' 'df.rename(columns={0:"count"})' -o table index</strong>
          count
  Male      157
  Female     87
  </code></pre>

* Find the mean tip broken down by gender and day
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.groupby(by=["sex","day"]).tip.mean()' -o table index</strong>
                    tip
  sex    day
  Female Fri   2.781111
         Sat   2.801786
         Sun   3.367222
         Thur  2.575625
  Male   Fri   2.693000
         Sat   3.083898
         Sun   3.220345
         Thur  2.980333
  </code></pre>

* If you have an appropriate backend specified for matplotlib (this should be configured out of the box for the 
  <a href="https://store.continuum.io/cshop/anaconda/">Anaconda Python Distribution</a>)
  the following command should pop open a window with a zoom/pan enabled version of the graph below.
  <pre><code><strong>[~]$ p.example_data -d tips | p.df 'df.sex.value_counts()' 'df.rename(columns={0:"count"})' 'df.plot(kind="barh")'</strong> 
  </code></pre>
  ![Output Image](/images/gender_bar.png?raw=true "Bar chart of gender tipper counts.")


Visualization Tools
----

* Plot tip vs total bill.
  <pre><code><strong>[~]$ p.example_data -d tips | p.plot -x total_bill -y tip -s 'o' --title 'Tip Vs Bill'</strong> 
  </code></pre>
  ![Output Image](/images/tips_vs_bill.png?raw=true "Bar chart of gender tipper counts.")


List of Tools
===

Existing Tool | Purpose
--- | ---
p.crypt | Encrypt/Decrypt files using open-ssl tools.
p.df |       Pandas dataframe manipulation of csv files
p.geocode | Use google to geocode addresses
p.parallel | Run shell command in parallel
p.plot | Plot data
p.rand | Generate samples from random distributions
p.sig_edit | Perform recursive sigma editing for outlier removal
p.hist | Create a histogram of input data
p.linspace | Create a linearly spaced set of numbers
p.cdf | Compute cumulative distributions of input data
p.regress | Perform (multi-variable) linear regression
p.scatter_matrix | plot a pandas scatter matrix of input columns
p.regplot | plot results of single variable polynomial regression


Planned Tool | Purpose
--- | ---
p.cov | Create a table of covariances between collumns
p.bar | Create a bar chart using seaborn
p.fft | Compute fft of input data
p.lombscargle | Compute lombscargle spectra of intput data
p.interp | Interpolate input data
p.map | Plot geometry on maps using basemap
p.mapDots2html | Plot points on a google map
p.mapPoly2html | Plot polygons on a google map
p.mongoDump | Dump mongodb records to csv
p.normalize | Normalize a column of numbers
p.pgsql2csv | Dump a postgres database using sql
p.smooth | Smooth input data
p.lowess | Do Lowess smoothing
p.distplot | seaborn distplot
p.kdeplot | do 1d and 2d kde plots using seaborn
p.facetgrid | make facet grid plots using seaborn
p.boxplot | either using pandas or seaborn

p.sshKeyPush | Push an ssh key to a remote server
p.template | Use the jinja2 package to render templates
p.timezone | Change timestamps between time zones

Half Baked Ideas
===
It might be nice to have a 
p.batch -n batch-size -g str-group-func --apply app-process --first first-group-process --last last-group-process --parallel 2 
p.batch -n batch-size -g str-group-func --apply app-process -i input-options -o output-options --parallel 2 


might also be nice to have a  
p.deal --file-field column-name -i input-options -o output-options



Here are some half-baked ideas for tool syntax that I'm still think about how to implement.

* p.regress - statmodels linear regression with full summary output. maybe use --fit to add fit results to df
* p.learn.regress_linear
* p.learn.regress_ridge
* p.learn.regress_tree
* p.learn.regress_forest
* p.learn.classify.logistic
* p.learn.classify.tree
* p.learn.classify.forest
* p.learn.classify.svm

* Always use patsy language

* the model.pkl files (which can be user-def names) hold the model as well as the string used to do the fit

* with --fit model.pkl
  saves model in model.pkl and displays rms R^2 and cross_val scores as well as the original string used to do the fit and the type of model


* with --predict model.pkl
  loads model, input and shows _fit variable to the dataframe
  with --stats, does same thing, but displays rms and R2
  with --hist shows hist of residuals
  with --plot shows fit vs residual

* of course classifiers have their own metrics and maybe have a
  --roc that plots the roc curve

* with
  --info model.pkl, just shows the model

* with --desc 'my desc'  allows you to store a description that will be displayed with the --info flag

* It would be nice to create a scikit.learn model/pipeline, save it to a pickle file and then
  have a pandaShells command that would run predictions based on that model for inputs from stdin.
