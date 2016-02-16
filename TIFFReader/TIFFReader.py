from tifffile import TiffFile
from glob import glob
import os
from oct2py import Oct2Py
import re
from . import VersionNumberException

si4 = re.compile("""^scanimage\.SI4\.(?P<attr>\w*)\s*=\s*(?P<value>.*\S)\s*$""")
si5 = re.compile("""^scanimage\.SI\.(?P<attr>[\.\w]*)\s*=\s*(?P<value>.*\S)\s*$""")


def get_scanimage_version_and_header(hdr):
    o2p = Oct2Py()

    tmp = [si4.match(s) for s in hdr if si4.match(s) is not None]
    if len(tmp) > 0:
        version = 4
        hdr = {g['attr']: g['value'] for g in map(lambda x: x.groupdict(), tmp)}
    else:
        tmp = [si5.match(s) for s in hdr if si5.match(s) is not None]
        version = 5
        hdr = {g['attr']: g['value'] for g in map(lambda x: x.groupdict(), tmp)}
    if len(hdr) == 0:
        raise VersionNumberException("Cannot find header information. Possibly wrong scanimage version")

    hdr_ret = {}
    for k, v in hdr.items():
        if not v[0] == "<" and not v[-1] == '>':
            hdr_ret[k.replace('.', '_')] = o2p.eval(v, verbose=False)
    return version, hdr_ret


class TIFFReader:
    def __init__(self, wildcard):
        self._files = sorted(map(os.path.abspath, glob(wildcard)), key=lambda x: x.split('/')[-1])
        self._stacks = [TiffFile(file) for file in self._files]
        self.load_header()
        # ----------------------------------
        # TODO: Remove this later
        from IPython import embed
        embed()
        exit()
        # ----------------------------------

    def load_header(self):
        first_frame = self._stacks[0].pages[0]
        hdr = [s.strip() for s in first_frame.tags['image_description'].value.decode('utf-8').split('\n')]
        self.scanimage_version, self.header = get_scanimage_version_and_header(hdr)

    @property
    def channels(self):
        ret = self.header['channelsSave'] if self.scanimage_version == 4 else self.header['hChannels_channelSave']
        return ret.squeeze()

    @property
    def nslices(self):
        return int(self.header['stackNumSlices'] if self.scanimage_version == 4 else self.header[
            'hFastZ_numFramesPerVolume'])

    @property
    def fill_fraction(self):
        return self.header['scanFillFraction'] if self.scanimage_version == 4 else self.header[
            'hScan2D_fillFractionTemporal']

    @property
    def fps(self):
        if self.scanimage_version == 4:
            if self.header['fastZactive']:
                fps = 1/self.header['fastZPeriod']
            else:
                assert self.nslices == 1
                fps = self.header['scanFrameRate']
        else:
            if self.nslices >= 1:
                fps = self.header['hRoiManager_scanVolumeRate']
            else:
                fps = self.header['hRoiManager_scanFrameRate']
        return fps


    @property
    def slice_pitch(self):
        if self.scanimage_version == 4:
            if self.header['fastZActive']:
                p = self.header['stackZStepSize']
            else:
                p = 0
        else:
            p = self.header['hStackManager_stackZStepSize']

        return p

    @property
    def requested_frames(self):
        if self.scanimage_version == 4:
            if self.header['fastZActive']:
                n = self.header['fastZNumVolumes']
            else:
                n = self.header['acqNumFrames']
        else:
            n = self.header['hFastZ_numVolumes']
        return int(n)


    @property
    def nframes(self):
        #----------------------------------
        # TODO: Remove this later
        from IPython import embed
        embed()
        # exit()
        #----------------------------------

        #return self.header[''] if self.scanimage_version == 4 else self.header['']

    @property
    def bidirectional(self):
        return bool(self.header['scanMode'] == 'uni' if self.scanimage_version == 4
                            else self.header['hScan2D_bidirectional'])

    @property
    def dwell_time(self):
        return self.header['scanPixelTimeMean']*1e6 if self.scanimage_version == 4 \
                                            else self.header['hScan2D_scanPixelTimeMean']*1e6

    @property
    def nchannels(self):
        return len(self.channels)

    @property
    def zoom(self):
        return self.header['scanZoomFactor'] if self.scanimage_version == 4 \
                                            else self.header['hRoiManager_scanZoomFactor']

    @property
    def shape(self):
        #----------------------------------
        # TODO: Remove this later
        from IPython import embed
        embed()
        # exit()
        #----------------------------------

    @property
    def frames_per_slice(self):
        assert self.scanimage_version == 5
        return int(self.header['hStackManager_framesPerSlice'])

    @property
    def slice_per_acq(self):
        assert self.scanimage_version == 5
        return int(self.header['hStackManager_slicesPerAcq'])


