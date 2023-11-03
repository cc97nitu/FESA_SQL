#!/usr/bin/env python3

"""Store single BPM readings to postgres."""

import time
from datetime import datetime
import numpy as np
import psycopg2
from psycopg2.extensions import register_adapter, AsIs

from pyda import SimpleClient
from pyda.data import DataFilter, TimingSelector
from pyda_rda3 import RdaProvider


TERMINAL_COLORS = [
"\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[34m", "\u001b[35m", "\u001b[36m", "\u001b[37m", "\u001b[31;1m", "\u001b[32;1m", "\u001b[33;1m", "\u001b[34;1m", "\u001b[35;1m",
]

TERMINAL_COLOR_RESET = "\u001b[0m"


def adapt_numpy_array(numpy_array):
    return AsIs(list(numpy_array))

register_adapter(np.ndarray, adapt_numpy_array)
register_adapter(np.int32, AsIs)
register_adapter(np.int64, AsIs)
register_adapter(np.float32, AsIs)
register_adapter(np.float64, AsIs)


class Array(str):
    def __init__(self, name):
        self.name = name
        
    def __repr__(self):
        return self.name


def createInsertionStatement(table, fields):
    values = list()
    for f in fields:
        if type(f) is Array:
            values.append("ARRAY %s")
        else:
            values.append("%s")

    ", ".join(values)
    
    fields_quoted = [f for f in fields]

    # rename fields that are protected names in SQL
    for (i,name) in enumerate(fields_quoted):
        if name == "offset":
            fields_quoted[i] = "record_offset"
    
    insertionStatement = "INSERT INTO " + table + "(" + ", ".join(fields_quoted) + ") VALUES(" + ", ".join(values) + ");"
    return insertionStatement


def main(insertionStatement) -> None:
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
    for response in subscription:

        ts = response.value["acquisitionStamp"] / 1e9
        ts_datetime = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        # store in database
        t_start = time.time()
        values = [response.value[f] for f in FIELD_NAMES]
        crsr.execute(insertionStatement, values)
        dbcon.commit()

        t_end = time.time() - t_start

        print(TERMINAL_COLORS[args.bpm - 1] + "BPM {:02d}".format(args.bpm) + 
              " committed S={}:P={}".format(response.value["sequenceIndex"], response.value["processIndex"]) +
              "    " + ts_datetime + "    completed within {:.2f}".format(t_end) +
              TERMINAL_COLOR_RESET)

        #return response

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
PROPERTY_NAME = "GS01DX/Acquisition"
DATA_FILTER = DataFilter(acqModeFilter=np.int32(2))
TABLE_NAME = "gs01dx_acquisition"
FIELD_NAMES = ["processStartStamp", "sequenceStartStamp", "eventStamp", "acquisitionStamp", "processIndex", "sequenceIndex", "gainTimestamp",
               Array("gainValue"), "acqMode", "acquiredOk", "offset", "temperature", Array("beamPosition"), Array("beamPosition_dim3_labels"), Array("sumSignal")]


##############################################
############## FAIR Selector #################
##############################################
FAIR_SELECTOR = "FAIR.SELECTOR.ALL"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
                    prog='SQL_dump_BPM',
                    description='Dump BPM data to SQL database.',
    )

    parser.add_argument("--bpm", type=int, required=True)

    args = parser.parse_args()

    ##############################################
    ############## FESA property #################
    ##############################################
    PROPERTY_NAME = "GS{:02d}DX/Acquisition".format(args.bpm)
    TABLE_NAME = "bpm_fesa_dump." + "gs{:02}dx_acquisition".format(args.bpm)
    print(PROPERTY_NAME, TABLE_NAME)
    
    # run dump loop
    resp = main(createInsertionStatement(TABLE_NAME, FIELD_NAMES))

