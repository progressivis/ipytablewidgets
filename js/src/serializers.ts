// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import ndarray = require('ndarray');
import { decompress } from "./compression";
type NdArray =  ndarray.NdArray;

import {
  WidgetModel, ManagerBase
} from '@jupyter-widgets/base';

export
interface IReceivedSerializedArray {
  shape: number[];
  dtype: "int8"|"int16"|"int32"|"uint8"|"uint16"|"uint32"|"float32"|"float64"|"str";
  buffer: DataView | string[];
  compression?: string;
}

const dtypeToArray = {
    int8: Int8Array,
    int16: Int16Array,
    int32: Int32Array,
    uint8: Uint8Array,
    uint16: Uint16Array,
    uint32: Uint32Array,
    float32: Float32Array,
    float64: Float64Array,
    str: Array
}

const RowIndex = Symbol('rowIndex');

export
interface IDict<T> {
    [Key: string]: T;
}


/**
 * The serialized representation of a received Table (i.e. dataframe)
 */
export
interface IReceivedSerializedTable {
  columns: string[];
  data: IDict<IReceivedSerializedArray>;
}

export
interface ISendSerializedTable {
  columns: string[];
  data: IDict<NdArray | string[]>;
  size: number;
}

export
function JSONToTable(obj: IReceivedSerializedTable | null, manager?: ManagerBase<any>): ISendSerializedTable | null {
  if (obj === null) {
    return null;
  }
  var data: IDict<NdArray | string[]> = {};
  var size: number = Infinity;
  let decoder = new TextDecoder("utf-8");
  let buffer: ArrayBuffer;
  for (const [col, val] of Object.entries(obj.data)) {
      // console.log(col, val);
      if(val.compression !== undefined){
        let valBuffer = val.buffer as DataView;
        buffer = decompress[val.compression](valBuffer.buffer);
	if(val.dtype==="str"){
	   let u8buf = buffer as Uint8Array;
	   let strcol = decoder.decode(u8buf);
	   let lstr: string[] = JSON.parse(strcol) as string[];
	   data[col] = lstr;
	} else { //numeric
	   data[col] = ndarray(new dtypeToArray[val.dtype](buffer), val.shape)
           size = Math.min(size, val.shape[0]);
	}
      } else { // no compression
        if(val.dtype==="str"){
           let lstr: string[] = val.buffer as string[];
           data[col] = lstr;
	   size = Math.min(size, lstr.length);
        } else { //numeric
	   let valBuffer = val.buffer as DataView;
           data[col] = ndarray(new dtypeToArray[val.dtype](valBuffer.buffer),
	                                                  val.shape)
           size = Math.min(size, val.shape[0]);
        }
     }
  }
  var result = {columns: obj.columns, data: data, size: size} as ISendSerializedTable;
  // console.log("result", result);
  //let objFoo = obj.data.foo;
  return result;
}

export
function rowProxy(table: ISendSerializedTable|null):any {
    if (table === null) {
        return null;
    }
    var fields: string[] = table.columns;
    var proto: any = {};

    fields.forEach((name: string) => {
        const column: NdArray | string[] = table.data[name];
        const arraycolumn = column as NdArray;
        const stringcolumn = column as string[];

        // skip columns with duplicate names
        if (proto.hasOwnProperty(name)) return;

        if (arraycolumn.shape===undefined) {
            Object.defineProperty(proto, name, {
                get: function():any {
                    const i:number = (this[RowIndex] as number)
                    return stringcolumn[i];
                },
                set: function() {
                    throw Error('Arrow field values can not be overwritten.');
                },
                enumerable: true
            });
        }
        else {
            Object.defineProperty(proto, name, {
                get: function():any {
                    const i:number = (this[RowIndex] as number)
                    return arraycolumn.get(i);
                },
                set: function() {
                    throw Error('Arrow field values can not be overwritten.');
                },
                enumerable: true
            });
        }
    });
    return (i: number):any  => {
        var r:any = Object.create(proto);
        r[RowIndex] = i;
        return r;
    };
}


export
function tableToJSON(obj: IDict<NdArray>| null, widget?: WidgetModel): ISendSerializedTable | null {

  return null; // TODO: implement or remove ...
}

/**
 * Serializers for to/from tables/dataframes
 */
export
const table_serialization = { deserialize: JSONToTable, serialize: tableToJSON };
