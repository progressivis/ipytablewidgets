import pako = require('pako');
import lz4 = require("lz4js");

import { assert } from 'chai'; 
import { IReceivedSerializedArray, IDict, IReceivedSerializedTable,
       ISendSerializedTable, tableToJSON,  JSONToTable } from '../serializers';

const SIZE = 64;

const OFFSET0 = 0;
const OFFSET15 = SIZE - 4;
const HEXA = "0123456789ABCDEF"

var dv1 = new DataView(new ArrayBuffer(SIZE));
dv1.setInt32(OFFSET0, 42, true);
dv1.setInt32(OFFSET15, 1981, true);

var sa1: IReceivedSerializedArray  = {'shape': [16], 'dtype': 'int32', 'buffer': dv1};
var sa2: IReceivedSerializedArray = {'shape': [16], 'dtype': 'str', 'buffer': HEXA.split('')};
var tdict: IDict<IReceivedSerializedArray> = {'a': sa1, 'b': sa2};
var table: IReceivedSerializedTable  = {'columns': ['a', 'b'], 'data': tdict};

var dv1Lz4 = lz4.compress(new Uint8Array(dv1.buffer));
var sa1Lz4: IReceivedSerializedArray  = {'shape': [16], 'dtype': 'int32', 'buffer': dv1Lz4, 'compression': 'lz4'};
var strCol = JSON.stringify(HEXA.split(''));
var enc = new TextEncoder(); 
var dv2Lz4 = new  DataView(lz4.compress(enc.encode(strCol)).buffer);
var sa2Lz4: IReceivedSerializedArray = {'shape': [16], 'dtype': 'str',
    	    			     'buffer': dv2Lz4, 'compression': 'lz4'};
var tdictLz4: IDict<IReceivedSerializedArray> = {'a': sa1Lz4, 'b': sa2Lz4};
var tableLz4: IReceivedSerializedTable  = {'columns': ['a', 'b'], 'data': tdictLz4};

// https://www.meziantou.net/test-javascript-code-using-karma-mocha-chai-and-headless-browsers.htm

describe('serializers', function () {
    describe('#tableToJSON()', function () {
        it('should return null', function () {
            assert.equal(null, tableToJSON(null));
        });

    });
    describe('#JSONToTable()', function () {
        it('should return null', function () {
            assert.equal(null, JSONToTable(null));
        });

    });
    describe('#JSONToTable()', function () {
        it('expected a[0]==42, a[15]==1981, b[0]=="0" and b[15]=="F"', function () {
	    let tbl: any = JSONToTable(table);
	    assert.equal(tbl.data['a'].size, 16);
	    assert.deepEqual(tbl.data['a'].shape, [16]);
	    assert.equal(tbl.data['a'].dtype, 'int32');	    
            assert.equal(tbl.data['a'].get(0), 42);
            assert.equal(tbl.data['a'].get(15), 1981);	    
            assert.equal(tbl.data['b'][0], '0');
            assert.equal(tbl.data['b'][15], 'F');	    
        });

    });
    describe('#JSONToTable()', function () {
        it('expected a[0]==42, a[15]==1981, b[0]=="0" and b[15]=="F"', function () {
	    let tbl: any = JSONToTable(tableLz4);
	    assert.equal(tbl.data['a'].size, 16);
	    assert.deepEqual(tbl.data['a'].shape, [16]);
	    assert.equal(tbl.data['a'].dtype, 'int32');	    
            assert.equal(tbl.data['a'].get(0), 42);
            assert.equal(tbl.data['a'].get(15), 1981);	    
            assert.equal(tbl.data['b'][0], '0');
            assert.equal(tbl.data['b'][15], 'F');
        });

    });
});