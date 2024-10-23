import numpy as np
import model
import solver
import matplotlib.pyplot as plt

def run_simulation():
    # Parameters
    m = 1.0      # mass (kg)
    k = 10.0     # stiffness (N/m)
    d = 0.5     # damping coefficient

    # initial conditions
    iniStates = np.array([3.0, 0.0])

    # Time parameters
    t_final = 15.0
    dt = 0.001
    num_steps = int(t_final / dt)

    # Create a model (SingleMassOscillator)
    myModel = model.SingleMassOscillator(iniStates, m, k, d)

    # Create a solver and pass the model to it
    mySolver = solver.SolverExplicit(myModel)

    # Arrays to store time and position for plotting
    times = np.linspace(0, t_final, num_steps)
    positions = np.zeros_like(times)

    # Simulation loop
    for step in range(num_steps):
        t = step * dt
        # Store the current position for plotting
        positions[step] = myModel.get_state()[0]
        
        # Take a time step
        mySolver.step(t, dt)

    # Plotting the result
    plt.plot(times, positions)
    plt.xlabel('Time (s)')
    plt.ylabel('Position (m)')
    plt.title('Position vs. Time')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    run_simulation()
