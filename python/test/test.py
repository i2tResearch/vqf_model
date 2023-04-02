import logging
from minizinc import Instance, Model, Solver

# Setup logging
logging.basicConfig(filename="test_logs.log", level=logging.DEBUG)

# Load model, set solver and create instance
model = Model("./test_model.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

# Assign 4 to n
instance["n"] = 4
result = instance.solve()

# Output the array q
print(result["q"])
