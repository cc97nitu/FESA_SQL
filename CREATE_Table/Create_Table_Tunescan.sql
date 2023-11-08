CREATE TABLE bpm_fesa_dump.tunescan (
    scanCompleted       bigint  PRIMARY KEY,
    scanStarted         bigint,
    qx_min              real,
    qx_max              real,
    qy_min              real,
    qy_max              real,
    direction           text,
    tunescan            jsonb
);
