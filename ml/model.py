class DummyOPSModel:
    def predict(self, X):
        # とりあえず「直近OPS」を返す
        return [X.iloc[0]["ops_t-1"]]
