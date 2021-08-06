if ((window as any).require !== undefined) {
    (window as any).require.config({
        map: {
            "*" : {
                "jupyter-tablewidgets": "nbextensions/jupyter-tablewidgets/index",
            }
        }
    });
}
export function load_ipython_extension() {}
