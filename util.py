import numpy as np
from numpy import random

class CaseGenerator():
    def __init__(self, rou, mu, Lambda, delta1, delta2, J, M, V):
        self.processTime = np.array(1, J)
        self.capacity = np.array(1, V)
        self.serviceTime = np.array(1, J + 1)
        self.MreadyTime = np.array(1, M)
        self.VreadyTime = np.array(1, V)
        self.ub = np.array(1, J)
        self.lb = np.array(1, J)
        self.rou = rou; self.mu = mu; self.Lambda = Lambda
        self.delta1 = delta1; self.delta2 = delta2
        self.J = J; self.M = M; self.V = V

    def construct_case(self):
        # Generate the process time for each job
        for i in range(0, self.J):
            time = self.generate_proc_time(self.rou)

    def generate_proc_time(self, rou):
        """
        Generate the process time for each job
        rou: the maximum process time defined by the user
        """
        return np.round(random.uniform(1, rou))

    def generate_job_size(self, p):
        """
        Generate the job size (related to the vehicle capacity) for each job
        p: the process time of the corresponding job
        """
        return np.round(random.uniform(1, p))

    def generate_vehicle_cap(self, U, mu):
        """
        Generate the vehicle capacity of each vehicle
        U: the size of all jobs
        mu: control parameter, the smaller mu, the smaller the capacities of the vehicles in relation to the job sizes.
        """
        max_cap = np.max(U)
        tao = np.round(random.uniform(0, mu * max_cap))
        return max_cap + tao

    def generate_travelMatrix(self, n, upper):
         """
         Generate the travel time
         n: The number of customers
         """
         upper_triangular = np.random.randint(0, upper + 1, size = (n, n))
         upper_triangular = np.triu(upper_triangular, k = 1)

         travel_time = upper_triangular + upper_triangular.T
         np.fill_diagonal(travel_time, 0)

         return travel_time

    def generate_service_time(self, Lambda, rou):
        """
        Generate the service time for each job (i.e. time required for each job to loading/unloading, registering)
        Lambda: control parameter
        rou: control parameter
        """
        limit = np.floor(Lambda * rou)
        return np.round(random.uniform(1, limit))

    def generate_ready_time(self, rou):
        """
        Generate the machine ready time. The machine that is the first ready to proces is labeled as 1 and scaled to r_1 = 0
        Following code aims to generate the ready time of the rest machines
        rou: control parameter
        """
        return np.round(random.uniform(1, rou))

    def generate_vehi_ready_time1(self, R, s_0, rou, Lambda, V, M):
        """
        Generate the ready time of the vehicle that deliver the last job of the previous set can start to be delivered
        R: the ready time of machines
        s_0: the service time at the depot
        rou: the maximum process time
        Lambda: control parameter used when generating the service time
        V: number of vehicles
        M: number of machines
        """
        max_time = np.max(R)
        a = np.floor(rou * (V / M))
        b = np.floor(Lambda * rou)
        gamma = np.round(random.uniform(3, a + b))

        return max_time + s_0 + gamma

    def generate_vehi_ready_time2(self, R, s_0, rou, Lambda, V, M):
        """
        Generate the ready time of the rest vehicles
        """
        max_time = np.max(R)
        a = np.floor(rou * (V / M))
        b = np.floor(Lambda * rou)

        return np.round(random.uniform(0, max_time + s_0 + a + b))

    def generate_lower_bound(self, p, s_0, t, delta1, rou, J, M, V):
        """
        Generate the lower bound for customer j.
        p: process time of the job j
        s_0: service time at the depot
        t: travel time between depot and customer j.
        delta1: control parameter, the smaller the delta1, the tighter the lower bounds
        rou: maximum process time.
        J: number of jobs
        M: number of machines
        V: number of vehicles
        """
        pi = np.round(random.uniform(0, np.floor(delta1 * rou * J / (M + V))))
        return p + s_0 + t + pi

    def generate_upper_bound(self, delta2, rou, lb):
        """
        Generate the upper bound for customer j
        delta2: control parameter.
        rou: maximum process time
        lb: lower bound calculated before
        """
        k = np.floor(random)
        return lb + k