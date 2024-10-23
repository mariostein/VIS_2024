import model

class Solver:
    def __init__(self, model2Solve):
        if not isinstance(model2Solve, model.Model):
            raise TypeError("Expected an instance of model.Model or its subclass.")
        self.__model__ = model2Solve

    def step(self, t, dt):
        """Should be implemented in derived classes."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class SolverExplicit(Solver):
    def __init__(self, model2Solve):
        super().__init__(model2Solve)

    def step(self, t, dt):
        """Perform one step of numerical integration."""
        # Get the current state (position and velocity)
        state = self.__model__.get_state()  # [position, velocity]
        
        # Get the derivatives (velocity and acceleration) from the model
        derivatives = self.__model__.dydt(t)
        
        # Update the position: x_new = x_old + v_old * dt
        new_position = state[0] + derivatives[0] * dt
        
        # Update the velocity: v_new = v_old + a * dt
        new_velocity = state[1] + derivatives[1] * dt
        
        # Set the new state in the model
        self.__model__.set_state([new_position, new_velocity])
