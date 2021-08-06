import * as plugin from './index';
import * as base from '@jupyter-widgets/base';

module.exports = {
  id: 'jupyter-tablewidgets',
  requires: [base.IJupyterWidgetRegistry],
  activate: (app: any, widgets: any) => {
    widgets.registerWidget({
      name: 'jupyter-tablewidgets',
      version: plugin.version,
      exports: plugin,
    });
  },
  autoStart: true,
};
