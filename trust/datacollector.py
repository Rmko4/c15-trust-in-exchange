""" This file contains the datacollector, extending the datacollector as
    defined in the MESA framework. 
"""
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from mesa.datacollection import DataCollector


class PDTDataCollector(DataCollector):
    """ Defines the datacollector.
    """
    def __init__(self, model_reporters: dict = None, agent_reporters: dict = None,
                 tables: dict = None, proportion_reporters: Dict[str, Tuple[str, str]] = None):
        """ Initializes the datacollector. In addition to the initialization of the
            MESA datacollector, proportional reporters are added. In the current implementation
            this consists of the trust in stranger proportion.
        """
        super().__init__(model_reporters, agent_reporters, tables)
        self.proportion_reporters = proportion_reporters

    def _get_agents_vars_sum(self):
        """ TODO
        """
        agent_vars_sum = {}
        records = self._agent_records.values()
        records = np.array(list(records))

        rep_names = self.agent_reporters.keys()
        for i, rep_name in zip(range(2, 2 + len(rep_names)), rep_names):
            summed_var = np.sum(records[:, :, i], axis=0)
            agent_vars_sum[rep_name] = summed_var
        
        return agent_vars_sum

    def get_agent_vars_sum_dataframe(self):
        """ TODO
        """
        agent_vars_sum = self._get_agents_vars_sum()
        return pd.DataFrame(agent_vars_sum)

    def _get_proportions(self):
        """ TODO
        """
        agent_proportions_vars = {}
        agent_vars_sum = self._get_agents_vars_sum()

        for rep_name, prop_names in self.proportion_reporters.items():
            a = agent_vars_sum[prop_names[0]]
            b = agent_vars_sum[prop_names[1]]
            prop = a/b
            agent_proportions_vars[rep_name] = prop
        
        return agent_proportions_vars
            
    def get_agent_props_dataframe(self):
        """ TODO
        """
        agent_proportions = self._get_proportions()
        return pd.DataFrame(agent_proportions)
