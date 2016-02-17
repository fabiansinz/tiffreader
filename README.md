# tiffreader
Python TIFF Stack Reader for ScanImage 4 and 5

### Installation
```shell
git clone https://github.com/atlab/tiffreader.git
pip install tiffreader/
```

### Usage
```python
from tiffreader import TIFFReader
t = TIFFReader('/home/fabee/cache/160208/m7588A_00001_00*.tif')
print(t.nframes)
print(t.fps)
print(t.dwell_time)
print(t.bidirectional)
print(t.fill_fraction)
print(t.nchannels)
print(t.nslices)
print(t.requested_frames)
print(t.scanimage_version)
print(t.shape)
print(t.slice_pitch)
print(t.zoom)

fr = t[:3,:3,:,:,1494:1505] # rows, columns, channels, slices, frames
```

`TIFFReader` supports several files which can be specified via a wildcard or as a list of strings.

`Ellipsis` (the `...` object) is not yet supported for indexing. 

`TIFFReader` needs octave to be installed on the system since ScanImage stores the meta-information as matlab code. Requests to change that in future versions can be submitted [here](http://scanimage.vidriotechnologies.com).

This reader is based on a Matlab [reader](https://github.com/atlab/commons/tree/master/lib/%2Bne7) for ScanImage files in Matlab written by Dimitri Yatsenko. 
