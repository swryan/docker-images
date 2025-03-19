
import philote_mdo.general as pmdo

from aviary.examples.external_subsystems.engine_NPSS.NPSS_Model.DesignEngineGroup import NPSSExternalCodeComp


class NPSSDiscipline(pmdo.ExplicitDiscipline):
    """
    NPSS Discipline
    """
    def __init__(self):
        super().__init__()
        self.npss = NPSSExternalCodeComp()

    def setup(self):
        for name, metadata in self.npss.list_inputs(all_procs=True):
            print("adding input", name, metadata)
            self.add_input(name, **metadata)

        for name, metadata in self.npss.list_outputs(all_procs=True):
            print("adding output", name, metadata)
            self.add_input(name, **metadata)

    # def setup_partials(self):
    #     # this external code does not provide derivatives, use finite difference
    #     # Note: step size should be larger than NPSS solver tolerance
    #     self.declare_partials(of='*', wrt='*', method='fd', step=1e-6)

    def compute(self, inputs, outputs):
        print("calling compute", inputs, outputs)
        self.npss.compute(inputs, outputs)


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
