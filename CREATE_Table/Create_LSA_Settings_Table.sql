CREATE TABLE bpm_fesa_dump.lsa_settings (
    SIS18BEAM_QH		real[],
    SIS18BEAM_QV		real[],
    SIS18BEAM_CH		real[],
    SIS18BEAM_CV		real[],
    SIS18BEAM_BRHO		real[],
    SIS18BEAM_DPFREV		real[],
    SIS18BEAM_TREV		real[],
    LOGICAL_GS02BE1_URF		real[],
    SIS18OPTICS_SIGMA		real[],
    SIS18OPTICS_TAU		real[],
    LOGICAL_GS01QS1F_K1L		real[],
    LOGICAL_GS01QS2D_K1L		real[],
    LOGICAL_GS12QS1F_K1L		real[],
    LOGICAL_GS12QS2D_K1L		real[],
    LOGICAL_GS12QS3T_K1L		real[],
    LOGICAL_GS02KQ1E_K1L		real[],
    LOGICAL_GS01KM3QS_K1L		real[],
    LOGICAL_GS02KM3QS_K1L		real[],
    LOGICAL_GS04KM3QS_K1L		real[],
    LOGICAL_GS06KM3QS_K1L		real[],
    LOGICAL_GS07KM3QS_K1L		real[],
    LOGICAL_GS08KM3QS_K1L		real[],
    LOGICAL_GS10KM3QS_K1L		real[],
    LOGICAL_GS12KM3QS_K1L		real[],
    LOGICAL_GS02KQ4_K1L		real[],
    LOGICAL_GS04KQ4_K1L		real[],
    LOGICAL_GS08KQ4_K1L		real[],
    LOGICAL_GS10KQ4_K1L		real[],
    LOGICAL_GS01KS1C_K2L		real[],
    LOGICAL_GS03KS1C_K2L		real[],
    LOGICAL_GS05KS1C_K2L		real[],
    LOGICAL_GS07KS1C_K2L		real[],
    LOGICAL_GS09KS1C_K2L		real[],
    LOGICAL_GS11KS1C_K2L		real[],
    LOGICAL_GS01KS3C_K2L		real[],
    LOGICAL_GS03KS3C_K2L		real[],
    LOGICAL_GS05KS3C_K2L		real[],
    LOGICAL_GS07KS3C_K2L		real[],
    LOGICAL_GS09KS3C_K2L		real[],
    LOGICAL_GS11KS3C_K2L		real[],
    LOGICAL_GS02KM5SS_K2L		real[],
    LOGICAL_GS08KM5SS_K2L		real[],
    pattern				        text,
    sequenceIndex			    integer,
    sequenceStartStamp			bigint  PRIMARY KEY
);
