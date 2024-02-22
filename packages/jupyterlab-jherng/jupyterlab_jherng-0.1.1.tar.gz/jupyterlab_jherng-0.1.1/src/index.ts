import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @jherng/jupyterlab-jherng extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@jherng/jupyterlab-jherng:plugin',
  description: 'A JupyterLab theme for me.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension @jherng/jupyterlab-jherng is activated!');
    const style = '@jherng/jupyterlab-jherng/index.css';

    manager.register({
      name: '@jherng/jupyterlab-jherng',
      isLight: true,
      themeScrollbars: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
