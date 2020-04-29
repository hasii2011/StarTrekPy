#!/bin/bash

export DIR=StarTrek.iconset

mkdir ${DIR}

sips -z 16 16 StarTrek.png  --out ${DIR}/icon_16x16.png

sips -z 32 32 StarTrek.png  --out ${DIR}/icon_16x16@2x.png
sips -z 32 32 StarTrek.png  --out ${DIR}/icon_32x32.png

sips -z 64 64 StarTrek.png  --out ${DIR}/icon_32x32@2x.png

sips -z 128 128 StarTrek.png  --out ${DIR}/icon_128x128.png

sips -z 256 256 StarTrek.png  --out ${DIR}/icon_128x128@x2.png
sips -z 256 256 StarTrek.png  --out ${DIR}/icon_256x256.png

sips -z 512 512 StarTrek.png  --out ${DIR}/icon_256x256@2x.png
sips -z 512 512 StarTrek.png  --out ${DIR}/icon_512x512.png

sips -z 1024 1024 StarTrek.png --out ${DIR}/icon_512x512@2x.png

iconutil -c icns StarTrek.iconset