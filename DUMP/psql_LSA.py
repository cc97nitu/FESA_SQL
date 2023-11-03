import pjlsa_gsiint as pjlsa

import time
from datetime import datetime
import numpy as np
import psycopg2
from psycopg2.extensions import register_adapter, AsIs

from pyda import SimpleClient
from pyda.data import DataFilter, TimingSelector
from pyda_rda3 import RdaProvider

with pjlsa.LSAClientGSI().java_api():
    from cern.lsa.client import ServiceLocator, ContextService, ParameterService, TrimService, SettingService
    from cern.accsoft.commons.value import ValueFactory
    from cern.lsa.domain.settings import TrimRequest, ContextSettingsRequest, Settings, SettingPartEnum
    from cern.lsa.domain.settings.type import  BeamProcessPurposes
    from de.gsi.lsa.domain.settings import GsiBeamProcessPurpose
    from java.util import Set, Collections


TERMINAL_COLORS = [
"\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[34m", "\u001b[35m", "\u001b[36m", "\u001b[37m", "\u001b[31;1m", "\u001b[32;1m", "\u001b[33;1m", "\u001b[34;1m", "\u001b[35;1m",
]

TERMINAL_COLOR_RESET = "\u001b[0m"


def adapt_numpy_array(numpy_array):
    return AsIs(numpy_array.tolist())

register_adapter(np.ndarray, adapt_numpy_array)
register_adapter(np.int32, AsIs)
register_adapter(np.int64, AsIs)
register_adapter(np.float64, AsIs)


### main LSA services
ts = ServiceLocator.getService(TrimService)
cs = ServiceLocator.getService(ContextService)
ps = ServiceLocator.getService(ParameterService)
ss = ServiceLocator.getService(SettingService)


def equal_numpyArrayList(list_1, list_2):
    return np.all([np.array_equal(a, b, equal_nan=True) for (a, b) in zip(list_1, list_2)])


def read_functionParameters(pattern, parameters, ss=ss):
    patternSettings = ss.findContextSettings(
    ContextSettingsRequest.byStandAloneContextAndParameters(pattern, Set.of(parameters)))

    param_values = list()
    for p in parameters:
        df = Settings.getFunction(patternSettings, p) 
        val = np.array((df.toXArray(), df.toYArray(),))
        param_values.append(val)

    return param_values


def main(pattern, functionParameters, insertionStatement) -> None:
    """Main function."""
    # connect to database
    try:

        dbcon = psycopg2.connect("dbname="+DBNAME + " user=" + USER + " host=" + HOST + " port=" + PORT + " password=" + PASSWORD)
    except Exception as e:
        print("Unable to connect to database")
        print(e)

    crsr = dbcon.cursor()

    # subscribe to FESA
    client = SimpleClient(provider=RdaProvider())
    subscription = client.subscribe(
        PROPERTY_NAME,
        context=[
            TimingSelector(FAIR_SELECTOR),
            DATA_FILTER 
        ],
    )

    it = 0
    old_sequenceStartStamp, old_values = -1, None
    for response in subscription:
        if response.value["sequenceStartStamp"] == old_sequenceStartStamp:
            # still on same cycle
            continue
        else:
            old_sequenceStartStamp = response.value["sequenceStartStamp"] 
    
        ts = response.value["sequenceStartStamp"] / 1e9
        ts_datetime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # store in database
        t0 = time.time()

        # values = read_functionParameters(pattern, functionParameters)
        values = [np.zeros((5,5)) for _ in functionParameters]

        if old_values is None:
            old_values = values
        else:
            if equal_numpyArrayList(values, old_values):
                print("nothing new")
                continue

        extended_values = values + [response.value["sequenceIndex"], response.value["sequenceStartStamp"],]
        print("len values", len(extended_values))
        crsr.execute(insertionStatement, extended_values )
        dbcon.commit()

        t_end = time.time() - t0

        print(TERMINAL_COLORS[1] + "LSA_settings" + 
              " committed S={}".format(response.value["sequenceIndex"]) +
              "    " + ts_datetime + "    completed within {:.2f}".format(t_end) +
              TERMINAL_COLOR_RESET)

        return read_functionParameters(pattern, functionParameters), values

    return None


##############################################
############## SQL  Settings #################
##############################################
#DBNAME = "fesa_test"
#HOST = "140.181.85.66"
#PORT = "54321"
#USER = "fesa_tester"
#PASSWORD = "save_bpm"

DBNAME = "bpm_fesa_dump"
HOST = "pgsql.gsi.de"
PORT = "8646"
USER = "bpm_fesa_dump_slave"
PASSWORD = "kuwLMKTcAap6mKTP"


##############################################
############## FESA property #################
##############################################
PROPERTY_NAME = "GS09DT_ML/Acquisition"
DATA_FILTER = DataFilter(requestPartialData=True)


##############################################
############## LSA Parameter #################
##############################################
FUNCTIONPARAMETER_NAMES = ["SIS18BEAM/QH","SIS18BEAM/QV","SIS18BEAM/CH","SIS18BEAM/CV","SIS18BEAM/BRHO",
                   "LOGICAL.GS02BE1/URF","SIS18OPTICS/SIGMA","SIS18OPTICS/TAU"]

# sextupoles
FUNCTIONPARAMETER_NAMES += ["LOGICAL.GS{:02d}KS1C/K2L".format(i) for i in [1,3,5,7,9,11]]
FUNCTIONPARAMETER_NAMES += ["LOGICAL.GS{:02d}KS3C/K2L".format(i) for i in [1,3,5,7,9,11]]


##############################################
############## FAIR Selector #################
##############################################
FAIR_SELECTOR = "FAIR.SELECTOR.ALL"


if __name__ == "__main__":
    # fetch pattern and parameters
    pattern = cs.findPattern("SCRATCH_RM_SIS18_PYTHON_TEST_20220728_124253")
    functionParameters = [ps.findParameterByName(p) for p in FUNCTIONPARAMETER_NAMES]

    # create SQL insertion statement
    extended_names = FUNCTIONPARAMETER_NAMES + ["sequenceIndex", "sequenceStartStamp",]
    formatted_names = ", ".join([s.replace("/", "_").replace(".", "_") for s in extended_names])
    placeholders = ", ".join("ARRAY %s" for _ in FUNCTIONPARAMETER_NAMES) + ", %s", ", %s"

    sql_insert = """
    INSERT INTO bpm_fesa_dump.lsa_settings ({}) VALUES ({});
    """.format(formatted_names, placeholders)



    resp, val = main(pattern, functionParameters, sql_insert)