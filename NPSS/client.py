
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

prob.setup()
prob.final_setup()

print("=========================================================================")

prob.set_val("Alt_DES", 30000.)
prob.set_val("MN_DES", 0.7)

prob.run_model()

prob.model.list_inputs(shape=True, units=True)
prob.model.list_outputs(shape=True, units=True)

print("=========================================================================")

prob.set_val("Alt_DES", 25000.)
prob.set_val("MN_DES", 0.5)

prob.run_model()

prob.model.list_inputs(shape=True, units=True)
prob.model.list_outputs(shape=True, units=True)
