#===============================================================================#
#                        TEMPLATE IMAGING SCRIPT                                #
# ==============================================================================#

# Updated: Wed Apr  8 15:13:30 MDT 2015

#-------------------------------------------------------------------------------#
#                     Data Preparation                                          #
# ------------------------------------------------------------------------------#

########################################
# Check CASA version

import re
import glob

if (re.search('^4.2', casadef.casa_version) or re.search('^4.3', casadef.casa_version))  == None:
 sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.2 or 4.3')

vislist = glob.glob('*.ms.split.cal')
vislist_ms = glob.glob('*.ms')
regridvis = 'source_calibrated_regrid.ms'
finalvis = 'calibrated_final.ms'
gcalfinalvis = 'gcal_calibrated_final.ms'
bpcalfinalvis = 'gcal_calibrated_final.ms'
fcalfinalvis = 'gcal_calibrated_final.ms'
SPW0 = str(range(0, 35, 5)).strip('[]')
SPW1 = str(range(1, 35, 5)).strip('[]')
SPW2 = str(range(2, 35, 5)).strip('[]')
SPW3 = str(range(3, 35, 5)).strip('[]')
SPW4 = str(range(4, 35, 5)).strip('[]')
contspws = SPW4
contvis = 'calibrated_final_cont.ms'
gcalcontvis = 'gcal_calibrated_final_cont.ms'


########################################
# Removing pointing table

# This step removes the pointing table from the data to avoid
# a bug with mosaics in CASA 4.2.2

for vis in vislist:
    tb.open(vis + '/POINTING', nomodify=False)
    a = tb.rownumbers()
    tb.removerows(a)
    tb.close()


###################################
# Splitting off science target data

for vis in vislist:
    listobs(vis=vis, listfile=vis + '.listobs', overwrite=True)

for vis in vislist_ms:
    listobs(vis=vis, listfile=vis + '.listobs', overwrite=True)

# Doing the split
for vis in vislist:
    sourcevis = vis + '.source'
    rmtables(sourcevis)
    os.system('rm -rf ' + sourcevis + '.flagversions')
    split(vis=vis,
          intent='*TARGET*', # split off the target sources
          outputvis=sourcevis,
          datacolumn='data')

for vis in vislist:
    gcalvis = vis + '.gcal'
    rmtables(gcalvis)
    os.system('rm -rf ' + gcalvis + '.flagversions')
    split(vis=vis,
          intent='*PHASE*', # split off the phase calibrators
          outputvis=gcalvis,
          datacolumn='data')

for vis in vislist:
    bpcalvis = vis + '.bpcal'
    rmtables(bpcalvis)
    os.system('rm -rf ' + bpcalvis + '.flagversions')
    split(vis=vis,
          intent='*BANDPASS*', # split off the bandpass calibrators
          outputvis=bpcalvis,
          datacolumn='data')

for vis in vislist:
    fcalvis = vis + '.fcal'
    rmtables(fcalvis)
    os.system('rm -rf ' + fcalvis + '.flagversions')
    split(vis=vis,
          intent='*FLUX*', # split off the flux calibrators
          outputvis=fcalvis,
          datacolumn='data')

    # Check that split worked as desired.
for vis in vislist:
    sourcevis = vis + '.source'
    listobs(vis=sourcevis, listfile=sourcevis + '.listobs', overwrite=True)


###############################################################
# Combining Measurement Sets from Multiple Executions [OPTIONAL]

# Simple concat (spws not combined)
# ---------------------------------
# Ms'es from multiple executions of the same scheduling block can be
# combined into one ms using concat. In this case, you will end up
# with a single ms with n spws, where n is (#original science spws) x
# (number executions). The multiple spws associated with a single
# frequency will not be regridded to a single spectral window in the
# ms. However, they can be regridded to a single spectral window
# later during cleaning.

sourcevislist = glob.glob("*.ms.split.cal.source")
regridvis = 'source_calibrated_regrid.ms'
rmtables(regridvis)
os.system('rm -rf ' + regridvis + '.flagversions')
concat(vis=sourcevislist, concatvis=regridvis) 
listobs(vis=regridvis, listfile=regridvis+'.listobs')

# Rename and backup data set

os.system('mv -i ' + regridvis + ' ' + 'calibrated_final.ms')
os.system('mv -i ' + regridvis + '.listobs calibrated_final.ms.listobs')

os.system('cp -ir calibrated_final.ms calibrated_final.ms.backup')

finalvis = 'calibrated_final.ms'

