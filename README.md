# HIRISE Blender

Source code for the HIRISE Blender add-on.

## Installation
Download the .zip from the [releases](https://github.com/dcellucci/hirise-blender/releases/) and install as you would a [typical Blender add-on](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons)

## Testing
Find yourself a cool, mega-detailed HIRISE DTM file and download it (I like [this one](https://www.uahirise.org/dtm/PSP_001981_1825))

Select `File -> Import -> HIRISE .IMG` and select your file. 

## Enjoy

Enjoy your new detailed mesh of Mars!
![Success](media/hirise_success.png)

## Import Options
There are a few options to note

### Pixels Per Grid Square
This effectively downsamples the original IMG file when creating the mesh. A single grid square in the mesh will correspond to this many pixels in the original data.

Note that this will directly relate to import time and memory usage. **Going below 4 PPGS might cause a memory error so that's why we have the safety option below**

### Safety
You must check the safety box if you select a PPGS below 4. This is for the best. 

### Quads
Select quads or tris for the mesh face. Defaults to quads.