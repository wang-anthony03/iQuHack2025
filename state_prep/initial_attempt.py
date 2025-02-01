from classiq import *
import numpy as np

def generate_gaussian(mu, sigma, num_qubits):
  resolution = num_qubits
  fraction_digits = resolution-2
  grid = np.linspace(-2**(resolution-fraction_digits-1), 2**(resolution-fraction_digits-1)-2**(-fraction_digits), 2**(resolution))
  probs = np.exp(-1 * grid**2)
  probs /= np.sum(probs)

  """
  rng = np.random.default_rng()

  probs = rng.normal(mu, sigma, 2**num_qubits)
  aggregate = np.sum(probs)
  probs /= aggregate
  probs = probs.tolist()
  """  
  return probs.tolist()

@qfunc
def main(x: Output[QArray]):
  num_qubits = 8
  mu = 0.5
  sigma = 0.1
  allocate(num_qubits, x)
  probs = generate_gaussian(mu, sigma, num_qubits)
  print(np.sum(probs))
  error = 0.01
  
  inplace_prepare_state(probabilities=probs, bound=error, target=x)


quantum_program = synthesize(create_model(main))
job = execute(quantum_program)
results = job.result()[0].value.parsed_counts
print(results)