# Data sets of calibrators, just in case

gcalvislist = glob.glob("*.ms.split.cal.gcal")
gcalfinalvis = 'gcal_calibrated_final.ms'
rmtables(gcalfinalvis)
os.system('rm -rf ' + gcalfinalvis + '.flagversions')
concat(vis=gcalvislist, concatvis=gcalfinalvis) 
listobs(vis=gcalfinalvis, listfile=gcalfinalvis+'.listobs')

bpcalvislist = glob.glob("*.ms.split.cal.bpcal")
bpcalfinalvis = 'bpcal_calibrated_final.ms'
rmtables(bpcalfinalvis)
os.system('rm -rf ' + bpcalfinalvis + '.flagversions')
concat(vis=bpcalvislist, concatvis=bpcalfinalvis) 
listobs(vis=bpcalfinalvis, listfile=bpcalfinalvis+'.listobs')

fcalvislist = glob.glob("*.ms.split.cal.fcal")
fcalfinalvis = 'fcal_calibrated_final.ms'
rmtables(fcalfinalvis)
os.system('rm -rf ' + fcalfinalvis + '.flagversions')
concat(vis=fcalvislist, concatvis=fcalfinalvis) 
listobs(vis=fcalfinalvis, listfile=fcalfinalvis+'.listobs')


############################################
# Identify Line-free SPWs and channels

# Define some convenience variables; lists of SPWs that make up each of the SPWs
# from the OT that can be passed into CASA tasks
SPW0 = str(range(0, 35, 5)).strip('[]')
SPW1 = str(range(1, 35, 5)).strip('[]')
SPW2 = str(range(2, 35, 5)).strip('[]')
SPW3 = str(range(3, 35, 5)).strip('[]')
SPW4 = str(range(4, 35, 5)).strip('[]')

#plot visibility spectra and iterate over pointings
plotms(vis=finalvis, spw=SPW0, xaxis='velocity', yaxis='amplitude',
       ydatacolumn='data', avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='field', coloraxis='corr', transform=True, freqframe='LSRK',
       restfreq='90979.02MHz', veldef='RADIO', plotrange=[-20, 40, 0, 10])

plotms(vis=finalvis, spw=SPW1, xaxis='velocity', yaxis='amplitude',
       ydatacolumn='data', avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='field', coloraxis='corr', transform=True, freqframe='LSRK',
       restfreq='90663.56MHz', veldef='RADIO', plotrange=[-20, 40, 0, 25])

plotms(vis=finalvis, spw=SPW2, xaxis='velocity', yaxis='amplitude',
       ydatacolumn='data', avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='field', coloraxis='corr', transform=True, freqframe='LSRK',
       restfreq='91980.00MHz', veldef='RADIO', plotrange=[-20, 40, 0, 10])

plotms(vis=finalvis, spw=SPW3, xaxis='velocity', yaxis='amplitude',
       ydatacolumn='data', avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='field', coloraxis='corr', transform=True, freqframe='LSRK',
       restfreq='93173.40MHz', veldef='RADIO', plotrange=[-20, 40, 0, 25])

plotms(vis=finalvis, spw=SPW4, xaxis='velocity', yaxis='amplitude',
       ydatacolumn='data', avgtime='1e8', avgscan=True, avgchannel='2',
       iteraxis='field', coloraxis='corr', transform=True, freqframe='LSRK',
       restfreq='92000.00MHz', veldef='RADIO')


##################################################
# Create an Averaged Continuum MS

# Continuum images can be sped up considerably by averaging the data
# together to reduce overall volume.

# Average channels within continuum SPW

contspws = SPW4
contvis = 'calibrated_final_cont.ms'
rmtables(contvis)
os.system('rm -rf ' + contvis + '.flagversions')
split(vis=finalvis,
      spw=contspws,
      outputvis=contvis,
      width=[128]*7,
      datacolumn='data')
listobs(vis=contvis, listfile=contvis+'.listobs', overwrite=True)

gcalcontvis = 'gcal_calibrated_final_cont.ms'
rmtables(gcalcontvis)
os.system('rm -rf ' + gcalcontvis + '.flagversions')
split(vis=gcalfinalvis,
      spw=contspws,
      outputvis=gcalcontvis,
      width=[128]*7,
      datacolumn='data')
listobs(vis=gcalcontvis, listfile=gcalcontvis+'.listobs', overwrite=True)


#############################################
# Imaging the Continuuum

# Image Parameters

