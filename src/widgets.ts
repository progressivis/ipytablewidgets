import { DOMWidgetView, DOMWidgetModel } from "@jupyter-widgets/base";
import * as ndarray from "ndarray";
import { table_serialization, rowProxy, IDict } from "./serializers";

export class TableWidgetModel extends DOMWidgetModel {
  defaults() {
        return {...DOMWidgetModel.prototype.defaults(),
            _model_name: "TableWidgetModule",
            _view_name: null,
      	    _model_module: 'ipytablewidgets',
      	    _view_module: null,
      	    _model_module_version: '0.1.0',	
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

