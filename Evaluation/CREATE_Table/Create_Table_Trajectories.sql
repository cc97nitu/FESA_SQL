CREATE TABLE Trajectories (
    acquisitionStamp        bigint  PRIMARY KEY,
    sequenceStartStamp      bigint,
    kickTime        	    bigint,
    T_rev_BPM               integer,
    x_traj                  double precision[],
    y_traj                  double precision[],
    x_orbit                 double precision[],
    y_orbit                 double precision[],
    amp_x                   double precision,
    amp_y                   double precision,
    tune_x                  double precision,
    tune_y                  double precision
);
