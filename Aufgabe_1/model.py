#model.py

import numpy as np

class Model:
    def __init__(self, iniState):
        self.state = iniState

    def get_state(self):
        return self.state
    
    def set_state(self, new_state):
        self.state = new_state

    def dydt(self, t, y):
        """Defines the system's dynamics: computes the derivative of the state vector."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class SingleMassOscillator(Model):
    def __init__(self, iniState, m, k, d):
        super().__init__(iniState)
        self.m = m  # mass
        self.k = k  # stiffness (spring constant)
        self.d = 2*d*np.sqrt(self.k*self.m)  # damping coefficient

    def dydt(self, t):
        """Compute the derivatives of the state (velocity and acceleration)."""
        # Unpack the state vector
        position = self.state[0]  # x (position)
        velocity = self.state[1]  # v (velocity)
        
        # Compute acceleration using the equation of motion
        acceleration = -(self.k / self.m) * position - (self.d / self.m) * velocity
        
        # Return the velocity and acceleration as the derivative of the state
        return np.array([velocity, acceleration])