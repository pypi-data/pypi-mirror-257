#Made by Abdelrahman Ashraf -- CairoUniversity --ID:20220190
#lasted edited 19/02/2024
import math  
import matplotlib.pyplot as plt  
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials


    TODO: Fill out all TODOs in the functions below

    """
  

    def __init__(self, prob=0.5, size=20):

        
        self.p = prob

        
        self.n = size
       
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
               
        pass

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set

        """

       

        self.mean = self.p * self.n
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """

        
        x = self.n * self.p * (1 - self.p)
        x = math.sqrt(x)
        self.stdev = x
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value

        """

       
        sum = 0
        for i in self.data:
            sum += i
        self.p = sum / len(self.data)
        self.n = len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p , self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """

       
        data = self.data
        counts = [data.count(0), data.count(1)]
        labels = ["0", "1"]
        plt.bar(labels, counts)
        plt.title("Bar Chart of Results")
        plt.xlabel("Result")
        plt.ylabel("Count")
        plt.show()

    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """

       

        x = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))
        y = (self.p**k) * ((1 - self.p) ** (self.n - k))
        return x * y

    def plot_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """

        x_values = []
        y_values = []
        for k in range(self.n + 1):
            x_values.append(k)
            y_values.append(self.pdf(k))

        plt.bar(x_values, y_values, align="center", alpha=0.75)

        
        plt.title("Probability Density Function (Binomial Distribution)")
        plt.xlabel("Number of Successes (k)")
        plt.ylabel("Probability Density")

        
        plt.show()

        return x_values, y_values

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, "p values are not equal"
        except AssertionError as error:  # noqa: F841
            raise
        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        return result
        

        pass

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Gaussian

        """

       
        print("mean {}, standard deviation {}, p {}, n {}".format(self.mean, self.stdev, self.p, self.n  ))
        pass
