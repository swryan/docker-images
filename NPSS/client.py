
import grpc
import openmdao.api as om
import philote_mdo.openmdao as pmom

prob = om.Problem()
model = prob.model

model.add_subsystem(
    "NPSS",
    pmom.RemoteExplicitComponent(channel=grpc.insecure_channel("localhost:50051")),
    promotes=["*"],
)

print("client setup()")
prob.setup()

prob.model.list_inputs(shape=True, units=True)
prob.model.list_outputs(shape=True, units=True)

print("client final_setup()")
prob.final_setup()

print("client set input Alt_DES")
prob.set_val("Alt_DES", 30000.)

print("client set input MN_DES")
prob.set_val("MN_DES", 0.7)

print("client run_model()")
prob.run_model()

print("client list_outputs()")
prob.model.list_outputs()

print(prob["Fn_SLS"])