# Generally, you want 5-8 cells (i.e., pixels) across the narrowest
# part of the beam, which is 206265.0/(longest baseline in
# wavelengths).  You can use plotms with xaxis='uvwave' and
# yaxis='amp' to see what the longest baseline is. Divide by five to
# eight to get your cell size. It's better to err on the side of
# slightly too many cells per beam than too few. Once you have made an
# image, please re-assess the cell size based on the beam of the
# image.

# To determine the image size (i.e., the imsize parameter), you need
# to determine whether or not the ms is a mosaic by either looking out
# the output from listobs or checking the spatial setup in the OT. For
# single fields, the imsize should be about the size of the primary
# beam. The ALMA 12m primary beam in arcsec scales as 6300 / nu[GHz]
# and the ALMA 7m primary beam in arcsec scales as 10608 / nu[GHz]. For
# mosaics, you can get the imsize from the spatial tab of
# the OT. If you're imaging a mosaic, pad the imsize substantially to
# avoid artifacts.

# The cleaning below is done interactively, so niter and threshold can
# be controlled within clean.

field = '4~14' # For a mosaic, select all mosaic fields. DO NOT LEAVE BLANK ('') OR YOU WILL TRIGGER A BUG IN CLEAN THAT WILL PUT THE WRONG COORDINATE SYSTEM ON YOUR FINAL IMAGE.
imagermode = 'mosaic' # uncomment if mosaic
phasecenter = 10
cell = '0.4arcsec'
imsize = [1400, 1400] # size of image in pixels.
weighting = 'briggs'
robust = 0.5
niter = 1000
threshold = '0.0mJy'

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=contvis)
#delmod(vis=contvis)

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an optional step.
#contmaskname = 'cont.mask'
##rmtables(contmaskname) # if you want to delete the old mask
#os.system('cp -ir ' + contimagename + '.mask ' + contmaskname)

# try interactive imaging
# gcal_calibrated_final_cont_image_0
# calibrated_final_cont_image_0

# for phase calibrator
gcalcontimagename = 'gcal_calibrated_final_cont_image_0'
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(gcalcontimagename+ext)

clean(vis=gcalcontvis,
      imagename=gcalcontimagename,
      field='2',
      phasecenter='2',
      mode='mfs',
      psfmode='clark',
      imsize=imsize,
      cell=cell,
      weighting=weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True)

# for the source
contimagename = 'calibrated_final_cont_image_0'
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename+ext)

clean(vis=contvis,
      imagename=contimagename,
      field=field,
      phasecenter=phasecenter,
      mode='mfs',
      psfmode='clark',
      imsize=imsize,
      cell=cell,
      weighting=weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)

# Ran 600 iterations with included calibrated_final_cont_image.mask
# RMS: 55 microJy
# Beam size: 3.47" x 2.05"

# try non-interactive imaging
# calibrated_final_cont_image_1

contimagename = 'calibrated_final_cont_image_1'
for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(contimagename+ext)

clean(vis=contvis,
      imagename=contimagename,
      field=field,
      phasecenter=phasecenter,
      mode='mfs',
      psfmode='clark',
      imsize=imsize,
      cell=cell,
      weighting=weighting,
      robust=robust,
      niter=niter,
      threshold=threshold,
      interactive=True,
      imagermode=imagermode)


########################################
# Continuum Subtraction for Line Imaging

# If you have observations that include both line and strong (>3 sigma
# per final line image channel) continuum emission, you need to
# subtract the continuum from the line data. You should not continuum
# subtract if the line of interest is in absorption.

# do continuum subtraction on each individual EB first to avoid a segmentation
# fault bug in CASA 4.2.2 uvcontsub
fitspw = '0:0~485;520~959,' + \
         '1:0~470;520~959,' + \
         '2,' + \
         '3:0~880;1090~1919,' + \
         '4'
linespw = '0,1,3' #skip SPW 2 because no obvious line in plotms
for vis in sourcevislist:
    uvcontsub(vis=vis,
              spw=linespw,
              fitspw=fitspw,
              combine='spw',
              solint='int',
              fitorder=1,
              want_cont=False)
linevis = finalvis + '.contsub'
rmtables(linevis)
os.system('rm -rf ' + linevis + '.flagversions')
contsubvislist = glob.glob('*.contsub')
concat(vis=contsubvislist, concatvis=linevis)
listobs(vis=linevis, listfile=linevis+'.listobs')
rmtables(contsubvislist)

