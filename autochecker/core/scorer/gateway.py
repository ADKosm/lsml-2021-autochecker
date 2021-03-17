from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from importlib.resources import path
from typing import Tuple, Optional, List

import pandas as pd
import requests
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class MnistHTTPScorer:
    def __init__(self):
        self._X_test, self._y_test = self._get_test_subset()

    def _get_test_subset(self):
        from core import scorer

        dataset_name = "mnist_sample.csv"
        with path(scorer, dataset_name) as dataset_path:
            df = pd.read_csv(dataset_path)
            y = df['class'].values
            X = df.drop(['class'], axis=1).values
            _, X_test, _, y_test = train_test_split(X, y, test_size=0.1, random_state=789)

        return X_test.tolist(), y_test.tolist()

    def _check_one_example(self, x_data, service_url: str) -> Tuple[float, Optional[str]]:
        try:
            request_data = [x_data]

            r = requests.post(service_url, json={
                'method': 'predict',
                'data': request_data
            })

            return r.json()['label'], ""
        except Exception as e:
            return -1, str(e)

    def check_solution(self, service_url: str) -> Tuple[float, List[str]]:
        with ThreadPoolExecutor(max_workers=20) as executor:
            result = executor.map(partial(self._check_one_example, service_url=service_url), self._X_test)

        y_pred, errors = list(zip(*result))

        y_true = self._y_test
        accuracy = accuracy_score(y_pred, y_true)

        return accuracy, [x for x in errors if x]