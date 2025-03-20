
import philote_mdo.general as pmdo
import openmdao.api as om

from aviary.examples.external_subsystems.engine_NPSS.NPSS_Model.DesignEngineGroup import NPSSExternalCodeComp


class NPSSDiscipline(pmdo.ExplicitDiscipline):
    """
    NPSS Discipline
    """
    def __init__(self):
        self.npss = om.Problem()
        self.npss.model.add_subsystem('npss', NPSSExternalCodeComp())
        super().__init__()

    def setup(self):
        self.npss.setup()

        for name, meta in self.npss.model.list_inputs(shape=True, units=True, val=False):
            name = name[5:]  # strip the npss. prefix
            units = meta['units']
            self.add_input(name, shape=meta['shape'], units=units if units else '')

        self.npss.model.list_outputs(shape=True, units=True)

        for name, meta in self.npss.model.list_outputs(shape=True, units=True, val=False):
            name = name[5:]  # strip the npss. prefix
            units = meta['units']
            self.add_output(name, shape=meta['shape'], units=units if units else '')

    def compute(self, inputs, outputs):
        for name, val in inputs.items():
            self.npss.set_val('npss.'+name, val)
        self.npss.run_model()
        for name, meta in self.npss.model.list_outputs():
            name = name[5:]  # strip the npss. prefix
            outputs[name] = meta['val']


if __name__ == '__main__':
    #
    # First, a gRPC channel needs to be generated:
    #
    from concurrent import futures
    import grpc

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    #
    # Next, the NPSS discipline is attached to the server:
    #
    import philote_mdo.general as pmdo
    discipline = pmdo.ExplicitServer(discipline=NPSSDiscipline())
    discipline.attach_to_server(server)

    #
    #  Finally, the port of the server is defined (opening a port is necessary for network communication) and the server is started:
    #
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. Listening on port 50051.")
    server.wait_for_termination()
