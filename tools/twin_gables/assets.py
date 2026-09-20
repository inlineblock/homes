"""Actual pinned collection/material adoption; no asset publication side effects."""
import json
from pathlib import Path
import bpy
from common.library import linked_collection,instance
ROOT=Path(__file__).resolve().parents[2]
PINS={};CACHE={}
def asset(category,slug,version='v001'):
 key=f'{category}/{slug}';PINS[key]=version
 if (key,version) not in CACHE:CACHE[key,version]=linked_collection(ROOT,category,slug,version)
 return CACHE[key,version]
def material(slug,version='v001'):
 key='materials/'+slug;PINS[key]=version
 if (key,version) not in CACHE:
  p=ROOT/'library'/key/version/f'{slug}.blend'
  with bpy.data.libraries.load(str(p),link=True) as (a,b):b.materials=[a.materials[0]]
  CACHE[key,version]=b.materials[0]
 return CACHE[key,version]
def put(name,category,slug,loc,rotation=0,version='v001',scale=1):
 o=instance(name,asset(category,slug,version),loc,rotation,scale)
 o['shared_asset_id']=category+'/'+slug;o['shared_asset_version']=version
 return o
