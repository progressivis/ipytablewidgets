// Initial software, Jean-Daniel Fekete, Christian Poli, Copyright (c) Inria, BSD 3-Clause License, 2021

import { DOMWidgetView, DOMWidgetModel, unpack_models } from "@jupyter-widgets/base";
import * as ndarray from "ndarray";
import * as ndarray_unpack from "ndarray-unpack";
import { table_serialization } from "./serializers";

let version = require('../package.json').version;

export class TableWidgetModel extends DOMWidgetModel {
  defaults() {
        return {...DOMWidgetModel.prototype.defaults(),
            _model_name: "TableWidgetModel",
            _view_name: null,
      	    _model_module: 'jupyter-tablewidgets',
      	    _view_module: null,
	    _model_module_version: version,
      	    _view_module_version: '',
            _table:  ndarray([]),
            _columns: []
            }
   };
  static serializers = {
        ...DOMWidgetModel.serializers,
        _table: table_serialization
    };

}

// https://gist.github.com/pbugnion/63cf43b41ec0eed2d0b7e7426d1c67d2

export class EchoTableWidgetModel extends DOMWidgetModel {
  defaults() {
        return {...DOMWidgetModel.prototype.defaults(),
            _model_name: "EchoTableWidgetModel",
            _view_name: "EchoTableWidgetView",
      	    _model_module: 'jupyter-tablewidgets',
      	    _view_module: 'jupyter-tablewidgets',
	    _model_module_version: version,
	    _view_module_version: version,
            data: [],
	    echo: []
            }
   };
     static serializers = {
        ...DOMWidgetModel.serializers,
        data: { deserialize: unpack_models as any }
    };

}

export class EchoTableWidgetView extends DOMWidgetView {
  async render() {
    let that:  any = this.model;
    let subwg: any =  that.get("data");
    let table: any = subwg.get("_table");
    let res: any = {'columns': table.columns, 'data': {}};
    for (const [col, v] of Object.entries(table.data)) {
      let val: any = v;
      if(val.dtype !== undefined){
        res.data[col] = ndarray_unpack( val);
      } else {
        res.data[col] = val;
      }
    }
    that.set("echo", res);
    this.touch();
  };
}