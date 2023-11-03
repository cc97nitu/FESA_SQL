CREATE TABLE gs99dx (
    processIndex                integer,
    sequenceIndex               integer,
--    processStartStamp       bigint  PRIMARY KEY,
    processStartStamp           bigint,
    sequenceStartStamp          bigint,
    eventStamp                  bigint,
    acquisitionStamp            bigint  PRIMARY KEY,
--    acquisitionStamp            bigint,
    gainTimestamp               bigint,
    gainValue                   integer[],
    acqMode                     integer,
    acquiredOk                  boolean,
    record_offset               bigint,
    temperature                 real,
    beamPosition                real[],
    beamPosition_dim3_labels    bigint[],
    sumSignal                   real[]
);
