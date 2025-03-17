
if __name__ == '__main__':
    #
    # First, a gRPC channel needs to be generated:
    #
    from concurrent import futures
    import grpc

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    #
    # Next, the Paraboloid discipline is attached to the server:
    #
    import philote_mdo.general as pmdo
    from philote_mdo.examples import Paraboloid
    discipline = pmdo.ExplicitServer(discipline=Paraboloid())
    discipline.attach_to_server(server)

    #
    #  Finally, the port of the server is defined (opening a port is necessary for network communication) and the server is started:
    #
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started. Listening on port 50051.")
    server.wait_for_termination()
