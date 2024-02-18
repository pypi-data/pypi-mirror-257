from typing import Sequence
from zipfile import ZipFile
from pathlib import Path
from shutil import rmtree
import subprocess

from PIL import Image

from .far4_tools import pack_to_mod
from .tex_tools import image2tex
from .mod_installer import get_sha1_hex, JSONINATOR_ARGS


_PHOTO_PLAN_TEMPLATE = '{"revision":626,"branch":{"id":"LD","revision":23},"type":"PLAN","resource":{"things":[{"UID":2,"planGUID":null,"parent":null,"group":null,"PBody":{"posVel":[0,0,0],"angVel":0,"frozen":0,"editingPlayer":null},"PPos":{"thingOfWhichIAmABone":null,"animHash":0,"localPosition":{"translation":[0,0,0],"rotation":[0,0,0,1],"scale":[1,1,1]},"worldPosition":{"translation":[0,0,0],"rotation":[0,0,0,1],"scale":[1,1,1]}},"PGeneratedMesh":{"gfxMaterial":{"value":11166,"type":"GFX_MATERIAL"},"bevel":null,"uvOffset":[0,0,0,0],"planGUID":null},"PStickers":{"decals":[{"texture":{"value":"139e05debc12f306fea45b810b5a0a467534915c","type":"TEXTURE"},"u":0,"v":1,"xvecu":0.64,"xvecv":0,"yvecu":0,"yvecv":0.36,"color":-1,"type":"STICKER","metadataIndex":-1,"numMetadata":0,"placedBy":-1,"playModeFrame":0,"scorchMark":false,"plan":null}],"costumeDecals":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]],"paintControl":[],"eyetoyData":[]},"PShape":{"polygon":{"vertices":[[-320,180,0],[320,180,0],[320,-180,0],[-320,-180,0]],"loops":[4]},"material":{"value":717,"type":"MATERIAL"},"oldMaterial":null,"thickness":0.01,"massDepth":0.2,"color":-11711155,"bevelSize":0.01,"interactPlayMode":0,"interactEditMode":0,"lethalType":"NOT","soundEnumOverride":"NONE","flags":7},"PGroup":{"planDescriptor":null,"creator":"USERNAME_HERE","emitter":null,"lifetime":0,"aliveFrames":0,"flags":0}}],"inventoryData":{"dateAdded":0,"levelUnlockSlotID":"NONE","highlightSound":null,"colour":-1,"type":["STICKER","USER_STICKER"],"subType":0,"titleKey":0,"descriptionKey":0,"userCreatedDetails":{"name":"ENTER_IMAGENAME_HERE","description":""},"creationHistory":["USERNAME_HERE"],"icon":{"value":"139e05debc12f306fea45b810b5a0a467534915c","type":"TEXTURE"},"photoData":{"icon":{"value":"139e05debc12f306fea45b810b5a0a467534915c","type":"TEXTURE"},"sticker":{"value":"139e05debc12f306fea45b810b5a0a467534915c","type":"TEXTURE"},"photoMetadata":{"photo":{"value":"139e05debc12f306fea45b810b5a0a467534915c","type":"TEXTURE"},"level":"POD:0","levelName":"","levelHash":"0d4b36e05ba1cf1427e282c56939a3781c6a865c","users":[],"timestamp":3413563468}},"eyetoyData":null,"locationIndex":-1,"categoryIndex":-1,"primaryIndex":0,"lastUsed":0,"numUses":0,"fluffCost":0,"allowEmit":false,"shareable":false,"copyright":false,"creator":"USERNAME_HERE","toolType":"NONE","location":0,"category":4126835505}}}'

def images_to_mod(the_images: Sequence[Path], output_mod: ZipFile, username: str = 'Zhaxxy', is_shareable: bool = True):
    my_image_template = _PHOTO_PLAN_TEMPLATE.replace('USERNAME_HERE',username).replace('"shareable":false','"shareable":true' if is_shareable else '"shareable":false')
    temp_folder = Path('the_images_mod_dumps_3467')
    temp_folder.mkdir()
    try:
        for image in the_images:
            if not image.is_file(): continue
            with Image.open(image) as img:
                with open(temp_folder / image.stem, 'wb') as f:
                    tex_data = image2tex(img)
                    tex_sha1 = get_sha1_hex(tex_data)
                    f.write(tex_data)
            photo_json = my_image_template.replace('ENTER_IMAGENAME_HERE',image.stem).replace('139e05debc12f306fea45b810b5a0a467534915c',tex_sha1)
            photo_temp_json_file = temp_folder / (image.stem + '.json')
            photo_temp_json_file.write_text(photo_json)
            photo_new_plan = temp_folder / (image.stem + '.plan')

            subprocess.run(JSONINATOR_ARGS + (photo_temp_json_file,photo_new_plan), capture_output = True, shell=False)

            photo_temp_json_file.unlink()

        pack_to_mod(temp_folder,output_mod)
    finally:
        rmtree(temp_folder)