# NOTE: Imaging the continuum produced by uvcontsub with
# want_cont=True will lead to extremely poor continuum images because
# of bandwidth smearing effects. For imaging the continuum, you should
# always create a line-free continuum data set using the process
# outlined above.

##############################################
# Image line emission

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=linevis)
#delmod(vis=linevis)

# velocity parameters
# -------------------

lineimagename = 'source_contsub_SPW0'

start = '0km/s'
nchan = 100
outframe = 'lsrk'
veltype = 'radio'
restfreq = '90.97902GHz'
spw = str(range(0, 21, 3)).strip('[]') # SPW 0

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw=spw,
      phasecenter=phasecenter,
      mode='velocity',
      start=start,
      nchan=nchan,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

# Beam size: 3.51" x 2.08"
# RMS: 6 mJy
# Ran 3300 iterations with included source_contsub_SPW0.mask

# If you'd like to redo your clean, but don't want to make a new mask
# use the following commands to save your original mask. This is an
# optional step.
# linemaskname = 'line.mask'
## rmtables(linemaskname) # uncomment if you want to overwrite the mask.
# os.system('cp -ir ' + lineimagename + '.mask ' + linemaskname)

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=linevis)
#delmod(vis=linevis)

# velocity parameters
# -------------------

lineimagename = 'source_contsub_SPW1'

start = '0km/s'
nchan = 100
outframe = 'lsrk'
veltype = 'radio'
restfreq = '90.66356GHz'
spw = str(range(1, 21, 3)).strip('[]') # SPW 1

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw=spw,
      phasecenter=phasecenter,
      mode='velocity',
      start=start,
      nchan=nchan,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

# Beam size: 3.52" x 2.08"
# RMS: 5.6 mJy
# Ran 4400 iterations with included source_contsub_SPW1.mask

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=finalvis)
#delmod(vis=finalvis)

# velocity parameters
# -------------------

lineimagename = 'source_no_contsub_SPW2'

start = '0km/s'
nchan = 100
width = '0.15km/s'
outframe = 'lsrk'
veltype = 'radio'
restfreq = '91.98000GHz'
spw = str(range(2, 35, 5)).strip('[]') # SPW 2

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=finalvis, #using non-contsub because no obvious line emission in plotms
      imagename=lineimagename,
      field=field,
      spw=spw,
      phasecenter=phasecenter,
      mode='velocity',
      start=start,
      nchan=nchan,
      width=width,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

# Beam size: 3.47" x 2.05"
# RMS: 7.5 mJy
# Ran 100 iterations with included source_contsub_SPW2.mask

# If necessary, run the following commands to get rid of older clean
# data.

#clearcal(vis=linevis)
#delmod(vis=linevis)

# velocity parameters
# -------------------

lineimagename = 'source_contsub_SPW3'

start = '-10km/s'
nchan = 234
width = '0.15km/s'
outframe = 'lsrk'
veltype = 'radio'
restfreq = '93.17340GHz'
spw = str(range(2, 21, 3)).strip('[]') # SPW 3

for ext in ['.flux','.image','.mask','.model','.pbcor','.psf','.residual','.flux.pbcoverage']:
    rmtables(lineimagename + ext)

clean(vis=linevis,
      imagename=lineimagename,
      field=field,
      spw=spw,
      phasecenter=phasecenter,
      mode='velocity',
      start=start,
      nchan=nchan,
      width=width,
      outframe=outframe,
      veltype=veltype,
      restfreq=restfreq,
      niter=niter,
      threshold=threshold,
      interactive=True,
      cell=cell,
      imsize=imsize,
      weighting=weighting,
      robust=robust,
      imagermode=imagermode,
      usescratch=True)

# Beam size: 3.44" x 2.02"
# RMS: 7.4 mJy
# Ran 2300 iterations with included source_contsub_SPW3.mask
##############################################
# Apply a primary beam correction

myimages = glob.glob("*.image")

rmtables('*.pbcor')
for image in myimages:
    impbcor(imagename=image, pbimage=image.replace('.image','.flux'), outfile = image.replace('.image','.pbcor'))

##############################################
# Export the images

myimages = glob.glob("*.image")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

myimages = glob.glob("*.pbcor")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

myimages = glob.glob("*.flux")
for image in myimages:
    exportfits(imagename=image, fitsimage=image+'.fits',overwrite=True)

##############################################
# Analysis

# For examples of how to get started analyzing your data, see
#     http://casaguides.nrao.edu/index.php?title=TWHydraBand7_Imaging_4.2
