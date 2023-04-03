import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG)

from minizinc import Instance, Model, Solver

# Load model, set solver and create instance
print("Configuring model")
model = Model("./test_model.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

# Assign 4 to n
print("Setting input variables")
instance["n"] = 4

# Solve model
print("Solving model")
result = instance.solve()

# Output the array q
print("Result")
print(result["q"])
