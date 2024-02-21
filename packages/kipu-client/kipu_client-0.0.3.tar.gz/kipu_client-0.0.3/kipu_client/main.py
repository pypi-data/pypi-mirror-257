import requests
import logging
import pandas as pd

from .datascience.helpers import get_ising_coeffs as feature_selection_coefs

class Client:
    """
    Python client meant to interact with the circuit composer service
    """

    def __init__(self,
                 api_key: str,
                 api_server_url: str = "https://api.kipustack.com"):

        # Endpoint(s)
        self._api_server_url = api_server_url

        # User information (token refresh)
        self._key = requests.utils.quote(api_key)

        # Header
        self.header = {
            "accept" : "application/json",
            "Content-type" : "application/json",
        }


    def optimize_portfolio(self, profit: list, risk: list, cost: list, budget: float):
        """
        Given a dataframe containing the evolution of finance instruments, builds the 
        QUBO model so that it can be solved by the DCQO endpoint obtaining best portfolio
        configuration.
        """
        # Build QUBO

        # Send to optimization endpoint

        raise NotImplementedError

    def compose_circuit(self,
                        linear_coeffs: list,
                        quadratic_coeffs : dict,
                        T:float = 0.03,
                        N:int = 3,
                        mode:str = "FULL"):
        """
        Given an Ising model gets solved by the DCQO endpoint

        Args:
            linear_coeffs (list): Linear coefficients
            quadratic_coeffs (dict): Quadratic coefficients
            T (float, optional): Annealing time. Defaults to 0.03.
            N (int, optional): Trotter steps. Defaults to 3.
            mode (str, optional): Mode between adiabatic ADB, counterdiabatic FULL 
                or simply adding the CD terms. Defaults to "FULL".

        Returns:
            str: QASM circuit encoding the problem
        """
        # Get coefficients
        ising = {
            "h" : linear_coeffs,
            "J" : quadratic_coeffs
        }

        # Send to optimization endpoint
        endpoint = f"/optimization/composer/dcqo?api_key={self._key}&mode={mode}&T={T}&N={N}"
        url = f"{self._api_server_url}{endpoint}"
        r = requests.post(url=url, headers=self.header, json=ising, timeout=20)

        if r.status_code == 200:
            response = r.json()
            return response
        else:
            logging.error(f"Something went wrong: {r.status_code} {r.reason}")

    def feature_selection(self,
                          data: pd.DataFrame,
                          target:str,
                          max_features: int,
                          reg_lambda: float = 5.0,
                          T:float = 0.03,
                          N:int = 3,
                          mode:str = "FULL"):
        """
        Given a dataframe containing a dataset, builds the 
        QUBO model so that it can be solved by the DCQO endpoint
        on which features should be selected.

        Args:
            data (pd.DataFrame): Dataframe to be used
            target (str): Target column within the dataframe
            max_features (int): Maximum number of features to be returned
            reg_lambda (float, optional): Regularization term. Defaults to 5.0.
            T (float, optional): Annealing time. Defaults to 0.03.
            N (int, optional): Trotter steps. Defaults to 3.
            mode (str, optional): Mode between adiabatic ADB, counterdiabatic FULL 
                or simply adding the CD terms. Defaults to "FULL".

        Returns:
            str: QASM circuit encoding the problem
        """
        # Get coefficients
        h, jp = feature_selection_coefs(data, target, max_features, reg_lambda)
        ising = {
            "h" : h,
            "J" : jp
        }

        # Send to optimization endpoint
        endpoint = f"/optimization/composer/dcqo?api_key={self._key}&mode={mode}&T={T}&N={N}"
        url = f"{self._api_server_url}{endpoint}"
        r = requests.post(url=url, headers=self.header, json=ising, timeout=20)

        if r.status_code == 200:
            response = r.json()
            return response
        else:
            logging.error(f"Something went wrong: {r.status_code} {r.reason}")
