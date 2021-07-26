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
});