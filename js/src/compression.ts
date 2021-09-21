// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import pako = require('pako');
import lz4 = require("lz4js");
export
const decompress : {[key:string]: Function} = {
      zlib: (input: ArrayBuffer): ArrayBuffer => {
           return pako.inflate(new Uint8Array(input)).buffer;
         },
      lz4: (input: ArrayBuffer): ArrayBuffer => {
          return lz4.decompress(new Uint8Array(input)).buffer;
         },

}