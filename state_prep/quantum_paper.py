from classiq import *

def generate_gaussian(num_qubits):
  resolution = num_qubits
  fraction_digits = resolution-2
  grid = np.linspace(-2**(resolution-fraction_digits-1), 2**(resolution-fraction_digits-1)-2**(-fraction_digits), 2**(resolution))
  probs = np.exp(-1 * grid**2)
  probs /= np.sum(probs)
  
  return probs.tolist()


@qfunc
def main(x: Output[QNum]):
  num_qubits = 8
  allocate(x, num_qubits)
  mu_hat = 0
  sigma_hat = 1
  probs = generate_gaussian(8)
  num_iters = 2
  l = 1
  n_1 = 1
  m = num_qubits - n_1 + 1

  bigN = 2**num_qubits
  sigma = (bigN^2 / l^2) * sigma_hat
  mu = (bigN / l) * mu_hat
  big_sum = 0
  for k in range(2, m+1):
    big_sum += 4^(m-k)
  iters = []
  iters[0] = (sigma - (4^(num_qubits-1)-1)/12 - (num_iters/4)*(big_sum)) / 4^(num_qubits-1)
  for i in range(1, m+1):
    iters[i] = num_iters

  for i in range(1, m+1): # loop IV: there are i qubits in the Gaussian state.
    for j in range(1, iters[i]+1):
      # add a state in |+> to the register
      hadamard_transform(x[i]) # TODO: apply hadamard to all of x at the beginning of the circuit.
      # add the register and 1 controlled on the |+> qubit
      control(ctrl=(x[i] == 1), stmt_block=(lambda: ))
      # apply a Hadamard to the |+> qubit
      # measure the (former) |+> qubit
      # if measured 1, try again. Else (move on or do next iteration?)??
      





quantum_program = synthesize(create_model(main))
job = execute(quantum_program)
results = job.result()[0].value.parsed_counts
print(results)


