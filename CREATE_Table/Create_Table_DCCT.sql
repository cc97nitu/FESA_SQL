CREATE TABLE dcct (
    processStartStamp       bigint  PRIMARY KEY,
    sequenceStartStamp      bigint,
    eventStamp              bigint,
    acquisitionStamp        bigint,
    lastInjection           bigint,
    lastExtraction          bigint,
    intensity               double precision[],
    processIndex            integer,
    sequenceIndex           integer,
    ionChargeState          integer
);
