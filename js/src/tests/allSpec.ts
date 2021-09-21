// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import pako = require('pako');
import lz4 = require("lz4js");

import { assert, expect } from 'chai';
import { IReceivedSerializedArray, IDict, IReceivedSerializedTable,
       ISendSerializedTable } from '../serializers';

import { decompress, rowProxy, table_serialization, TableWidgetModel } from '../index';

var JSONToTable = table_serialization['deserialize'];
var tableToJSON = table_serialization['serialize']

const SIZE = 64;

const OFFSET0 = 0;
const OFFSET15 = SIZE - 4;
const HEXA = "0123456789ABCDEF"

var dv1 = new DataView(new ArrayBuffer(SIZE));
dv1.setInt32(OFFSET0, 42, true);
dv1.setInt32(OFFSET15, 1984, true);

var sa1: IReceivedSerializedArray  = {'shape': [16], 'dtype': 'int32', 'buffer': dv1};
var sa2: IReceivedSerializedArray = {'shape': [16], 'dtype': 'str', 'buffer': HEXA.split('')};
var tdict: IDict<IReceivedSerializedArray> = {'a': sa1, 'b': sa2};
var table: IReceivedSerializedTable  = {'columns': ['a', 'b'], 'data': tdict};

var dv1Lz4 = lz4.compress(new Uint8Array(dv1.buffer));
var dv1Zlib = new DataView(pako.deflate(new Uint8Array(dv1.buffer)).buffer);
var sa1Lz4: IReceivedSerializedArray  = {'shape': [16], 'dtype': 'int32',
    	    			      	'buffer': dv1Lz4, 'compression': 'lz4'};
var sa1Zlib: IReceivedSerializedArray  = {'shape': [16], 'dtype': 'int32',
    	    			      	'buffer': dv1Zlib, 'compression': 'zlib'};
var strCol = JSON.stringify(HEXA.split(''));
var enc = new TextEncoder();
var dv2Lz4 = new  DataView(lz4.compress(enc.encode(strCol)).buffer);
var dv2Zlib = new  DataView(pako.deflate(enc.encode(strCol)).buffer);
var sa2Lz4: IReceivedSerializedArray = {'shape': [16], 'dtype': 'str',
    	    			     'buffer': dv2Lz4, 'compression': 'lz4'};
var sa2Zlib: IReceivedSerializedArray = {'shape': [16], 'dtype': 'str',
    	    			     'buffer': dv2Zlib, 'compression': 'zlib'};
var tdictLz4: IDict<IReceivedSerializedArray> = {'a': sa1Lz4, 'b': sa2Lz4};
var tdictZlib: IDict<IReceivedSerializedArray> = {'a': sa1Zlib, 'b': sa2Zlib};
var tableLz4: IReceivedSerializedTable  = {'columns': ['a', 'b'], 'data': tdictLz4};
var tableZlib: IReceivedSerializedTable  = {'columns': ['a', 'b'], 'data': tdictZlib};

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
        it('Without compression', function () {
	    let tbl: any = JSONToTable(table);
	    assert.equal(tbl.data['a'].size, 16);
	    assert.deepEqual(tbl.data['a'].shape, [16]);
	    assert.equal(tbl.data['a'].dtype, 'int32');
            assert.equal(tbl.data['a'].get(0), 42);
            assert.equal(tbl.data['a'].get(15), 1984);
            assert.equal(tbl.data['b'][0], '0');
            assert.equal(tbl.data['b'][15], 'F');
        });

    });
    describe('#JSONToTable()', function () {
        it('LZ4 compression', function () {
	    let tbl: any = JSONToTable(tableLz4);
	    assert.equal(tbl.data['a'].size, 16);
	    assert.deepEqual(tbl.data['a'].shape, [16]);
	    assert.equal(tbl.data['a'].dtype, 'int32');
            assert.equal(tbl.data['a'].get(0), 42);
            assert.equal(tbl.data['a'].get(15), 1984);
            assert.equal(tbl.data['b'][0], '0');
            assert.equal(tbl.data['b'][15], 'F');
        });

    });
    describe('#JSONToTable()', function () {
        it('ZLIB compression', function () {
	    let tbl: any = JSONToTable(tableZlib);
	    assert.equal(tbl.data['a'].size, 16);
	    assert.deepEqual(tbl.data['a'].shape, [16]);
	    assert.equal(tbl.data['a'].dtype, 'int32');
            assert.equal(tbl.data['a'].get(0), 42);
            assert.equal(tbl.data['a'].get(15), 1984);
            assert.equal(tbl.data['b'][0], '0');
            assert.equal(tbl.data['b'][15], 'F');
        });

    });
    describe('#rowProxy()', function () {
        it('should return null', function () {
            assert.equal(null, rowProxy(null));
        });

    });
    describe('#rowProxy()', function () {
        it('should NOT return null', function () {
            assert.notEqual(null, rowProxy(JSONToTable(table)));
        });

    });
    describe('#rowProxy()', function () {
        it('checking content', function () {
            var proxy = rowProxy(JSONToTable(table));
            assert.notEqual(null, proxy(0));
            assert.equal(42, proxy(0)['a']);
            assert.equal('0', proxy(0)['b']);
	    var setFuncA = function () { proxy(0)['a']=5;};
	    expect(setFuncA).to.throw();
	    var setFuncB = function () { proxy(0)['b']=5;};
	    expect(setFuncB).to.throw();
        });

    });
    describe('#decompress()', function () {
        it('LZ4 decompression', function () {
            assert.notEqual(null, decompress['lz4'](dv1Lz4));
        });
    });
    describe('#decompress()', function () {
        it('ZLIB decompression', function () {
            assert.notEqual(null, decompress['zlib'](dv1Zlib.buffer));
        });

    });
    describe('#TableWidgetModel()', function () {
        it('test not yet implemented', function () {
	    var noWidget = function () { return new TableWidgetModel();};
            expect(noWidget).to.throw();
        });

    });

});