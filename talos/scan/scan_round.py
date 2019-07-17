def scan_round(self):

    '''The main operational function that manages the experiment
    on the level of execution of each round.'''

    import time as ti
    import gc

    # print round params
    if self.print_params is True:
        print(self.round_params)

    # set start time
    round_start = ti.strftime('%D-%H%M%S')
    start = ti.time()

    # fit the model
    from ..model.ingest_model import ingest_model
    self.model_history, self.keras_model = ingest_model(self)
    self.round_history.append(self.model_history.history)

    # handle logging of results
    from ..logging.logging_run import logging_run
    self = logging_run(self, round_start, start, self.model_history)

    # apply reductions
    from ..reducers.reduce_run import reduce_run
    self = reduce_run(self)

    # save model and weights
    self.saved_models.append(self.keras_model.to_json())
    self.saved_weights.append(self.keras_model.get_weights())

    # clear tensorflow sessions
    if self.clear_session is True:

        del self.keras_model
        gc.collect()

        # try TF specific and pass for everyone else
        try:
            from keras import backend as K
            K.clear_session()
        except:
            pass

    return self
