from recipes.almahelpers import fixsyscaltimes # SACM/JAO - Fixes
__rethrow_casa_exceptions = True
h_init()
try:
    hifa_importdata(vis=['uid___A002_X9998b8_Xee3', 'uid___A002_X9998b8_X11eb', 'uid___A002_X9a3e71_Xffc', 'uid___A002_X9a3e71_X1256', 'uid___A002_X9a3e71_X15ca', 'uid___A002_X9a3e71_X1839', 'uid___A002_X9aca45_Xf3f'], session=['session_1', 'session_2', 'session_3', 'session_3', 'session_4', 'session_4', 'session_5'])
    fixsyscaltimes(vis = 'uid___A002_X9998b8_Xee3.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9998b8_X11eb.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9a3e71_Xffc.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9a3e71_X1256.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9a3e71_X15ca.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9a3e71_X1839.ms')# SACM/JAO - Fixes
    fixsyscaltimes(vis = 'uid___A002_X9aca45_Xf3f.ms')# SACM/JAO - Fixes
    h_save() # SACM/JAO - Finish weblog after fixes
    h_init() # SACM/JAO - Restart weblog after fixes
    hifa_importdata(vis=['uid___A002_X9998b8_Xee3', 'uid___A002_X9998b8_X11eb', 'uid___A002_X9a3e71_Xffc', 'uid___A002_X9a3e71_X1256', 'uid___A002_X9a3e71_X15ca', 'uid___A002_X9a3e71_X1839', 'uid___A002_X9aca45_Xf3f'], session=['session_1', 'session_2', 'session_3', 'session_3', 'session_4', 'session_4', 'session_5'])
    hifa_flagdata(pipelinemode="automatic")
    hifa_fluxcalflag(pipelinemode="automatic")
    hif_refant(pipelinemode="automatic")
    hifa_tsyscal(pipelinemode="automatic")
    hifa_tsysflag(pipelinemode="automatic")
    hifa_wvrgcalflag(pipelinemode="automatic")
    hif_lowgainflag(pipelinemode="automatic")
    hif_setjy(pipelinemode="automatic")
    hif_bandpass(pipelinemode="automatic")
    hif_bpflagchans(pipelinemode="automatic")
    hifa_gfluxscale(pipelinemode="automatic")
    hifa_timegaincal(pipelinemode="automatic")
    hif_applycal(pipelinemode="automatic")
    hif_makecleanlist(intent='PHASE,BANDPASS,CHECK')
    hif_cleanlist(pipelinemode="automatic")
finally:
    h_save()
